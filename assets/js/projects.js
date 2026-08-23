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
