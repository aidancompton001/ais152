/* ---- part 01 ---- */
/* ============================================================
   FRITZ AUTO ANKAUF — ТОЧНАЯ КОПИЯ, ЧАСТЬ 1/3
   Поведение базы и верхней зоны:
     1) .reveal — общий наблюдатель появления (им пользуются части 2 и 3;
        новые узлы можно подключить через window.fritzObserveReveal)
     2) шапка: класс .is-stuck при прокрутке
     3) выдвижное меню: открытие/закрытие, Esc, блокировка прокрутки,
        ловушка фокуса, аккордеон подпунктов
     4) мобильная панель: показывается после ухода первого экрана
     5) плавная прокрутка по якорям с поправкой на высоту шапки
   Всё уважает prefers-reduced-motion.
   ============================================================ */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 1. Reveal ---------- */
  var revealObserver = null;

  if ('IntersectionObserver' in window && !reduced) {
    revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.12 });
  }

  function observeReveal(root) {
    var scope = root || document;
    var nodes = scope.querySelectorAll('.reveal:not(.is-in)');
    for (var i = 0; i < nodes.length; i++) {
      if (revealObserver) revealObserver.observe(nodes[i]);
      else nodes[i].classList.add('is-in');
    }
  }

  /* публичная точка входа для частей 2 и 3 */
  window.fritzObserveReveal = observeReveal;
  observeReveal();

  /* ---------- 2. Шапка ---------- */
  var hd = document.querySelector('.hd');
  var ticking = false;

  function onScroll() {
    if (hd) hd.classList.toggle('is-stuck', window.pageYOffset > 8);
    toggleMobilebar();
    ticking = false;
  }

  window.addEventListener('scroll', function () {
    if (!ticking) {
      window.requestAnimationFrame(onScroll);
      ticking = true;
    }
  }, { passive: true });

  /* ---------- 3. Выдвижное меню ---------- */
  var burger = document.getElementById('burger');
  var mnav = document.getElementById('mnav');
  var mnavClose = document.getElementById('mnavClose');
  var lastFocused = null;

  function focusables() {
    if (!mnav) return [];
    return Array.prototype.filter.call(
      mnav.querySelectorAll('a[href], button:not([disabled])'),
      function (el) { return el.offsetParent !== null; }
    );
  }

  function openMenu() {
    if (!mnav || !burger) return;
    lastFocused = document.activeElement;
    mnav.hidden = false;
    /* даём браузеру кадр, чтобы сработал переход */
    window.requestAnimationFrame(function () { mnav.classList.add('is-open'); });
    burger.setAttribute('aria-expanded', 'true');
    burger.setAttribute('aria-label', 'Menü schließen');
    document.body.classList.add('is-locked');
    var f = focusables();
    if (f.length) f[0].focus();
  }

  function closeMenu() {
    if (!mnav || !burger) return;
    mnav.classList.remove('is-open');
    burger.setAttribute('aria-expanded', 'false');
    burger.setAttribute('aria-label', 'Menü öffnen');
    document.body.classList.remove('is-locked');
    window.setTimeout(function () {
      if (!mnav.classList.contains('is-open')) mnav.hidden = true;
    }, reduced ? 0 : 340);
    if (lastFocused && lastFocused.focus) lastFocused.focus();
  }

  if (burger) {
    burger.addEventListener('click', function () {
      if (burger.getAttribute('aria-expanded') === 'true') closeMenu();
      else openMenu();
    });
  }
  if (mnavClose) mnavClose.addEventListener('click', closeMenu);

  document.addEventListener('keydown', function (e) {
    if (!mnav || !mnav.classList.contains('is-open')) return;

    if (e.key === 'Escape') { closeMenu(); return; }

    if (e.key === 'Tab') {
      var f = focusables();
      if (!f.length) return;
      var first = f[0];
      var last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });

  /* аккордеон подпунктов */
  if (mnav) {
    var toggles = mnav.querySelectorAll('.mnav__toggle');
    Array.prototype.forEach.call(toggles, function (btn) {
      btn.addEventListener('click', function () {
        var item = btn.closest('.mnav__item');
        var sub = item ? item.querySelector('.mnav__sub') : null;
        if (!sub) return;
        var open = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', open ? 'false' : 'true');
        sub.style.maxHeight = open ? '0px' : sub.scrollHeight + 'px';
      });
    });

    /* клик по пункту меню закрывает панель */
    Array.prototype.forEach.call(mnav.querySelectorAll('a[href^="#"]'), function (a) {
      a.addEventListener('click', closeMenu);
    });
  }

  /* при переходе на десктоп меню закрывается принудительно */
  var wide = window.matchMedia('(min-width: 1025px)');
  var onWide = function (e) { if (e.matches) closeMenu(); };
  if (wide.addEventListener) wide.addEventListener('change', onWide);
  else if (wide.addListener) wide.addListener(onWide);

  /* ---------- 4. Мобильная панель ---------- */
  var mobilebar = document.getElementById('mobilebar');
  var hero = document.getElementById('hero');

  function toggleMobilebar() {
    if (!mobilebar) return;
    var trigger = hero ? hero.offsetHeight * 0.6 : 400;
    mobilebar.classList.toggle('is-in', window.pageYOffset > trigger);
  }
  toggleMobilebar();

  /* ---------- 5. Плавная прокрутка по якорям ---------- */
  document.addEventListener('click', function (e) {
    var link = e.target.closest ? e.target.closest('a[href^="#"]') : null;
    if (!link) return;
    var id = link.getAttribute('href');
    if (!id || id === '#' || id.length < 2) return;
    var target = document.querySelector(id);
    if (!target) return;

    e.preventDefault();
    var offset = hd ? hd.offsetHeight : 0;
    var y = target.getBoundingClientRect().top + window.pageYOffset - offset;
    window.scrollTo({ top: y < 0 ? 0 : y, behavior: reduced ? 'auto' : 'smooth' });
  });
})();

/* Zum-Anfang-Knopf: erscheint nach dem ersten Bildschirm */
(function () {
  var btn = document.querySelector('.totop');
  if (!btn) return;
  var hero = document.getElementById('hero');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  btn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
  });

  if (hero && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      btn.classList.toggle('is-on', !entries[0].isIntersecting);
    }, { rootMargin: '-40% 0px 0px 0px' }).observe(hero);
  } else {
    btn.classList.add('is-on');
  }
})();

/* ---- part 02 ---- */
/* ============================================================
   FRITZ AUTO ANKAUF — ЧАСТЬ 2 из 3
   Появление элементов средних секций при прокрутке.

   Скрипт намеренно не трогает класс .reveal — его владелец
   ЧАСТЬ 1. Если общий наблюдатель уже подключён (флаг
   window.__fritzRevealBound или атрибут data-reveal-ready на
   <html>), часть 2 не делает ничего и отдаёт анимацию ему.
   Иначе включает собственный слой .p2-anim / .is-p2-in,
   который живёт только внутри секций about/usp/steps/buy.
   ============================================================ */
(function () {
  'use strict';

  if (window.__fritzPart2Init) { return; }
  window.__fritzPart2Init = true;

  var SELECTOR = [
    '.about-photos',
    '.about-body',
    '.usp-item',
    '.steps-title',
    '.steps-extra',
    '.steps-item',
    '.buy-head',
    '.buy-card'
  ].join(',');

  function start() {
    // Часть 1 уже управляет появлением — не дублируем
    if (window.__fritzRevealBound ||
        document.documentElement.hasAttribute('data-reveal-ready')) {
      return;
    }

    var nodes = document.querySelectorAll(SELECTOR);
    if (!nodes.length) { return; }

    var reduced = window.matchMedia &&
                  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (reduced || !('IntersectionObserver' in window)) {
      // без анимации — просто показать
      return;
    }

    document.documentElement.classList.add('p2-anim');

    var io = new IntersectionObserver(function (entries) {
      for (var i = 0; i < entries.length; i++) {
        var e = entries[i];
        if (e.isIntersecting) {
          e.target.classList.add('is-p2-in');
          io.unobserve(e.target);
        }
      }
    }, { root: null, rootMargin: '0px 0px -8% 0px', threshold: 0.12 });

    for (var i = 0; i < nodes.length; i++) {
      // лёгкая лесенка внутри одной группы
      var group = nodes[i].parentNode;
      var idx = group ? Array.prototype.indexOf.call(group.children, nodes[i]) : 0;
      nodes[i].style.transitionDelay = Math.min(idx, 4) * 70 + 'ms';
      io.observe(nodes[i]);
    }

    // страховка: если через 3 с что-то не показалось — показать принудительно
    window.setTimeout(function () {
      var still = document.querySelectorAll(SELECTOR);
      for (var k = 0; k < still.length; k++) {
        var r = still[k].getBoundingClientRect();
        if (r.top < window.innerHeight && r.bottom > 0) {
          still[k].classList.add('is-p2-in');
        }
      }
    }, 3000);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start, { once: true });
  } else {
    start();
  }
})();

/* ---- part 03 ---- */
/* ============================================================
   FRITZ AUTOANKAUF — ЧАСТЬ 3/3, поведение формы

   Что делает:
   1. HTML5-валидация через Constraint Validation API. На форме
      стоит novalidate, чтобы браузерные пузыри не спорили с
      оформлением карточки — но проверяют её именно нативные
      правила (required / type=email / pattern), не самописный regex.
   2. preventDefault на submit: бэкенда у превью нет, отправлять
      некуда. Данные собираются и показываются в подтверждении.
   3. Подтверждение на немецком с повтором марки и модели.
      Пользовательский ввод попадает в DOM только через
      textContent — разметка из поля не исполняется никогда.
   4. Кнопка «Neue Anfrage» возвращает форму в исходное состояние.
   5. Honeypot `website`: заполнен — значит бот. Блокировка тихая:
      человек ничего не замечает, бот получает обычный экран
      «спасибо» и не понимает, что заявка не ушла.

   Своих зависимостей нет, глобальных имён не создаёт.
   ============================================================ */
(function () {
  'use strict';

  var form = document.getElementById('fritz-form');
  if (!form) return;

  var card     = form.closest('.form-card');
  var doneText = document.getElementById('form-done-text');
  var resetBtn = document.getElementById('form-reset');
  var hpField  = form.elements.website;
  var seite    = document.getElementById('f-seite');

  /* страница-источник заявки — чтобы в письме было видно,
     с какого городского лендинга пришёл человек */
  if (seite && !seite.value.replace(/^\/$/, '')) {
    seite.value = window.location.pathname || '/';
  }

  /* ---------- Сообщения об ошибках, по-немецки и по делу ---------- */
  var MESSAGES = {
    valueMissing: 'Bitte ausfüllen',
    typeMismatch: 'Bitte eine gültige E-Mail-Adresse eingeben',
    patternMismatch: 'Bitte im angegebenen Format eingeben',
    tooShort: 'Eingabe ist zu kurz',
    tooLong: 'Eingabe ist zu lang',
    fallback: 'Bitte Eingabe prüfen'
  };

  function messageFor(field) {
    var v = field.validity;
    if (v.valueMissing) {
      return field.type === 'checkbox'
        ? 'Ohne dein Einverständnis können wir die Anfrage nicht bearbeiten'
        : MESSAGES.valueMissing;
    }
    if (v.typeMismatch) return MESSAGES.typeMismatch;
    if (v.patternMismatch) {
      if (field.id === 'f-ez') return 'Vierstelliges Jahr, z. B. 2015';
      if (field.id === 'f-km') return 'Nur Ziffern, z. B. 145000';
      return MESSAGES.patternMismatch;
    }
    if (v.tooShort) return MESSAGES.tooShort;
    if (v.tooLong)  return MESSAGES.tooLong;
    return MESSAGES.fallback;
  }

  function errorSlot(field) {
    if (field.id === 'f-consent') return document.getElementById('e-consent');
    var wrap = field.closest('.form-field');
    return wrap ? wrap.querySelector('.form-error') : null;
  }

  function clearError(field) {
    var slot = errorSlot(field);
    if (slot) slot.textContent = '';
    field.removeAttribute('aria-invalid');
    field.removeAttribute('aria-describedby');
  }

  function showError(field) {
    var slot = errorSlot(field);
    if (slot) {
      slot.textContent = messageFor(field);
      if (slot.id) field.setAttribute('aria-describedby', slot.id);
    }
    field.setAttribute('aria-invalid', 'true');
  }

  /* ошибка снимается сразу, как только поле стало валидным —
     не заставляем человека повторно жать «отправить», чтобы это увидеть */
  Array.prototype.forEach.call(form.elements, function (field) {
    if (!field.name || field.name === 'website') return;
    var ev = field.type === 'checkbox' ? 'change' : 'input';
    field.addEventListener(ev, function () {
      if (field.checkValidity()) clearError(field);
    });
    field.addEventListener('blur', function () {
      if (field.value !== '' && !field.checkValidity()) showError(field);
    });
  });

  /* ---------- Подтверждение ---------- */
  function showConfirmation(marke, modell) {
    if (doneText) {
      /* textContent, не innerHTML: марка и модель приходят от пользователя */
      doneText.textContent =
        'Wir haben deine Anfrage zu ' + marke + ' ' + modell +
        ' erhalten und melden uns telefonisch zurück – in der Regel noch am selben Werktag. ' +
        'Halte bitte Fahrzeugschein und Kilometerstand bereit.';
    }
    if (card) card.setAttribute('data-state', 'done');
    var title = document.getElementById('form-done-title');
    if (title) {
      title.setAttribute('tabindex', '-1');
      title.focus({ preventScroll: false });
    }
  }

  /* ---------- Отправка ---------- */
  form.addEventListener('submit', function (event) {
    event.preventDefault();

    var marke  = (form.elements.marke  && form.elements.marke.value  || '').trim();
    var modell = (form.elements.modell && form.elements.modell.value || '').trim();

    /* Honeypot заполнен → бот. Ничего не проверяем, ничего не отправляем,
       показываем тот же экран благодарности. Тишина — часть защиты. */
    if (hpField && hpField.value.trim() !== '') {
      showConfirmation(marke || 'deinem Fahrzeug', modell || '');
      return;
    }

    /* нативная HTML5-валидация всех полей */
    var firstInvalid = null;
    Array.prototype.forEach.call(form.elements, function (field) {
      if (!field.name || field.name === 'website' || field.disabled) return;
      if (field.checkValidity()) {
        clearError(field);
      } else {
        showError(field);
        if (!firstInvalid) firstInvalid = field;
      }
    });

    if (firstInvalid) {
      firstInvalid.focus({ preventScroll: true });
      firstInvalid.scrollIntoView({ block: 'center', behavior: 'smooth' });
      return;
    }

    /* Отправка на server/lead.php. Экран благодарности показывается ТОЛЬКО
       после ответа сервера: подтверждение, нарисованное раньше ответа, врёт
       посетителю ровно в том случае, когда заявка не дошла. */
    var btn = form.querySelector('.form-submit');
    var btnText = btn ? btn.textContent : '';
    if (btn) { btn.disabled = true; btn.textContent = 'Wird gesendet …'; }

    var restore = function () {
      if (btn) { btn.disabled = false; btn.textContent = btnText; }
    };

    var failed = function (msg) {
      restore();
      var box = document.getElementById('e-consent');
      if (box) {
        box.textContent = msg || 'Das hat gerade nicht geklappt. Ruf uns kurz an: 01577 6466164';
        box.setAttribute('data-shown', '1');
      }
    };

    if (!window.fetch) {           /* очень старый браузер — обычный POST */
      form.submit();
      return;
    }

    fetch(form.getAttribute('action'), {
      method: 'POST',
      body: new FormData(form),
      headers: { 'Accept': 'application/json' }
    }).then(function (r) {
      return r.json().catch(function () { return { ok: r.ok }; });
    }).then(function (data) {
      if (data && data.ok) {
        restore();
        showConfirmation(marke, modell);
      } else {
        failed(data && data.error);
      }
    }).catch(function () {
      failed();
    });
  });

  /* ---------- «Neue Anfrage» ---------- */
  if (resetBtn) {
    resetBtn.addEventListener('click', function () {
      form.reset();
      Array.prototype.forEach.call(form.elements, function (field) {
        if (field.name && field.name !== 'website') clearError(field);
      });
      if (card) card.setAttribute('data-state', 'edit');
      if (doneText) doneText.textContent = '';
      var first = document.getElementById('f-name');
      if (first) first.focus();
    });
  }

})();