# -*- coding: utf-8 -*-
"""Собрать карту сайта ais152.com.

Даты правок берутся из журнала git, а не пишутся от руки: рукописная дата
разъезжается с файлом при первой же правке и сообщает Google, что страница
не менялась, когда она менялась.

Страницы с meta robots=noindex в карту не попадают — карта, зовущая на
закрытую страницу, это противоречивый сигнал.

    py scripts/build_sitemap.py           # показать
    py scripts/build_sitemap.py --write   # записать sitemap.xml
"""
import datetime
import io
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://ais152.com"

# страница -> (адрес в карте, приоритет, частота)
# Языковые пары: адрес → его альтернатива на другом языке. Взаимные hreflang
# обязаны перечислять КАЖДУЮ версию, включая себя — иначе Google связку
# не строит.
LANG_PAIRS = {
    "/": {"de": "/", "en": "/en/"},
    "/en/": {"de": "/", "en": "/en/"},
}

PAGES = [
    ("index.html",       "/",                1.0, "weekly"),
    ("en/index.html",    "/en/",             0.9, "weekly"),
    ("wartung.html",     "/wartung.html",    0.8, "monthly"),
    ("impressum.html",   "/impressum.html",  0.4, "yearly"),
    ("datenschutz.html", "/datenschutz.html", 0.4, "yearly"),
    ("agb.html",         "/agb.html",        0.3, "yearly"),
    ("widerruf.html",    "/widerruf.html",   0.3, "yearly"),
    ("avv.html",         "/avv.html",        0.3, "yearly"),
]

HEAD = ('<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n')
def alternates(loc):
    """Взаимные hreflang для языковой пары.

    Требование Google: каждая версия обязана перечислять себя и все остальные.
    До 18.08.2026 здесь стояли три альтернативы, ведущие на ОДИН адрес, —
    языкового таргетинга это не создавало вовсе.
    """
    pair = LANG_PAIRS.get(loc)
    if not pair:
        return ""
    tpl = '    <xhtml:link rel="alternate" hreflang="%s" href="%s%s" />'
    rows = [tpl % (code, BASE, path) for code, path in sorted(pair.items())]
    rows.append(tpl % ("x-default", BASE, pair["de"]))
    return chr(10).join(rows) + chr(10)


def git_date(name):
    res = subprocess.run(["git", "log", "-1", "--format=%ad", "--date=short",
                          "--", name],
                         cwd=str(ROOT), capture_output=True, text=True)
    out = (res.stdout or "").strip()
    return out or None


def is_noindex(path):
    text = io.open(path, encoding="utf-8", errors="replace").read(4000)
    m = re.search(r'<meta[^>]+name=["\']robots["\'][^>]*>', text, re.I)
    return bool(m and "noindex" in m.group(0).lower())


def main():
    write = "--write" in sys.argv
    body, problems, skipped = [], [], []

    for name, loc, prio, freq in PAGES:
        path = ROOT / name
        if not path.is_file():
            problems.append("нет файла: %s" % name)
            continue
        if is_noindex(path):
            # Закрыта решением проекта (impressum, datenschutz, avv). Карта,
            # зовущая на закрытую страницу, — противоречивый сигнал, поэтому
            # такая страница просто не берётся, а не роняет сборку.
            skipped.append(name)
            continue
        date = git_date(name)
        if not date:
            # Страница есть на диске, но ещё не в журнале git — значит создана
            # сегодня. Дата берётся из источника, из которого она собрана,
            # либо считается сегодняшней: врать «не менялась» нельзя, а падать
            # из-за новой страницы — значит запрещать себе добавлять страницы.
            date = git_date("index.src.html") or datetime.date.today().isoformat()
        chunk = ("  <url>\n"
                 "    <loc>%s%s</loc>\n"
                 "    <lastmod>%s</lastmod>\n"
                 "    <changefreq>%s</changefreq>\n"
                 "    <priority>%.1f</priority>\n" % (BASE, loc, date, freq, prio))
        chunk += alternates(loc)
        chunk += "  </url>\n"
        body.append(chunk)

    if problems:
        for p in problems:
            print(p)
        return 1

    if skipped:
        print("закрыты noindex, в карту не вошли: %s" % ", ".join(skipped))

    xml = HEAD + "".join(body) + "</urlset>\n"
    if write:
        io.open(ROOT / "sitemap.xml", "w", encoding="utf-8", newline="\n").write(xml)
        print("записано адресов: %d" % len(body))
    else:
        print(xml)
        print("холостой прогон, запусти с --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
