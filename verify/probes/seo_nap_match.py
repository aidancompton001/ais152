# -*- coding: utf-8 -*-
"""Проба: название, адрес и телефон в разметке совпадают с Impressum.

Google связывает сайт с карточкой Business по совпадению названия, адреса
и телефона — это и есть NAP. Расхождение любого из трёх — сигнал
несоответствия.

Находка #14, круг 2 (F-22): прежняя версия называлась NAP, а сверяла только
адрес. Мутация «телефон в разметке не совпадает с Impressum» проходила
насквозь. Теперь сверяются все три.

Сверяются ДВЕ ЖИВЫЕ СТРАНИЦЫ друг с другом, а не страница с текстом плана:
иначе проба доказывала бы, что план сам себе не противоречит.

Печатает 'NAP_MATCH <улица> <индекс> <телефон>'.
"""
import json
import re
import sys
import urllib.request

UA = {"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}


def get(url):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers=UA), timeout=25
    ).read().decode("utf-8", "replace")


def norm_street(text):
    """Улица пишется то через ß, то через ss, то сокращённо."""
    text = text.lower().replace("ß", "ss")
    text = text.replace("strasse", "str").replace("straße", "str")
    return re.sub(r"[^a-z0-9]", "", text)


def digits(text):
    """Телефон пишется как +49 155…, 0155…, с пробелами и скобками."""
    only = re.sub(r"\D", "", text or "")
    if only.startswith("49"):
        only = only[2:]
    return only.lstrip("0")


def main():
    try:
        home = get("https://ais152.com/")
        impressum = get("https://ais152.com/impressum.html")
    except Exception as exc:
        print("СТРАНИЦА НЕДОСТУПНА: %s" % exc)
        return 1

    block = re.search(r'<script type="application/ld\+json">(.*?)</script>',
                      home, re.S)
    if not block:
        print("НА ГЛАВНОЙ НЕТ РАЗМЕТКИ JSON-LD")
        return 1
    try:
        data = json.loads(block.group(1))
    except ValueError as exc:
        print("РАЗМЕТКА НЕ РАЗБИРАЕТСЯ: %s" % exc)
        return 1

    node = None
    for item in data.get("@graph", [data]):
        if item.get("@type") == "ProfessionalService":
            node = item
    if not node:
        print("В РАЗМЕТКЕ НЕТ УЗЛА ОРГАНИЗАЦИИ")
        return 1

    addr = node.get("address") or {}
    street = addr.get("streetAddress") or ""
    code = addr.get("postalCode") or ""
    phone = node.get("telephone") or ""
    if not (street and code and phone):
        print("В РАЗМЕТКЕ НЕПОЛНЫЙ NAP: улица=%r индекс=%r телефон=%r"
              % (street, code, phone))
        return 1

    plain = re.sub(r"<[^>]+>", " ", impressum)

    if norm_street(street) not in norm_street(plain):
        print("УЛИЦА В РАЗМЕТКЕ НЕ НАЙДЕНА В IMPRESSUM: %s" % street)
        return 1
    if code not in plain:
        print("ИНДЕКС В РАЗМЕТКЕ НЕ НАЙДЕН В IMPRESSUM: %s" % code)
        return 1

    want = digits(phone)
    have = digits(re.sub(r"\s+", "", plain))
    if not want or want not in have:
        print("ТЕЛЕФОН В РАЗМЕТКЕ НЕ НАЙДЕН В IMPRESSUM: %s" % phone)
        return 1

    print("NAP_MATCH %s %s %s"
          % (street.replace("ß", "ss").replace(" ", "-"), code, want))
    return 0


if __name__ == "__main__":
    sys.exit(main())
