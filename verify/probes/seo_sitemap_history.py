# -*- coding: utf-8 -*-
"""Проба: какие адреса появились в карте ПОСЛЕ последнего чтения её Google.

Находка #14, круг 2 (F-15), тяжесть CRITICAL. Вторая редакция плана заявила:
«три открытых адреса Google обошёл и не проиндексировал, категория присутствует
гарантированно». Это неправда, и доказательство создал сам автор: Google читал
карту 01.08.2026, тогда в ней было два адреса. Адрес, которого не было в карте
на момент её чтения, не мог быть по ней обойдён. Его состояние неизвестно —
и это утверждение о НЕЗНАНИИ, а не о факте.

Находки круга 3, закрытые здесь:
  F-34а: дата последнего чтения была вписана константой в исходник пробы.
         Проба не могла заметить, что Google перечитал карту, — а Задача 4.2
         плана прямо велит подать карту заново. Дата берётся из датированного
         снимка показаний Search Console в docs/verification/, и если снимка
         нет, проба падает, а не притворяется знающей.
  F-34б: проба читала только журнал git и была слепа к рабочей копии.
         Теперь адреса берутся из рабочей копии карты, а дата появления
         каждого — из журнала.
  F-43:  адрес, удалённый и добавленный заново, датировался первым появлением.
         Теперь берётся ПОСЛЕДНЕЕ добавление — оно и определяет, видел ли
         Google этот адрес.
  F-44:  граница «строго позже» заменена на «в тот же день или позже»:
         час чтения неизвестен, и совпадение дат толковать в свою пользу
         нельзя.

Печатает 'ADDED_AFTER_LAST_READ=<сколько>;' последней строкой.
"""
import datetime
import io
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"c:\Projects\AiS152")
SNAPSHOT = ROOT / "docs" / "verification" / "gsc_sitemap_last_read.json"
MAX_AGE_DAYS = 30


def last_read():
    """Дата последнего чтения карты Google — только из датированного снимка."""
    if not SNAPSHOT.is_file():
        return None, ("НЕТ СНИМКА ПОКАЗАНИЙ: %s\n"
                      "Дату последнего чтения карты знает только Search "
                      "Console. Выдумывать её нельзя." % SNAPSHOT)
    try:
        data = json.load(io.open(SNAPSHOT, encoding="utf-8"))
    except Exception as exc:
        return None, "СНИМОК НЕ РАЗБИРАЕТСЯ: %s" % exc
    date = (data.get("last_read") or "").strip()
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        return None, "В СНИМКЕ НЕТ ДАТЫ last_read вида ГГГГ-ММ-ДД"

    # Находка #14, круг 4 (F-58): отсутствия снимка проба боялась, а его
    # устаревания — нет. План собственным шагом (Задача 4.2 — подать карту
    # заново) делает last_read ложью, и проба осталась бы зелёной и уверенной.
    # Устаревший снимок — это притворство знанием.
    taken = (data.get("captured_at") or "").strip()
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", taken):
        return None, "В СНИМКЕ НЕТ ДАТЫ captured_at — неизвестно, когда сняли"
    age = (datetime.date.today()
           - datetime.date(*map(int, taken.split("-")))).days
    if age > MAX_AGE_DAYS:
        return None, ("СНИМОК ПОКАЗАНИЙ УСТАРЕЛ: снят %s, %d дней назад "
                      "(предел %d). Google мог перечитать карту, и утверждение "
                      "о ней сейчас недоказуемо. Обнови снимок по свежему "
                      "экрану Search Console." % (taken, age, MAX_AGE_DAYS))
    return date, None


def added_dates():
    """Для каждого адреса — дата ПОСЛЕДНЕГО его добавления в карту."""
    res = subprocess.run(
        ["git", "log", "--format=COMMIT %ad", "--date=short", "-p",
         "--follow", "--", "sitemap.xml"],
        cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8",
        errors="replace")
    if res.returncode != 0:
        return None

    out = {}
    date = None
    for line in (res.stdout or "").splitlines():
        if line.startswith("COMMIT "):
            date = line.split(" ", 1)[1].strip()
            continue
        found = re.match(r"\+\s*<loc>([^<]+)</loc>", line)
        if found and date:
            # git log идёт от новых к старым, поэтому первое встреченное
            # добавление и есть последнее по времени.
            out.setdefault(found.group(1).strip(), date)
    return out


def current_urls():
    """Адреса из рабочей копии карты, а не из журнала."""
    path = ROOT / "sitemap.xml"
    if not path.is_file():
        return []
    text = io.open(path, encoding="utf-8", errors="replace").read()
    return re.findall(r"<loc>([^<]+)</loc>", text)


def main():
    date, problem = last_read()
    if problem:
        print(problem)
        return 1

    dates = added_dates()
    if dates is None:
        print("ЖУРНАЛ GIT НЕДОСТУПЕН")
        return 1

    urls = current_urls()
    if not urls:
        print("КАРТА В РАБОЧЕЙ КОПИИ ПУСТА ИЛИ ОТСУТСТВУЕТ")
        return 1

    late, unknown = [], []
    for url in urls:
        when = dates.get(url)
        if when is None:
            # Есть в рабочей копии, но ещё не закоммичен — значит появился
            # сегодня, то есть заведомо позже любого прошлого чтения.
            unknown.append(url)
        elif when >= date:
            late.append((url, when))

    for url, when in sorted(late):
        print("  %s — в карте с %s, не раньше чтения %s" % (url, when, date))
    for url in sorted(unknown):
        print("  %s — ещё не закоммичен, в карте появился сегодня" % url)

    # Маркер завершается точкой с запятой: без границы подстрока "…_READ 3"
    # совпала бы и с выводом "…_READ 30" (находка #14, круг 3, F-33).
    print("ADDED_AFTER_LAST_READ=%d;" % (len(late) + len(unknown)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
