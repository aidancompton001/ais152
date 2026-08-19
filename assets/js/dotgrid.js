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
