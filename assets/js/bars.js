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

  // Барс есть везде — решение CEO. Различается способ.
  //
  //   широкий экран  — номер кадра задаёт прокрутка
  //   телефон        — ролик проигрывается сам, когда сцена входит в вид
  //   «без движения» — неподвижный кадр, ролики не грузятся вовсе
  //
  // Перемотка по прокрутке в Safari на iPhone до сих пор не проверена
  // на живом устройстве, а проигрывание без звука там работает годами.
  // Поэтому на телефоне не перемотка, а проигрывание: персонаж на месте,
  // непроверенное поведение не используется.
  const wide = window.matchMedia('(min-width: 1024px)');
  const calm = window.matchMedia('(prefers-reduced-motion: reduce)');

  const clips = Array.from(layer.querySelectorAll('.bars-clip'));
  const stills = Array.from(layer.querySelectorAll('.bars-still'));
  if (clips.length !== 4 || stills.length !== 4) return;

  const mode = calm.matches ? 'still' : (wide.matches ? 'scrub' : 'play');

  if (mode === 'still') {
    // Ролики не нужны: ни один кадр не сменится. Снимаем источник, чтобы
    // человек, попросивший убрать движение, не платил за него трафиком.
    clips.forEach((v) => { v.removeAttribute('src'); v.load(); });
  }

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
    stills.forEach((img, i) => {
      if (i === index) img.setAttribute('data-on', '');
      else img.removeAttribute('data-on');
    });

    if (mode === 'play') {
      // Цикл бега зациклен, остальные проигрываются один раз и замирают
      // на последнем кадре — он же стартовый кадр следующей сцены.
      clips.forEach((v, i) => {
        if (i !== index) { v.pause(); return; }
        v.loop = (i === 1);
        v.currentTime = 0;
        const p = v.play();
        // Отказ в проигрывании — не поломка: остаётся постер, то есть
        // неподвижный барс. Ронять на этом сцену нельзя.
        if (p && p.catch) p.catch(() => {});
      });
    }

    shown = index;
  }

  // Перемотка ставится только когда ролик к ней готов. До готовности
  // присвоение currentTime молча игнорируется — и кадр не меняется,
  // хотя страница уже уехала.
  function seek(video, fraction) {
    if (mode !== 'scrub') return;
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
