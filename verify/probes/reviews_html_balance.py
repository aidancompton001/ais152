# -*- coding: utf-8 -*-
"""Вставка не должна разъезжаться по тегам.

Считаются открывающие и закрывающие section и article на обеих главных.
Проба грубая намеренно: её задача — поймать оборванную вставку, а не
подменить собой валидатор разметки.
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
        for tag in ("section", "article"):
            op = len(re.findall(r"<%s\b" % tag, html))
            cl = len(re.findall(r"</%s>" % tag, html))
            if op != cl:
                bad.append("%s: <%s> %d, </%s> %d" % (rel, tag, op, tag, cl))
        if (html.count("<!-- reviews:static:start -->")
                != html.count("<!-- reviews:static:end -->")):
            bad.append("%s: маркеры сборщика не парные" % rel)
    if bad:
        print("UNBALANCED: " + "; ".join(bad))
        return 1
    print("BALANCED")
    return 0


sys.exit(main())
