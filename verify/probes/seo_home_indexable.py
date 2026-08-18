# -*- coding: utf-8 -*-
"""Проба: главную страницу ничто не закрывает от индексации.

Находка #14, круг 3 (F-40): прежнее доказательство искало только тег meta
в разметке. Закрыть страницу от Google можно ещё двумя способами, и оба
проба не видела: заголовком ответа X-Robots-Tag и правилом Disallow
в robots.txt. Мутация «дописать Disallow: / в robots.txt» оставляла
утверждение «главная не закрыта» зелёным.

Проверяются все три канала сразу.

Печатает 'HOME_INDEXABLE meta=no header=no robots_txt=no;'.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from robots_check import closed as page_closed  # noqa: E402
from robots_check import closed_by_header  # noqa: E402
from robots_check import crawl_blocked, parse_disallow  # noqa: E402
import urllib.request

HOME = "https://ais152.com/"
UA = {"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}


def main():
    try:
        res = urllib.request.urlopen(
            urllib.request.Request(HOME, headers=UA), timeout=25)
        html = res.read().decode("utf-8", "replace")
        header = res.headers.get("X-Robots-Tag") or ""
    except Exception as exc:
        print("ГЛАВНАЯ НЕДОСТУПНА: %s" % exc)
        return 1

    by_meta = page_closed(html)
    # Круг 6, F-80: здесь лежала СВОЯ копия проверки заголовка, слепая
    # к директиве none — то есть ровно тот дефект «одна проверка
    # в нескольких копиях», ради которого robots_check и заводился.
    by_header = closed_by_header(res.headers)

    try:
        robots = urllib.request.urlopen(
            urllib.request.Request("https://ais152.com/robots.txt", headers=UA),
            timeout=25).read().decode("utf-8", "replace")
    except Exception as exc:
        print("НЕ ПРОЧИТАТЬ robots.txt: %s" % exc)
        return 1

    # Круг F-104: своя проверка видела только буквальное "Disallow: /"
    # и не понимала ни "Disallow: /*" ни "Disallow: /index.html".
    by_robots = crawl_blocked("/", parse_disallow(robots)) or         crawl_blocked("/index.html", parse_disallow(robots))

    if by_meta or by_header or by_robots:
        print("ГЛАВНАЯ ЗАКРЫТА ОТ ИНДЕКСАЦИИ: meta=%s header=%s robots_txt=%s"
              % (by_meta, by_header, by_robots))
        return 1

    print("HOME_INDEXABLE meta=no header=no robots_txt=no;")
    return 0


if __name__ == "__main__":
    sys.exit(main())
