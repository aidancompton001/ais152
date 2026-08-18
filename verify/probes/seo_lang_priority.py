# -*- coding: utf-8 -*-
"""Проба: в каком порядке lang.js выбирает язык.

Находка #14, круг 3 (F-32). Утверждение реестра гласило: «язык выбирается
по настройке браузера, а НЕ по адресу страницы». Это неправда — `lang.js`
читает параметр `?lang=` из адреса, причём с наивысшим приоритетом:

    const urlLang = url.searchParams.get('lang');
    const initial = urlLang || stored || (browserLang === 'de' ? 'de' : 'en');

Практический вывод плана держится по другой причине: у краулера в адресе
параметра `?lang=` нет и сохранённого выбора нет, поэтому решает третий
источник — настройка браузера, а она даёт английский для любого значения,
кроме de. Но утверждение обязано описывать код, а не пересказ.

Проба печатает фактический порядок источников, извлечённый из кода.

Печатает 'LANG_PRIORITY url,stored,browser default=en'.
"""
import io
import re
import sys
from pathlib import Path

SCRIPT = Path(r"c:\Projects\AiS152\assets\js\lang.js")


def main():
    if not SCRIPT.is_file():
        print("НЕТ ФАЙЛА: %s" % SCRIPT)
        return 1
    code = io.open(SCRIPT, encoding="utf-8", errors="replace").read()

    line = re.search(r"const\s+initial\s*=\s*([^;]+);", code)
    if not line:
        print("НЕ НАЙДЕНА СТРОКА ВЫБОРА ЯЗЫКА — код изменился, проба устарела")
        return 1
    expr = line.group(1)

    order = []
    for name, token in (("url", "urlLang"), ("stored", "stored"),
                        ("browser", "browserLang")):
        pos = expr.find(token)
        if pos >= 0:
            order.append((pos, name))
    order.sort()
    if not order:
        print("НИ ОДИН ИЗВЕСТНЫЙ ИСТОЧНИК ЯЗЫКА НЕ УЧАСТВУЕТ: %s" % expr)
        return 1

    # Язык по умолчанию: то, что стоит в последней ветке тернарного оператора.
    fallback = re.search(r"\?\s*['\"](\w+)['\"]\s*:\s*['\"](\w+)['\"]", expr)
    default = fallback.group(2) if fallback else "?"

    print("LANG_PRIORITY %s default=%s"
          % (",".join(n for _p, n in order), default))
    return 0


if __name__ == "__main__":
    sys.exit(main())
