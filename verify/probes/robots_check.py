# -*- coding: utf-8 -*-
"""Общая проверка: закрыта ли страница от индексации.

Находка #14, круг 4 (F-52): пять проб независимо друг от друга брали ПЕРВЫЙ
найденный тег robots через re.search и молча игнорировали остальные. Разметка

    <meta name="robots" content="index,follow">
    <meta name="googlebot" content="noindex">

закрывает страницу от Google, а пробы отвечали «открыта».

Находка #14, круг 5 (F-67): у централизации есть обратная сторона — одна дыра
множится на пять проб сразу. Не ловились два случая:
  * `content="none"` — документированный Google эквивалент `noindex, nofollow`;
  * `name=robots` без кавычек — валидный HTML5.

Оба закрыты. Значение считается закрывающим, если содержит noindex ЛИБО none.
"""
import re

TAG = re.compile(
    r"""<meta[^>]+name\s*=\s*["']?(?:robots|googlebot)["']?[^>]*>""", re.I)
DENY = re.compile(r"\b(?:noindex|none)\b", re.I)


def closed_by_meta(html):
    """Любой из тегов robots/googlebot с noindex или none закрывает страницу."""
    return any(DENY.search(tag) for tag in TAG.findall(html or ""))


def closed_by_header(headers):
    """Заголовок ответа X-Robots-Tag действует наравне с тегом в разметке."""
    if headers is None:
        return False
    return bool(DENY.search(headers.get("X-Robots-Tag") or ""))


def closed(html, headers=None):
    return closed_by_meta(html) or closed_by_header(headers)
