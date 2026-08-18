# -*- coding: utf-8 -*-
"""Проба: форма обращения настроена, и её НАСТОЯЩИЙ приёмник жив.

Находка #14, круг 4 (F-61): сайт продаёт услуги, трафик упрётся в форму,
а её работоспособность не проверяло ничто.

Находка #14, круг 5 (F-65), тяжесть CRITICAL: первая версия этой пробы
доставала адрес приёмника из кода формы, клала его в переменную — и
запрашивала ГЛАВНУЮ СТРАНИЦУ сервиса, а печатала ответ рядом со словами
«основной приёмник отвечает». Ревьюер подставил заведомо мёртвый домен
в form.js — проба напечатала primary=200 и прошла. Число было верное,
подпись под ним считала другой ресурс: тот же класс, за который отклонены
круги 1, 2 и 4.

Теперь запрашивается ровно тот адрес, что стоит в коде формы. Приёмник
FormSubmit на GET отвечает 405 (метод не тот) — это признак живого адреса;
мёртвым считается 404 и любой 5xx, а также недостижимость.

Чего проба НЕ проверяет и врать об этом не будет: доходит ли письмо.
Отправить настоящее обращение — значит слать CEO письмо с каждой проверки,
а FormSubmit до подтверждения адреса писем не шлёт вовсе и об этом молчит.
Это состояние определяется только человеком.

Печатает 'FORM_OK to=<почта> endpoint=<код> fallback=<настроен|ЗАГЛУШКА>;'.
"""
import io
import re
import sys
import urllib.error
import urllib.request

UA = {"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}
PLACEHOLDER = re.compile(r"YOUR_|ACCESS_KEY|xxx+|<.*?>", re.I)
DEAD = {404, 410}


def probe_endpoint(url):
    """Код ответа настоящего приёмника. GET на него — законная проверка живости."""
    try:
        res = urllib.request.urlopen(
            urllib.request.Request(url, headers=UA), timeout=25)
        return res.status, None
    except urllib.error.HTTPError as exc:
        return exc.code, None
    except Exception as exc:
        return None, str(exc)


def main():
    try:
        html = urllib.request.urlopen(
            urllib.request.Request("https://ais152.com/", headers=UA),
            timeout=25).read().decode("utf-8", "replace")
    except Exception as exc:
        print("ГЛАВНАЯ НЕДОСТУПНА: %s" % exc)
        return 1

    if 'id="contact-form"' not in html:
        print("НА ЖИВОЙ СТРАНИЦЕ НЕТ ФОРМЫ ОБРАЩЕНИЯ")
        return 1

    try:
        code = io.open("assets/js/form.js", encoding="utf-8").read()
    except OSError as exc:
        print("НЕТ ОБРАБОТЧИКА ФОРМЫ: %s" % exc)
        return 1

    email = re.search(r"FORMSUBMIT_EMAIL\s*=\s*['\"]([^'\"]+)", code)
    tmpl = re.search(r"FORMSUBMIT_URL\s*=\s*[`'\"]([^`'\"]+)", code)
    if not tmpl:
        print("В ОБРАБОТЧИКЕ НЕ НАЙДЕН АДРЕС ПРИЁМНИКА")
        return 1

    url = tmpl.group(1)
    if "${FORMSUBMIT_EMAIL}" in url:
        if not email:
            print("АДРЕС ПРИЁМНИКА СОБИРАЕТСЯ ИЗ ПОЧТЫ, А ПОЧТА НЕ НАЙДЕНА")
            return 1
        url = url.replace("${FORMSUBMIT_EMAIL}", email.group(1))

    status, error = probe_endpoint(url)
    if error is not None:
        print("ПРИЁМНИК ФОРМЫ НЕДОСТИЖИМ: %s — %s" % (url, error))
        return 1
    if status in DEAD or status >= 500:
        print("ПРИЁМНИК ФОРМЫ МЁРТВ: %s отвечает %s" % (url, status))
        return 1

    key = re.search(r"WEB3FORMS_KEY\s*=\s*['\"]([^'\"]+)", code)
    fallback = "настроен"
    if not key or PLACEHOLDER.search(key.group(1)):
        fallback = "ЗАГЛУШКА"

    # Круг 6, F-81: сервис отвечает 405 на ЛЮБОЙ путь /ajax/*, поэтому
    # опечатка в адресе получателя проходила и пробу, и реестр. Адрес
    # вынесен в маркер: любая его правка теперь краснит реестр.
    to = email.group(1) if email else "?"
    print("FORM_OK to=%s endpoint=%s fallback=%s;" % (to, status, fallback))
    print("  проверенный адрес: %s" % url)
    if fallback == "ЗАГЛУШКА":
        print("  ВНИМАНИЕ: запасной приёмник не настроен — в коде оставлен "
              "ключ-заглушка. Если основной откажет, обращение пропадёт молча.")
    print("  НЕ ПРОВЕРЕНО: доходит ли письмо. FormSubmit не шлёт писем, пока "
          "адрес не подтверждён с первой отправки, и об этом не сообщает. "
          "Проверяется только человеком: отправить форму и увидеть письмо.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
