# -*- coding: utf-8 -*-
"""Проба: Impressum и Datenschutz открыты для индексации и стоят в карте.

Решение принято CEO 17.08.2026 («как надо, так и сделаем») и исполнено:
раньше обе страницы несли noindex, из-за чего Google не мог прочитать адрес
и телефон там, где на них строится связка с карточкой Business.

Находка #14, круг 3 (F-29): в плане это состояние было описано как «решение
за CEO, страницы закрыты», хотя правка уже лежала в рабочей копии. Поэтому
здесь проверяется ЖИВОЙ сайт: раздел плана и реальность обязаны совпадать.

AVV остаётся закрытым намеренно — это шаблон договора, он нужен клиенту
по прямой ссылке, а не в поисковой выдаче. Проба следит и за этим: если
AVV вдруг откроется, значит правку сделали шире решения.

Печатает 'LEGAL open=impressum,datenschutz closed=avv in_sitemap=2;'.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from robots_check import closed as page_closed  # noqa: E402
import urllib.request

BASE = "https://ais152.com/"
OPEN = ["impressum.html", "datenschutz.html"]
CLOSED = ["avv.html"]
UA = {"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}


def get(url):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers=UA), timeout=25
    ).read().decode("utf-8", "replace")


def is_closed(html):
    return page_closed(html)


def main():
    problems = []
    try:
        sitemap = get(BASE + "sitemap.xml")
    except Exception as exc:
        print("КАРТА НЕДОСТУПНА: %s" % exc)
        return 1
    locs = set(re.findall(r"<loc>([^<]+)</loc>", sitemap))

    in_map = 0
    for name in OPEN:
        try:
            html = get(BASE + name)
        except Exception as exc:
            problems.append("%s: %s" % (name, exc))
            continue
        if is_closed(html):
            problems.append("%s ЗАКРЫТА, хотя решено открыть" % name)
        if BASE + name in locs:
            in_map += 1
        else:
            problems.append("%s открыта, но её нет в карте сайта" % name)

    for name in CLOSED:
        try:
            html = get(BASE + name)
        except Exception as exc:
            problems.append("%s: %s" % (name, exc))
            continue
        if not is_closed(html):
            problems.append("%s ОТКРЫТА, хотя решено оставить закрытой — "
                            "правку сделали шире решения" % name)

    if problems:
        for item in problems:
            print(item)
        return 1

    print("LEGAL open=%s closed=%s in_sitemap=%d;"
          % (",".join(n.replace(".html", "") for n in OPEN),
             ",".join(n.replace(".html", "") for n in CLOSED), in_map))
    return 0


if __name__ == "__main__":
    sys.exit(main())
