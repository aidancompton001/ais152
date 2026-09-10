# -*- coding: utf-8 -*-
"""Пробы приёмки PX-022 — The Crazy Bee первой карточкой, счётчик 15 → 16.

Логика вынесена сюда, а не в строки acceptance-файла: команды с кавычками
внутри JSON — место, где опечатка выглядит как провал проверки.

    py verify/probe_px022.py <имя пробы>
"""
import io
import json
import os
import re
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

BUILT = ["index.html", "en/index.html", "leistungen/index.html", "projekte/index.html"]
LIMITS = {"title": 60, "tagline_en": 80, "tagline_de": 80, "summary_en": 280, "summary_de": 280}


def data():
    return json.load(io.open("data/projects.json", encoding="utf-8"))


def read(p):
    return io.open(p, encoding="utf-8").read()


def p_first():
    ps = sorted(data(), key=lambda x: x["order"])
    return "%s order=%d" % (ps[0]["slug"], ps[0]["order"])


def p_total():
    return str(len([p for p in data() if p.get("status") == "live"]))


def p_orders():
    o = sorted(p["order"] for p in data())
    return "ok" if o == list(range(1, len(o) + 1)) else "дыры или дубли: %s" % o


def p_old_order():
    """Прежние 15 проектов идут в том же порядке, что до задачи."""
    old = json.loads(subprocess.run(["git", "show", "v2-pre-px022:data/projects.json"],
                                    capture_output=True, text=True, encoding="utf-8").stdout)
    was = [p["slug"] for p in sorted(old, key=lambda x: x["order"])]
    now = [p["slug"] for p in sorted(data(), key=lambda x: x["order"]) if p["slug"] != "staskiewitz"]
    return "сохранён" if was == now else "изменён"


def p_lengths():
    e = [p for p in data() if p["slug"] == "staskiewitz"][0]
    bad = [k for k, lim in LIMITS.items() if len(e.get(k, "")) > lim]
    return "ok" if not bad else "длиннее лимита: %s" % bad


def p_url():
    return [p for p in data() if p["slug"] == "staskiewitz"][0]["url"]


def p_shot():
    from PIL import Image
    f = "assets/staskiewitz-site.jpg"
    im = Image.open(f)
    return "%dx%d %s" % (im.size[0], im.size[1], os.path.getsize(f) > 10 * 1024)


def p_mark():
    return " ".join(str(read(f).count('id="mark-staskiewitz"')) for f in ("index.html", "en/index.html"))


def p_first_card():
    out = []
    for f in ("index.html", "en/index.html"):
        slugs = re.findall(r'data-slug="([a-z0-9-]+)"', read(f))
        out.append(slugs[0] if slugs else "нет")
    return " ".join(out)


def p_cards():
    return " ".join(str(read(f).count('class="card layout-')) for f in ("index.html", "en/index.html"))


def p_sixteen():
    """16 стоит во всех местах, где сайт называет число проектов."""
    de, en = read("index.html"), read("en/index.html")
    hub, cases = read("leistungen/index.html"), read("projekte/index.html")
    checks = [
        'data-target="16"' in de, 'data-target="16"' in en,
        "16 live" in de, "16 live" in en,
        "16 projects" in en, "Sechzehn" in de, "Sixteen" in en,
        "Sechzehn ausgelieferte" in hub, "sechzehn" in cases,
    ]
    return "%d/%d" % (sum(checks), len(checks))


def p_no_fifteen():
    """Старого числа не осталось ни на одной собранной странице."""
    pat = re.compile(r"\b15 (live|projects|Projekte|Live-Projekte)\b|Fünfzehn|fünfzehn|Fifteen|fifteen"
                     r'|data-target="15"')
    files = BUILT + [os.path.join("leistungen", f) for f in os.listdir("leistungen") if f.endswith(".html")]
    hits = [f for f in sorted(set(files)) if pat.search(read(f))]
    return "0" if not hits else "%d: %s" % (len(hits), hits)


def p_src_from_data():
    """Два места, где число писали руками, теперь берут его из данных."""
    src = read("_src/index.src.html")
    hub = read("_src/leistungen_index.html")
    return "%s %s" % ('data-target="{{N}}"' in src, "{{WORD_DE}} ausgelieferte" in hub)


def p_case_page():
    f = "projekte/staskiewitz.html"
    return "%s %s" % (os.path.isfile(f), os.path.isfile(f) and "thecrazybee.de" in read(f))


def p_sitemap():
    return str("projekte/staskiewitz.html" in read("sitemap.xml"))


def p_live():
    req = urllib.request.Request("https://thecrazybee.de/", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return str(r.status)


def _dotted(txt):
    out = set()
    for m in re.findall(r"<h[1-4][^>]*>(.*?)</h[1-4]>", txt, re.S):
        t = re.sub(r"<[^>]+>", "", m).strip()
        if t.endswith("."):
            out.add(t)
    return out


def p_periods():
    """Глобальное правило типографики: задача не добавила ни одного h1–h4 с точкой.

    Меряется прирост против состояния до задачи, а не абсолют: на главной уже
    стоит «Website-Wartung — ab 39 €/Mon.» — точка там от сокращения «Monat»,
    заголовок чужой задачи, и трогать его в этой значит ломать то, о чём
    не просили.
    """
    n = 0
    for f in ("index.html", "en/index.html", "projekte/staskiewitz.html"):
        old = subprocess.run(["git", "show", "v2-pre-px022:" + f], capture_output=True,
                             text=True, encoding="utf-8")
        was = _dotted(old.stdout) if old.returncode == 0 else set()
        n += len(_dotted(read(f)) - was)
    return str(n)


PROBES = {k[2:]: v for k, v in globals().items() if k.startswith("p_")}

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else ""
    if name not in PROBES:
        sys.exit("пробы: %s" % ", ".join(sorted(PROBES)))
    print(PROBES[name]())
