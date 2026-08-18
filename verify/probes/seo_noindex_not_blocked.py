# -*- coding: utf-8 -*-
"""Проба: ни одна страница с noindex не закрыта ещё и от обхода.

Два механизма взаимно исключают друг друга. Краулер, которому запрещён обход,
не читает страницу — а значит не видит и noindex. Адрес остаётся в выдаче
с пометкой «проиндексировано, несмотря на блокировку в robots.txt», и вывести
его оттуда уже нечем.

Находка #14, F-94 (дельта-ревью 18.08.2026): robots.txt закрывал от обхода те
же concept-* и quiz, на которых стоит noindex.

Находка #14, F-99: защита от рецидива была встроена в пробу сирот, а та
перебирает ТОЛЬКО сирот. noindex стоит ещё на avv.html, rechnungen/muster.html
и 404.html — они залинкованы, сиротами не считаются, в перебор не попадали.
Мутация «добавить Disallow: /rechnungen/» проходила насквозь, а это не
гипотетика: каталог со счетами — первое, что хочется закрыть.

Здесь перебираются ВСЕ html, отслеживаемые git.

Печатает 'NOINDEX_NOT_BLOCKED checked=<сколько> conflicts=0;'.
"""
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from robots_check import closed as page_closed  # noqa: E402

ROOT = r"c:\Projects\AiS152"
UA = {"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}


def tracked_html():
    out = subprocess.run(["git", "ls-files", "*.html"], cwd=ROOT,
                         capture_output=True, text=True, encoding="utf-8",
                         errors="replace")
    return sorted(f.strip() for f in (out.stdout or "").splitlines() if f.strip())


def robots_rules():
    try:
        text = urllib.request.urlopen(
            urllib.request.Request("https://ais152.com/robots.txt", headers=UA),
            timeout=25).read().decode("utf-8", "replace")
    except Exception as exc:
        print("НЕ ПРОЧИТАТЬ robots.txt: %s" % exc)
        return None
    return [m.group(1).strip()
            for m in re.finditer(r"(?im)^\s*Disallow:\s*(\S+)\s*$", text)]


def crawl_blocked(name, rules):
    target = "/" + name
    for rule in rules:
        if not rule or rule == "/":
            continue
        body = rule[:-1] if rule.endswith("$") else rule
        body = body.rstrip("*")
        if body and target.startswith(body):
            return True
    return False


def main():
    rules = robots_rules()
    if rules is None:
        return 1

    files = tracked_html()
    if not files:
        print("В GIT НЕТ HTML — проба меряет пустоту")
        return 1

    checked, conflicts = 0, []
    for name in files:
        try:
            res = urllib.request.urlopen(
                urllib.request.Request("https://ais152.com/" + name, headers=UA),
                timeout=25)
            html = res.read().decode("utf-8", "replace")
        except urllib.error.HTTPError:
            continue          # страницы нет в публикации — конфликта быть не может
        except Exception as exc:
            print("НЕ ПРОВЕРИТЬ %s: %s" % (name, exc))
            return 1

        checked += 1
        if page_closed(html, res.headers) and crawl_blocked(name, rules):
            conflicts.append(name)

    if conflicts:
        print("NOINDEX ЗАГЛУШЁН ЗАПРЕТОМ ОБХОДА — Google не прочитает тег: %s"
              % ", ".join(conflicts))
        return 1

    print("NOINDEX_NOT_BLOCKED checked=%d conflicts=0;" % checked)
    return 0


if __name__ == "__main__":
    sys.exit(main())
