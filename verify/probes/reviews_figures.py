# -*- coding: utf-8 -*-
"""Числа блока не должны противоречить друг другу.

Закон 27 §1: рядом с каждым числом печатается запрос, которым оно получено.
Здесь запрос — сам этот файл: карточки считаются по разметке, профильные
числа берутся из data/reviews.json, и они сверяются между собой.
"""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    data = json.load(io.open(ROOT / "data" / "reviews.json", encoding="utf-8"))
    items = data.get("reviews") or []
    prof = data.get("googleProfile") or {}
    rc = prof.get("ratingCount") or 0
    rv = prof.get("ratingValue")
    best = prof.get("bestRating") or 5
    worst = prof.get("worstRating") or 1
    bad = []

    if items and len(items) > rc:
        bad.append("карточек %d > отзывов в профиле %d" % (len(items), rc))
    if rv is not None and not (worst <= rv <= best):
        bad.append("рейтинг %s вне шкалы %s..%s" % (rv, worst, best))
    if items and rv is None:
        bad.append("есть отзывы, но у профиля нет рейтинга")

    for r in items:
        rid = r.get("id") or "(без id)"
        if not (worst <= int(r.get("rating") or 0) <= best):
            bad.append("оценка вне шкалы у %s" % rid)
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", r.get("datePublished") or ""):
            bad.append("нет корректной даты у %s" % rid)
        if not (r.get("author") or "").strip():
            bad.append("нет автора у %s" % rid)
        if not (r.get("text") or "").strip():
            bad.append("пустой текст у %s" % rid)

    for rel in ("index.html", "en/index.html"):
        html = io.open(ROOT / rel, encoding="utf-8").read()
        n = html.count('class="review"')
        if n != len(items):
            bad.append("%s: карточек в разметке %d, в данных %d"
                       % (rel, n, len(items)))

    if bad:
        print("FIGURES_BROKEN: " + "; ".join(bad))
        return 1
    print("FIGURES_CONSISTENT cards=%d profile_count=%d rating=%s"
          % (len(items), rc, rv))
    return 0


sys.exit(main())
