/* ─────────────────────────────────────────────────────────────
   AiS1.52 — lang.js
   EN/DE language switcher. Updates <html lang> and data-lang.
   Persists choice in localStorage. Honors ?lang=de URL param.
   ───────────────────────────────────────────────────────────── */

(() => {
  'use strict';

  const STORAGE_KEY = 'ais152.lang';
  const html = document.documentElement;
  const toggle = document.getElementById('lang-toggle');

  function setLang(code) {
    if (code !== 'en' && code !== 'de') code = 'en';
    html.setAttribute('lang', code);
    html.setAttribute('data-lang', code);
    try { localStorage.setItem(STORAGE_KEY, code); } catch (_) {}

    // sync <title> from sibling <meta name="title-en|de" content="…">
    const titleMeta = document.querySelector(`meta[name="title-${code}"]`);
    if (titleMeta) {
      const titleEl = document.querySelector('title');
      if (titleEl) titleEl.textContent = titleMeta.getAttribute('content') || titleEl.textContent;
    }

    const evt = new CustomEvent('ais:lang-changed', { detail: { lang: code } });
    document.dispatchEvent(evt);
  }

  // 1. Determine initial language: URL param > storage > html attr > browser > 'en'
  const url = new URL(window.location.href);
  const urlLang = url.searchParams.get('lang');
  let stored = null;
  try { stored = localStorage.getItem(STORAGE_KEY); } catch (_) {}
  const browserLang = (navigator.language || '').slice(0, 2).toLowerCase();
  const initial = urlLang || stored || (browserLang === 'de' ? 'de' : 'en');
  setLang(initial);

  // 2. Wire up toggle
  if (toggle) {
    toggle.addEventListener('click', () => {
      const current = html.getAttribute('data-lang') || 'en';
      setLang(current === 'en' ? 'de' : 'en');
    });
  }

  // 3. Public API
  window.AIS = window.AIS || {};
  window.AIS.setLang = setLang;
  window.AIS.getLang = () => html.getAttribute('data-lang') || 'en';
})();
