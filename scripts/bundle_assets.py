# -*- coding: utf-8 -*-
"""Слить стили и скрипты в два файла вместо четырнадцати.

Замерено на живом сайте 23.08 (телефон, медленный 4G, процессор ×4):
страница тянула семь файлов стилей и семь своих скриптов — четырнадцать
отдельных запросов, и все семь стилей блокировали показ.

Исходники остаются раздельными: править удобно по файлам, отдавать —
одним. Порядок склейки задан здесь и повторяет порядок подключения,
который был в источнике: у стилей от него зависит переопределение,
у скриптов — доступность общих объектов.

Сборка проверяет, что ни один файл не потерялся: список ниже и список
подключений в _src/index.src.html обязаны совпадать. Разошлись — сборка
падает, а не отдаёт молча урезанный сайт.

    py scripts/bundle_assets.py           # показать
    py scripts/bundle_assets.py --write   # собрать
"""
import hashlib
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_src" / "index.src.html"
OUT = ROOT / "assets" / "build"

CSS_ORDER = ["tokens", "base", "layout", "components", "motion", "hero", "marks"]
JS_ORDER = ["lang", "dotgrid", "terminal", "projects", "form", "whatsapp", "main"]


def listed(kind):
    """Что подключено в источнике — источник правды, а не память."""
    html = io.open(SRC, encoding="utf-8").read()
    if kind == "css":
        found = re.findall(r'assets/css/([a-z0-9_-]+)\.css', html)
    else:
        found = re.findall(r'assets/js/([a-z0-9_-]+)\.js', html)
    out = []
    for name in found:
        if name not in out:
            out.append(name)
    return out


def build(kind, order, ext, comment):
    names = listed(kind)
    missing = [n for n in names if n not in order]
    extra = [n for n in order if n not in names]
    if missing or extra:
        print("СПИСКИ РАЗОШЛИСЬ (%s): нет в порядке склейки %s; нет в источнике %s"
              % (kind, missing or "—", extra or "—"))
        return None
    parts = []
    for n in order:
        f = ROOT / "assets" / kind / (n + "." + ext)
        if not f.is_file():
            print("НЕТ ФАЙЛА: %s" % f)
            return None
        parts.append(comment % n + io.open(f, encoding="utf-8").read())
    return "\n".join(parts)


def main():
    write = "--write" in sys.argv
    css = build("css", CSS_ORDER, "css", "\n/* ── %s ── */\n")
    js = build("js", JS_ORDER, "js", "\n/* ── %s ── */\n")
    if css is None or js is None:
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    for name, body in (("site.css", css), ("site.js", js)):
        h = hashlib.md5(body.encode("utf-8")).hexdigest()[:10]
        if write:
            io.open(OUT / name, "w", encoding="utf-8", newline="\n").write(body)
        print("%-10s %7.1f КБ  метка %s" % (name, len(body.encode("utf-8")) / 1024.0, h))

    print("собрано" if write else "холостой прогон, запусти с --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
