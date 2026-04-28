/* ─────────────────────────────────────────────────────────────
   AiS1.52 — whatsapp.js
   DSGVO-compliant 2-click WhatsApp opener.
   Modal explicitly informs user that data goes to Meta before
   the wa.me/ link is followed.
   ───────────────────────────────────────────────────────────── */

(() => {
  'use strict';

  const modal = document.getElementById('wa-modal');
  if (!modal) return;

  const card = modal.querySelector('.wa-modal-card');
  const triggers = document.querySelectorAll('[data-wa-trigger]');
  const closers = modal.querySelectorAll('[data-wa-close]');

  let lastFocused = null;

  function open() {
    lastFocused = document.activeElement;
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    setTimeout(() => {
      const firstFocusable = card.querySelector('button, a, [tabindex]');
      if (firstFocusable) firstFocusable.focus();
    }, 50);
    document.addEventListener('keydown', onKey);
  }

  function close() {
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    document.removeEventListener('keydown', onKey);
    if (lastFocused && typeof lastFocused.focus === 'function') {
      lastFocused.focus();
    }
  }

  function onKey(e) {
    if (e.key === 'Escape') close();
    if (e.key === 'Tab') {
      const focusables = card.querySelectorAll('button, a[href]');
      if (!focusables.length) return;
      const first = focusables[0];
      const last = focusables[focusables.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
  }

  triggers.forEach((t) => t.addEventListener('click', (e) => {
    e.preventDefault();
    open();
  }));

  closers.forEach((c) => c.addEventListener('click', (e) => {
    e.preventDefault();
    close();
  }));

  // Confirm button is a real <a target="_blank"> — close modal after click
  const confirm = modal.querySelector('#wa-confirm');
  if (confirm) {
    confirm.addEventListener('click', () => {
      // small delay so target="_blank" navigation kicks in before modal teardown
      setTimeout(close, 150);
    });
  }
})();
