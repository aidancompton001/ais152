# -*- coding: utf-8 -*-
"""Проба: сколько на главной внешних скриптов, где они стоят и помечены ли.

История ошибок в этом месте — три круга подряд:

  круг 1: «6 блокирующих скриптов» — неверно по количеству;
  круг 2: исправили на 10, но слово «блокирующие» осталось, хотя все десять
          стоят перед </body> и отрисовку не задерживают;
  круг 3 (F-30): проба, написанная ради фикса круга 2, не проверяла defer,
          async и module, а утверждение реестра про них говорило. Мутация
          «пометить все десять defer» проходила пробу насквозь.

Поэтому проба печатает ЧЕТЫРЕ величины, и каждая закрывает своё утверждение:
всего внешних скриптов, из них в голове документа, из них без пометки
отложенной загрузки, и где расположены все.

Печатает 'SCRIPTS <всего> <в head> <без пометки> <tail|mixed>'.
"""
import io
import re
import sys
from pathlib import Path

PAGE = Path(r"c:\Projects\AiS152\index.html")
DEFERRED = re.compile(r"\b(?:defer|async)\b|type\s*=\s*[\"']module[\"']", re.I)


def main():
    if not PAGE.is_file():
        print("НЕТ ФАЙЛА: %s" % PAGE)
        return 1
    html = io.open(PAGE, encoding="utf-8", errors="replace").read()

    head_end = html.lower().find("</head>")
    body_end = html.lower().rfind("</body>")
    if head_end < 0 or body_end < 0:
        print("НЕ НАЙДЕНЫ ГРАНИЦЫ ДОКУМЕНТА")
        return 1

    total, in_head, in_tail, plain = 0, 0, 0, 0
    for match in re.finditer(r"<script[^>]*\ssrc=[^>]*>", html, re.I):
        total += 1
        tag, pos = match.group(0), match.start()
        if not DEFERRED.search(tag):
            plain += 1
        if pos < head_end:
            in_head += 1
        elif pos > body_end - 4000:
            in_tail += 1

    if not total:
        print("ВНЕШНИХ СКРИПТОВ НЕТ — проба меряет пустоту")
        return 1

    where = "tail" if in_tail == total else "mixed"
    print("SCRIPTS %d %d %d %s" % (total, in_head, plain, where))
    return 0


if __name__ == "__main__":
    sys.exit(main())
