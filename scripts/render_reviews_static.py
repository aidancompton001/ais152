# -*- coding: utf-8 -*-
"""Вписать отзывы из data/reviews.json в исходный код обеих главных страниц.

Почему статикой, а не скриптом в браузере. Ровно та же причина, что у
scripts/render_work_static.py: краулер получает HTML и не выполняет JS.
Блок отзывов — единственный на сайте текст, написанный не нами, и терять
его для поиска нельзя. Здесь скрипта в браузере нет вообще: карточки
кладутся в разметку на этапе сборки, и всё.

Юридический слой — не украшение:
  * § 5b Abs. 3 UWG требует сказать, проверяем ли мы подлинность отзывов
    и как. Мы не проверяем — значит так и написано, и написано рядом
    с самими отзывами, а не на другой странице.
  * Anhang Nr. 23b zu § 3 UWG запрещает утверждать, что отзывы проверены,
    если мер по проверке не принято. Поэтому слов из семьи «geprüft»,
    «verifiziert», «echtheitsgeprüft» в блоке нет и быть не должно.
  * Ссылка на профиль — это проверяемость цифр. Без неё и рейтинг,
    и число отзывов висят в воздухе.

Пока googleProfile.profileUrl пуст или отзывов ноль, секция ставится
скрытой (hidden). Пустой блок «Kundenstimmen» хуже отсутствующего.

    py scripts/render_reviews_static.py           # холостой прогон
    py scripts/render_reviews_static.py --write   # вписать
"""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "reviews.json"
PAGES = {"de": ROOT / "index.html", "en": ROOT / "en" / "index.html"}
MARK_OPEN = "<!-- reviews:static:start -->"
MARK_CLOSE = "<!-- reviews:static:end -->"
ANCHOR = '<section class="contact" id="contact">'
SECTION_RE = r'<section class="reviews" id="reviews"[^>]*>'

T = {
    "de": {
        "overline": "Stimmen",
        "title": "Was Kunden bei Google schreiben",
        "aria_stars": "%d von %d Sternen",
        "figures": "%s bei Google · %d Bewertungen (Stand: %s)",
        "shown": "Hier zeigen wir %d davon",
        "note": ("Diese Bewertungen haben Kundinnen und Kunden bei Google "
                 "veröffentlicht. Wir haben sie von dort übernommen (Stand: %s) "
                 "und prüfen sie nicht selbst auf Echtheit — Veröffentlichung "
                 "und Moderation erfolgen durch Google."),
        "profile": "Alle Bewertungen bei Google ansehen",
        "ask_lead": "Sie waren Kunde? Eine kurze Bewertung hilft weiter",
        "ask_cta": "Bei Google bewerten",
        "months": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
                   "August", "September", "Oktober", "November", "Dezember"],
    },
    "en": {
        "overline": "Reviews",
        "title": "What clients write on Google",
        "aria_stars": "%d out of %d stars",
        "figures": "%s on Google · %d reviews (as of %s)",
        "shown": "Showing %d of them",
        "note": ("These reviews were published by customers on Google. We "
                 "copied them from there (as of %s) and do not check their "
                 "authenticity ourselves — publication and moderation are "
                 "handled by Google."),
        "profile": "See all reviews on Google",
        "ask_lead": "Worked with me? A short review goes a long way",
        "ask_cta": "Review on Google",
        "months": ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November",
                   "December"],
    },
}


def esc(text):
    return ((text or "")
            .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def stars(rating, best, label):
    """Звёзды — символами, не картинками: скринридер должен получить одну
    подпись, а не пять иконок подряд."""
    full = '<span class="review-star is-on" aria-hidden="true">&#9733;</span>'
    empty = '<span class="review-star" aria-hidden="true">&#9733;</span>'
    body = full * int(rating) + empty * (int(best) - int(rating))
    return ('<span class="review-stars" role="img" aria-label="%s">%s</span>'
            % (esc(label % (rating, best)), body))


def human_date(iso, t):
    m = re.match(r"^(\d{4})-(\d{2})", iso or "")
    if not m:
        return ""
    return "%s %s" % (t["months"][int(m.group(2)) - 1], m.group(1))


def cards(items, prof, t):
    out = []
    best = prof.get("bestRating") or 5
    for r in items:
        meta = []
        if r.get("city"):
            meta.append(esc(r["city"]))
        if r.get("service"):
            meta.append('<span class="review-service">%s</span>'
                        % esc(r["service"]))
        iso = r.get("datePublished") or ""
        paras = "".join("<p>%s</p>" % esc(p)
                        for p in (r.get("text") or "").split("\n") if p.strip())
        out.append(
            '        <article class="review">\n'
            '          <div class="review-top">\n'
            '            %s\n'
            '            <time class="review-date" datetime="%s">%s</time>\n'
            '          </div>\n'
            '          <blockquote class="review-text">%s</blockquote>\n'
            '          <footer class="review-by"><strong>%s</strong>%s</footer>\n'
            '        </article>'
            % (stars(r.get("rating") or best, best, t["aria_stars"]),
               esc(iso), human_date(iso, t), paras,
               esc(r.get("author") or ""),
               (" — " + " · ".join(meta)) if meta else "")
        )
    return "\n".join(out)


def block(items, prof, lang, num):
    t = T[lang]
    rating = prof.get("ratingValue")
    rating_txt = ""
    if rating is not None:
        rating_txt = ("%.1f" % rating).replace(".", "," if lang == "de" else ".")
    as_of = prof.get("asOfShort") or ""
    as_of_long = prof.get("asOfLabel") or as_of

    figures = ""
    if rating is not None and prof.get("ratingCount"):
        figures = ('      <p class="reviews-figures">%s <span>%s</span></p>\n'
                   % (stars(int(round(rating)), prof.get("bestRating") or 5,
                            t["aria_stars"]),
                      esc(t["figures"] % (rating_txt, prof["ratingCount"],
                                          as_of))))

    shown = ('      <p class="reviews-shown">%s</p>\n'
             % esc(t["shown"] % len(items))) if items else ""

    profile_btn = ""
    if prof.get("profileUrl"):
        profile_btn = ('      <a class="reviews-profile" href="%s" '
                       'target="_blank" rel="noopener noreferrer">%s</a>\n'
                       % (esc(prof["profileUrl"]), esc(t["profile"])))

    ask = ""
    if prof.get("reviewUrl"):
        ask = ('      <div class="reviews-ask">\n'
               '        <p>%s</p>\n'
               '        <a class="reviews-ask-cta" href="%s" target="_blank" '
               'rel="noopener noreferrer">%s</a>\n'
               '      </div>\n'
               % (esc(t["ask_lead"]), esc(prof["reviewUrl"]),
                  esc(t["ask_cta"])))

    return (
        '  <div class="container">\n'
        '    <div class="reviews-head">\n'
        '      <span class="overline">%02d / <span>%s</span></span>\n'
        '      <h2 class="section-title"><span>%s</span></h2>\n'
        '%s%s'
        '    </div>\n'
        '    <div class="reviews-grid">\n'
        '%s\n'
        '    </div>\n'
        '    <p class="reviews-note">%s</p>\n'
        '%s%s'
        '  </div>'
        % (num, esc(t["overline"]), esc(t["title"]), figures, shown,
           cards(items, prof, t), esc(t["note"] % as_of_long),
           profile_btn, ask)
    )


def section(items, prof, lang, num):
    return (
        '<!-- ════════════════════════ REVIEWS ════════════════════════ -->\n'
        '<section class="reviews" id="reviews"%s>\n'
        '%s\n%s\n%s\n'
        '</section>\n\n'
        % (" hidden" if not items else "", MARK_OPEN,
           block(items, prof, lang, num), MARK_CLOSE)
    )


def renumber_contact(html, num):
    """Контакт был 05. С появлением отзывов он становится 06 — иначе на
    странице два раздела под одним номером."""
    return re.sub(
        r'(<span class="overline">)\d\d( / <span>(?:Kontakt|Contact)</span>)',
        lambda m: "%s%02d%s" % (m.group(1), num, m.group(2)), html)


def main():
    write = "--write" in sys.argv
    data = json.load(io.open(DATA, encoding="utf-8"))
    items = data.get("reviews") or []
    prof = data.get("googleProfile") or {}

    if items and not prof.get("profileUrl"):
        print("ОТКАЗ: есть отзывы, но нет profileUrl — цифры станут "
              "непроверяемыми, а ссылка на профиль обязательна")
        return 1

    rc = prof.get("ratingCount") or 0
    if items and len(items) > rc:
        print("ОТКАЗ: карточек %d, а в профиле числится %d отзывов"
              % (len(items), rc))
        return 1

    for lang, path in PAGES.items():
        if not path.is_file():
            print("НЕТ ФАЙЛА: %s" % path)
            return 1
        html = io.open(path, encoding="utf-8").read()

        body = block(items, prof, lang, 5)
        if MARK_OPEN in html:
            html = re.sub(re.escape(MARK_OPEN) + r".*?" + re.escape(MARK_CLOSE),
                          MARK_OPEN + "\n" + body + "\n" + MARK_CLOSE,
                          html, flags=re.S)
            html = re.sub(SECTION_RE,
                          '<section class="reviews" id="reviews"%s>'
                          % ("" if items else " hidden"), html)
        else:
            if ANCHOR not in html:
                print("НЕ НАЙДЕН ЯКОРЬ КОНТАКТА в %s" % path.name)
                return 1
            html = html.replace(ANCHOR, section(items, prof, lang, 5) + ANCHOR, 1)

        html = renumber_contact(html, 6)

        if write:
            io.open(path, "w", encoding="utf-8", newline="\n").write(html)
        # Имя файла у обеих страниц одинаковое — печатается путь от корня,
        # иначе в выводе дважды стоит index.html и не видно, что английская
        # версия вообще обрабатывалась.
        rel = path.relative_to(ROOT).as_posix()
        print("%-16s карточек: %-3d секция: %s"
              % (rel, html.count('class="review"'),
                 "скрыта" if not items else "видима"))

    print("вписано" if write else "холостой прогон, запусти с --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
