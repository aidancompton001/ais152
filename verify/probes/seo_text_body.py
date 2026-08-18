# -*- coding: utf-8 -*-
"""Проба: сколько на главной настоящего текста и какая доля немецкая.

Закон 27 §1: рядом с числом обязан стоять запрос, которым оно получено.
В первой редакции плана стояло «10 098 байт», и напечатанная рядом команда
давала 14 951 — расхождение 48 %. Причина: команда снимала только теги,
оставляя внутри исходники скриптов, и не схлопывала пробелы.

Здесь измерение зафиксировано целиком, включая все три шага:
  1. вырезаются script и style вместе с содержимым;
  2. снимаются теги;
  3. пробелы схлопываются в один.

Доля немецкого считается тем же способом по блокам data-lang-de, чтобы обе
величины держались одним измерением, а не двумя разными.

Печатает 'TEXT_BODY <байт> <доля немецкого в процентах>'.
"""
import io
import re
import sys
from pathlib import Path

PAGE = Path(r"c:\Projects\AiS152\index.html")


def body_bytes(html):
    no_code = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html,
                     flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", "", no_code)
    return len(re.sub(r"\s+", " ", text).strip().encode("utf-8"))


def main():
    if not PAGE.is_file():
        print("НЕТ ФАЙЛА: %s" % PAGE)
        return 1
    html = io.open(PAGE, encoding="utf-8", errors="replace").read()

    total = body_bytes(html)
    if not total:
        print("ТЕКСТА НА СТРАНИЦЕ НЕТ")
        return 1

    # Немецкие блоки: элемент с атрибутом data-lang-de целиком.
    german = 0
    for match in re.finditer(r"<(\w+)[^>]*\bdata-lang-de\b[^>]*>(.*?)</\1>",
                             html, re.S | re.I):
        german += body_bytes(match.group(2))

    share = int(round(german * 100.0 / total))
    print("TEXT_BODY %d %d" % (total, share))
    return 0


if __name__ == "__main__":
    sys.exit(main())
