# -*- coding: utf-8 -*-
"""Состояние секции обязано соответствовать данным.

Отзывов ноль — секция скрыта. Отзывы есть — показана. Проверяется на обеих
главных, потому что забыть английскую проще всего.
"""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEC = r'<section class="reviews" id="reviews"([^>]*)>'


def main():
    data = json.load(io.open(ROOT / "data" / "reviews.json", encoding="utf-8"))
    n = len(data.get("reviews") or [])
    want_hidden = (n == 0)
    bad = []
    for rel in ("index.html", "en/index.html"):
        html = io.open(ROOT / rel, encoding="utf-8").read()
        m = re.search(SEC, html)
        if not m:
            bad.append("%s: секции нет" % rel)
            continue
        is_hidden = "hidden" in m.group(1)
        cards = html.count('class="review"')
        if is_hidden != want_hidden:
            bad.append("%s: hidden=%s при %d отзывах" % (rel, is_hidden, n))
        if cards != n:
            bad.append("%s: карточек %d, в данных %d" % (rel, cards, n))
    if bad:
        print("STATE_BROKEN: " + "; ".join(bad))
        return 1
    print("STATE_CONSISTENT reviews=%d hidden=%s" % (n, want_hidden))
    return 0


sys.exit(main())
