# -*- coding: utf-8 -*-
"""Проба: у каждого языка свой адрес, и на нём нет чужого языка.

Главный дефект, из-за которого сайт не имел немецкого трафика: обе версии
жили в одном документе, немецкая скрывалась правилом CSS, а язык выбирался
по настройке браузера, которой у краулера нет. Google получал английскую
страницу всегда.

Проверяется ЖИВОЙ сайт, и проверяется то, что видит краулер, — исходный
код, а не отрендеренная страница:

  1. на каждом адресе объявлен свой язык документа;
  2. в исходном коде нет ни одного блока другого языка;
  3. заголовок и описание у версий разные — иначе Google видит дубль;
  4. canonical каждой версии указывает на себя;
  5. hreflang перечисляет обе версии и себя в том числе — требование Google;
  6. между версиями есть ССЫЛКА, а не кнопка: по кнопке краулер не пройдёт;
  7. стили и скрипты на вложенном адресе не отдают 404 — путь абсолютный.

Печатает 'LANG_SPLIT de=/ en=/en/ foreign=0 assets_ok;'.
"""
import re
import sys
import urllib.error
import urllib.request

PAGES = {"de": "https://ais152.com/", "en": "https://ais152.com/en/"}
UA = {"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}


def get(url):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers=UA), timeout=25
    ).read().decode("utf-8", "replace")


def main():
    problems, meta = [], {}

    for lang, url in PAGES.items():
        try:
            html = get(url)
        except Exception as exc:
            print("СТРАНИЦА НЕДОСТУПНА: %s — %s" % (url, exc))
            return 1

        declared = re.search(r"<html[^>]*\blang=[\"']([a-z-]+)[\"']", html, re.I)
        if not declared or not declared.group(1).lower().startswith(lang):
            problems.append("%s: объявлен язык %r, ждали %s"
                            % (url, declared.group(1) if declared else None, lang))

        other = "en" if lang == "de" else "de"
        foreign = html.count("data-lang-%s" % other)
        if foreign:
            problems.append("%s: в исходном коде %d блоков языка %s"
                            % (url, foreign, other))

        title = re.search(r"<title>(.*?)</title>", html, re.S)
        desc = re.search(r'<meta name="description" content="([^"]*)"', html)
        meta[lang] = (title.group(1).strip() if title else "",
                      desc.group(1).strip() if desc else "")

        canon = re.search(r'<link rel="canonical" href="([^"]+)"', html)
        if not canon or canon.group(1).rstrip("/") != url.rstrip("/"):
            problems.append("%s: canonical ведёт на %s"
                            % (url, canon.group(1) if canon else None))

        alts = dict(re.findall(r'hreflang="([a-z-]+)" href="([^"]+)"', html))
        for code, target in PAGES.items():
            if alts.get(code, "").rstrip("/") != target.rstrip("/"):
                problems.append("%s: hreflang %s ведёт на %r, ждали %s"
                                % (url, code, alts.get(code), target))

        if not re.search(r'<a[^>]+class="lang-toggle"[^>]+href=', html):
            problems.append("%s: переключатель языка не ссылка — краулер по нему "
                            "не пройдёт и вторую версию не найдёт" % url)

    if meta.get("de", ("",))[0] == meta.get("en", ("",))[0]:
        problems.append("заголовки версий совпадают — для Google это дубль")
    if meta.get("de", ("", ""))[1] == meta.get("en", ("", ""))[1]:
        problems.append("описания версий совпадают — для Google это дубль")

    # Пути на вложенном адресе: относительный assets/... разрешился бы
    # в /en/assets/... и дал бы 404 тихо — страница отдаёт 200 и сломана.
    en_html = get(PAGES["en"])
    assets = re.findall(r'(?:href|src)="(/assets/[^"]+)"', en_html)[:6]
    if not assets:
        problems.append("/en/: не найдено ни одного абсолютного пути к ресурсам")
    for path in assets:
        try:
            urllib.request.urlopen(
                urllib.request.Request("https://ais152.com" + path, headers=UA),
                timeout=25)
        except urllib.error.HTTPError as exc:
            problems.append("/en/: ресурс %s отдаёт %s" % (path, exc.code))
        except Exception as exc:
            problems.append("/en/: ресурс %s — %s" % (path, exc))

    if problems:
        for item in problems:
            print(item)
        return 1

    print("LANG_SPLIT de=/ en=/en/ foreign=0 assets_ok;")
    return 0


if __name__ == "__main__":
    sys.exit(main())
