# -*- coding: utf-8 -*-
"""Собрать одноязычные страницы из двуязычного шаблона.

Зачем это существует. До 18.08.2026 обе версии жили в одном документе:
немецкие блоки скрывались правилом CSS, язык выбирался скриптом по настройке
браузера. У Googlebot такой настройки нет, поэтому он ВСЕГДА получал
английскую страницу — при том что бизнес в Мюнхене и клиенты ищут по-немецки.
Google документирует такие страницы отдельно и рекомендует вместо них разные
адреса на каждый язык.

Что делает скрипт: из `index.src.html` (двуязычный источник) собирает
`index.html` — только немецкий — и `en/index.html` — только английский.
Блоки другого языка не прячутся, а вырезаются: в исходном коде страницы
не остаётся ни байта чужого языка.

    py scripts/build_langs.py           # показать, что получится
    py scripts/build_langs.py --write   # собрать файлы
"""
import io
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bundle_tags  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
# Источник лежит в каталоге с подчёркиванием намеренно: GitHub Pages прогоняет
# Jekyll, а тот не публикует пути, начинающиеся с подчёркивания. Иначе двуязычный
# шаблон отдавался бы публично и был бы страницей-сиротой, дублирующей обе
# версии сразу — проба сирот поймала это через минуту после публикации.
SOURCE = ROOT / "_src" / "index.src.html"

# Куда какой язык кладётся. Решение CEO 18.08.2026: немецкий в корень —
# основной рынок получает самый сильный адрес.
TARGETS = {
    "de": {"path": ROOT / "index.html", "url": "https://ais152.com/"},
    "en": {"path": ROOT / "en" / "index.html", "url": "https://ais152.com/en/"},
}

# Заголовок и описание на каждый язык. Прежний заголовок был один на обе версии
# и звучал «AIS.152 — Engineering AI systems · Munich»: он не совпадает ни с одним
# запросом, который вводит немецкий клиент. Немецкий заголовок содержит целевую
# фразу дословно — так устроены все девять разобранных сайтов немецкой выдачи.
META = {
    "de": {
        "title": "KI-Automatisierung & n8n für den Mittelstand — München | AIS.152",
        "description": ("Unabhängiges Engineering-Studio in München. Prozesse mit n8n "
                        "automatisieren, KI dort integrieren, wo sie wirklich Arbeit "
                        "abnimmt. Apps und Plattformen im produktiven Einsatz."),
        "og_locale": "de_DE",
        "og_locale_alt": "en_US",
    },
    "en": {
        "title": "AIS.152 — Engineering AI systems · Munich",
        "description": ("Independent engineering studio in Munich. Production AI systems, "
                        "mobile platforms, and automation for teams that need to ship."),
        "og_locale": "en_US",
        "og_locale_alt": "de_DE",
    },
}


def strip_other(html, keep):
    """Вырезать элементы другого языка целиком, вместе с содержимым."""
    drop = "en" if keep == "de" else "de"
    out, pos = [], 0
    pattern = re.compile(r"<(\w+)([^>]*\bdata-lang-%s\b[^>]*)>" % drop, re.I)
    while True:
        m = pattern.search(html, pos)
        if not m:
            out.append(html[pos:])
            break
        out.append(html[pos:m.start()])
        tag = m.group(1)
        # Найти парный закрывающий тег с учётом вложенности одноимённых.
        depth, cur = 1, m.end()
        token = re.compile(r"</?%s\b" % re.escape(tag), re.I)
        while depth and cur < len(html):
            tm = token.search(html, cur)
            if not tm:
                break
            depth += -1 if tm.group(0).startswith("</") else 1
            cur = tm.end()
        end = html.find(">", cur - 1)
        pos = (end + 1) if end >= 0 else len(html)
    text = "".join(out)
    # Атрибут-маркер у оставшегося языка больше не нужен.
    text = re.sub(r"\s+data-lang-%s\b" % keep, "", text)
    # Пустые строки, оставшиеся от вырезанных блоков.
    text = re.sub(r"\n[ \t]*\n[ \t]*\n+", "\n\n", text)
    return text


def absolutise(html):
    """Относительные пути от корня.

    Английская версия лежит на /en/, и относительный путь assets/... из неё
    разрешается как /en/assets/... — то есть 404 на все стили, скрипты
    и картинки. Ошибка тихая: страница отдаёт 200 и выглядит сломанной.
    """
    def fix(m):
        attr, value = m.group(1), m.group(2)
        if value.startswith(("http://", "https://", "/", "#", "mailto:", "tel:",
                             "data:", "javascript:")):
            return m.group(0)
        return '%s="/%s"' % (attr, value)
    return re.sub(r'(?<![a-zA-Z-])(href|src)="([^"]+)"', fix, html)


def apply_meta(html, lang):
    """Свой заголовок, описание и локаль на каждый язык."""
    meta = META[lang]
    html = re.sub(r"<title>.*?</title>",
                  "<title>%s</title>" % meta["title"], html, count=1, flags=re.S)
    html = re.sub(r'<meta name="description" content="[^"]*">',
                  '<meta name="description" content="%s">' % meta["description"],
                  html, count=1)
    html = re.sub(r'<meta property="og:title" content="[^"]*">',
                  '<meta property="og:title" content="%s">' % meta["title"],
                  html, count=1)
    html = re.sub(r'<meta property="og:description" content="[^"]*">',
                  '<meta property="og:description" content="%s">' % meta["description"],
                  html, count=1)
    html = re.sub(r'<meta property="og:url" content="[^"]*">',
                  '<meta property="og:url" content="%s">' % TARGETS[lang]["url"],
                  html, count=1)
    html = re.sub(r'<meta property="og:locale" content="[^"]*">',
                  '<meta property="og:locale" content="%s">' % meta["og_locale"],
                  html, count=1)
    html = re.sub(r'<meta property="og:locale:alternate" content="[^"]*">',
                  '<meta property="og:locale:alternate" content="%s">' % meta["og_locale_alt"],
                  html, count=1)
    html = re.sub(r'<meta name="twitter:title" content="[^"]*">',
                  '<meta name="twitter:title" content="%s">' % meta["title"],
                  html, count=1)
    html = re.sub(r'<meta name="twitter:description" content="[^"]*">',
                  '<meta name="twitter:description" content="%s">' % meta["description"],
                  html, count=1)
    # Служебные метки прежнего механизма переключения языка больше не нужны.
    html = re.sub(r'\s*<meta name="title-(?:en|de)" content="[^"]*">', "", html)
    return html


def apply_head(html, lang):
    """Язык документа, canonical и взаимные hreflang."""
    html = re.sub(r'<html[^>]*>', '<html lang="%s" data-lang="%s">' % (lang, lang),
                  html, count=1)
    html = re.sub(r'<link rel="canonical"[^>]*>',
                  '<link rel="canonical" href="%s">' % TARGETS[lang]["url"],
                  html, count=1)

    alts = "\n".join(
        '<link rel="alternate" hreflang="%s" href="%s" />' % (code, TARGETS[code]["url"])
        for code in ("de", "en"))
    alts += '\n<link rel="alternate" hreflang="x-default" href="%s" />' % TARGETS["de"]["url"]
    html = re.sub(r'(<link rel="alternate" hreflang="[^"]*"[^>]*>\s*)+', alts + "\n",
                  html, count=1)
    return html


def stamp_assets(html):
    """Проставить каждому стилю и скрипту метку по его содержимому.

    В источнике стояла метка ?v=2026-08-14-px014 с припиской «заменить на
    хеш при выкладке». Её никто не заменял, и всё, что менялось в стилях и
    скриптах после четырнадцатого августа, до вернувшегося посетителя не
    доходило: браузер держал старый файл под тем же адресом. Именно так
    потеплевшая палитра не появилась на экране CEO.

    Метка теперь считается из содержимого файла: изменился файл — изменился
    адрес. Не изменился — адрес прежний, и кеш работает как задумано.
    """
    import hashlib

    def repl(m):
        rel = m.group(1)
        f = ROOT / rel
        if not f.is_file():
            return m.group(0)
        h = hashlib.md5(f.read_bytes()).hexdigest()[:10]
        return '%s?v=%s' % (rel, h)

    return re.sub(r"(assets/(?:css|js)/[A-Za-z0-9._-]+\.(?:css|js))\?v=[^\"']*", repl, html)


NUM_DE = {13: "Dreizehn", 14: "Vierzehn", 15: "Fünfzehn", 16: "Sechzehn",
          17: "Siebzehn", 18: "Achtzehn", 19: "Neunzehn", 20: "Zwanzig"}
NUM_EN = {13: "Thirteen", 14: "Fourteen", 15: "Fifteen", 16: "Sixteen",
          17: "Seventeen", 18: "Eighteen", 19: "Nineteen", 20: "Twenty"}


def fill_counts(html):
    """Подставить число проектов и число коммитов из данных, а не из памяти.

    Число проектов стояло в семи местах на двух языках. Убрали один проект —
    и все семь стали враньём одновременно, причём молча: ни одна проверка
    этого не ловила, потому что числа были просто текстом.

    Число коммитов стояло как 2 418 и не сходилось ни с чем: в репозитории
    их 127. Теперь берётся из git.
    """
    import json
    import subprocess

    data = json.load(io.open(ROOT / "data" / "projects.json", encoding="utf-8"))
    items = data if isinstance(data, list) else data.get("projects", [])
    n = len([p for p in items if (p.get("status") or "") == "live"])

    try:
        commits = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=str(ROOT),
                                 capture_output=True, text=True).stdout.strip()
        commits = "{:,}".format(int(commits))
    except Exception:
        commits = ""

    html = html.replace("{{N}}", str(n))
    html = html.replace("{{COMMITS}}", commits or "—")
    html = html.replace("{{WORD_DE}}", NUM_DE.get(n, str(n)))
    html = html.replace("{{WORD_EN}}", NUM_EN.get(n, str(n)))
    html = html.replace("{{WORD_DE_L}}", NUM_DE.get(n, str(n)).lower())
    html = html.replace("{{WORD_EN_L}}", NUM_EN.get(n, str(n)).lower())
    return html


def main():
    write = "--write" in sys.argv
    if not SOURCE.is_file():
        print("НЕТ ИСТОЧНИКА: %s" % SOURCE)
        print("Источник — двуязычный шаблон, из которого собираются обе версии.")
        return 1

    src = io.open(SOURCE, encoding="utf-8").read()
    problems = []
    for lang, target in TARGETS.items():
        page = bundle_tags.apply(
            stamp_assets(fill_counts(
                apply_head(apply_meta(absolutise(strip_other(src, lang)), lang), lang))),
            ROOT)

        other = "en" if lang == "de" else "de"
        left = page.count("data-lang-%s" % other)
        if left:
            problems.append("%s: осталось %d блоков языка %s" % (lang, left, other))

        if write:
            target["path"].parent.mkdir(parents=True, exist_ok=True)
            io.open(target["path"], "w", encoding="utf-8", newline="\n").write(page)
        print("%-3s %-28s %6d байт" % (lang, target["path"].name, len(page.encode("utf-8"))))

    if problems:
        for p in problems:
            print("ОСТАТКИ ЧУЖОГО ЯЗЫКА: %s" % p)
        return 1

    # Склейка стилей и скриптов идёт ПЕРЕД тем, как страницы получат метки
    # версий: метка считается по содержимому собранного файла, и порядок
    # здесь не вопрос вкуса. Запускается один раз, до записи страниц.
    if write:
        import subprocess
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "bundle_assets.py"),
                            "--write"], cwd=str(ROOT), capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        for line in (r.stdout or "").strip().splitlines():
            print("  %s" % line)
        if r.returncode != 0:
            print("СКЛЕЙКА НЕ СОБРАЛАСЬ")
            return 1

    # Карточки работ вписываются в исходный код ПОСЛЕ сборки языковых версий:
    # иначе эта же сборка их и затрёт. Порядок важен и потому зафиксирован
    # здесь, а не в памяти того, кто запускает скрипты.
    if write:
        import subprocess
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "render_work_static.py"),
                            "--write"], cwd=str(ROOT), capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        for line in (r.stdout or "").strip().splitlines():
            print("  %s" % line)
        if r.returncode != 0:
            print("КАРТОЧКИ РАБОТ НЕ ВПИСАНЫ")
            return 1

    print("собрано" if write else "холостой прогон, запусти с --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
