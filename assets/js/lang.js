/* ─────────────────────────────────────────────────────────────
   AIS.152 — lang.js
   Переключатель языка. С 18.08.2026 он НЕ прячет и не показывает
   блоки — он переводит на другой адрес.

   Почему так. Прежняя схема держала обе версии в одном документе:
   немецкие блоки скрывались правилом CSS, язык выбирался по настройке
   браузера. У Googlebot такой настройки нет — он всегда получал
   английскую страницу, при том что бизнес в Мюнхене и клиенты ищут
   по-немецки. Google документирует такие страницы отдельно и
   рекомендует вместо них разные адреса на каждый язык.

   Теперь: / — немецкий, /en/ — английский. Выбор запоминается и
   применяется при следующем заходе на корень, но НЕ подменяет
   содержимое: адрес и язык всегда совпадают.
   ───────────────────────────────────────────────────────────── */

(() => {
  'use strict';

  const STORAGE_KEY = 'ais152.lang';
  const html = document.documentElement;
  const toggle = document.getElementById('lang-toggle');

  // Язык страницы задан сервером в разметке и подмене не подлежит.
  const current = (html.getAttribute('lang') || 'de').slice(0, 2).toLowerCase();

  function urlFor(code, path) {
    // Соответствие адресов: немецкий в корне, английский в /en/.
    const clean = (path || location.pathname).replace(/^\/en(\/|$)/, '/');
    return code === 'en'
      ? '/en' + (clean === '/' ? '/' : clean)
      : clean;
  }

  function remember(code) {
    try { localStorage.setItem(STORAGE_KEY, code); } catch (_) {}
  }

  remember(current);

  if (toggle) {
    const other = current === 'de' ? 'en' : 'de';
    const target = urlFor(other);

    // Переключатель — обычная ссылка. Поисковик проходит по ней и находит
    // вторую версию; при отключённом JS она тоже работает.
    if (toggle.tagName === 'A') {
      toggle.setAttribute('href', target);
      toggle.setAttribute('hreflang', other);
      toggle.setAttribute('rel', 'alternate');
    }
    toggle.addEventListener('click', (e) => {
      e.preventDefault();
      remember(other);
      location.href = target;
    });
  }

  // Совместимость со старыми ссылками вида ?lang=de — их раздавали до
  // перехода на отдельные адреса. Без этого они молча показывали бы
  // не тот язык, а теперь ведут туда, где он действительно живёт.
  const wanted = new URL(location.href).searchParams.get('lang');
  if (wanted && (wanted === 'de' || wanted === 'en') && wanted !== current) {
    remember(wanted);
    location.replace(urlFor(wanted));
  }

  document.dispatchEvent(new CustomEvent('ais:lang-changed', { detail: { lang: current } }));
})();
