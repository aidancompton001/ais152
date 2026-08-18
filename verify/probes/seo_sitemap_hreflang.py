# -*- coding: utf-8 -*-
"""Проба: языковые альтернативы в карте сайта ведут на РАЗНЫЕ адреса.

До 18.08.2026 в карте стояли три альтернативы — de, en и x-default, — и все
три указывали на один и тот же адрес. Механизм hreflang подразумевает разные
адреса на разные версии; три ссылки на один адрес не создают языкового
таргетинга вовсе, они просто ничего не значат.

Требование Google: каждая версия обязана перечислять себя И все остальные.
Проверяется на ЖИВОЙ карте.

Печатает 'SITEMAP_HREFLANG pairs=<сколько адресов с альтернативами> distinct=<сколько разных адресов>;'.
"""
import re
import sys
import urllib.request

UA = {"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}


def main():
    try:
        xml = urllib.request.urlopen(
            urllib.request.Request("https://ais152.com/sitemap.xml", headers=UA),
            timeout=25).read().decode("utf-8", "replace")
    except Exception as exc:
        print("КАРТА НЕДОСТУПНА: %s" % exc)
        return 1

    blocks = re.findall(r"<url>(.*?)</url>", xml, re.S)
    if not blocks:
        print("КАРТА ПУСТА")
        return 1

    pairs, problems = 0, []
    distinct = set()
    for block in blocks:
        loc = re.search(r"<loc>([^<]+)</loc>", block)
        alts = re.findall(r'hreflang="([a-z-]+)" href="([^"]+)"', block)
        if not alts:
            continue
        pairs += 1
        langs = {code: url for code, url in alts if code != "x-default"}
        urls = set(langs.values())
        distinct |= urls
        if len(langs) < 2:
            problems.append("%s: альтернатив меньше двух" % (loc.group(1) if loc else "?"))
        if len(urls) < len(langs):
            problems.append("%s: разные языки ведут на один адрес — таргетинга не будет"
                            % (loc.group(1) if loc else "?"))
        if loc and loc.group(1) not in urls:
            problems.append("%s: версия не перечисляет саму себя" % loc.group(1))

    if not pairs:
        print("НИ У ОДНОГО АДРЕСА НЕТ ЯЗЫКОВЫХ АЛЬТЕРНАТИВ")
        return 1
    if problems:
        for item in problems:
            print(item)
        return 1

    print("SITEMAP_HREFLANG pairs=%d distinct=%d;" % (pairs, len(distinct)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
