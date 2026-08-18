# -*- coding: utf-8 -*-
"""Собрать страницы услуг из содержания в _src/leistungen/*.json.

Зачем. У сайта была одна страница на все запросы. У конкурентов, занимающих
немецкую выдачу, — одна страница на один запрос: ключ стоит дословно в title,
в h1 и повторён в подзаголовках. Одностраничник конкурировать с этим не может
структурно: у него один заголовок на всё.

Оформление берётся из собранной немецкой главной: head, шапка и подвал
переиспользуются целиком, чтобы страницы не расходились по виду и чтобы
правка навигации не требовала правки пяти файлов.

    py scripts/build_services.py           # показать
    py scripts/build_services.py --write   # собрать
"""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "_src" / "leistungen"
OUT = ROOT / "leistungen"
BASE = "https://ais152.com"


def shell():
    """Голова, шапка и подвал немецкой главной."""
    home = io.open(ROOT / "index.html", encoding="utf-8").read()
    head = re.search(r"<head>(.*?)</head>", home, re.S).group(1)
    header = re.search(r"<header\b.*?</header>", home, re.S).group(0)
    footer_m = re.search(r"<footer\b.*?</footer>\s*(?=<script|</body>)", home, re.S)
    footer = footer_m.group(0) if footer_m else ""
    scripts = "".join(re.findall(r"<script[^>]*src=[^>]*></script>", home))
    return head, header, footer, scripts


def head_for(head, page):
    url = ("%s/leistungen/" % BASE if page["slug"] == "index"
           else "%s/leistungen/%s.html" % (BASE, page["slug"]))
    head = re.sub(r"<title>.*?</title>", "<title>%s</title>" % page["title"],
                  head, count=1, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*">',
                  '<meta name="description" content="%s">' % page["description"],
                  head, count=1)
    head = re.sub(r'<link rel="canonical"[^>]*>',
                  '<link rel="canonical" href="%s">' % url, head, count=1)
    # Страница существует только по-немецки: языковых альтернатив у неё нет,
    # и объявлять несуществующую английскую версию нельзя.
    head = re.sub(r'(\s*<link rel="alternate" hreflang="[^"]*"[^>]*>)+', "", head)
    head = re.sub(r'<meta property="og:title" content="[^"]*">',
                  '<meta property="og:title" content="%s">' % page["title"], head, count=1)
    head = re.sub(r'<meta property="og:description" content="[^"]*">',
                  '<meta property="og:description" content="%s">' % page["description"],
                  head, count=1)
    head = re.sub(r'<meta property="og:url" content="[^"]*">',
                  '<meta property="og:url" content="%s">' % url, head, count=1)

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Service", "@id": url + "#service",
             "name": page["phrase"], "description": page["description"],
             "serviceType": page["phrase"], "url": url,
             "areaServed": {"@type": "City", "name": "München"},
             "provider": {"@id": BASE + "/#service"}},
            {"@type": "BreadcrumbList", "@id": url + "#breadcrumb",
             "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Start", "item": BASE + "/"},
                 {"@type": "ListItem", "position": 2, "name": "Leistungen",
                  "item": BASE + "/leistungen/"},
                 {"@type": "ListItem", "position": 3, "name": page["phrase"], "item": url},
             ]},
        ],
    }
    head += ('\n<script type="application/ld+json">\n%s\n</script>\n'
             % json.dumps(ld, ensure_ascii=False, indent=2))
    return head


def body_for(page):
    parts = ['<main id="main" class="page-leistung">',
             '  <section class="section" id="top">',
             '    <div class="container">',
             '      <nav class="breadcrumb" aria-label="Brotkrumen">',
             '        <a href="/">Start</a> <span aria-hidden="true">/</span> '
             '<a href="/leistungen/">Leistungen</a> <span aria-hidden="true">/</span> '
             '<span aria-current="page">%s</span>' % page["phrase"],
             '      </nav>',
             '      <h1 class="hero-title">%s</h1>' % page["h1"],
             '      <p class="hero-sub">%s</p>' % page["lead"],
             '    </div>',
             '  </section>']

    for i, sec in enumerate(page["sections"]):
        parts.append('  <section class="section">')
        parts.append('    <div class="container">')
        parts.append('      <h2 class="section-title">%s</h2>' % sec["h2"])
        for block in sec["body"]:
            parts.append("      %s" % (block if block.lstrip().startswith("<")
                                       else "<p>%s</p>" % block))
        parts.append('    </div>')
        parts.append('  </section>')

    rel = " ".join('<a href="/leistungen/%s.html" class="link-inline">%s</a>' % (slug, name)
                   for slug, name in page["related"])
    parts += ['  <section class="section" id="contact">',
              '    <div class="container">',
              '      <h2 class="section-title">%s</h2>' % page["cta"],
              '      <p><a href="/#contact" class="btn btn-primary">Projekt beschreiben</a></p>',
              '      <p>Verwandte Leistungen: %s</p>' % rel,
              '      <p>Sechzehn ausgelieferte Projekte stehen unter '
              '<a href="/#work" class="link-inline">Ausgewählte Arbeiten</a></p>',
              '    </div>',
              '  </section>',
              '</main>']
    return "\n".join(parts)


def main():
    write = "--write" in sys.argv
    files = sorted(CONTENT.glob("*.json"))
    if not files:
        print("НЕТ СОДЕРЖАНИЯ: %s" % CONTENT)
        return 1

    head, header, footer, scripts = shell()
    pages = []
    for f in files:
        page = json.load(io.open(f, encoding="utf-8"))
        html = ("<!DOCTYPE html>\n"
                '<html lang="de" data-lang="de">\n<head>%s</head>\n<body>\n%s\n%s\n%s\n%s\n'
                "</body>\n</html>\n"
                % (head_for(head, page), header, body_for(page), footer, scripts))

        # Ключ обязан стоять в title, в h1 и минимум в двух h2 — иначе Google
        # перепишет заголовок своим, и он из выдачи исчезнет.
        key = page["phrase"].split()[0].lower()
        h2s = [re.sub(r"<[^>]+>", "", x) for x in re.findall(r"<h2[^>]*>(.*?)</h2>", html, re.S)]
        hits = sum(1 for x in h2s if key in x.lower())
        if key not in page["title"].lower() or key not in page["h1"].lower() or hits < 2:
            print("КЛЮЧ '%s' НЕ ЗАКРЕПЛЁН: title=%s h1=%s h2=%d — %s"
                  % (key, key in page["title"].lower(), key in page["h1"].lower(),
                     hits, page["slug"]))
            return 1

        if write:
            OUT.mkdir(parents=True, exist_ok=True)
            io.open(OUT / (page["slug"] + ".html"), "w", encoding="utf-8",
                    newline="\n").write(html)
        pages.append((page["slug"], len(html.encode("utf-8")), hits))

    # Хаб-страница раздела: без неё пять страниц висят на одном абзаце
    # главной, а раздел не существует как сущность.
    hub_body = io.open(ROOT / "_src" / "leistungen_index.html", encoding="utf-8").read()
    hub = {"slug": "index", "phrase": "Leistungen",
           "title": "Leistungen — Automatisierung und KI für den Mittelstand | AIS.152",
           "description": ("Automatisierung mit n8n, KI-Integration und Betrieb. "
                           "Fünf Leistungen, jede einzeln beschrieben — mit dem, "
                           "was sie kann und was nicht.")}
    hub_html = ("<!DOCTYPE html>" + chr(10) +
                '<html lang="de" data-lang="de">' + chr(10) + "<head>%s</head>" + chr(10) +
                "<body>" + chr(10) + "%s" + chr(10) + "%s" + chr(10) + "%s" + chr(10) + "%s" + chr(10) +
                "</body>" + chr(10) + "</html>" + chr(10))
    hub_html = hub_html % (head_for(head, hub), header, hub_body, footer, scripts)
    if write:
        io.open(OUT / "index.html", "w", encoding="utf-8",
                newline=chr(10)).write(hub_html)
    pages.append(("index (хаб раздела)", len(hub_html.encode("utf-8")), 0))

    for slug, size, hits in pages:
        print("%-34s %6d байт  ключ в %d подзаголовках" % (slug, size, hits))
    print("собрано: %d" % len(pages) if write else "холостой прогон, запусти с --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
