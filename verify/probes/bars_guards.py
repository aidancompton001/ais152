# -*- coding: utf-8 -*-
"""Три режима персонажа существуют и различаются по способу, а не по наличию.

До 19.08 эта проба проверяла обратное: что на узком экране персонажа нет.
CEO решил, что барс есть везде. Значит проверять надо не отсутствие,
а то, что на телефоне не используется непроверенное поведение —
перемотка прокруткой в Safari на iPhone, — и что просьба убрать движение
убирает движение, а не заменяет его замедленным.
"""
import io
import sys


def main():
    css = io.open("assets/css/bars.css", encoding="utf-8").read()
    js = io.open("assets/js/bars.js", encoding="utf-8").read()
    bad = []

    # 1. Персонаж не спрятан ни на телефоне, ни при выключенном движении.
    if "display: none" in css.split("@media (max-width: 1023px)")[-1][:200]:
        bad.append("на узком экране слой спрятан — CEO решил обратное")

    # 2. Три режима объявлены в скрипте.
    for word in ["'scrub'", "'play'", "'still'"]:
        if word not in js:
            bad.append("в скрипте нет режима %s" % word)

    # 3. Перемотка не запускается нигде, кроме широкого экрана.
    if "if (mode !== 'scrub') return;" not in js:
        bad.append("перемотка не ограничена широким экраном")

    # 4. При выключенном движении ролики не грузятся вовсе.
    if "removeAttribute('src')" not in js:
        bad.append("при выключенном движении ролики всё равно грузятся")

    # 5. При выключенном движении показывается неподвижный кадр.
    if "prefers-reduced-motion" not in css or ".bars-still" not in css:
        bad.append("нет неподвижного кадра для режима без движения")

    for b in bad:
        print("НЕ ТАК: %s" % b)
    print("guards=%d;" % (0 if bad else 3))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
