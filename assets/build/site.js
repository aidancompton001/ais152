
/* ── lang ── */
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


/* ── dotgrid ── */
/* ─────────────────────────────────────────────────────────────
   AIS.152 — dotgrid.js
   Animated canvas dot field for hero background.
   Mouse position creates a subtle gravitational pull.
   Auto-skips on reduced-motion or mobile.
   ───────────────────────────────────────────────────────────── */

(() => {
  'use strict';

  const canvas = document.getElementById('hero-grid');
  if (!canvas) return;

  const REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const IS_MOBILE = matchMedia('(max-width: 640px)').matches;
  if (REDUCED || IS_MOBILE) {
    canvas.style.display = 'none';
    return;
  }

  const ctx = canvas.getContext('2d', { alpha: true });
  if (!ctx) return;

  let dpr = Math.min(window.devicePixelRatio || 1, 2);
  let W = 0, H = 0;
  let dots = [];
  const SPACING = 28;
  const RADIUS = 1.0;
  const PULL_RADIUS = 140;
  const PULL_STRENGTH = 18;

  let mx = -9999, my = -9999;

  function resize() {
    const r = canvas.getBoundingClientRect();
    W = r.width;
    H = r.height;
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    dots = [];
    const cols = Math.ceil(W / SPACING) + 2;
    const rows = Math.ceil(H / SPACING) + 2;
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const x = c * SPACING - SPACING / 2;
        const y = r * SPACING - SPACING / 2;
        // Distance-from-center fade
        const cx = W / 2, cy = H / 2;
        const dist = Math.hypot(x - cx, y - cy);
        const maxDist = Math.hypot(cx, cy);
        const fade = 1 - Math.min(1, dist / maxDist) * 0.5;
        dots.push({ ox: x, oy: y, x, y, fade });
      }
    }
  }

  let running = false;
  let visible = true;

  function draw() {
    ctx.clearRect(0, 0, W, H);
    for (let i = 0; i < dots.length; i++) {
      const d = dots[i];
      const dx = mx - d.ox;
      const dy = my - d.oy;
      const dist = Math.hypot(dx, dy);
      let tx = d.ox, ty = d.oy;
      if (dist < PULL_RADIUS) {
        const force = (1 - dist / PULL_RADIUS) * PULL_STRENGTH;
        const angle = Math.atan2(dy, dx);
        tx -= Math.cos(angle) * force;
        ty -= Math.sin(angle) * force;
      }
      // ease towards target
      d.x += (tx - d.x) * 0.12;
      d.y += (ty - d.y) * 0.12;

      const distFromMouse = Math.hypot(mx - d.x, my - d.y);
      const glow = distFromMouse < PULL_RADIUS ? (1 - distFromMouse / PULL_RADIUS) : 0;

      const baseAlpha = 0.18 * d.fade;
      const alpha = Math.min(0.85, baseAlpha + glow * 0.6);
      const r = RADIUS + glow * 0.8;

      ctx.beginPath();
      ctx.fillStyle = glow > 0.1
        ? `rgba(255, 106, 60, ${alpha})`
        : `rgba(244, 239, 229, ${alpha})`;
      ctx.arc(d.x, d.y, r, 0, Math.PI * 2);
      ctx.fill();
    }
    if (running) raf = requestAnimationFrame(draw);
  }

  let raf = 0;

  window.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mx = e.clientX - rect.left;
    my = e.clientY - rect.top;
  });
  window.addEventListener('mouseleave', () => { mx = -9999; my = -9999; });
  window.addEventListener('resize', resize);

  // Холст рисует, только пока он на экране и вкладка активна.
  //
  // До 19.08.2026 draw() безусловно ставил следующий кадр и крутился вечно:
  // человек давно ниже первого экрана, холста не видит, а тот продолжает
  // перебирать все точки и перерисовывать их шестьдесят раз в секунду.
  // Заметить это было нельзя, пока страница ничего тяжёлого не делала.
  // Со сценами персонажа он начнёт отбирать те же 16 миллисекунд у декода
  // кадра — то есть у того единственного, что человек в этот момент видит.
  // Нашёл агент при разборе конфликтов, 19.08.2026.

  function start() {
    if (running) return;
    running = true;
    draw();
  }

  function stop() {
    running = false;
    if (raf) { cancelAnimationFrame(raf); raf = 0; }
  }

  // Вкладка ушла в фон — рисовать некому.
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) stop();
    else if (visible) start();
  });

  if ('IntersectionObserver' in window) {
    new IntersectionObserver((entries) => {
      visible = entries[0].isIntersecting;
      if (visible && !document.hidden) start(); else stop();
    }, { rootMargin: '100px' }).observe(canvas);
  }

  resize();
  start();
})();


/* ── terminal ── */
/* ─────────────────────────────────────────────────────────────
   AIS.152 — terminal.js
   Animated terminal panel in the hero. Cycles through 3 "files"
   (TS, Markdown, log) typing each one out, then switches.
   Auto-pauses on reduced-motion (renders fully-typed last frame).
   ───────────────────────────────────────────────────────────── */

(() => {
  'use strict';

  const code = document.getElementById('hero-terminal-code');
  const path = document.getElementById('hero-terminal-path');
  const tabs = document.querySelectorAll('.hero-terminal-tab');
  if (!code) return;

  const REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Token-based code samples. Each token: ['class', 'text']
  const FILES = [
    {
      tab: 'quote',
      label: 'quote.ts',
      path: '~/projects/baupreis/api/quote.ts',
      tokens: [
        ['tc', '// generate cost estimate from blueprint\n'],
        ['tk', 'export async function '], ['tf', 'estimate'], ['tp', '('],
        ['tf', 'plan'], ['tp', ': '], ['tf', 'Blueprint'], ['tp', ') {\n'],
        ['tp', '  '], ['tk', 'const '], ['tf', 'rooms'], ['tp', ' = '],
        ['tk', 'await '], ['tf', 'parseLayout'], ['tp', '('], ['tf', 'plan'], ['tp', ')\n'],
        ['tp', '  '], ['tk', 'const '], ['tf', 'rates'], ['tp', ' = '],
        ['tk', 'await '], ['tf', 'fetchRates'], ['tp', '('], ['ts', "'munich'"], ['tp', ')\n\n'],
        ['tp', '  '], ['tk', 'return '], ['tf', 'rooms'], ['tp', '.'],
        ['tf', 'reduce'], ['tp', '(('], ['tf', 'sum'], ['tp', ', '],
        ['tf', 'r'], ['tp', ') => {\n'],
        ['tp', '    '], ['tk', 'const '], ['tf', 'cost'], ['tp', ' = '],
        ['tf', 'r'], ['tp', '.'], ['tf', 'area'], ['tp', ' * '],
        ['tf', 'rates'], ['tp', '['], ['tf', 'r'], ['tp', '.'],
        ['tf', 'type'], ['tp', '] * '], ['tn', '1.18'], ['tp', '  '],
        ['tc', '// VAT'], ['tp', '\n'],
        ['tp', '    '], ['tk', 'return '], ['tf', 'sum'], ['tp', ' + '],
        ['tf', 'cost'], ['tp', '\n'],
        ['tp', '  }, '], ['tn', '0'], ['tp', ')\n'],
        ['tp', '}\n'],
      ],
    },
    {
      tab: 'process',
      label: 'process.md',
      path: '~/projects/.notes/process.md',
      tokens: [
        ['tcoral', '# Speed is the moat\n\n'],
        ['tk', '## '], ['tf', '01 — Reply'], ['tp', '    '],
        ['tc', '// within 1 hour'], ['tp', '\n'],
        ['tp', 'One real human, one hour, no funnel.\n'],
        ['tp', 'You get a yes/no and a price.\n\n'],
        ['tk', '## '], ['tf', '02 — Concept'], ['tp', '  '],
        ['tc', '// within 24 hours'], ['tp', '\n'],
        ['tp', 'Working draft on a private URL.\n'],
        ['tp', 'Click-through, not a slide deck.\n\n'],
        ['tk', '## '], ['tf', '03 — Ship'], ['tp', '     '],
        ['tc', '// within 3 days'], ['tp', '\n'],
        ['tp', 'Production deploy. Custom domain,\n'],
        ['tp', 'SSL, monitoring, docs for humans.\n'],
      ],
    },
    {
      tab: 'commits',
      label: 'commits.log',
      path: '~/projects/baupreis/.git/log',
      tokens: [
        ['tn', 'a4f83e1'], ['tp', '  '], ['ts', '2026-04-22'], ['tp', '  '],
        ['tf', 'feat'], ['tp', ': '], ['tcoral', 'multi-tenant audit log\n'],
        ['tn', 'b8c721a'], ['tp', '  '], ['ts', '2026-04-19'], ['tp', '  '],
        ['tf', 'fix'], ['tp', ': VAT calc rounding edge case\n'],
        ['tn', 'd6e4019'], ['tp', '  '], ['ts', '2026-04-15'], ['tp', '  '],
        ['tf', 'feat'], ['tp', ': '], ['tcoral', 'AI plan analyzer v2\n'],
        ['tn', '3ad9c52'], ['tp', '  '], ['ts', '2026-04-12'], ['tp', '  '],
        ['tf', 'perf'], ['tp', ': memo room parser, -340ms\n'],
        ['tn', 'f02b41d'], ['tp', '  '], ['ts', '2026-04-08'], ['tp', '  '],
        ['tf', 'docs'], ['tp', ': API reference auto-gen\n'],
        ['tn', '1c87a93'], ['tp', '  '], ['ts', '2026-04-05'], ['tp', '  '],
        ['tf', 'feat'], ['tp', ': PDF quote export\n'],
        ['tc', '\n# 8 projects · 2,418 commits · last reply 12m ago'],
      ],
    },
  ];

  let fileIdx = 0;
  let typingTimer = null;
  let switchTimer = null;
  let abort = false;

  function escapeHTML(s) {
    return s
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  function renderFully(file) {
    const html = file.tokens
      .map(([cls, txt]) => `<span class="${cls}">${escapeHTML(txt)}</span>`)
      .join('');
    code.innerHTML = html + '<span class="caret">█</span>';
  }

  function setActiveTab(idx) {
    tabs.forEach((t, i) => t.classList.toggle('is-active', i === idx));
    if (path) path.textContent = FILES[idx].path;
  }

  async function typeFile(idx) {
    abort = false;
    const file = FILES[idx];
    setActiveTab(idx);

    if (REDUCED) {
      renderFully(file);
      return;
    }

    code.innerHTML = '';
    let html = '';
    for (let t = 0; t < file.tokens.length; t++) {
      if (abort) return;
      const [cls, text] = file.tokens[t];
      // For code-heavy tokens type char by char; for whitespace flush at once.
      if (text.length <= 3 || cls === 'tp' || cls === 'tc') {
        html += `<span class="${cls}">${escapeHTML(text)}</span>`;
        code.innerHTML = html + '<span class="caret">█</span>';
        await sleep(text.includes('\n') ? 90 : 24);
      } else {
        const chunks = text.match(/.{1,2}/g) || [text];
        let acc = '';
        for (const ch of chunks) {
          if (abort) return;
          acc += ch;
          code.innerHTML = html + `<span class="${cls}">${escapeHTML(acc)}</span>` + '<span class="caret">█</span>';
          await sleep(28);
        }
        html += `<span class="${cls}">${escapeHTML(text)}</span>`;
      }
    }
    code.innerHTML = html + '<span class="caret">█</span>';
  }

  function sleep(ms) {
    return new Promise((r) => { typingTimer = setTimeout(r, ms); });
  }

  async function loop() {
    while (true) {
      await typeFile(fileIdx);
      await new Promise((r) => { switchTimer = setTimeout(r, 5500); });
      fileIdx = (fileIdx + 1) % FILES.length;
    }
  }

  // Click on a tab → jump to that file
  tabs.forEach((t, i) => {
    t.addEventListener('click', () => {
      abort = true;
      clearTimeout(typingTimer);
      clearTimeout(switchTimer);
      fileIdx = i;
      setTimeout(() => { abort = false; loop(); }, 50);
    });
  });

  // Initial: show fully-rendered first file, then start animating after a beat
  setActiveTab(0);
  if (REDUCED) {
    renderFully(FILES[0]);
  } else {
    setTimeout(loop, 800);
  }
})();


/* ── projects ── */
/* ─────────────────────────────────────────────────────────────
   AIS.152 — projects.js (v2)
   Reads data/projects.json, renders cards into #work-track.
   Adds layout classes (feature/wide/square/tall/tile) and
   custom <use href="#mark-{slug}"/> SVG mark per project.
   ───────────────────────────────────────────────────────────── */

(() => {
  'use strict';

  const TRACK = document.getElementById('work-track');
  const TPL = document.getElementById('project-card-tpl');
  const LOADING = document.getElementById('work-loading');
  if (!TRACK || !TPL) return;

  // Карточки собраны на этапе сборки (scripts/render_work_static.py) и уже
  // лежат в странице. Раньше скрипт стирал их и строил заново: замер на
  // живом сайте 23.08 (телефон, медленный 4G, процессор ×4) дал пересчёт
  // вёрстки на 526 мс с 1014 узлами плюс отдельный запрос за
  // data/projects.json уже после загрузки. Теперь скрипт их только оживляет.
  const STATIC = TRACK.querySelectorAll('.card').length > 0;

  const STATUS_LABELS = {
    live: { en: 'Live', de: 'Live' },
    'in-development': { en: 'In dev', de: 'In Arbeit' },
    archived: { en: 'Archived', de: 'Archiv' },
  };

  function renderCard(project, index, total) {
    const node = TPL.content.cloneNode(true);
    const article = node.querySelector('.card');
    const numEl = node.querySelector('.card-num');
    const linkEl = node.querySelector('.card-link');
    const imgEl = node.querySelector('.card-img');
    const statusEl = node.querySelector('.card-status');
    const yearEl = node.querySelector('.card-year');
    const tagPrimaryEl = node.querySelector('.card-tag-primary');
    const titleEl = node.querySelector('.card-title');
    const taglineEl = node.querySelector('.card-tagline');
    const tagsEl = node.querySelector('.card-tags');
    const bodyEl = node.querySelector('.card-body');
    const caseEl = node.querySelector('.card-case');

    article.dataset.slug = project.slug;
    article.classList.add('layout-' + (project.layout || 'square'));
    if (project.featured) article.classList.add('is-featured');

    numEl.textContent = `${String(index + 1).padStart(2, '0')} / ${String(total).padStart(2, '0')}`;

    if (project.url && project.url !== '#') {
      linkEl.href = project.url;
    } else {
      linkEl.removeAttribute('target');
      linkEl.href = '#';
      linkEl.setAttribute('aria-disabled', 'true');
      linkEl.style.cursor = 'default';
    }

    if (caseEl) caseEl.href = '/projekte/' + project.slug + '.html';

    imgEl.src = project.screenshot;
    if (project.screenshot_2x) {
      imgEl.srcset = `${project.screenshot} 1x, ${project.screenshot_2x} 2x`;
    }
    imgEl.alt = `${project.title} — ${project.tagline_en || ''}`;

    statusEl.dataset.status = project.status;
    const labels = STATUS_LABELS[project.status] || { en: project.status, de: project.status };
    statusEl.innerHTML = `<span data-lang-en>${labels.en}</span><span data-lang-de>${labels.de}</span>`;

    yearEl.textContent = String(project.year || '');
    tagPrimaryEl.textContent = (project.tags && project.tags[0]) || '';

    titleEl.textContent = project.title;

    if (project.tagline_en || project.tagline_de) {
      taglineEl.innerHTML = `
        <span data-lang-en>${project.tagline_en || ''}</span>
        <span data-lang-de>${project.tagline_de || project.tagline_en || ''}</span>
      `;
    } else {
      taglineEl.textContent = '';
    }

    tagsEl.innerHTML = '';
    (project.tags || []).slice(0, 5).forEach((t) => {
      const li = document.createElement('li');
      li.textContent = t;
      tagsEl.appendChild(li);
    });

    // Insert custom SVG mark at start of card-body
    if (project.mark && bodyEl) {
      const svgNS = 'http://www.w3.org/2000/svg';
      const svg = document.createElementNS(svgNS, 'svg');
      svg.classList.add('card-mark');
      svg.setAttribute('viewBox', '0 0 24 24');
      svg.setAttribute('aria-hidden', 'true');
      svg.setAttribute('focusable', 'false');
      const use = document.createElementNS(svgNS, 'use');
      use.setAttribute('href', '#mark-' + project.mark);
      svg.appendChild(use);
      bodyEl.insertBefore(svg, bodyEl.firstChild);
    }

    return node;
  }

  function renderError(msg) {
    if (LOADING) {
      LOADING.innerHTML = `<span style="color:var(--status-err)">${msg}</span>`;
    }
  }

  function animateMarks() {
    if ('IntersectionObserver' in window) {
      const mObs = new IntersectionObserver((entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add('is-drawn');
            mObs.unobserve(e.target);
          }
        });
      }, { threshold: 0.4 });
      TRACK.querySelectorAll('.card-mark').forEach((m) => mObs.observe(m));
    } else {
      TRACK.querySelectorAll('.card-mark').forEach((m) => m.classList.add('is-drawn'));
    }
  }

  function announce(count, error) {
    // Отметка переживает событие. Событие могло уйти раньше, чем на него
    // подписались: карточки теперь готовы сразу, а не после загрузки данных.
    window.AIS = window.AIS || {};
    window.AIS.projectsReady = !error;
    document.dispatchEvent(new CustomEvent('ais:projects-rendered', {
      detail: error ? { count: 0, error: error } : { count: count },
    }));
  }

  // Обычный путь: карточки уже в странице. Ни запроса, ни перерисовки,
  // ни пересчёта вёрстки — только оживление и сообщение остальным скриптам.
  if (STATIC) {
    if (LOADING) LOADING.remove();
    animateMarks();
    announce(TRACK.querySelectorAll('.card').length);
    return;
  }

  // Запасной путь: карточек в разметке нет. Такое бывает, если страницу
  // собрали в обход сборщика. Тогда рисуем сами, как раньше.
  fetch('/data/projects.json', { cache: 'no-cache' })
    .then((r) => {
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return r.json();
    })
    .then((projects) => {
      const list = Array.isArray(projects) ? projects : (projects.projects || []);
      const visible = list
        .filter((p) => p && p.status !== 'archived')
        .sort((a, b) => (a.order || 0) - (b.order || 0));
      if (LOADING) LOADING.remove();
      const frag = document.createDocumentFragment();
      visible.forEach((p, i) => frag.appendChild(renderCard(p, i, visible.length)));
      TRACK.appendChild(frag);
      animateMarks();
      announce(visible.length);
    })
    .catch((err) => {
      console.error('[projects.js] failed to load projects.json:', err);
      renderError('Could not load projects. Check data/projects.json.');
      announce(0, err.message);
    });
})();


/* ── form ── */
/* ─────────────────────────────────────────────────────────────
   AIS.152 — form.js
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
      _subject: `[AIS.152] New project inquiry from ${data.name}`,
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
      from_name: 'AIS.152 Contact Form',
      subject: `[AIS.152] New project inquiry from ${data.name}`,
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
        "Couldn't send the form. Use one of the channels below.",
        'Formular konnte nicht gesendet werden. Bitte unten einen Kanal wählen.'
      ));
      // PX-008: show graceful fallback (mailto + WhatsApp + Telegram) instead of plain-text email
      const fb = document.getElementById('form-fallback');
      if (fb) fb.hidden = false;
    } finally {
      setLoading(false);
    }
  });
})();


/* ── whatsapp ── */
/* ─────────────────────────────────────────────────────────────
   AIS.152 — whatsapp.js
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


/* ── main ── */
/* ─────────────────────────────────────────────────────────────
   AIS.152 — main.js
   Entry point. Initializes Lenis + GSAP + ScrollTrigger,
   wires up scroll progress, magnetic buttons, counters,
   header behavior, mobile menu, and reveal timelines.
   ───────────────────────────────────────────────────────────── */

(() => {
  'use strict';

  const REDUCED_MOTION = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const IS_MOBILE = matchMedia('(max-width: 1024px)').matches;
  // PX-013: distinct touch-small breakpoint — keeps iPad landscape on desktop pin-scroll
  // while routing phones to native CSS scroll-snap carousel (no GSAP pin).
  const IS_TOUCH_SMALL = matchMedia('(max-width: 768px)').matches;

  // ──────────────── SAFE LIBRARY DETECTION ────────────────
  const hasLenis = typeof window.Lenis === 'function';
  const hasGSAP  = typeof window.gsap === 'object';
  const hasST    = hasGSAP && typeof window.ScrollTrigger !== 'undefined';

  if (hasGSAP && hasST) {
    gsap.registerPlugin(ScrollTrigger);
  }

  // ──────────────── LENIS SMOOTH SCROLL ────────────────
  let lenis = null;
  if (hasLenis && !REDUCED_MOTION) {
    lenis = new Lenis({
      duration: 0.85,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true,
      wheelMultiplier: 1,
      touchMultiplier: 1.5,
    });
    // Привод ОДИН. До 19.08.2026 lenis.raf() вызывался дважды за кадр:
    // собственным requestAnimationFrame и тикером GSAP, с разными часами
    // и разным шагом. Пока анимации были декоративными, это давало едва
    // заметную неровность сглаживания. Для анимации, привязанной к прокрутке,
    // это смертельно: положение прокрутки — вход анимации, и оно обновлялось
    // дважды с расхождением. Нашёл агент при замере отзывчивости, 19.08.2026.
    if (hasST) {
      // Тикер GSAP — единственный источник времени. ScrollTrigger и Lenis
      // идут от одних часов, расхождения нет по построению.
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add((time) => { lenis.raf(time * 1000); });
      gsap.ticker.lagSmoothing(0);
    } else {
      // GSAP не загрузился (блокировщик, сбой CDN) — Lenis крутится сам.
      const raf = (time) => { lenis.raf(time); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
    }
  }

  // ──────────────── SMOOTH ANCHOR CLICKS ────────────────
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener('click', (e) => {
      const id = a.getAttribute('href');
      if (!id || id === '#') return;
      const tgt = document.querySelector(id);
      if (!tgt) return;
      e.preventDefault();
      if (lenis) {
        lenis.scrollTo(tgt, { offset: -64, duration: 1.2 });
      } else {
        tgt.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
      const burger = document.getElementById('nav-burger');
      const navMobile = document.getElementById('nav-mobile');
      if (burger && navMobile && burger.getAttribute('aria-expanded') === 'true') {
        burger.setAttribute('aria-expanded', 'false');
        navMobile.classList.remove('is-open');
        navMobile.setAttribute('aria-hidden', 'true');
      }
    });
  });

  // ──────────────── HEADER SCROLL STATE ────────────────
  const header = document.getElementById('header');
  if (header) {
    const onScroll = () => {
      if (window.scrollY > 16) header.classList.add('is-scrolled');
      else header.classList.remove('is-scrolled');
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // ──────────────── SCROLL PROGRESS BAR ────────────────
  const sp = document.getElementById('scroll-progress');
  if (sp) {
    const updateProgress = () => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      const p = max > 0 ? window.scrollY / max : 0;
      sp.style.setProperty('--p', p.toFixed(4));
    };
    window.addEventListener('scroll', updateProgress, { passive: true });
    window.addEventListener('resize', updateProgress);
    updateProgress();
  }

  // ──────────────── MOBILE MENU ────────────────
  const burger = document.getElementById('nav-burger');
  const navMobile = document.getElementById('nav-mobile');
  if (burger && navMobile) {
    burger.addEventListener('click', () => {
      const expanded = burger.getAttribute('aria-expanded') === 'true';
      burger.setAttribute('aria-expanded', String(!expanded));
      navMobile.classList.toggle('is-open', !expanded);
      navMobile.setAttribute('aria-hidden', String(expanded));
    });
  }

  // ──────────────── MAGNETIC BUTTONS ────────────────
  if (!IS_MOBILE && !REDUCED_MOTION) {
    document.querySelectorAll('[data-magnetic]').forEach((el) => {
      const strength = 0.25;
      const rect = () => el.getBoundingClientRect();
      el.addEventListener('mousemove', (e) => {
        const r = rect();
        const x = e.clientX - r.left - r.width / 2;
        const y = e.clientY - r.top - r.height / 2;
        if (hasGSAP) {
          gsap.to(el, { x: x * strength, y: y * strength, duration: 0.4, ease: 'power3.out' });
        } else {
          el.style.transform = `translate(${x * strength}px, ${y * strength}px)`;
        }
      });
      el.addEventListener('mouseleave', () => {
        if (hasGSAP) {
          gsap.to(el, { x: 0, y: 0, duration: 0.5, ease: 'elastic.out(1, 0.4)' });
        } else {
          el.style.transform = '';
        }
      });
    });
  }

  // ──────────────── MARQUEE INFINITE LOOP (PX-008) ────────────────
  // CSS keyframe animates translateX(0 → -50%); requires the track content to be
  // doubled so the second half slides into the original's position seamlessly.
  // Skip on reduced-motion (motion.css already disables the animation there).
  const marqueeTrack = document.getElementById('marquee-track');
  if (marqueeTrack && !REDUCED_MOTION) {
    const originals = Array.from(marqueeTrack.children);
    originals.forEach((node) => {
      const c = node.cloneNode(true);
      c.setAttribute('aria-hidden', 'true');
      marqueeTrack.appendChild(c);
    });
    if (hasGSAP && hasST) {
      requestAnimationFrame(() => ScrollTrigger.refresh());
    }
  }

  // ──────────────── COUNTERS ────────────────
  const counters = document.querySelectorAll('.counter');
  const animateCounter = (el) => {
    const target = parseInt(el.dataset.target, 10) || 0;
    const dur = 1400;
    const start = performance.now();
    const easeOutCubic = (t) => 1 - Math.pow(1 - t, 3);
    const tick = (now) => {
      const t = Math.min(1, (now - start) / dur);
      el.textContent = Math.round(target * easeOutCubic(t));
      if (t < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  if ('IntersectionObserver' in window) {
    const cObs = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          cObs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.4 });
    counters.forEach((c) => cObs.observe(c));
  } else {
    counters.forEach(animateCounter);
  }

  // ──────────────── SPLIT TEXT (manual, no plugin) ────────────────
  const splitTitle = document.querySelector('[data-split]');
  if (splitTitle && !REDUCED_MOTION) {
    const lines = splitTitle.querySelectorAll('.hero-title-line');
    lines.forEach((line) => {
      const text = line.cloneNode(true);
      const wrapWord = (node) => {
        const walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT, null);
        const textNodes = [];
        let n;
        while ((n = walker.nextNode())) textNodes.push(n);
        textNodes.forEach((tn) => {
          const frag = document.createDocumentFragment();
          tn.textContent.split(/(\s+)/).forEach((part) => {
            if (/^\s+$/.test(part)) {
              frag.appendChild(document.createTextNode(part));
            } else if (part.length) {
              const word = document.createElement('span');
              word.style.display = 'inline-block';
              word.style.overflow = 'hidden';
              const inner = document.createElement('span');
              inner.className = 'split-char';
              inner.textContent = part;
              word.appendChild(inner);
              frag.appendChild(word);
            }
          });
          tn.parentNode.replaceChild(frag, tn);
        });
      };
      wrapWord(line);
    });
    splitTitle.style.visibility = 'visible';
  } else if (splitTitle) {
    splitTitle.style.visibility = 'visible';
  }

  // ──────────────── GSAP REVEALS ────────────────
  if (hasGSAP && hasST && !REDUCED_MOTION) {
    // Hero stagger
    const splitChars = document.querySelectorAll('.hero-title .split-char');
    if (splitChars.length) {
      gsap.to(splitChars, {
        y: 0, opacity: 1,
        duration: 1, ease: 'power3.out',
        stagger: 0.025, delay: 0.1,
      });
    }

    // Hero supplementary
    gsap.from('.hero-status', { y: 12, opacity: 0, duration: 0.8, ease: 'power2.out', delay: 0.05 });
    gsap.from('.hero-lead',   { y: 16, opacity: 0, duration: 0.9, ease: 'power2.out', delay: 0.4 });
    gsap.from('.hero-actions',{ y: 16, opacity: 0, duration: 0.9, ease: 'power2.out', delay: 0.55 });
    gsap.from('.hero-meta-item', { y: 12, opacity: 0, duration: 0.7, ease: 'power2.out', delay: 0.7, stagger: 0.06 });

    // Section heads
    gsap.utils.toArray('.section-head').forEach((head) => {
      gsap.from(head.children, {
        y: 30, opacity: 0,
        duration: 0.9, ease: 'power3.out',
        stagger: 0.08,
        scrollTrigger: { trigger: head, start: 'top 85%', toggleActions: 'play none none none' },
      });
    });

    // Stats grid
    gsap.utils.toArray('.stat').forEach((s, i) => {
      gsap.from(s, {
        y: 30, opacity: 0,
        duration: 0.7, ease: 'power3.out',
        delay: i * 0.06,
        scrollTrigger: { trigger: s, start: 'top 90%', toggleActions: 'play none none none' },
      });
    });

    // Services
    gsap.utils.toArray('.service').forEach((s, i) => {
      gsap.from(s, {
        y: 40, opacity: 0,
        duration: 0.8, ease: 'power3.out',
        delay: i * 0.08,
        scrollTrigger: { trigger: s, start: 'top 88%', toggleActions: 'play none none none' },
      });
    });

    // Process steps
    gsap.utils.toArray('.process-step').forEach((s) => {
      gsap.from(s, {
        x: -24, opacity: 0,
        duration: 0.7, ease: 'power3.out',
        scrollTrigger: { trigger: s, start: 'top 88%', toggleActions: 'play none none none' },
      });
    });

    // About
    gsap.utils.toArray('.about-text > *').forEach((p, i) => {
      gsap.from(p, {
        y: 24, opacity: 0,
        duration: 0.8, ease: 'power3.out',
        delay: i * 0.06,
        scrollTrigger: { trigger: p, start: 'top 90%', toggleActions: 'play none none none' },
      });
    });

    // Form
    gsap.utils.toArray('.form-row').forEach((row, i) => {
      gsap.from(row, {
        y: 16, opacity: 0,
        duration: 0.7, ease: 'power3.out',
        delay: i * 0.05,
        scrollTrigger: { trigger: row, start: 'top 92%', toggleActions: 'play none none none' },
      });
    });
  }

  // ──────────────── EXPOSE FOR projects.js ────────────────
  window.AIS = window.AIS || {};
  window.AIS.lenis = lenis;
  window.AIS.hasGSAP = hasGSAP;
  window.AIS.hasST = hasST;
  window.AIS.REDUCED_MOTION = REDUCED_MOTION;
  window.AIS.IS_MOBILE = IS_MOBILE;

  // ──────────────── HORIZONTAL WORK SCROLL ────────────────
  // Initialized inside projects.js after cards are rendered (event-based)
  document.addEventListener('ais:projects-rendered', initWork);

  // Карточки собираются на этапе сборки и готовы ещё до того, как этот файл
  // начал выполняться, — значит событие могло пройти без слушателя. Смотрим
  // на отметку и на саму разметку и заводим карусель сами.
  if (window.AIS && window.AIS.projectsReady) {
    initWork();
  } else {
    const t0 = document.getElementById('work-track');
    if (t0 && t0.querySelectorAll('.card').length) initWork();
  }

  // PX-014: раньше вся карусель жила внутри initWorkHorizontal() за проверкой
  // «есть GSAP и не просили меньше анимации». Когда GSAP не загружался
  // (блокировщик, сбой CDN, офлайн), выход происходил ДО всего: карточки
  // оставались обрезанным рядом, который нечем прокрутить, а «/ NN» держал
  // заглушку 09, зашитую в index.html ещё при девяти проектах.
  // Воспроизведено в headless Chrome блокировкой cdnjs: gsap undefined,
  // total "09", ноль ScrollTrigger'ов. Теперь два правила: общее число
  // проставляется всегда, и любой путь без закрепления всё равно листается.
  function initWork() {
    setWorkTotal();
    if (IS_TOUCH_SMALL) return initWorkMobileSnap();
    if (!hasGSAP || !hasST || REDUCED_MOTION) return initWorkNativeScroll();
    return initWorkHorizontal();
  }

  function setWorkTotal() {
    const track = document.getElementById('work-track');
    const tot = document.getElementById('work-progress-total');
    if (!track || !tot) return;
    const n = track.querySelectorAll('.card').length;
    if (n) tot.textContent = String(n).padStart(2, '0');
  }

  // Нативная горизонтальная прокрутка: без GSAP, без анимации.
  // Прокрутку делает пользователь, это не анимация, поэтому режиму
  // «меньше анимации» она не противоречит. Противоречил как раз отказ
  // прокручиваться вообще.
  function initWorkNativeScroll() {
    const pin = document.getElementById('work-pin');
    const track = document.getElementById('work-track');
    if (!pin || !track) return;
    const cards = Array.from(track.querySelectorAll('.card'));
    if (!cards.length) return;

    pin.classList.add('is-native');
    track.classList.add('is-native');
    track.tabIndex = 0;
    track.setAttribute('aria-label', 'Selected work');

    // Колесо над лентой листает её вбок. Фаза перехвата и остановка всплытия,
    // иначе Lenis прокрутит страницу под ней.
    track.addEventListener('wheel', (e) => {
      const delta = Math.abs(e.deltaY) > Math.abs(e.deltaX) ? e.deltaY : e.deltaX;
      if (!delta) return;
      const max = track.scrollWidth - track.clientWidth;
      if ((track.scrollLeft <= 0 && delta < 0) || (track.scrollLeft >= max - 1 && delta > 0)) return;
      e.preventDefault();
      e.stopPropagation();
      track.scrollLeft += delta;
    }, { passive: false, capture: true });

    trackCounterByVisibility(track, cards);
  }

  // Общий для нативной прокрутки и мобильного пути: счётчик следует за той
  // карточкой, которой видно больше всего.
  function trackCounterByVisibility(track, cards) {
    const cur = document.getElementById('work-progress-current');
    if (!cur || !('IntersectionObserver' in window)) return;
    const obs = new IntersectionObserver((entries) => {
      let best = null;
      entries.forEach((e) => {
        if (e.isIntersecting && (!best || e.intersectionRatio > best.intersectionRatio)) best = e;
      });
      if (best) {
        const idx = cards.indexOf(best.target) + 1;
        if (idx > 0) cur.textContent = String(idx).padStart(2, '0');
      }
    }, { root: track, threshold: [0.5, 0.75, 1.0] });
    cards.forEach((c) => obs.observe(c));
  }

  function initWorkHorizontal() {
    if (!hasGSAP || !hasST || REDUCED_MOTION) return;
    // PX-013: on touch-small viewports the pin freezes the page (no wheel events to
    // drive scrub, touch consumed by pin without advancing tween). Route to native
    // CSS scroll-snap path. iPad landscape (>768px) keeps the desktop pin experience.
    // Note: Lenis stays active on all devices — with smoothTouch=off (default) it's
    // dormant on touch and only handles wheel + lenis.scrollTo() for anchor clicks.
    // Disabling Lenis would break smooth-anchor and gain nothing. (Landa WARN-3)
    // Known limitation: desktop→mobile resize in the same session does NOT re-route
    // (IS_TOUCH_SMALL is evaluated once at load). Reload needed. (Landa WARN-2)
    if (IS_TOUCH_SMALL) return initWorkMobileSnap();

    const pin = document.getElementById('work-pin');
    const track = document.getElementById('work-track');
    const fill = document.getElementById('work-progress-fill');
    const cur = document.getElementById('work-progress-current');
    const tot = document.getElementById('work-progress-total');
    if (!pin || !track) return;

    const cards = track.querySelectorAll('.card');
    if (!cards.length) return;
    const total = cards.length;
    if (tot) tot.textContent = String(total).padStart(2, '0');

    // distance to scroll horizontally
    const calc = () => track.scrollWidth - window.innerWidth + 64;

    const tween = gsap.to(track, {
      x: () => -calc(),
      ease: 'none',
      scrollTrigger: {
        trigger: pin,
        start: 'top top',
        end: () => `+=${calc()}`,
        scrub: 0.6,
        pin: true,
        anticipatePin: 1,
        invalidateOnRefresh: true,
        onUpdate: (st) => {
          if (fill) fill.style.width = (st.progress * 100).toFixed(1) + '%';
          if (cur) {
            const idx = Math.min(total, Math.floor(st.progress * total) + 1);
            cur.textContent = String(idx).padStart(2, '0');
          }
        },
      },
    });

    // Пересчёт закреплений — с задержкой и только при смене ШИРИНЫ.
    //
    // До 19.08.2026 здесь стоял голый ScrollTrigger.refresh() на каждое
    // событие resize. На телефоне адресная строка при прокрутке меняет высоту
    // окна и порождает поток таких событий — каждое запускало полный пересчёт
    // всех закреплений. Пока закрепление было одно, это терпелось. Со сценами
    // персонажа их станет семь, и страница начнёт заикаться именно там, где
    // человек её листает. Нашёл агент при разборе конфликтов, 19.08.2026.
    //
    // Высота окна меняется от адресной строки и клавиатуры, ширина — только
    // от настоящего изменения размера или поворота. Считаем по ширине.
    let lastWidth = window.innerWidth;
    let resizeTimer = null;
    window.addEventListener('resize', () => {
      if (window.innerWidth === lastWidth) return;
      lastWidth = window.innerWidth;
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => ScrollTrigger.refresh(), 200);
    });
  }

  // PX-013: mobile path — native horizontal scroll-snap, no pin. Repurposes the
  // .work-progress-current "NN" counter via IntersectionObserver on cards.
  // .work-progress-track is hidden via CSS (pin-bound bar makes no sense without pin).
  // The total "/ NN" already comes from projects.js render (no change needed).
  function initWorkMobileSnap() {
    const track = document.getElementById('work-track');
    if (!track) return;
    const cards = Array.from(track.querySelectorAll('.card'));
    if (!cards.length) return;
    trackCounterByVisibility(track, cards);
  }

  // ──────────────── VARIABLE FONT — HERO H1 SCROLL AXIS ────────────────
  // As the user scrolls the hero out of view, the H1 letters thicken
  // and condense slightly. Subtle but signature.
  if (hasGSAP && hasST && !REDUCED_MOTION) {
    const heroH1 = document.querySelector('.hero-title');
    if (heroH1) {
      // PX-007: removed wdth axis from scroll — width changes per character were
      // causing layout reflow on every scroll frame (visible jitter on H1 next to
      // the terminal panel). wght-only axis is composite-friendly and visually
      // sufficient (text gets bolder as the hero scrolls out).
      const obj = { wght: 620 };
      const apply = () => {
        heroH1.style.fontVariationSettings = `"wght" ${obj.wght.toFixed(0)}`;
      };
      ScrollTrigger.create({
        trigger: '.hero',
        start: 'top top',
        end: 'bottom 30%',
        scrub: 0.4,
        onUpdate: (st) => {
          obj.wght = 620 + st.progress * 200;   // 620 → 820
          apply();
        },
      });
    }
  }

  // ──────────────── VARIABLE FONT — HOVER PULSE ────────────────
  // PX-007: dropped wdth from hover (was 88) — same reflow reason as scroll axis above.
  document.querySelectorAll('[data-vfont-hover]').forEach((el) => {
    el.addEventListener('mouseenter', () => {
      el.style.fontVariationSettings = `"wght" 740`;
    });
    el.addEventListener('mouseleave', () => {
      el.style.fontVariationSettings = '';
    });
  });

  // ──────────────── DEV CONSOLE BANNER ────────────────
  if (typeof console !== 'undefined' && console.log) {
    console.log('%cAIS.152','color:#FF6A3C;font:700 14px "JetBrains Mono", monospace');
    console.log('%cBuilt with vanilla HTML + GSAP. No frameworks. No trackers.','color:#7DC4FF;font:11px monospace');
  }
})();
