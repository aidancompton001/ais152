# -*- coding: utf-8 -*-
"""Блок отзывов стоит сразу над работами — на обеих главных, ровно один раз,
и при показе нумерация становится 01 отзывы … 06 контакт.

Место выбрано CEO 10.09.2026. Вторая половина пробы включает блок на копии
страницы в памяти (рабочие файлы не трогаются): иначе ветка «блок показан»
доказывалась бы только тогда, когда придёт первый живой отзыв.
"""
import importlib.util
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "r", ROOT / "scripts" / "render_reviews_static.py")
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)

OVER = re.compile(r'<span class="overline">(\d\d) / <span>')


def main():
    bad = []
    for rel in ("index.html", "en/index.html"):
        html = io.open(ROOT / rel, encoding="utf-8").read()
        ids = re.findall(r'<section class="[a-z]+" id="([a-z]+)"', html)
        if ids.count("reviews") != 1:
            bad.append("%s: блоков отзывов %d" % (rel, ids.count("reviews")))
            continue
        i = ids.index("reviews")
        if i + 1 >= len(ids) or ids[i + 1] != "work":
            bad.append("%s: после отзывов идёт %s" % (rel, ids[i + 1:i + 2]))
        shown = r.renumber_sections(html.replace(
            '<section class="reviews" id="reviews" hidden>',
            '<section class="reviews" id="reviews">'))
        nums = OVER.findall(shown)
        want = ["%02d" % k for k in range(1, len(nums) + 1)]
        # Ждём ровно на один раздел больше, чем видно при скрытом блоке, —
        # от числа разделов на странице, а не от константы (Закон 27 §5).
        before = len(OVER.findall(r.renumber_sections(html))) - 1
        if nums != want or len(nums) != before + 1:
            bad.append("%s: при показе номера %s" % (rel, ",".join(nums)))
    if bad:
        print("PLACEMENT_BAD: " + "; ".join(bad))
        return 1
    print("PLACEMENT_OK reviews->work, shown 01..06")
    return 0


sys.exit(main())
