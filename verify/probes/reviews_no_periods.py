# -*- coding: utf-8 -*-
"""Правило типографики MainCore: без точек в конце заголовков и кнопок.

Тело отзыва и обязательная юридическая пометка — длинные предложения,
там точки уместны и намеренно не проверяются.
"""
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGETS = [
    (r'<h2 class="section-title"><span>(.*?)</span>', "заголовок"),
    (r'class="reviews-shown">(.*?)<', "подпись выборки"),
    (r'class="reviews-profile"[^>]*>(.*?)<', "ссылка на профиль"),
    (r'class="reviews-ask-cta"[^>]*>(.*?)<', "кнопка отзыва"),
    (r'<div class="reviews-ask">\s*<p>(.*?)</p>', "призыв"),
]


def main():
    bad = []
    for rel in ("index.html", "en/index.html"):
        html = io.open(ROOT / rel, encoding="utf-8").read()
        m = re.search(r'<section class="reviews".*?</section>', html, re.S)
        if not m:
            continue
        body = m.group(0)
        for pat, name in TARGETS:
            for txt in re.findall(pat, body, re.S):
                if txt.strip().endswith("."):
                    bad.append("%s: %s кончается точкой — %r"
                               % (rel, name, txt.strip()[:60]))
    if bad:
        print("PERIODS_FOUND: " + "; ".join(bad))
        return 1
    print("NO_PERIODS")
    return 0


sys.exit(main())
