# -*- coding: utf-8 -*-
"""Перенести тексты кейсов из docs/cases/<slug>.json в data/projects.json (поле case_de).

docs/cases/ — черновик с источниками каждого утверждения (claims), его проверяет
ревьюер. В projects.json уходят только три раздела текста; claims остаются в docs.

    py scripts/merge_cases.py           # холостой прогон
    py scripts/merge_cases.py --write   # записать
"""
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "projects.json"
CASES = ROOT / "docs" / "cases"
KEYS = ("ausgangslage", "umsetzung", "ergebnis")


def main():
    write = "--write" in sys.argv
    data = json.load(io.open(DATA, encoding="utf-8"))
    items = data if isinstance(data, list) else data["projects"]
    by_slug = {p["slug"]: p for p in items}
    done = 0
    for f in sorted(CASES.glob("*.json")):
        c = json.load(io.open(f, encoding="utf-8"))
        slug = c.get("slug") or f.stem
        if slug not in by_slug:
            print("НЕТ ПРОЕКТА %s — пропущен" % slug)
            continue
        if not all((c.get(k) or "").strip() for k in KEYS):
            print("НЕПОЛНЫЙ %s — пропущен" % slug)
            continue
        by_slug[slug]["case_de"] = {k: c[k].strip() for k in KEYS}
        done += 1
        print("%-24s %4d слов" % (slug, sum(len(c[k].split()) for k in KEYS)))
    if write:
        io.open(DATA, "w", encoding="utf-8", newline="\n").write(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print("перенесено: %d" % done if write else "холостой прогон: %d" % done)
    return 0


if __name__ == "__main__":
    sys.exit(main())
