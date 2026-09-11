# -*- coding: utf-8 -*-
"""Тексты кейсов соблюдают docs/CASE_TEXT_RULES.md.

Проверяется каждый docs/cases/<slug>.json:
  - 300+ слов в трёх разделах;
  - у проекта есть согласие в data/consents.json;
  - нет IP-адресов, сумм в евро, условий оплаты, цитат переписки;
  - у каждого утверждения есть источник, файл существует, дословная выдержка в нём есть.
"""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KEYS = ("ausgangslage", "umsetzung", "ergebnis")
FORBIDDEN = [
    (r"\b\d{1,3}(?:\.\d{1,3}){3}\b", "IP-адрес"),
    # После «€» границы слова нет (оба символа не буквенные) — поэтому \b только у EUR/Euro.
    (r"\d[\d.,]*\s*(?:€|EUR\b|Euro\b)|€\s*\d", "сумма"),
    (r"(?i)\b(zahlungsziel|zahlbar|anzahlung|rate[n]?zahlung|vorkasse des kunden|honorar|stundensatz|festpreis)\b", "условия оплаты"),
    # WhatsApp как функция сайта (кнопка, канал заявок) разрешён; запрещено
    # ссылаться на то, что клиент писал или присылал.
    (r"(?i)\b(e-mail vom|schrieb mir|laut nachricht|per whatsapp (?:mitgeteilt|geschickt|gemeldet)|hat mir .{0,30}geschickt)\b", "переписка"),
    # Внутренняя кухня проекта (правило 11.09.2026).
    (r"(?i)\b(offen (?:waren|sind|ist|bleib\w*)|fehlt noch|fehlten noch|\d+\s+(?:automatische\w*\s+|automatisierte\w*\s+)?Tests|Audit\w*|Nachprüfung|Kernprobleme|noch nicht (?:angebunden|live|verbunden|umgestellt))\b", "внутренняя кухня"),
    # Добавлено по кругу 1 ревью #14 (11.09.2026): то, что сито пропустило.
    (r"(?i)\bServer in\b|\bRechenzentrum\b|\bHetzner\b|\bClouding\b", "сервер/хостинг"),
    (r"(?i)\b(erfüllt|konform|rechtssicher)\b", "заявление о соответствии праву"),
    (r"(?i)\b(als einzige\w*|der einzige|die einzige|allein in der Region|ist .{0,30} allein)\b", "«единственный»"),
    (r"(?i)\bLighthouse\b|\bPageSpeed\b|\d+[,.]?\d*\s*(?:MB|KB)\b|\bindexiert\w*\b", "служебная метрика (Закон 27 §7)"),
    # Круг 2 ревью #14: склейки абзацев без пробела и заявления о доступности без аудита.
    (r"[a-zäöüß)]\.[A-ZÄÖÜ]", "нет пробела после точки"),
    (r"\bWCAG\b|\bbarrierefrei nach\b", "заявление о доступности без аудита"),
]


def main():
    consents = json.load(io.open(ROOT / "data" / "consents.json", encoding="utf-8"))["consents"]
    files = sorted((ROOT / "docs" / "cases").glob("*.json"))
    if not files:
        print("CASES_EMPTY")
        return 1
    bad = []
    for f in files:
        c = json.load(io.open(f, encoding="utf-8"))
        slug = c.get("slug") or f.stem
        text = "\n".join(c.get(k) or "" for k in KEYS)
        words = len(re.findall(r"\w+", text))
        if words < 300:
            bad.append("%s: %d слов" % (slug, words))
        if not consents.get(slug, {}).get("name"):
            bad.append("%s: нет согласия" % slug)
        for rx, what in FORBIDDEN:
            m = re.search(rx, text)
            if m:
                bad.append("%s: %s «%s»" % (slug, what, m.group(0)))
        claims = c.get("claims") or []
        if not claims:
            bad.append("%s: нет claims" % slug)
        for cl in claims:
            src = (cl.get("source") or "").rsplit(":", 1)[0]
            p = Path(src)
            if not p.is_file():
                bad.append("%s: нет файла источника %s" % (slug, src))
                continue
            q = (cl.get("quote") or "").strip()
            lines = io.open(p, encoding="utf-8", errors="replace").read().splitlines()
            norm = lambda s: re.sub(r"\s+", " ", s)
            # Выдержка ищется у указанной строки (±3), а не где угодно в файле:
            # иначе ссылка на строку не проверяется вовсе (ревью #14, круг 1).
            m = re.search(r":(\d+)(?:[-–]\d+)?$", cl.get("source") or "")
            if m:
                n = int(m.group(1))
                window = "\n".join(lines[max(0, n - 4):n + 3])
            else:
                window = "\n".join(lines)
            if not q or norm(q) not in norm(window):
                bad.append("%s: выдержки нет у %s: «%s»" % (slug, cl.get("source"), q[:60]))
    if bad:
        print("CASE_RULES_BAD (%d):" % len(bad))
        for b in bad:
            print("  " + b)
        return 1
    print("CASE_RULES_OK files=%d" % len(files))
    return 0


sys.exit(main())
