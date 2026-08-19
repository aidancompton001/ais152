# -*- coding: utf-8 -*-
"""Вес сцен не выходит за бюджет.

Восемь мегабайт — потолок на все ролики с постерами вместе. Проверка
привязана к охраняемой величине (вес сцен), а не к размеру проекта:
иначе она сломается от роста проекта, а не от поломки.
"""
import glob
import os
import sys

BUDGET = 8 * 1024 * 1024


def main():
    files = glob.glob("assets/video/bars/*.mp4") + glob.glob("assets/video/bars/*.jpg")
    total = sum(os.path.getsize(f) for f in files)
    over = 1 if total > BUDGET else 0
    print("файлов %d, вместе %.2f МБ, бюджет %.0f МБ" %
          (len(files), total / 1048576.0, BUDGET / 1048576.0))
    print("over_budget=%d;" % over)
    return over


if __name__ == "__main__":
    sys.exit(main())
