# -*- coding: utf-8 -*-
"""Проба: каждый адрес из карты сайта достижим кликами с главной и жив.

Страница без входящих внутренних ссылок попадает в «обнаружено, но не
проиндексировано» — ровно тот статус, из которого сайт и вылезает. Карта
сайта для статического сайта без внешних ссылок — слабый канал обнаружения.

Находки #14:
  круг 2: критерий приёмки ссылался на эту пробу, а файла не существовало;
  круг 3 (F-36): адрес попадал в «пройденные» ДО запроса, поэтому страница,
          отдающая 404, считалась достижимой — мутация «удалить wartung,
          оставив ссылку в футере» проходила насквозь;
  круг 3 (F-37): в обход шёл любой href, включая rel=canonical, rel=alternate
          и ссылки внутри HTML-комментариев. Мутация «закомментировать весь
          футер» оставляла пробу зелёной.

Теперь: комментарии вырезаются, берутся только <a href>, и адрес считается
достижимым лишь после ответа 200.

Обход идёт по СЫРОМУ HTML: ссылка, которую рисует скрипт, для краулера
не существует так же, как и для этой пробы.

Печатает 'REACHABLE=<живых>/<в карте>; UNREACHABLE=0;'.
"""
import re
import sys
import urllib.error
import urllib.request
from urllib.parse import urljoin, urlsplit, urlunsplit

BASE = "https://ais152.com"
DEPTH = 3
UA = {"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}
COMMENT = re.compile(r"<!--.*?-->", re.S)
ANCHOR = re.compile(r"<a\b[^>]*?\bhref\s*=\s*[\"']([^\"']+)[\"']", re.I)


def get(url):
    res = urllib.request.urlopen(
        urllib.request.Request(url, headers=UA), timeout=25)
    return res.status, res.read().decode("utf-8", "replace")


def canon(url):
    """Один документ — один ключ: без якоря, без параметров, без хвостового /."""
    parts = urlsplit(url)
    path = parts.path or "/"
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    return urlunsplit((parts.scheme, parts.netloc, path, "", ""))


def main():
    try:
        _code, xml = get(BASE + "/sitemap.xml")
    except Exception as exc:
        print("КАРТА НЕДОСТУПНА: %s" % exc)
        return 1

    wanted = {canon(u) for u in re.findall(r"<loc>([^<]+)</loc>", xml)}
    if not wanted:
        print("КАРТА ПУСТА")
        return 1

    alive, tried, frontier = set(), set(), [canon(BASE + "/")]
    dead = {}
    for _level in range(DEPTH):
        nxt = []
        for url in frontier:
            if url in tried:
                continue
            tried.add(url)
            try:
                code, html = get(url)
            except urllib.error.HTTPError as exc:
                dead[url] = "HTTP %s" % exc.code
                continue
            except Exception as exc:
                dead[url] = str(exc)
                continue
            if code != 200:
                dead[url] = "HTTP %s" % code
                continue

            alive.add(url)
            for href in ANCHOR.findall(COMMENT.sub("", html)):
                if href.startswith(("mailto:", "tel:", "javascript:", "#")):
                    continue
                target = canon(urljoin(url, href))
                if target.startswith(BASE) and target not in tried:
                    nxt.append(target)
        frontier = nxt
        if not frontier:
            break

    broken = {u: why for u, why in dead.items() if u in wanted}
    if broken:
        print("АДРЕСА ИЗ КАРТЫ НЕ ОТВЕЧАЮТ: %s"
              % "; ".join("%s — %s" % (u, w) for u, w in sorted(broken.items())))
        return 1
    if dead:
        # Битая ссылка вне карты — тоже дефект, но другого класса: сайт зовёт
        # посетителя в никуда. Печатается, пробу не роняет.
        print("битые ссылки вне карты: %s"
              % "; ".join("%s — %s" % (u, w) for u, w in sorted(dead.items())))

    unreachable = sorted(wanted - alive)
    if unreachable:
        print("НЕДОСТИЖИМЫ ССЫЛКАМИ С ГЛАВНОЙ ЗА %d ПЕРЕХОДА: %s"
              % (DEPTH, ", ".join(unreachable)))
        return 1

    # Инвариант отделён от снимка: "UNREACHABLE=0;" переживает рост сайта,
    # а число адресов честно меняется (находка #14, круг 3, F-38).
    print("REACHABLE=%d/%d; UNREACHABLE=0;" % (len(wanted), len(wanted)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
