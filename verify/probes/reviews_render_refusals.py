# -*- coding: utf-8 -*-
"""Сборщик отказывает на данных, которые дали бы кривой блок, и склоняет число.

Всё на временном файле данных в памяти процесса: DATA сборщика подменяется,
запуск без --write, рабочие страницы не трогаются.
  A отзыв есть, даты «Stand» нет            -> отказ (находка #14 F-01)
  B один отзыв в профиле                    -> «1 Bewertung», не «1 Bewertungen» (F-08)
  C блок без комментария-маркера вырезается -> один блок, не два (F-03)
"""
import importlib.util
import io
import json
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "r", ROOT / "scripts" / "render_reviews_static.py")
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)

REVIEW = {"author": "Test", "rating": 5, "text": "Gut",
          "datePublished": "2026-09-01"}


def run(prof):
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "reviews.json"
        f.write_text(json.dumps({"googleProfile": prof, "reviews": [REVIEW]}),
                     encoding="utf-8")
        r.DATA = f
        sys.argv = ["x"]
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = r.main()
        return rc, buf.getvalue()


def main():
    bad = []
    base = {"profileUrl": "https://example.invalid/p", "ratingValue": 5.0,
            "ratingCount": 1, "bestRating": 5}
    rc, out = run(dict(base))
    if rc != 1 or "asOfShort" not in out:
        bad.append("A: без даты не отказал (rc=%s)" % rc)
    prof = dict(base, asOfShort="09/2026", asOfLabel="September 2026")
    b = r.block([REVIEW], prof, "de", 1)
    if "1 Bewertung (" not in b or "Stand: )" in b:
        bad.append("B: строка цифр '%s'" % b[b.find("bei Google"):][:40])
    if "1 review (" not in r.block([REVIEW], prof, "en", 1):
        bad.append("B: en не склоняет")
    html = ('<section class="reviews" id="reviews" hidden>x</section>\n'
            + r.ANCHOR + '</section>')
    import re
    cut = re.sub(r.OLD_BLOCK_RE, "", html, flags=re.S)
    if 'id="reviews"' in cut:
        bad.append("C: блок без маркера не вырезан")
    if bad:
        print("REFUSALS_BAD: " + "; ".join(bad))
        return 1
    print("REFUSALS_OK A B C")
    return 0


sys.exit(main())
