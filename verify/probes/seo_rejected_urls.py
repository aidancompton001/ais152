# -*- coding: utf-8 -*-
"""Проба: разбор выгрузки Search Console «обойдено, но не проиндексировано».

Четыре подряд версии — три исполнителя и одна ревьюера — пытались объяснить
число 12 без списка адресов, и ни одна не попала:
  «это наши закрытые страницы»          — категории noindex в отчёте нет;
  «Google обошёл три открытых адреса»   — их не было в карте на момент чтения;
  «Google отверг содержимое сайта»      — в списке ноль страниц сайта;
  «это внутренние документы .md»        — в списке нет ни одного .md.

Список стоил одного клика CEO. Проба разбирает сохранённую выгрузку и печатает
разложение по происхождению адресов: числа Google командой не воспроизводятся,
но файл датирован и лежит в git — это доказательство, а не память.

Печатает 'REJECTED total=N own_https=N http_dupes=N subdomains=N;'.
"""
import csv
import io
import sys
from pathlib import Path
from urllib.parse import urlsplit

TABLE = Path(r"c:\Projects\AiS152\docs\verification"
             r"\gsc-drilldown-2026-08-18\Table.csv")
OWN = ("ais152.com", "www.ais152.com")


def main():
    if not TABLE.is_file():
        print("НЕТ ВЫГРУЗКИ: %s" % TABLE)
        return 1

    rows = list(csv.DictReader(io.open(TABLE, encoding="utf-8-sig")))
    if not rows:
        print("ВЫГРУЗКА ПУСТА — проба меряет пустоту")
        return 1

    own_https, http_dupes, subdomains = [], [], []
    for row in rows:
        url = (row.get("URL") or "").strip()
        if not url:
            continue
        host = urlsplit(url).netloc
        if host not in OWN:
            subdomains.append(url)
        elif url.startswith("http://"):
            http_dupes.append(url)
        else:
            own_https.append(url)

    if own_https:
        print("В СПИСКЕ ОТВЕРГНУТЫХ ЕСТЬ СТРАНИЦЫ САМОГО САЙТА: %s"
              % ", ".join(own_https))

    print("REJECTED total=%d own_https=%d http_dupes=%d subdomains=%d;"
          % (len(rows), len(own_https), len(http_dupes), len(subdomains)))
    for url in http_dupes:
        print("  дубль по протоколу: %s" % url)
    hosts = {}
    for url in subdomains:
        hosts[urlsplit(url).netloc] = hosts.get(urlsplit(url).netloc, 0) + 1
    for host, n in sorted(hosts.items()):
        print("  чужой поддомен: %-24s %d" % (host, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
