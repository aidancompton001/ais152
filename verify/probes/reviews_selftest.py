# -*- coding: utf-8 -*-
"""Самопроверка блока отзывов: гейт обязан не только разрешать, но и запрещать.

Пока в data/reviews.json ноль отзывов, все пробы проходят на пустоте — а
проверка, которая зелена на пустых данных и никогда не краснела, ничего
не проверяет. Прецедент MacsStore и Закон 25: чувствительность гейта
доказывается тремя ветками, иначе он пустышка.

Здесь прогоняются шесть веток на ВРЕМЕННЫХ данных:
  ветка A  отзывы есть   → секция становится видимой, карточки появляются
  ветка B  нет пометки § 5b UWG          → reviews_uwg_note краснеет
  ветка C  точка в конце кнопки          → reviews_no_periods краснеет
  ветка D  карточек больше, чем в профиле → сборщик отказывается работать
  ветка E  отзывы есть, ссылки на профиль нет → сборщик отказывается
  ветка F  секция скрыта при живых отзывах   → reviews_state краснеет

Рабочие файлы восстанавливаются в finally — даже если проба упала
посередине. Восстановление проверяется сверкой байтов, а не надеждой.
"""
import io
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "reviews.json"
PAGES = [ROOT / "index.html", ROOT / "en" / "index.html"]
PROBES = ROOT / "verify" / "probes"
BUILD = ROOT / "scripts" / "render_reviews_static.py"

FIXTURE = {
    "googleProfile": {
        "placeId": "SELFTEST", "profileUrl": "https://example.invalid/profile",
        "reviewUrl": "https://example.invalid/review", "ratingValue": 5.0,
        "ratingCount": 3, "bestRating": 5, "worstRating": 1,
        "asOfLabel": "August 2026", "asOfShort": "08/2026",
    },
    "reviews": [
        {"id": "s1", "author": "Selftest Eins", "city": "München", "rating": 5,
         "datePublished": "2026-08-01", "text": "Erste Zeile.\n\nZweite Zeile.",
         "service": "n8n"},
        {"id": "s2", "author": "Selftest Zwei", "city": "Osnabrück",
         "rating": 4, "datePublished": "2026-07-15", "text": "Kurzer Text.",
         "service": None},
    ],
}


def run(*args):
    r = subprocess.run([sys.executable] + list(args), cwd=str(ROOT),
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def probe(name):
    return run(str(PROBES / name))


def write_data(payload):
    io.open(DATA, "w", encoding="utf-8", newline="\n").write(
        json.dumps(payload, ensure_ascii=False, indent=2))


def build(write=True):
    return run(str(BUILD), "--write") if write else run(str(BUILD))


def main():
    saved = {p: p.read_bytes() for p in PAGES}
    saved[DATA] = DATA.read_bytes()
    fails = []

    try:
        # ── ветка A: отзывы есть → блок оживает ──────────────────────────
        write_data(json.loads(json.dumps(FIXTURE)))
        code, out = build()
        if code != 0 or "видима" not in out:
            fails.append("A: сборщик не показал секцию при живых отзывах: %s"
                         % out.strip()[:120])
        for p in PAGES:
            if p.read_text(encoding="utf-8").count('class="review"') != 2:
                fails.append("A: в %s не две карточки" % p.name)
        code, out = probe("reviews_state.py")
        if code != 0:
            fails.append("A: reviews_state покраснел на исправных данных: %s"
                         % out.strip()[:120])
        code, out = probe("reviews_uwg_note.py")
        if code != 0:
            fails.append("A: пометка § 5b UWG не встала: %s" % out.strip()[:120])

        # ── ветка B: пометка удалена → проба обязана покраснеть ──────────
        import re
        html = PAGES[0].read_text(encoding="utf-8")
        PAGES[0].write_text(
            re.sub(r'<p class="reviews-note">.*?</p>', "", html, flags=re.S),
            encoding="utf-8", newline="\n")
        code, out = probe("reviews_uwg_note.py")
        if code == 0:
            fails.append("B: пометка удалена, а проба промолчала")
        build()

        # ── ветка C: точка в конце кнопки ────────────────────────────────
        html = PAGES[0].read_text(encoding="utf-8")
        PAGES[0].write_text(
            html.replace(">Bei Google bewerten<", ">Bei Google bewerten.<"),
            encoding="utf-8", newline="\n")
        code, out = probe("reviews_no_periods.py")
        if code == 0:
            fails.append("C: точка в кнопке, а проба промолчала")
        build()

        # ── ветка F: секция скрыта при живых отзывах ─────────────────────
        html = PAGES[0].read_text(encoding="utf-8")
        PAGES[0].write_text(
            html.replace('<section class="reviews" id="reviews">',
                         '<section class="reviews" id="reviews" hidden>'),
            encoding="utf-8", newline="\n")
        code, out = probe("reviews_state.py")
        if code == 0:
            fails.append("F: секция спрятана при живых отзывах, проба молчит")
        build()

        # ── ветка D: карточек больше, чем отзывов в профиле ──────────────
        bad = json.loads(json.dumps(FIXTURE))
        bad["googleProfile"]["ratingCount"] = 1
        write_data(bad)
        code, out = build(write=False)
        if code == 0:
            fails.append("D: карточек больше, чем в профиле, а сборщик молчит")

        # ── ветка E: отзывы есть, ссылки на профиль нет ──────────────────
        bad = json.loads(json.dumps(FIXTURE))
        bad["googleProfile"]["profileUrl"] = None
        write_data(bad)
        code, out = build(write=False)
        if code == 0:
            fails.append("E: нет ссылки на профиль, а сборщик молчит")

    finally:
        for path, blob in saved.items():
            path.write_bytes(blob)
        restored = all(p.read_bytes() == saved[p] for p in saved)
        if not restored:
            fails.append("рабочие файлы НЕ восстановлены — проверь git diff")

    if fails:
        print("SELFTEST_FAILED: " + "; ".join(fails))
        return 1
    print("SELFTEST_OK ветки: A видимость, B пометка UWG, C точка, "
          "D перебор карточек, E нет ссылки, F ложное сокрытие")
    return 0


sys.exit(main())
