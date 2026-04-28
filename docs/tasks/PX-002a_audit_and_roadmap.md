# PX-002a — Audit & Redesign Roadmap

**Дата:** 2026-04-27
**Статус:** P0 завершено, ожидает OK CEO для перехода в P1
**Ответственные:** #1 Viktor Neumann (lead) + #2 Lena Richter (UI) + #3 Andrei Volkov (frontend) + #14 Hans Landa (review)
**Размер:** XL
**Скиллы:** `design:user-research`, `design:design-critique`, `design:design-system`, `design:accessibility-review`, `design:ux-copy`, `design:research-synthesis`

---

## TL;DR (для CEO, 30 секунд)

Текущий `ais152.com` — 1056-строчный single-file HTML. Технически рабочий, но **не показывает уровень CEO с 9 production-проектами**. Главные дыры: Google Fonts CDN (DSGVO violation), отсутствие формы, отсутствие WhatsApp FAB, отсутствие Impressum/Datenschutz, отсутствие GSAP-уровня анимаций (только базовый IntersectionObserver), bento-cards на `<div onclick>` вместо `<a>` (объясняет жалобу «не все CTA кликаются»). Скриншоты 6 проектов — есть. URL'ы — есть. Контент-фундамент стоит, нужен переnew layer.

Редизайн = новый визуал + GSAP/ScrollTrigger pinned horizontal scroll в Selected Work + форма (FormSubmit + Web3Forms fallback) + WhatsApp FAB с DSGVO 2-click + self-hosted шрифты + data-driven `data/projects.json` (CEO добавляет проект за 30 сек). Стек **не меняется** — Static HTML/CSS/JS на GitHub Pages.

---

## Baseline Lighthouse

⏳ **TBD — измерить вручную перед стартом P1.**
CEO запускает: <https://pagespeed.web.dev/analysis?url=https%3A%2F%2Fais152.com> → присылает числа.
Ожидаемый худший показатель — Performance mobile (Google Fonts CDN + грейн SVG + cursor LERP RAF). Цели P2: Perf ≥90 mobile, A11y ≥95, BP =100, SEO ≥90.

---

## Что работает (на сегодня)

- Двуязычность EN/DE через `data-lang-en/de` атрибуты — корректна, каждый текст имеет оба span'а
- Lenis smooth scroll (CDN 1.1.14) — интегрирован, easing разумный
- IntersectionObserver scroll reveal (`.rv` + `.rv-1/2/3` cascade)
- Aurora orb backgrounds (`.orb-1..4`) с CSS animations
- Custom cursor (`.cur` + `.cur-ring`, LERP follow через requestAnimationFrame) — desktop only
- 3D card tilt на `.bento-card` (perspective + rotateX/Y on mousemove)
- Magnetic button (`#btnMag` CTA)
- Counter animation в stats (RAF + easeOutCubic)
- Scroll progress bar (`#sp` fixed top scaleX)
- Film grain (SVG feTurbulence overlay)
- `prefers-reduced-motion` обработан (строка 543)
- Все 6 проектов отрендерены с правильными URL'ами и скриншотами
- Контакты: tel/mailto/wa.me/t.me — все валидны (HTTP не проверял по решению CEO, верю что live)

## Что сломано / требует замены

| # | Проблема | Локация | Severity | План |
|---|----------|---------|----------|------|
| 1 | **Google Fonts CDN** (Outfit) | `index.html:12-14` | 🔴 CRITICAL — DSGVO violation (BGH 2022, LG München I 3 O 17493/20) | P2: self-host WOFF2 шрифты выбранного семейства, удалить preconnect+CSS link |
| 2 | **Нет контактной формы** — только `mailto:` | везде | 🔴 HIGH — CEO жалоба «форма не отправляется» = её нет | P2: FormSubmit.co + Web3Forms fallback (рецепт из EKO_OYLIS_LESSONS) |
| 3 | **Нет WhatsApp FAB** — только текстовая ссылка в footer | `index.html:1041` | 🟡 MEDIUM — CEO жалоба «WhatsApp не работает» вероятно про отсутствие плавающей кнопки | P2: sticky FAB bottom-right + 2-click DSGVO warning перед `wa.me/` |
| 4 | **Bento-cards = `<div role="link" onclick>`** | `index.html:768,809,829,849,869,889,909` | 🔴 HIGH — CEO жалоба «не все CTA кликаются»; на mobile div+onclick нестабилен; a11y фейл (не tab-focusable нативно) | P2: заменить на `<a href target="_blank" rel="noopener noreferrer">` |
| 5 | **Нет Impressum / Datenschutz** | footer | 🔴 CRITICAL — TMG §5 + DDG для DE требует обязательно | P2: создать `impressum.html` + `datenschutz.html` (заглушка с TODO для CEO) |
| 6 | **Нет cookie-banner** | — | 🟢 LOW (на сегодня нет аналитики, ОК); если CEO решит подключать analytics → блокер | P2: пока пропускаем, отдельная задача если CEO решит |
| 7 | **Buzzwords в копирайте** | `index.html:7,9,625,626,1021,1022` | 🟡 MEDIUM — запрещено P2.11 | P1/P2: переписать. «AI-powered», «Senior-level. Fast. Done right.», «Replace the staff you can't find» — на инженерный тон |
| 8 | **og:image отсутствует, нет JSON-LD, нет canonical** | head | 🟡 MEDIUM — SEO + рендер при шаринге в Slack/WA/LinkedIn | P2: создать OG image (1200×630), добавить JSON-LD `Organization` + `Person`, добавить canonical |
| 9 | **GSAP / ScrollTrigger / SplitText отсутствуют** | — | 🟡 MEDIUM — блокирует KPI протокола (pinned horizontal, character-stagger) | P2: добавить через CDN (jsdelivr) с SRI, реализовать ≥3 ST scenes + pinned + SplitText + magnetic + marquee + counter |
| 10 | **Данные проектов захардкожены в HTML** | `index.html:768-927` | 🟡 MEDIUM — CEO просил «легко добавлять проекты» | P2: вынести в `data/projects.json` + `<template id="project-card">` + vanilla JS render |
| 11 | **Lenis CDN от jsdelivr.net** | `index.html:1056` | 🟢 LOW — DSGVO grey area, можно self-host если строго | P2: оставить CDN с SRI hash, либо self-host `assets/js/lenis.min.js` (CEO решает) |
| 12 | **`html lang="en"`** при переключении на DE не меняется | — | 🟡 MEDIUM — screen reader читает DE-текст с английским произношением | P2: `langSwitch()` JS обновляет `<html lang>` |
| 13 | **Stat "Projects Delivered" data-t="8"** | `index.html:682-area` | 🟢 LOW | P1: проверить число, у CEO 9 проектов (включая текущий AiS152) — может стоит «9» |

---

## 6 проектов — финальный список (после PX-001)

| Slug | Title | URL | Screenshot | Featured | Order |
|------|-------|-----|-----------|----------|-------|
| baupreis | BauPreis AI | https://baupreis.ais152.com | `assets/baupreis-dashboard.png` | true | 1 |
| mono | MONO Men Only | — (no public URL, app store TBD) | `assets/mono-app-1.jpg` (или коллаж из mono-slide-*) | true | 2 |
| edmi | EDMI Landing | https://aidancompton001.github.io/edmi-landing/variant-d.html | `assets/edmi-landing-site.jpg` | true | 3 |
| stormguard | StormGuard Professional | https://www.stormguardprofessional.eu/ | `assets/stormguard-site.jpg` | true | 4 |
| eko-oylis | Eko-OYLIS | https://eco-oylis.info | `assets/eko-oylis-site.jpg` | false | 5 |
| rundumshaus | RundUmsHaus Littawe | https://rundumshaus-littawe.de/ | `assets/rundumshaus-site.jpg` | false | 6 |
| provenly-homes | Provenly Homes | https://aidancompton001.github.io/provenly-homes | `assets/provenly-homes-site.jpg` | false | 7 |
| studioglamour | Studio of Glamour | https://glamour.ais152.com/ | `assets/studioglamour-site.jpg` | true | 8 |

**Всего: 8 карточек.** Если CEO считает себя за 9-й проект (AiS152 сам по себе) — добавить self-card (`AiS152 Portfolio`) в About-секции, не в Selected Work.

**StudioGlamour:** URL мигрирован на custom domain `glamour.ais152.com` (per PX-001, статус «✅ Живой», CNAME настроен). Старый GitHub Pages URL `aidancompton001.github.io/studioglamour/` (404 на 2026-04-17) — устарел, не используем.

---

## Open Questions для CEO

1. **Структура:** SPA one-pager (как сейчас) или multi-page (отдельные страницы для cases, about, contact)? **Моя рекомендация — SPA one-pager**, удерживает скорость GitHub Pages и упрощает GSAP timeline.
2. **Tone of voice:** инженерный/сдержанный (Linear, Vercel) ИЛИ смелый/контрастный (gsap.com) ИЛИ редакционный/премиум (Awwwards)? — выбор повлияет на P1 (3 варианта токенов).
3. **Шрифты:** оставляем Outfit (но self-host)? Или меняем — предлагаю в P1 пары: Inter+JetBrains Mono / Geist+Geist Mono / Fraunces+Inter. Какие предпочтения?
4. **Цветовая палитра:** оставляем dark `#070810` + lime `#C8FF00` (текущее)? Или CEO готов на смену в P1?
5. **Аналитика:** подключаем (если да — нужен cookie-banner, GoatCounter / Plausible self-host лучше Cookiebot)? Если нет — экономим cookie-banner и DSGVO-сложности.
6. **Impressum / Datenschutz:** есть ли готовые тексты от юриста (Mein Drucker / Munich Chamber of Crafts) или нужны заглушки + TODO для CEO? Для DE Impressum обязателен по TMG §5 (имя+адрес+контакт+USt-IdNr или Kleinunternehmer-Hinweis).
7. **9 vs 8 проектов:** показываем 8 в Selected Work или 9 (включая self-AiS152)? Я бы 8 в Work + AiS152 как «Made by» в About.
8. **Concept-файлы (`concept-*.html`):** оставляем рядом с index.html, переносим в `archive/`, или удаляем? Per CLAUDE.md «не трогать без указания CEO».
9. **Telegram bot `assit_ais152_bot`:** оставляем в footer как 4-й контакт, убираем, или превращаем в feature (CEO «у меня есть AI-ассистент которому можно написать»)?
10. **Lighthouse цели:** Perf ≥90 / A11y ≥95 / BP =100 / SEO ≥90 — принимаем как gate перед merge?
11. **Self-host vs CDN для GSAP+Lenis:** строгий self-host (DSGVO-параноидально) или CDN+SRI (легче поддерживать)?
12. **OG image:** генерируем (1200×630, brand) или CEO даёт готовый файл?

---

## Предлагаемая структура редизайна (one-pager SPA)

```
HEADER (sticky, blur backdrop)
├── Logo "AiS 1.52"
├── Nav: Work · Process · About · Contact
└── CTA "Book a Call" + Lang toggle EN/DE

HERO (1 экран)
├── Status pill "● Available · Munich"
├── H1 (2 строки, character-stagger SplitText reveal)
├── Description (2 строки, blur-in)
├── Trust dots (3 пункта, NO buzzwords)
├── 2 CTA: primary (magnetic) → form anchor / secondary → #work
└── Marquee внизу (smooth scroll, technologies list)

SELECTED WORK (главная фишка — pinned horizontal scroll)
├── Section title (sticky на time pinned)
├── Horizontal track: 8 cards × ~80vw (или 60vw)
├── Each card = full project preview (image left, info right)
│   ├── Tag · Year
│   ├── Title (large, lime accent on hover)
│   ├── Tagline (1 строка)
│   ├── Tags (pills)
│   └── "Visit site →" (arrow magnetic on hover)
├── Progress indicator (bar внизу секции, скроллится с timeline)
└── Источник правды: data/projects.json

STATS / ABOUT (single section)
├── Counter cards: 9 projects · X years · 24/7 AI · 60-85% savings
├── Short manifest (2-3 параграфа, NO buzzwords, инженерный тон)
└── Tech stack chips

PROCESS (3-4 шага)
├── 01 Discovery → 02 Build → 03 Ship → 04 Maintain (или 3 шага если CEO предпочитает)
└── Each step: icon · title · description (no fluff)

CONTACT (форма + альтернативы)
├── Form: Name · Email · Project type select · Message · Submit
│   ├── FormSubmit.co primary
│   ├── Web3Forms fallback (auto-switch если 1-й вернул error)
│   └── States: idle/sending/success/error (aria-live="polite")
├── Alternative contacts: tel · mailto · WhatsApp (с 2-click) · Telegram
└── "Response in 24h" promise

FOOTER (4 columns)
├── Brand + tagline
├── Services (anchors)
├── Company (anchors + Impressum + Datenschutz)
├── Contact (4 channels)
└── © 2026 + Munich + lang toggle (повтор)

WHATSAPP FAB (sticky bottom-right, all sections)
├── Click → 2-click DSGVO warning popover
└── Confirm → wa.me/4915563675772
```

---

## Архитектура «легко добавлять проекты»

**Структура:**

```
data/
├── projects.json         ← источник правды
├── projects.schema.json  ← JSON Schema draft-07 для валидации
└── README.md             ← инструкция CEO «как добавить за 30 сек»
```

**Schema (объект проекта):**

```json
{
  "slug": "stormguard",
  "title": "StormGuard Professional",
  "tagline_en": "E-commerce for organic pet care",
  "tagline_de": "E-Commerce für Bio-Tierpflege",
  "year": 2026,
  "url": "https://www.stormguardprofessional.eu/",
  "status": "live",
  "tags": ["E-commerce", "Multi-language", "Static"],
  "summary_en": "Production e-commerce for premium organic pet cosmetics — 3 languages, full catalog, order system.",
  "summary_de": "Production E-Commerce für Bio-Tierpflege — 3 Sprachen, Katalog, Bestellsystem.",
  "screenshot": "assets/projects/stormguard.jpg",
  "screenshot_2x": "assets/projects/stormguard@2x.jpg",
  "featured": true,
  "order": 4
}
```

**Как CEO добавляет новый проект:**

1. Скриншот 1280×800 → `assets/projects/{slug}.jpg`, и 2560×1600 → `{slug}@2x.jpg`
2. Открыть `data/projects.json`, добавить объект
3. `git add . && git commit -m "feat: add project X" && git push`
4. GitHub Pages обновляет за ~2 минуты

**Никаких правок HTML/CSS/JS.** Vanilla JS читает JSON, клонирует `<template id="project-card-tpl">`, рендерит карточки + инициализирует ScrollTrigger horizontal scene.

---

## Performance Budget

| Метрика | Цель |
|---------|------|
| CSS (gzip) | ≤ 60 KB |
| JS (gzip, всё включая GSAP+Lenis) | ≤ 120 KB |
| Шрифты (WOFF2, total) | ≤ 200 KB (4 файла max: Regular, Medium, Bold + опционально Mono) |
| LCP (mobile, Slow 4G) | ≤ 2.5 s |
| CLS | ≤ 0.1 |
| TBT | ≤ 200 ms |
| INP | ≤ 200 ms |
| DOM nodes | ≤ 1500 |
| Total page weight (без images) | ≤ 400 KB |

---

## KPI «next-level» (минимум, измеримо)

- ✅ ≥ 3 ScrollTrigger-сцены (hero reveal, projects pin/scrub, stats counter)
- ✅ ≥ 1 pinned-section с horizontal scroll-progress (Selected Work — главная фишка)
- ✅ ≥ 1 SplitText character-stagger reveal (hero H1)
- ✅ ≥ 1 magnetic-cursor элемент (primary CTA)
- ✅ ≥ 1 smooth marquee/ticker (hero bottom — technologies)
- ✅ ≥ 1 counter с RAF (stats)
- ✅ Кастомный cursor (опционально — оставить или убрать, CEO решает в P1)

---

## Browser matrix

| Браузер | Минимум | Тестируем особо |
|---------|---------|----------------|
| Chrome | ≥ 120 | LCP, ST timeline |
| Edge | ≥ 120 | — |
| Firefox | ≥ 120 | custom cursor (известные баги pre-FF 120) |
| Safari macOS | ≥ 17 | backdrop-filter, scroll-snap |
| Safari iOS | ≥ 17 | **Lenis известная проблема** с overflow:hidden — workaround `body { overscroll-behavior: none }` |
| Chrome Android | latest | touch события, magnetic cursor disabled на mobile |

---

## Breakpoints (Tailwind стандарт)

```
640  → sm  (small phones landscape, large phones)
768  → md  (tablets portrait)
1024 → lg  (tablets landscape, small laptops)
1280 → xl  (laptops, desktops)
1536 → 2xl (large desktops)
```

Mobile-first. CSS `clamp()` для fluid typography между точками.

---

## DSGVO / GDPR pre-merge gate

Без этих 5 пунктов — **не мержим**:

1. ✅ **Self-hosted WOFF2.** Удалить `fonts.googleapis.com` + `fonts.gstatic.com`. Скачать выбранные шрифты, положить в `assets/fonts/`. Лицензии (SIL OFL / Apache 2.0) — копии в `assets/fonts/LICENSE-{name}.txt`.
2. ✅ **WhatsApp 2-click warning.** Перед `wa.me/` показываем popover: «Контакт через WhatsApp откроет сторонний сервис Meta Platforms Ireland Ltd. См. Datenschutz.» После явного клика «OK» → редирект.
3. ✅ **Impressum.** Создать `impressum.html` (TMG §5: имя, адрес Munich, контакт, опциональный USt-IdNr или Kleinunternehmer-Hinweis). Ссылка в footer.
4. ✅ **Datenschutz.** Создать `datenschutz.html` (DSGVO Art. 13: контроллер, цели обработки, основания, права). Ссылка в footer.
5. ✅ **Никакого Google Analytics / Cookiebot.** На сегодня — `<script>` с трекерами = 0. Если CEO позже захочет аналитику — отдельная задача с cookie-banner.

**Owner DSGVO-секции:** #14 Hans Landa проверяет ДО merge.

---

## Fallback-матрица

| Сбой | Резерв |
|------|--------|
| FormSubmit.co лимит 50/мес free | Web3Forms 2-й endpoint (auto-switch на error 429/500) |
| Web3Forms тоже лежит | `mailto:` link в success-state «Or write directly» |
| GitHub Pages cache (≤10 мин) | `?v={git-short-hash}` на CSS/JS |
| WhatsApp FAB на desktop без WhatsApp Web | Параллельный `tel:` link в FAB popover |
| `prefers-reduced-motion` включён | Не инициализируем Lenis + GSAP timelines, оставляем opacity-fade |
| GSAP CDN недоступен (jsdelivr down) | SRI failure → graceful: страница работает без анимаций (только базовый IntersectionObserver) |
| Lighthouse mobile <90 после P2 | Профилировать, оптимизировать images (WebP + srcset), defer GSAP до post-LCP |

---

## Запреты (повтор для команды)

❌ Менять стек (никакого Next.js/React/Vue/Svelte/build-step)
❌ Подключать Framer Motion / AOS / ScrollMagic / Locomotive Scroll / Three.js heavy WebGL
❌ Google Fonts CDN (DSGVO violation)
❌ Stock-фото / AI-баззворды / lorem ipsum / фейковые отзывы
❌ Удалять CNAME
❌ Удалять `assets/*-site.jpg` (это базовые скриншоты)
❌ Удалять `concept-*.html` без явного OK CEO
❌ Запускать P1 без OK на P0, P2 без OK на P1
❌ Игнорировать `prefers-reduced-motion`
❌ Срезать KPI-минимум анимаций

---

## Следующий шаг

CEO выбирает из P1 (приду с 2-3 вариантами токенов после получения ответов на Open Questions).

После OK на P0 → P1 (дизайн-токены) → OK → P2 (билд + тесты + финальный чеклист).

---

## Артефакты

- `c:\Projects\AiS152\docs\tasks\PX-002a_audit_and_roadmap.md` (этот файл)

## Журнал

- 2026-04-27 — P0 завершено #1, ожидание OK CEO
