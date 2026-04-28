/* ─────────────────────────────────────────────────────────────
   AiS1.52 — main.js
   Entry point. Initializes Lenis + GSAP + ScrollTrigger,
   wires up scroll progress, magnetic buttons, counters,
   header behavior, mobile menu, and reveal timelines.
   ───────────────────────────────────────────────────────────── */

(() => {
  'use strict';

  const REDUCED_MOTION = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const IS_MOBILE = matchMedia('(max-width: 1024px)').matches;

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
    function raf(time) {
      lenis.raf(time);
      requestAnimationFrame(raf);
    }
    requestAnimationFrame(raf);

    if (hasST) {
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add((t) => { lenis.raf(t * 1000); });
      gsap.ticker.lagSmoothing(0);
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
  document.addEventListener('ais:projects-rendered', initWorkHorizontal);

  function initWorkHorizontal() {
    if (!hasGSAP || !hasST || REDUCED_MOTION) return;

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

    // Resize handle
    window.addEventListener('resize', () => ScrollTrigger.refresh());
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
    console.log('%cAiS 1.52','color:#FF6A3C;font:700 14px "JetBrains Mono", monospace');
    console.log('%cBuilt with vanilla HTML + GSAP. No frameworks. No trackers.','color:#7DC4FF;font:11px monospace');
  }
})();
