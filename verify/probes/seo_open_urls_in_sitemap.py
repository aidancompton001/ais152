"""Проба: сколько адресов в карте сайта и все ли они открыты для индексации.

Проба меряет РОВНО ЭТО и ничего больше.

Находка #14, круг 2 (F-15) и круг 4 (F-57). Здесь стояло рассуждение: «если
в карте N открытых адресов, а Search Console показывает одну проиндексированную
страницу, значит N-1 адресов обойдены и НЕ проиндексированы, и эта категория
присутствует независимо от того, что покажет отчёт».

Это ложь, и она стоила двух отклонений. Google читает карту в конкретный день;
адрес, добавленный позже, по ней обойдён быть не мог. Из текста плана и из
формулировки утверждения ложь вычистили в круге 3 — а из исходника пробы,
которая производит доказательство, не вычистили. Следующий читатель взял бы
вывод отсюда.

Про то, каких адресов Google ещё не видел, отвечает отдельная проба
seo_sitemap_history.py — и отвечает утверждением о НЕЗНАНИИ.

Печатает 'OPEN_IN_SITEMAP=<сколько открыто>; CLOSED=0;'.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from robots_check import closed as page_closed  # noqa: E402
import urllib.request

UA = {"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}


def get(url):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers=UA), timeout=25
    ).read().decode("utf-8", "replace")


def main():
    try:
        xml = get("https://ais152.com/sitemap.xml")
    except Exception as exc:
        print("КАРТА НЕДОСТУПНА: %s" % exc)
        return 1

    locs = re.findall(r"<loc>([^<]+)</loc>", xml)
    if not locs:
        print("КАРТА ПУСТА")
        return 1

    open_urls, closed = [], []
    for url in locs:
        try:
            body = get(url)
        except Exception as exc:
            print("АДРЕС ИЗ КАРТЫ НЕ ОТВЕЧАЕТ: %s — %s" % (url, exc))
            return 1
        if page_closed(body):
            closed.append(url)
        else:
            open_urls.append(url)

    if closed:
        print("В КАРТЕ ЕСТЬ ЗАКРЫТЫЕ АДРЕСА — противоречивый сигнал: %s"
              % ", ".join(closed))
        return 1

    print("OPEN_IN_SITEMAP=%d; CLOSED=0;" % len(open_urls))
    return 0


if __name__ == "__main__":
    sys.exit(main())
