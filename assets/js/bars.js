/* ─────────────────────────────────────────────────────────────
   AIS.152 — сцены с барсом: прокрутка задаёт номер кадра

   Ни один ролик не играет сам. Положение страницы внутри отрезка сцены
   переводится в позицию внутри ролика. Крутишь вниз — вперёд, вверх —
   назад; отдельных роликов возврата поэтому не нужно.

   Слой ни к чему не крепится. Раздел работ уже закреплён своим
   механизмом в main.js, и второй закрепляющий механизм на том же
   отрезке с ним не уживается — здесь только чтение положения.
   ───────────────────────────────────────────────────────────── */
(() => {
  'use strict';

  const layer = document.getElementById('bars-layer');
  if (!layer) return;

  // Те же две границы, что и в bars.css. Если человек попросил убрать
  // движение или пришёл с узкого экрана, слой не оживает вообще: на
  // телефоне перемотка прокруткой не проверена ни на одном живом Safari.
  const wide = window.matchMedia('(min-width: 1024px)');
  const calm = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (!wide.matches || calm.matches) return;

  const clips = Array.from(layer.querySelectorAll('.bars-clip'));
  if (clips.length !== 4) return;

  // Отрезки прокрутки из раскадровки, приведённые к долям своего этапа.
  // Этап A — от начала первого экрана до конца услуг, этап B — контакт.
  //   ролик 1: 0–20 %  первый экран и выход на дорожку
  //   ролик 2: 20–58 % проекты, зациклен
  //   ролик 3: 58–90 % услуги
  // 90 % — конец этапа A, поэтому доли считаются от 0,90.
  const STAGE_A = [
    { clip: 0, from: 0.00 / 0.90, to: 0.20 / 0.90 },
    { clip: 1, from: 0.20 / 0.90, to: 0.58 / 0.90 },
    { clip: 2, from: 0.58 / 0.90, to: 1.00 },
  ];

  const hero = document.getElementById('top');
  const services = document.getElementById('services');
  const contact = document.getElementById('contact');
  if (!hero || !services || !contact) return;

  const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);

  // Границы этапов считаются заново после каждого пересчёта закреплений:
  // закрепление раздела работ добавляет к странице переменную длину,
  // посчитанную из ширины ленты, и она меняется от ширины окна.
  let stageA = null;
  let stageB = null;

  function measure() {
    const page = window.scrollY || window.pageYOffset;
    const box = (el) => {
      const r = el.getBoundingClientRect();
      return { top: r.top + page, bottom: r.bottom + page };
    };
    const h = box(hero);
    const s = box(services);
    const c = box(contact);
    const vh = window.innerHeight;
    // Конец этапа A — не низ услуг минус целый экран: при таком запасе
    // последняя треть третьего ролика не проигрывалась никогда, и поза
    // удержания, на которой строится стык со сценой контакта, на экран
    // не попадала. Проверено в браузере: ролик доходил до 3,10 из 4,04.
    stageA = { start: h.top, end: Math.max(h.top + 1, s.bottom - vh * 0.15) };
    stageB = { start: c.top - vh * 0.8, end: Math.max(c.top, c.bottom - vh) };
  }

  let shown = -1;

  function show(index) {
    if (index === shown) return;
    clips.forEach((v, i) => {
      if (i === index) v.setAttribute('data-on', '');
      else v.removeAttribute('data-on');
    });
    shown = index;
  }

  // Перемотка ставится только когда ролик к ней готов. До готовности
  // присвоение currentTime молча игнорируется — и кадр не меняется,
  // хотя страница уже уехала.
  function seek(video, fraction) {
    if (!video.duration || !isFinite(video.duration)) return;
    const t = clamp01(fraction) * (video.duration - 0.001);
    if (Math.abs(video.currentTime - t) > 0.008) video.currentTime = t;
  }

  function frame() {
    if (!stageA) measure();
    const y = window.scrollY || window.pageYOffset;

    // Этап B перекрывает этап A, если человек уже дошёл до контакта.
    if (y >= stageB.start) {
      const p = clamp01((y - stageB.start) / Math.max(1, stageB.end - stageB.start));
      layer.setAttribute('data-active', '');
      show(3);
      seek(clips[3], p);
      return;
    }

    if (y < stageA.start - window.innerHeight || y > stageA.end + window.innerHeight) {
      layer.removeAttribute('data-active');
      return;
    }

    const p = clamp01((y - stageA.start) / Math.max(1, stageA.end - stageA.start));
    const seg = STAGE_A.find((s) => p < s.to) || STAGE_A[STAGE_A.length - 1];
    const local = (p - seg.from) / Math.max(0.0001, seg.to - seg.from);

    layer.setAttribute('data-active', '');
    show(seg.clip);
    seek(clips[seg.clip], local);
  }

  let ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      frame();
      ticking = false;
    });
  }

  // Пересчёт границ — только при смене ШИРИНЫ окна и с задержкой.
  // Высота на телефоне меняется от адресной строки десятки раз за
  // прокрутку; на этом уже спотыкался пересчёт закреплений в main.js.
  let lastWidth = window.innerWidth;
  let timer = null;
  window.addEventListener('resize', () => {
    if (window.innerWidth === lastWidth) return;
    lastWidth = window.innerWidth;
    clearTimeout(timer);
    timer = setTimeout(() => { measure(); frame(); }, 200);
  });

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('load', () => { measure(); frame(); });

  // Закрепление раздела работ пересчитывает длину страницы уже после
  // загрузки — границы этапов надо снять после него, иначе весь отрезок
  // проектов посчитается по старой длине.
  if (window.ScrollTrigger) {
    window.ScrollTrigger.addEventListener('refresh', () => { measure(); frame(); });
  }

  clips.forEach((v) => {
    v.addEventListener('loadedmetadata', () => { measure(); frame(); }, { once: true });
  });

  measure();
  frame();
})();
