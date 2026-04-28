/* ─────────────────────────────────────────────────────────────
   AiS1.52 — form.js
   Contact form submission with FormSubmit.co primary +
   Web3Forms fallback. UI states: idle / loading / success / error.
   No external dependencies.
   ───────────────────────────────────────────────────────────── */

(() => {
  'use strict';

  const form = document.getElementById('contact-form');
  if (!form) return;

  const status = document.getElementById('form-status');
  const submitBtn = document.getElementById('form-submit');

  // ─── PROVIDERS ───────────────────────────────────────────
  // Primary: FormSubmit.co (no signup, but CEO must confirm email on first submission)
  const FORMSUBMIT_EMAIL = 'ebaias.muc@gmail.com';
  const FORMSUBMIT_URL = `https://formsubmit.co/ajax/${FORMSUBMIT_EMAIL}`;

  // Fallback: Web3Forms.com — replace ACCESS_KEY with the one CEO gets from web3forms.com/dashboard
  // (free tier: 250 submissions/month, no signup-required for the trial key, but get your own)
  const WEB3FORMS_KEY = 'YOUR_WEB3FORMS_ACCESS_KEY';
  const WEB3FORMS_URL = 'https://api.web3forms.com/submit';

  const lang = () => document.documentElement.getAttribute('data-lang') || 'en';
  const t = (en, de) => (lang() === 'de' ? de : en);

  function setStatus(state, message = '') {
    if (!status) return;
    status.classList.remove('is-success', 'is-error');
    if (state === 'success') status.classList.add('is-success');
    if (state === 'error')   status.classList.add('is-error');
    status.textContent = message;
  }

  function setLoading(isLoading) {
    form.classList.toggle('is-loading', isLoading);
    if (submitBtn) submitBtn.disabled = isLoading;
  }

  function validate(data) {
    const errors = [];
    if (!data.name || data.name.trim().length < 2) {
      errors.push(t('Please enter your name.', 'Bitte gib deinen Namen ein.'));
    }
    if (!data.email || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(data.email)) {
      errors.push(t('Please enter a valid email.', 'Bitte gib eine gültige E-Mail ein.'));
    }
    if (!data.message || data.message.trim().length < 10) {
      errors.push(t('Message is too short (min 10 chars).', 'Nachricht zu kurz (min. 10 Zeichen).'));
    }
    if (data._honey) {
      errors.push('bot');
    }
    return errors;
  }

  async function submitFormSubmit(data) {
    const payload = {
      name: data.name,
      email: data.email,
      project_type: data.project_type,
      message: data.message,
      _subject: `[AiS152] New project inquiry from ${data.name}`,
      _captcha: 'false',
      _template: 'table',
    };
    const resp = await fetch(FORMSUBMIT_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!resp.ok) throw new Error(`FormSubmit HTTP ${resp.status}`);
    const json = await resp.json().catch(() => ({}));
    if (json.success === 'false' || json.success === false) {
      throw new Error(json.message || 'FormSubmit returned non-success');
    }
    return { provider: 'formsubmit', json };
  }

  async function submitWeb3Forms(data) {
    if (!WEB3FORMS_KEY || WEB3FORMS_KEY === 'YOUR_WEB3FORMS_ACCESS_KEY') {
      throw new Error('Web3Forms access key not configured');
    }
    const payload = {
      access_key: WEB3FORMS_KEY,
      name: data.name,
      email: data.email,
      project_type: data.project_type,
      message: data.message,
      from_name: 'AiS152 Contact Form',
      subject: `[AiS152] New project inquiry from ${data.name}`,
    };
    const resp = await fetch(WEB3FORMS_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!resp.ok) throw new Error(`Web3Forms HTTP ${resp.status}`);
    const json = await resp.json();
    if (!json.success) throw new Error(json.message || 'Web3Forms returned non-success');
    return { provider: 'web3forms', json };
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const fd = new FormData(form);
    const data = {
      name: fd.get('name')?.toString() || '',
      email: fd.get('email')?.toString() || '',
      project_type: fd.get('project_type')?.toString() || '',
      message: fd.get('message')?.toString() || '',
      _honey: fd.get('_honey')?.toString() || '',
    };

    const errors = validate(data);
    if (errors.length) {
      setStatus('error', errors[0] === 'bot' ? '' : errors[0]);
      return;
    }

    setStatus('idle');
    setLoading(true);

    try {
      let result;
      try {
        result = await submitFormSubmit(data);
      } catch (primaryErr) {
        console.warn('[form] FormSubmit failed, trying Web3Forms…', primaryErr);
        result = await submitWeb3Forms(data);
      }

      console.log('[form] sent via', result.provider);
      form.reset();
      setStatus('success', t(
        '✓ Message sent. I\'ll reply within one business day.',
        '✓ Nachricht gesendet. Antwort innerhalb eines Werktages.'
      ));
    } catch (err) {
      console.error('[form] all providers failed:', err);
      setStatus('error', t(
        'Could not send. Please email ebaias.muc@gmail.com directly.',
        'Konnte nicht senden. Bitte direkt an ebaias.muc@gmail.com schreiben.'
      ));
    } finally {
      setLoading(false);
    }
  });
})();
