# -*- coding: utf-8 -*-
"""Номера разделов не задваиваются.

Секция отзывов встаёт пятой, контакт обязан стать шестым. Если сборщик
не перенумеровал контакт, на странице два раздела «05» — читателю это
видно, и выглядит как поломка вёрстки.
"""
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    bad = []
    for rel in ("index.html", "en/index.html"):
        html = io.open(ROOT / rel, encoding="utf-8").read()
        nums = re.findall(r'<span class="overline">(\d\d) / ', html)
        dupes = sorted({n for n in nums if nums.count(n) > 1})
        if dupes:
            bad.append("%s: повторы %s (все: %s)"
                       % (rel, ",".join(dupes), ",".join(nums)))
    if bad:
        print("OVERLINE_DUPLICATED: " + "; ".join(bad))
        return 1
    print("OVERLINE_UNIQUE")
    return 0


sys.exit(main())
