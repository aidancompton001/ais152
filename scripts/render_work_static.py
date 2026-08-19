# -*- coding: utf-8 -*-
"""Вписать проекты в исходный код страницы, а не рисовать их скриптом.

Шестнадцать проектов существовали только после выполнения JS: краулер,
получив HTML, видел пустой контейнер и надпись «Projekte werden geladen…».
Крупнейший блок уникального текста на сайте для поиска не существовал.

Проверено до правки:
    grep -c "Henner Heede" index.html  -> 0
    grep -c "noscript" index.html      -> 0

Решение — не отказ от скрипта, а запасной слой: карточки кладутся в HTML
на этапе сборки. Скрипт продолжает работать как раньше и просто заменяет
их собой, если загрузился. Не загрузился — человек и краулер всё равно
видят шестнадцать работ со ссылками.

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


def esc(text):
    return (text or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def cards(items, lang):
    out = []
    for i, p in enumerate(items, 1):
        if (p.get("status") or "") != "live":
            continue
        tag = p.get("tagline_de" if lang == "de" else "tagline_en") or ""
        tags = "".join("<li>%s</li>" % esc(t) for t in (p.get("tags") or [])[:4])
        shot = p.get("screenshot") or ""
        img = ('<img class="card-img" src="/%s" alt="%s" loading="lazy" decoding="async">'
               % (shot, esc(p["title"]))) if shot else ""
        out.append(
            '      <article class="card" role="listitem">\n'
            '        <span class="card-num">%02d</span>\n'
            '        <a class="card-link" href="/projekte/%s.html">\n'
            '          <div class="card-media">%s</div>\n'
            '          <div class="card-body">\n'
            '            <div class="card-meta"><span class="card-year">%s</span></div>\n'
            '            <h3 class="card-title">%s</h3>\n'
            '            <p class="card-tagline">%s</p>\n'
            '            <ul class="card-tags">%s</ul>\n'
            '          </div>\n'
            '        </a>\n'
            '      </article>'
            % (i, p["slug"], img, esc(str(p.get("year") or "")),
               esc(p["title"]), esc(tag), tags))
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
                 "      <!-- Карточки в исходном коде: без них шестнадцать работ\n"
                 "           не существуют для поиска. Скрипт projects.js заменяет\n"
                 "           этот блок собой, если загрузился. Правится сборщиком\n"
                 "           scripts/render_work_static.py из data/projects.json. -->\n"
                 + cards(items, lang) + "\n      " + MARK_CLOSE)

        if MARK_OPEN in html:
            html = re.sub(re.escape(MARK_OPEN) + r".*?" + re.escape(MARK_CLOSE),
                          block, html, flags=re.S)
        else:
            anchor = re.search(
                r'(<div class="work-track"[^>]*>)(.*?)(</div>)', html, re.S)
            if not anchor:
                print("НЕ НАЙДЕН КОНТЕЙНЕР РАБОТ в %s" % path.name)
                return 1
            html = (html[:anchor.end(1)] + "\n" + block + "\n    "
                    + html[anchor.start(3):])

        n = html.count('class="card"')
        if write:
            io.open(path, "w", encoding="utf-8", newline="\n").write(html)
        print("%-16s карточек в исходном коде: %d" % (path.name, n))

    print("вписано" if write else "холостой прогон, запусти с --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
