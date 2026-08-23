# -*- coding: utf-8 -*-
"""Заменить в готовой странице четырнадцать подключений на два файла.

Источник по-прежнему перечисляет семь стилей и семь скриптов: так их
удобно править и так виден порядок. В отданной посетителю странице
остаются два собранных файла — замерено 23.08, семь стилей блокировали
показ каждым своим запросом.

Здесь же чужие библиотеки переезжают на свой адрес. Причина не только в
скорости: при загрузке с cdnjs.cloudflare.com и cdn.jsdelivr.net браузер
посетителя сам обращается к чужому серверу и передаёт ему свой IP-адрес.
Для немецкого сайта это передача персональных данных третьему лицу без
согласия — то, за что суд в Мюнхене взыскал с владельца сайта деньги за
подключённые шрифты Google (LG München I, 20.01.2022, 3 O 17493/20).

Отдельным модулем, а не внутри build_langs.py, потому что здесь много
регулярных выражений с обратными слэшами: править их внутри чужого файла
через подстановку строк — верный способ сломать сборку.
"""
import hashlib
import re

VENDOR = [
    (r'<script src="https://cdn\.jsdelivr\.net/npm/lenis[^"]*"([^>]*)></script>',
     "assets/vendor/lenis.min.js"),
    (r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/gsap/[^/]+/gsap\.min\.js"([^>]*)></script>',
     "assets/vendor/gsap.min.js"),
    (r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/gsap/[^/]+/ScrollTrigger\.min\.js"([^>]*)></script>',
     "assets/vendor/ScrollTrigger.min.js"),
]

# К этому моменту пути уже сделаны корневыми (absolutise в build_langs) и
# несут метку версии. Шаблон обязан допускать ведущую косую черту, иначе он
# молча ничего не находит и страница уходит с четырнадцатью подключениями —
# ровно это и случилось при первой попытке.
CSS_TAG = re.compile(r'[ \t]*<link rel="stylesheet" href="/?assets/css/[^"]+">\n?')
JS_TAG = re.compile(r'[ \t]*<script src="/?assets/js/[^"]+"[^>]*></script>\n?')


def _stamp(root, rel):
    """Метка версии по содержимому файла, а не по дате в голове."""
    f = root / rel
    if not f.is_file():
        return "/" + rel
    return "/%s?v=%s" % (rel, hashlib.md5(f.read_bytes()).hexdigest()[:10])


def apply(html, root):
    css = CSS_TAG.findall(html)
    if css:
        html = CSS_TAG.sub("", html, count=len(css))
        tag = '<link rel="stylesheet" href="%s">\n' % _stamp(root, "assets/build/site.css")
        html = html.replace("</head>", tag + "</head>", 1)

    for pattern, path in VENDOR:
        html = re.sub(pattern,
                      lambda m, p=path: '<script src="%s"%s></script>'
                      % (_stamp(root, p), m.group(1)), html)

    js = JS_TAG.findall(html)
    if js:
        first = js[0]
        html = JS_TAG.sub("", html, count=len(js))
        indent = first[:len(first) - len(first.lstrip())]
        tag = '%s<script src="%s" defer></script>\n' % (
            indent, _stamp(root, "assets/build/site.js"))
        html = html.replace("</body>", tag + "</body>", 1)

    return html
