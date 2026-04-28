/* ─────────────────────────────────────────────────────────────
   AiS1.52 — projects.js (v2)
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

  fetch('data/projects.json', { cache: 'no-cache' })
    .then((r) => {
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return r.json();
    })
    .then((projects) => {
      if (!Array.isArray(projects)) throw new Error('projects.json must be an array');

      const visible = projects
        .filter((p) => p && p.status !== 'archived')
        .sort((a, b) => (a.order || 0) - (b.order || 0));

      if (LOADING) LOADING.remove();

      const frag = document.createDocumentFragment();
      visible.forEach((p, i) => frag.appendChild(renderCard(p, i, visible.length)));
      TRACK.appendChild(frag);

      // Animate marks in via IntersectionObserver
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

      document.dispatchEvent(new CustomEvent('ais:projects-rendered', {
        detail: { count: visible.length, projects: visible },
      }));
    })
    .catch((err) => {
      console.error('[projects.js] failed to load projects.json:', err);
      renderError('Could not load projects. Check data/projects.json.');
      document.dispatchEvent(new CustomEvent('ais:projects-rendered', {
        detail: { count: 0, error: err.message },
      }));
    });
})();
