# -*- coding: utf-8 -*-
"""Персонаж не показывается там, где его поведение не проверено.

Две границы, и обе обязаны стоять И в стиле, И в скрипте: стиль прячет
слой, скрипт не запускает перемотку. Одной границы мало — без скрипта
слой невидим, но ролики всё равно грузятся и перематываются.
"""
import io
import re
import sys


def main():
    css = io.open("assets/css/bars.css", encoding="utf-8").read()
    js = io.open("assets/js/bars.js", encoding="utf-8").read()
    found = 0
    if re.search(r"max-width:\s*1023px", css) and re.search(r"min-width:\s*1024px", js):
        found += 1
    else:
        print("НЕТ границы по ширине экрана в стиле или в скрипте")
    if "prefers-reduced-motion" in css and "prefers-reduced-motion" in js:
        found += 1
    else:
        print("НЕТ границы по «уменьшить движение» в стиле или в скрипте")
    print("guards=%d;" % found)
    return 0 if found == 2 else 1


if __name__ == "__main__":
    sys.exit(main())
