# -*- coding: utf-8 -*-
"""§ 5b Abs. 3 UWG: пометка о происхождении отзывов стоит В блоке.

Проверяется не наличие слова где-то на странице, а то, что абзац лежит
внутри секции отзывов — закон требует зрительной связи с самими отзывами.
Когда секция скрыта, проверять нечего: блока для читателя нет.
"""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    data = json.load(io.open(ROOT / "data" / "reviews.json", encoding="utf-8"))
    if not (data.get("reviews") or []):
        print("UWG_NOTE_OK (секция скрыта, отзывов нет)")
        return 0
    bad = []
    for rel in ("index.html", "en/index.html"):
        html = io.open(ROOT / rel, encoding="utf-8").read()
        m = re.search(r'<section class="reviews".*?</section>', html, re.S)
        if not m:
            bad.append("%s: секции нет" % rel)
            continue
        body = m.group(0)
        note = re.search(r'<p class="reviews-note">(.*?)</p>', body, re.S)
        if not note:
            bad.append("%s: нет абзаца-пометки" % rel)
            continue
        txt = note.group(1).lower()
        if "google" not in txt:
            bad.append("%s: пометка не называет источник" % rel)
        if not re.search(r"nicht selbst|do not check|do not verify", txt):
            bad.append("%s: не сказано, что мы не проверяем" % rel)
    if bad:
        print("UWG_NOTE_MISSING: " + "; ".join(bad))
        return 1
    print("UWG_NOTE_OK")
    return 0


sys.exit(main())
