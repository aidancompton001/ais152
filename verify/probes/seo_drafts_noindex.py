# -*- coding: utf-8 -*-
"""Проба: ни одна страница-сирота не открыта для индексации.

Сирота — страница, на которую нет ни одной ссылки с сайта и которой нет
в карте. Google такую либо не найдёт, либо найдёт и не поймёт, зачем она.
Черновики концептов и квиз — именно такие.

Находки #14:
  круг 2, F-21: список файлов был вписан в исходник пробы, и новый черновик
        она бы не заметила. Список стал браться из git — но фильтр
        `concept-*.html`, `quiz.html` остался вписанным руками;
  круг 4, F-53: значит утверждение «все черновые страницы» было шире
        доказательства «эти девять файлов». Черновик с именем draft.html
        или entwurf.html проба не видела.

Теперь сироты определяются по свойству, а не по имени: берутся ВСЕ html
из git, вычитаются те, на которые есть ссылка из любого html, и те, что
стоят в карте. Что осталось — сирота, и она обязана быть закрыта.

Проверяется ЖИВОЙ сайт: 17.08.2026 CEO увидел на живом сайте старую
заставку, потому что правка осталась на диске.

Печатает 'ORPHANS_CLOSED <закрыто или убрано>/<всего сирот>;'.

Область поиска — ВСЕ html из git, а не только корень: сирота определяется
свойством, а не расположением.
"""
import io
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from robots_check import closed as page_closed  # noqa: E402

ROOT = Path(r"c:\Projects\AiS152")
UA = {"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}
# Служебные страницы, которым сиротство положено по назначению.
SERVICE = re.compile(r"^(404|google[0-9a-f]+)\.html$", re.I)


def tracked_html():
    out = subprocess.run(["git", "ls-files", "*.html"], cwd=str(ROOT),
                         capture_output=True, text=True, encoding="utf-8",
                         errors="replace")
    return sorted(f.strip() for f in (out.stdout or "").splitlines() if f.strip())


def linked_names(files):
    """Имена, на которые есть ссылка хотя бы из одного html."""
    linked = set()
    for name in files:
        path = ROOT / name
        if not path.is_file():
            continue
        text = io.open(path, encoding="utf-8", errors="replace").read()
        text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
        for href in re.findall(r"""<a\b[^>]*?\bhref\s*=\s*["']([^"']+)["']""",
                               text, re.I):
            linked.add(href.split("?")[0].split("#")[0].lstrip("./"))
    return linked


def sitemap_names():
    try:
        xml = urllib.request.urlopen(
            urllib.request.Request("https://ais152.com/sitemap.xml", headers=UA),
            timeout=25).read().decode("utf-8", "replace")
    except Exception:
        return set()
    return {u.rsplit("/", 1)[-1] or "index.html"
            for u in re.findall(r"<loc>([^<]+)</loc>", xml)}


def main():
    files = tracked_html()
    if not files:
        print("В GIT НЕТ HTML — проба меряет пустоту")
        return 1

    # Круг 5, F-68: область поиска была вписана руками — только корень. Файлы
    # вроде assets/kleinanzeigen/_logo.src.html сегодня отдают 404 лишь потому,
    # что Jekyll прячет имена с подчёркиванием, а Задача 0.5 обсуждает его
    # отключение. После этого страницы ожили бы, а проба их не увидела бы.
    candidates = [f for f in files
                  if f != "index.html" and not SERVICE.match(f.rsplit("/", 1)[-1])]

    # Круг 5, F-69: ссылки собирались из ВСЕХ страниц, включая сами черновики,
    # поэтому пара взаимно ссылающихся черновиков спрятала бы друг друга.
    # Ссылка засчитывается только с НЕсиротской страницы, и множество
    # сокращается до неподвижной точки.
    in_map = sitemap_names()
    orphans = list(candidates)
    while True:
        pages = [f for f in files if f not in orphans]
        linked = linked_names(pages)
        nxt = [f for f in candidates
               if f not in in_map
               and f not in linked
               and f.rsplit("/", 1)[-1] not in linked]
        if nxt == orphans:
            break
        orphans = nxt
    if not orphans:
        print("СИРОТ НЕ НАЙДЕНО — либо их правда нет, либо проба ослепла")
        return 1

    ok, open_pages = 0, []
    for name in orphans:
        url = "https://ais152.com/" + name
        try:
            res = urllib.request.urlopen(
                urllib.request.Request(url, headers=UA), timeout=25)
            html = res.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                ok += 1          # убрана из продакшена — сильнее, чем noindex
                continue
            open_pages.append("%s: HTTP %s" % (name, exc.code))
            continue
        except Exception as exc:
            open_pages.append("%s: %s" % (name, exc))
            continue

        if page_closed(html, res.headers):
            ok += 1
        else:
            open_pages.append("%s: ОТКРЫТА" % name)

    if open_pages:
        print("СИРОТЫ ОТКРЫТЫ ДЛЯ ИНДЕКСАЦИИ: %s" % "; ".join(open_pages))
        return 1

    print("ORPHANS_CLOSED %d/%d;" % (ok, len(orphans)))
    print("  сироты: %s" % ", ".join(orphans))
    return 0


if __name__ == "__main__":
    sys.exit(main())
