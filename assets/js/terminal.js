/* ─────────────────────────────────────────────────────────────
   AiS1.52 — terminal.js
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
        ['tcoral', '# How a project gets shipped\n\n'],
        ['tk', '## '], ['tf', '01 — Discover'], ['tp', '  '],
        ['tc', '// days 1-2'], ['tp', '\n'],
        ['tp', 'One call. We map the problem and define\n'],
        ['tp', 'success in concrete numbers. You get a\n'],
        ['tp', 'written brief by end of day 2.\n\n'],
        ['tk', '## '], ['tf', '02 — Build'], ['tp', '   '],
        ['tc', '// week 1-3'], ['tp', '\n'],
        ['tp', 'Daily commits to a private repo. You see\n'],
        ['tp', 'progress every morning. No surprises.\n\n'],
        ['tk', '## '], ['tf', '03 — Ship'], ['tp', '    '],
        ['tc', '// week 4'], ['tp', '\n'],
        ['tp', 'Production deploy with monitoring.\n'],
        ['tp', 'Custom domain. SSL. Docs for humans.\n'],
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
        ['tc', '\n# 8 projects · 2,418 commits · last deploy 4h ago'],
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
