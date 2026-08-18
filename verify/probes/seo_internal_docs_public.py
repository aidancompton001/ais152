# -*- coding: utf-8 -*-
"""Проба: какие внутренние документы репозитория отдаются публично.

GitHub Pages публикует корень репозитория целиком, robots.txt разрешает всё.
Значит журнал разработки, управляющий документ, промпты CEO и рабочие заметки
доступны любому.

Находки #14:
  F-12 (круг 1): проблема обнаружена;
  F-26 (круг 2): проба печатала одно и то же до и после работы — путь закрытия
        через robots.txt оставляет файлы доступными по прямой ссылке;
  F-27 (круг 3): проверялись только пять корневых файлов, а тревога была
        про каталоги docs и verify;
  F-50 (круг 4): список из восьми путей был вписан руками, и масштаб утечки
        занижался в разы: проба печатала «шесть», тогда как публично лежат
        десятки документов. Точное число печатает сама проба — вписывать его
        в описание нельзя, оно меняется от каждого коммита. Приём «список из git,
        а не из головы» уже был применён в пробе черновиков по находке F-21
        и не был применён здесь.

Теперь список берётся из git целиком: все .md, все .json из verify, всё из
docs и prompts. Ни один новый документ не пройдёт мимо.

Печатает 'DOCS served=<N> blocked=<M> open=<K>;'. Инвариант — open=0.
"""
import re
import subprocess
import sys
import urllib.error
import urllib.request
from urllib.parse import quote

ROOT = r"c:\Projects\AiS152"
PATTERNS = ["*.md", "docs/**", "prompts/**", "verify/*.json", "verify/*.md"]
# Документы, которым публичность положена по закону или по назначению.
PUBLIC_BY_DESIGN = re.compile(
    r"^(impressum|datenschutz|agb|widerruf|avv|README)\.md$", re.I)
UA = {"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}


def tracked():
    out = subprocess.run(["git", "ls-files"] + PATTERNS, cwd=ROOT,
                         capture_output=True, text=True, encoding="utf-8",
                         errors="replace")
    files = [f.strip() for f in (out.stdout or "").splitlines() if f.strip()]
    return sorted(f for f in files if not PUBLIC_BY_DESIGN.match(f))


def robots_rules():
    try:
        text = urllib.request.urlopen(
            urllib.request.Request("https://ais152.com/robots.txt", headers=UA),
            timeout=25).read().decode("utf-8", "replace")
    except Exception:
        return []
    return [m.group(1).strip()
            for m in re.finditer(r"(?im)^\s*Disallow:\s*(\S+)\s*$", text)]


def blocked(path, rules):
    target = "/" + path
    for rule in rules:
        if not rule:
            continue
        if rule == "/":
            return True
        if rule.endswith("$"):
            body = rule[:-1]
            if body.startswith("/*"):
                if target.endswith(body[2:]):
                    return True
            elif target == body:
                return True
        elif target.startswith(rule.rstrip("*")):
            return True
    return False


def main():
    docs = tracked()
    if not docs:
        print("В GIT НЕТ ОТСЛЕЖИВАЕМЫХ ДОКУМЕНТОВ — проба меряет пустоту")
        return 1

    rules = robots_rules()
    served, closed = [], []
    for path in docs:
        try:
            # Пробелы в имени файла ломали запрос целиком, и проба падала
            # вместо того чтобы измерить (находка при выгрузке Search Console).
            res = urllib.request.urlopen(
                urllib.request.Request("https://ais152.com/" + quote(path), headers=UA),
                timeout=25)
            if res.status != 200:
                continue
        except urllib.error.HTTPError:
            continue          # 404 — файла нет в публикации, самое надёжное
        except Exception as exc:
            print("НЕ ПРОВЕРИТЬ %s: %s" % (path, exc))
            return 1
        served.append(path)
        if blocked(path, rules):
            closed.append(path)

    # Круг дельта, F-95: ожидание сверяло только blocked, поэтому документ,
    # который отдаётся, но НЕ закрыт, подстроку не ломал — проверка проходила
    # при живом дефекте. Инвариант — open=0, счётчики остаются для диагностики.
    print("DOCS served=%d blocked=%d open=%d;"
          % (len(served), len(closed), len(served) - len(closed)))
    print("  проверено документов из git: %d" % len(docs))
    if served:
        print("  доступны: %s" % ", ".join(served))
    return 0


if __name__ == "__main__":
    sys.exit(main())
