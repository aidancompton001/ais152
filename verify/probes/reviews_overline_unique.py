# -*- coding: utf-8 -*-
"""Номера разделов идут подряд 01..N и не задваиваются — по ВИДИМЫМ разделам.

Блок отзывов стоит над работами (решение CEO 10.09.2026). Пока он скрыт,
посетитель видит 01 Arbeiten … 05 Kontakt; когда он показан — 01 отзывы …
06 контакт. Номер внутри скрытого раздела никто не видит, поэтому он в
счёт не идёт: иначе проба ругалась бы на то, чего на экране нет.
"""
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def visible_numbers(html):
    sections = [(m.start(), " hidden" in m.group(0))
                for m in re.finditer(r"<section\b[^>]*>", html)]
    nums = []
    for m in re.finditer(r'<span class="overline">(\d\d) / ', html):
        owner = [h for pos, h in sections if pos < m.start()]
        if not (owner and owner[-1]):
            nums.append(m.group(1))
    return nums


def main():
    bad = []
    for rel in ("index.html", "en/index.html"):
        html = io.open(ROOT / rel, encoding="utf-8").read()
        nums = visible_numbers(html)
        want = ["%02d" % i for i in range(1, len(nums) + 1)]
        if nums != want:
            bad.append("%s: видно %s, ждали %s"
                       % (rel, ",".join(nums), ",".join(want)))
    if bad:
        print("OVERLINE_DUPLICATED: " + "; ".join(bad))
        return 1
    print("OVERLINE_UNIQUE")
    return 0


sys.exit(main())
