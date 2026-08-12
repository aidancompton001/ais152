#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_check.py — поведенческий пруф для утверждений о ВНЕШНИХ источниках.

Скачивает URL прямо сейчас, снимает HTML-теги, декодирует HTML-сущности
(важно: в законах пробел в числах записан как &#160;, поэтому наивный grep
по "5 000 Euro" даёт ложный минус) и проверяет наличие фразы.

Использование:
    python verify/fetch_check.py <URL> "<фраза>" ["<фраза2>" ...]

Exit 0  — ВСЕ фразы найдены в живом документе.
Exit 1  — хотя бы одна не найдена, либо источник недоступен.

Печатает найдено/не найдено по каждой фразе — вывод идёт в отчёт HRC.
"""
import sys
import re
import html
import urllib.request
import urllib.error

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
     "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"


def fetch_text(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    raw = urllib.request.urlopen(req, timeout=timeout).read()
    txt = raw.decode("utf-8", "replace")
    txt = re.sub(r"<script.*?</script>", " ", txt, flags=re.S | re.I)
    txt = re.sub(r"<style.*?</style>", " ", txt, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = html.unescape(txt)
    return re.sub(r"\s+", " ", txt)


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: fetch_check.py <URL> <phrase> [phrase...]")
        return 2

    url, phrases = sys.argv[1], sys.argv[2:]

    try:
        text = fetch_text(url)
    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as exc:
        print(f"UNREACHABLE {url} -> {exc}")
        return 1

    missing = []
    for p in phrases:
        if p in text:
            print(f"FOUND    {p!r}")
        else:
            print(f"MISSING  {p!r}")
            missing.append(p)

    print(f"SOURCE   {url}  ({len(text)} Zeichen)")
    if missing:
        print(f"RESULT   FAIL — {len(missing)} von {len(phrases)} nicht gefunden")
        return 1
    print(f"RESULT   OK — alle {len(phrases)} Phrasen im Live-Dokument")
    return 0


if __name__ == "__main__":
    sys.exit(main())
