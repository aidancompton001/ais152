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


# ─── Правила robots.txt ────────────────────────────────────────────────
#
# Находка #14, F-104: матчер robots.txt существовал в ТРЁХ несовместимых
# копиях — и это ровно F-52/F-67 повторно: одна логика в нескольких местах
# чинится не везде. Дыры в двух из трёх:
#   * `Disallow: /` явно выбрасывалось из перебора как «пустое правило».
#     То есть максимальный возможный конфликт — закрыт весь сайт, ни один
#     noindex не читается — проба объявляла «конфликтов нет»;
#   * `*` внутри правила и `$` на конце не понимались, хотя `Disallow: /*.md$`
#     стоит в этом самом robots.txt. Мутация `Disallow: /*.html$` глушила
#     noindex на всех страницах разом и проходила насквозь.

def parse_disallow(text):
    """Список правил Disallow из текста robots.txt.

    Находка #14, F-111: прежний разбор требовал, чтобы после пути не было
    ничего, и строка `Disallow: / # рабочие документы` не распознавалась
    вовсе. Краулер по RFC 9309 комментарий отбрасывает и правило исполняет —
    то есть Google закрыл бы весь сайт, а проба напечатала бы «конфликтов
    нет». Тот же провал в безопасную сторону, что и выброшенное `Disallow: /`,
    только с решёткой. В нашем robots.txt комментариев больше, чем директив.
    """
    out = []
    for line in (text or "").splitlines():
        line = line.split("#", 1)[0].strip()
        found = re.match(r"(?i)^Disallow:\s*(\S*)\s*$", line)
        if found and found.group(1):
            out.append(found.group(1))
    return out


def _rule_to_regex(rule):
    """Правило robots.txt в регулярное выражение по правилам Google.

    `*` — любая последовательность, `$` на конце — конец адреса,
    в остальном совпадение по префиксу.
    """
    anchored = rule.endswith("$")
    body = rule[:-1] if anchored else rule
    parts = [re.escape(p) for p in body.split("*")]
    pattern = ".*".join(parts)
    return re.compile("^" + pattern + ("$" if anchored else ""))


def crawl_blocked(path, rules):
    """Закрыт ли обход этого пути правилами robots.txt.

    path — с ведущим слэшем или без, приводится к виду '/что-то'.
    """
    target = path if path.startswith("/") else "/" + path
    for rule in rules or ():
        if not rule:
            continue
        if rule == "/":
            # Закрыт весь сайт. Раньше это правило пропускалось как пустое.
            return True
        if _rule_to_regex(rule).match(target):
            return True
    return False
