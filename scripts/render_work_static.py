# -*- coding: utf-8 -*-
"""Собрать карточки работ в исходный код страницы.

Зачем вообще. Проекты существовали только после выполнения JS: краулер,
получив HTML, видел пустой контейнер и надпись «Projekte werden geladen…».
Крупнейший блок уникального текста на сайте для поиска не существовал.

Почему карточка теперь ПОЛНАЯ. Раньше здесь лежала урезанная версия, а
скрипт в браузере всё равно стирал её и строил полную заново. Замерено на
живом сайте 23.08 (телефон, медленный 4G, процессор вчетверо слабее):
этот шаг стирал и пересоздавал 463 элемента и давал пересчёт вёрстки на
526 мс с 1014 узлами — плюс отдельный запрос за data/projects.json уже
после загрузки страницы. Две разметки одного и того же расходились и
стоили полсекунды на каждой загрузке.

Теперь разметка одна и приходит отсюда. Скрипт projects.js её не трогает,
а только навешивает поведение.

    py scripts/render_work_static.py           # показать
    py scripts/render_work_static.py --write   # вписать
"""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "projects.json"
PAGES = {"de": ROOT / "index.html", "en": ROOT / "en" / "index.html"}
MARK_OPEN = "<!-- work:static:start -->"
MARK_CLOSE = "<!-- work:static:end -->"

LABEL = {
    "de": {"live": "Live", "in-development": "In Arbeit", "archived": "Archiv"},
    "en": {"live": "Live", "in-development": "In dev", "archived": "Archived"},
}
CTA = {"de": "Site öffnen", "en": "Visit site"}
CASE = {"de": "Projekt ansehen", "en": "Read the case"}

CARD = (
    '      <article class="{classes}" role="listitem" data-slug="{slug}">\n'
    '        <span class="card-num">{num:02d} / {total:02d}</span>\n'
    '        <a class="card-link"{ext}>\n'
    '          <div class="card-media">{img}'
    '<span class="card-status" data-status="{status}">{label}</span></div>\n'
    '          <div class="card-body">{mark}\n'
    '            <div class="card-meta"><span class="card-year">{year}</span>'
    '<span class="card-sep">·</span>'
    '<span class="card-tag-primary">{tag1}</span></div>\n'
    '            <h3 class="card-title">{title}</h3>\n'
    '            <p class="card-tagline">{tagline}</p>\n'
    '            <ul class="card-tags">{tags}</ul>\n'
    '            <span class="card-cta"><span class="card-cta-text">{cta}</span>'
    '<svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true">'
    '<path d="M3 3h6v6M3 9l6-6" stroke="currentColor" stroke-width="1.5" '
    'stroke-linecap="square"/></svg></span>\n'
    '          </div>\n'
    '        </a>\n'
    '        <a class="card-case" href="/projekte/{slug}.html">{case}</a>\n'
    '      </article>'
)


def esc(text):
    return ((text or "").replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def cards(items, lang):
    live = [p for p in items if (p.get("status") or "") == "live"]
    live.sort(key=lambda p: p.get("order") or 0)
    total = len(live)
    out = []
    for i, p in enumerate(live, 1):
        tag = (p.get("tagline_de" if lang == "de" else "tagline_en")
               or p.get("tagline_en") or "")
        shot = p.get("screenshot") or ""
        srcset = ""
        if shot and p.get("screenshot_2x"):
            srcset = ' srcset="/%s 1x, /%s 2x"' % (shot, p["screenshot_2x"])
        img = ""
        if shot:
            # Размеры проставлены, чтобы браузер занял место под картинку
            # заранее: без них страница дёргается, когда снимок догружается.
            img = ('<img class="card-img" src="/%s"%s alt="%s" loading="lazy" '
                   'decoding="async" width="1200" height="900">'
                   % (shot, srcset, esc("%s, %s" % (p["title"], tag))))
        mark = ""
        if p.get("mark"):
            mark = ('<svg class="card-mark" viewBox="0 0 24 24" aria-hidden="true" '
                    'focusable="false"><use href="#mark-%s"></use></svg>'
                    % esc(p["mark"]))
        url = p.get("url") or ""
        if url and url != "#":
            ext = ' href="%s" target="_blank" rel="noopener noreferrer"' % esc(url)
        else:
            ext = ' href="#" aria-disabled="true"'
        classes = "card layout-" + (p.get("layout") or "square")
        if p.get("featured"):
            classes += " is-featured"
        out.append(CARD.format(
            classes=classes, slug=esc(p["slug"]), num=i, total=total, ext=ext,
            img=img, status=esc(p.get("status") or ""),
            label=LABEL[lang].get(p.get("status"), ""), mark=mark,
            year=esc(str(p.get("year") or "")),
            tag1=esc((p.get("tags") or [""])[0]),
            title=esc(p["title"]), tagline=esc(tag),
            tags="".join("<li>%s</li>" % esc(t) for t in (p.get("tags") or [])[:5]),
            cta=CTA[lang], case=CASE[lang]))
    return "\n".join(out)


def main():
    write = "--write" in sys.argv
    data = json.load(io.open(DATA, encoding="utf-8"))
    items = data if isinstance(data, list) else data.get("projects", [])

    for lang, path in PAGES.items():
        if not path.is_file():
            print("НЕТ ФАЙЛА: %s" % path)
            return 1
        html = io.open(path, encoding="utf-8").read()

        block = (MARK_OPEN + "\n"
                 "      <!-- Карточки собраны здесь, а не в браузере: скрипт их\n"
                 "           только оживляет и не перерисовывает. Правится\n"
                 "           scripts/render_work_static.py из data/projects.json. -->\n"
                 + cards(items, lang) + "\n      " + MARK_CLOSE)

        if MARK_OPEN in html:
            html = re.sub(re.escape(MARK_OPEN) + r".*?" + re.escape(MARK_CLOSE),
                          lambda m: block, html, flags=re.S)
        else:
            anchor = re.search(r'(<div class="work-track"[^>]*>)(.*?)(</div>)',
                               html, re.S)
            if not anchor:
                print("НЕ НАЙДЕН КОНТЕЙНЕР РАБОТ в %s" % path.name)
                return 1
            html = (html[:anchor.end(1)] + "\n" + block + "\n    "
                    + html[anchor.start(3):])

        n = html.count('class="card layout-')
        if write:
            io.open(path, "w", encoding="utf-8", newline="\n").write(html)
        print("%-16s карточек в исходном коде: %d" % (path.name, n))

    print("вписано" if write else "холостой прогон, запусти с --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
