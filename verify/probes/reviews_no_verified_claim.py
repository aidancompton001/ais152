# -*- coding: utf-8 -*-
"""Anhang Nr. 23b zu § 3 UWG: запрещено утверждать, что отзывы проверены.

Ищутся слова из семьи «проверено» внутри секции. Отрицание вида
«prüfen sie nicht selbst» — это не утверждение о проверке, поэтому оно
вырезается перед поиском: иначе проба ловила бы собственную обязательную
пометку и запрещала ставить то, что закон требует.
"""
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BAN = (r"(echtheitsgepr|verifiziert|geprüfte bewertung|verified review"
       r"|authenticity verified|von uns geprüft)")
NEG = (r"(prüfen sie nicht selbst|prüfen wir nicht selbst"
       r"|do not check their|do not verify their)")


def main():
    bad = []
    for rel in ("index.html", "en/index.html"):
        html = io.open(ROOT / rel, encoding="utf-8").read()
        m = re.search(r'<section class="reviews".*?</section>', html, re.S)
        if not m:
            continue
        body = re.sub(NEG, " ", m.group(0).lower())
        for hit in re.findall(BAN, body):
            bad.append("%s: %s" % (rel, hit))
    if bad:
        print("VERIFIED_CLAIM_FOUND: " + "; ".join(bad))
        return 1
    print("NO_VERIFIED_CLAIM")
    return 0


sys.exit(main())
