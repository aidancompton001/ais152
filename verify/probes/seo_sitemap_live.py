# -*- coding: utf-8 -*-
"""Проба: карта сайта не зовёт Google на закрытые, мёртвые или переехавшие адреса.

Карта, перечисляющая страницу с noindex, — противоречивый сигнал: приглашение
туда, куда вход запрещён. Карта, перечисляющая редирект, тратит обход и
размывает сигнал: адрес в карте обязан быть конечным.

Находка #14, круг 2 (F-20): прежняя версия молча шла по редиректам, и адрес,
отдающий 301, проходил как здоровый — то есть проба не проверяла того, что
заявлено в её же названии. Плюс ожидание в реестре не содержало числа, и
карта из одного адреса прошла бы так же зелено, как из сорока.

Находка #14, круг 2 (F-19): закрыть страницу можно и директивой, адресованной
именно Googlebot. Прежняя регулярка её не видела.

Печатает 'SITEMAP urls=<адресов>; broken=0;'.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from robots_check import closed as page_closed  # noqa: E402
import urllib.error
import urllib.request

UA = {"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Редирект — не успех. Адрес в карте обязан быть конечным."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def fetch(url, follow=True):
    req = urllib.request.Request(url, headers=UA)
    res = (urllib.request.urlopen(req, timeout=25) if follow
           else OPENER.open(req, timeout=25))
    return res.status, res.read().decode("utf-8", "replace")


def main():
    try:
        _code, xml = fetch("https://ais152.com/sitemap.xml")
    except Exception as exc:
        print("КАРТА САЙТА НЕДОСТУПНА: %s" % exc)
        return 1

    locs = re.findall(r"<loc>([^<]+)</loc>", xml)
    if not locs:
        print("КАРТА САЙТА ПУСТА")
        return 1

    problems = []
    for url in locs:
        try:
            code, body = fetch(url, follow=False)
        except urllib.error.HTTPError as exc:
            if exc.code in (301, 302, 303, 307, 308):
                problems.append("%s: редирект %s на %s — адрес в карте должен "
                                "быть конечным"
                                % (url, exc.code, exc.headers.get("Location")))
            else:
                problems.append("%s: HTTP %s" % (url, exc.code))
            continue
        except Exception as exc:
            problems.append("%s: %s" % (url, exc))
            continue

        if code != 200:
            problems.append("%s: HTTP %s" % (url, code))
            continue

        if page_closed(body):
            problems.append("%s: закрыта от индексации, но стоит в карте" % url)

    if problems:
        for item in problems:
            print(item)
        return 1

    # Инвариант "broken=0;" не зависит от размера карты; число адресов —
    # снимок (находка #14, круг 3, F-38).
    print("SITEMAP urls=%d; broken=0;" % len(locs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
