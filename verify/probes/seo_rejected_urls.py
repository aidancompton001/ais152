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
import zipfile
from pathlib import Path
from urllib.parse import urlsplit

# Находка #14, F-109: проба читала CSV из репозитория — файл, который автор
# утверждения может переписать. Рядом лежит нетронутый архив, скачанный из
# Search Console. Читаем из архива: тогда это выгрузка Google, а не файл
# в нашем репозитории.
ARCHIVE = (Path(r"c:/Projects/AiS152/docs/verification")
           / "gsc-drilldown-2026-08-18"
           / "ais152.com-Coverage-Drilldown-2026-08-18.zip")
EXPECTED_ISSUE = "Crawled - currently not indexed"
OWN = ("ais152.com", "www.ais152.com")


def read_from_archive(name):
    with zipfile.ZipFile(ARCHIVE) as z:
        return z.read(name).decode("utf-8-sig", "replace")


def main():
    if not ARCHIVE.is_file():
        print("НЕТ АРХИВА ВЫГРУЗКИ: %s" % ARCHIVE)
        return 1

    # Проверяем, что разбираем именно ту категорию, о которой утверждение:
    # в архиве лежит Metadata.csv с названием отчёта.
    meta = dict((r.get("Property"), r.get("Value"))
                for r in csv.DictReader(io.StringIO(read_from_archive("Metadata.csv"))))
    issue = (meta.get("Issue") or "").strip()
    if issue != EXPECTED_ISSUE:
        print("АРХИВ НЕ О ТОЙ КАТЕГОРИИ: '%s', ждали '%s'" % (issue, EXPECTED_ISSUE))
        return 1

    rows = list(csv.DictReader(io.StringIO(read_from_archive("Table.csv"))))
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
        # F-108: раньше проба печатала тревогу и возвращала 0 — запущенная
        # руками, соврала бы зелёным.
        print("В СПИСКЕ ОТВЕРГНУТЫХ ЕСТЬ СТРАНИЦЫ САМОГО САЙТА: %s"
              % ", ".join(own_https))
        return 1

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
