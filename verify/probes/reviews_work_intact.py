# -*- coding: utf-8 -*-
"""Вставка блока отзывов ничего не съела: карточек работ столько же, сколько
проектов в data/projects.json, на обеих главных, и ссылка на Impressum на месте.

Число сверяется с источником данных, а не с константой «16»: константа
ломается от нового проекта, а не от поломки (Закон 27 §5). Прежняя проба
искала точное class="card", а у карточек работ есть классы раскладки —
она находила одну и падала ещё до этой задачи.
"""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    data = json.load(io.open(ROOT / "data" / "projects.json", encoding="utf-8"))
    projects = data if isinstance(data, list) else data.get("projects", [])
    # На главной показываются только live-проекты: снятый с публикации
    # (status archived, например Studio of Glamour 11.09.2026) карточки не имеет.
    need = len([p for p in projects if (p.get("status") or "") == "live"])
    bad = []
    for rel in ("index.html", "en/index.html"):
        html = io.open(ROOT / rel, encoding="utf-8").read()
        got = len(re.findall(r'class="card layout-', html))
        if got != need:
            bad.append("%s: карточек %d, проектов %d" % (rel, got, need))
        if "impressum" not in html.lower():
            bad.append("%s: нет ссылки на Impressum" % rel)
    if bad:
        print("WORK_BROKEN: " + "; ".join(bad))
        return 1
    print("WORK_INTACT cards=%d" % need)
    return 0


sys.exit(main())
