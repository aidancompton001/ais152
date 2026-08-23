/* ─────────────────────────────────────────────────────────────
   AIS.152 — выход из ленты работ и возврат наверх

   Зачем. Раздел работ листается вбок колесом, пока указатель над лентой.
   Человек, который этого не понял или не захотел листать пятнадцать
   карточек, должен иметь очевидный способ уйти дальше по странице —
   не догадываясь, что мышь надо увести в сторону.

   Две кнопки, обе справа, обе не перекрывают друг друга и кнопку WhatsApp:

     «дальше»   видна, пока раздел работ на экране; уводит под него
     «наверх»   видна в нижней трети страницы; возвращает к началу

   Одна кнопка за раз. Язык берётся из <html lang>: вторая языковая версия
   собирается отдельно, и лишних узлов в ней быть не должно.

   Узлы собираются методами DOM, а не разметкой строкой: строковая сборка
   на странице, где рядом лежат данные проектов, — привычка, которая рано
   или поздно приводит к вставке чужого текста как разметки.
   ───────────────────────────────────────────────────────────── */
(() => {
  'use strict';

  const work = document.getElementById('work');
  if (!work) return;

  const de = (document.documentElement.lang || 'de').toLowerCase().startsWith('de');
  const T = de
    ? { start: 'Scrollen', startFull: 'Nach unten scrollen',
        next: 'Weiter', nextFull: 'Weiter zu den Leistungen',
        top: 'Nach oben', topFull: 'Zum Seitenanfang' }
    : { start: 'Scroll', startFull: 'Scroll down',
        next: 'Skip', nextFull: 'Skip the projects',
        top: 'Top', topFull: 'Back to top' };

  const SVG = 'http://www.w3.org/2000/svg';
  const PATH_DOWN = 'M8 2v11M3.5 8.5 8 13l4.5-4.5';
  const PATH_UP = 'M8 14V3M3.5 7.5 8 3l4.5 4.5';

  function arrow(d) {
    const svg = document.createElementNS(SVG, 'svg');
    svg.setAttribute('viewBox', '0 0 16 16');
    svg.setAttribute('width', '14');
    svg.setAttribute('height', '14');
    svg.setAttribute('fill', 'none');
    svg.setAttribute('aria-hidden', 'true');
    const path = document.createElementNS(SVG, 'path');
    path.setAttribute('d', d);
    path.setAttribute('stroke', 'currentColor');
    path.setAttribute('stroke-width', '1.6');
    path.setAttribute('stroke-linecap', 'square');
    svg.appendChild(path);
    return svg;
  }

  function make(kind, label, full, d) {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'navhelp navhelp-' + kind;
    b.setAttribute('aria-label', full);
    b.title = full;
    b.appendChild(arrow(d));
    const span = document.createElement('span');
    span.className = 'navhelp-text';
    span.textContent = label;
    b.appendChild(span);
    document.body.appendChild(b);
    return b;
  }

  const start = make('start', T.start, T.startFull, PATH_DOWN);
  const next = make('next', T.next, T.nextFull, PATH_DOWN);
  const top = make('top', T.top, T.topFull, PATH_UP);

  // Прокрутка идёт через Lenis, если он есть: иначе плавная прокрутка
  // браузера и Lenis тянут страницу одновременно и дерутся за неё.
  function goTo(target) {
    const lenis = window.AIS && window.AIS.lenis;
    if (lenis && typeof lenis.scrollTo === 'function') {
      lenis.scrollTo(target, { offset: -72 });
    } else if (typeof target === 'number') {
      window.scrollTo({ top: target, behavior: 'smooth' });
    } else {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    // Пересчёт после собственного перехода: плавная прокрутка двигает
    // страницу своим циклом, и обычное событие прокрутки до слушателя в
    // этот момент не доходит. Поймано в браузере — кнопка оставалась
    // включённой после нажатия.
    setTimeout(update, 120);
    setTimeout(update, 900);
  }

  next.addEventListener('click', () => {
    // Следующий за работами раздел, а не жёстко «услуги»: разделы уже
    // дважды переставляли, и жёсткая ссылка переживёт это молча.
    let el = work.nextElementSibling;
    while (el && el.tagName !== 'SECTION') el = el.nextElementSibling;
    goTo(el || (work.getBoundingClientRect().bottom + window.scrollY));
  });

  top.addEventListener('click', () => goTo(0));

  // Подсказка в начале уводит к первому разделу под первым экраном, а не
  // на фиксированное число пикселей: высота первого экрана зависит от окна.
  start.addEventListener('click', () => {
    const hero = document.getElementById('top');
    let el = hero ? hero.nextElementSibling : null;
    while (el && el.tagName !== 'SECTION') el = el.nextElementSibling;
    goTo(el || window.innerHeight);
  });

  let ticking = false;

  function update() {
    const y = window.scrollY || window.pageYOffset;
    const vh = window.innerHeight;
    const doc = document.documentElement.scrollHeight - vh;
    const r = work.getBoundingClientRect();

    // Раздел работ занимает экран — значит застрять можно именно здесь.
    const inWork = r.top < vh * 0.6 && r.bottom > vh * 0.4;
    // Нижняя треть страницы: возвращаться к началу колесом слишком долго.
    const nearEnd = doc > 0 && y > doc * 0.66;

    // Самое начало: человек ещё не тронул страницу и не знает, что ниже
    // что-то есть. Порог маленький — подсказка уходит от первого движения.
    const atStart = y < vh * 0.25;

    start.classList.toggle('is-on', atStart);
    next.classList.toggle('is-on', !atStart && inWork && !nearEnd);
    top.classList.toggle('is-on', !atStart && nearEnd);
  }

  window.addEventListener('scroll', () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => { update(); ticking = false; });
  }, { passive: true });

  window.addEventListener('resize', update);
  update();
})();
