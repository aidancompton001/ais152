# -*- coding: utf-8 -*-
"""Самопроверка общей проверки robots: пять случаев, каждый — мутация.

Находка #14, круг 5 (F-67): robots_check.py — единая точка для пяти проб,
и любая её дыра множится на пять сразу. Значит она сама обязана иметь
проверку, а не приниматься на веру.

Случаи подобраны как мутации, каждая из которых раньше проходила насквозь:
  1. закрывает ВТОРОЙ тег, первый открывает — дыра круга 4;
  2. директива none — документированный Google эквивалент noindex, nofollow;
  3. значение атрибута без кавычек — валидный HTML5;
  4. открытая страница с явным index,follow не должна считаться закрытой;
  5. страница без тега вовсе — тоже открыта.

Печатает 'ROBOTS_CHECK_OK 5/5;'.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from robots_check import closed  # noqa: E402

CASES = [
    ("закрывает второй тег",
     '<meta name="robots" content="index,follow">'
     '<meta name="googlebot" content="noindex">', True),
    ("директива none",
     '<meta name="robots" content="none">', True),
    ("значение без кавычек",
     '<meta name=robots content=noindex>', True),
    ("явно открытая",
     '<meta name="robots" content="index,follow">', False),
    ("тега нет вовсе",
     '<html><head><title>x</title></head>', False),
]


def main():
    ok = 0
    for name, html, want in CASES:
        got = closed(html)
        if got == want:
            ok += 1
        else:
            print("ПРОВАЛ: %s — получили %s, ждали %s" % (name, got, want))

    # Заголовок ответа действует наравне с тегом.
    if not closed("<html></html>", {"X-Robots-Tag": "noindex"}):
        print("ПРОВАЛ: заголовок X-Robots-Tag не учитывается")
        return 1

    if ok != len(CASES):
        return 1
    print("ROBOTS_CHECK_OK %d/%d;" % (ok, len(CASES)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
