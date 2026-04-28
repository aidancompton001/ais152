# AiS152 — Полный редизайн портфолио

> **Промпт для Claude Desktop.** Не для Claude Code. Не для ChatGPT.
> Источник: PX-002 (MainCore methodology). Версия: 1.0 — 2026-04-27.
> Автор протокола: #1 Chief Methodologist + #14 Hans Landa (review).

---

## КАК ПОЛЬЗОВАТЬСЯ (для CEO)

1. Открой Claude Desktop → новый чат
2. Скопируй **весь** этот файл и вставь в первое сообщение
3. Подожди — Claude вернёт **roadmap аудита** и остановится с маркером `=== WAITING_FOR_CEO_OK ===`
4. Дай ОК (или правки) → Claude вернёт **2–3 варианта дизайна** и снова остановится
5. Выбери палитру/типо → Claude построит сайт
6. Если контекст оборвётся в середине — напиши «продолжи с фазы P1» (или P2). Claude вспомнит этот промпт и продолжит

**Подставить перед запуском:**
- `{TODO_WHATSAPP}` — твой WhatsApp в международном формате без `+` (пример: `4915123456789`)
- `{TODO_EMAIL_FORMSUBMIT}` — email для контактной формы
- Остальное Claude спросит сам в P0

---

## РОЛЬ

Ты — ведущий дизайнер + frontend-архитектор уровня Awwwards. Специализация: **технологичные портфолио инженеров**, не «шаблоны Webflow». Твой эталон тона — gsap.com, Linear, Vercel.

**Обязательно перед началом работы запусти skills:**
- `ui-ux-pro-max`
- `design:user-research`

Если этих skills нет в Claude Desktop — STOP, попроси CEO их активировать.

---

## АМБИЦИЯ

CEO — создатель **9 production-проектов** (MONO booking app, BauPreis SaaS, EDMI, StormGuard, Eko-OYLIS, RundUmsHaus, StudioGlamour, Provenly Homes, AiS152). Текущий ais152.com этот уровень не показывает.

Цель редизайна: посетитель за 5 секунд понимает «этот человек делает не сайты-визитки, а серьёзный production». Ключевой эффект — **горизонтальный scroll-progress в секции Selected Work** (как gsap.com), инженерная плавность анимаций, рабочий интерактив без багов.

---

## PROJECT FACTS (зафиксировано — не спорь, не меняй)

- **Название:** AiS1.52 / AiS152
- **Production:** https://ais152.com
- **Исходники:** `c:\Projects\AiS152`
- **Стек:** Static HTML / CSS / vanilla JS — **менять НЕЛЬЗЯ** (GitHub Pages деплой сломается)
- **Хостинг:** GitHub Pages с CNAME (репозиторий `aidancompton001/aidancompton001.github.io` или подобный)
- **Хозяин:** CEO живёт в Мюнхене → DSGVO/GDPR обязательно
- **Языки:** EN (основной) + DE
- **Запреты:** Next.js, React, Vue, Svelte, любой build-step, package.json с `npm run build`, Three.js heavy, Framer Motion, AOS, ScrollMagic, Locomotive Scroll
- **Разрешено (Закон 19 — CREATIVE_TOOLKIT.md, MainCore):** GSAP + ScrollTrigger + SplitText + Lenis (это индустриальный стандарт, см. строку 35–40 toolkit'а — процитируй её в P2 перед использованием)

---

## ПРОТОКОЛ ИСПОЛНЕНИЯ — 3 ФАЗЫ

```
P0 АУДИТ → roadmap-файл → === WAITING_FOR_CEO_OK ===
                                    ↓ ОК
P1 ДИЗАЙН → 2-3 варианта токенов → === WAITING_FOR_CEO_OK ===
                                    ↓ ОК
P2 БИЛД   → код + data-driven каталог + тесты → финальный чеклист ✅/❌
```

**КРИТИЧНО:** между фазами ты ОБЯЗАН остановиться и вернуть строку-маркер `=== WAITING_FOR_CEO_OK ===`. Если ты запустишь P1 без ОК на P0 — это нарушение протокола, CEO простреляет бошку.

---

## PRE-FLIGHT (выполни ПЕРВЫМ)

Проверь свой toolset:

- [ ] `WebFetch` доступен? (нужен для аудита ais152.com и проверки 6 проектов)
- [ ] Filesystem MCP доступен и видит `c:\Projects\AiS152`? (нужен для чтения index.html и записи новых файлов)
- [ ] Skills `ui-ux-pro-max` + `design:user-research` активны?

Если хоть одно — нет: STOP. Скажи CEO что включить, не пытайся «обойти».

Если всё ок: подтверди коротко («Toolset OK, начинаю P0») и переходи к P0.

---

# ФАЗА P0 — АУДИТ И ROADMAP

**Цель:** разобраться что есть на ais152.com, что работает, что сломано, какие baseline-метрики, и предложить план редизайна. **Без единой строки кода имплементации.**

## P0.1 — Прочитай локальный код

- `c:\Projects\AiS152\index.html` (текущая prod-версия)
- `c:\Projects\AiS152\concept-a.html` ... `concept-g.html` (черновики дизайна, могут содержать идеи)
- `c:\Projects\AiS152\CLAUDE.md` (правила проекта)
- `c:\Projects\AiS152\TEAM.md` (роли)
- `c:\Projects\AiS152\DEVLOG.md` (история)
- `c:\Projects\AiS152\docs\tasks\PX-001_portfolio_update.md` (что уже планировалось)
- `c:\Projects\AiS152\assets\` — инвентарь скриншотов проектов (.jpg уже есть для всех 6)

## P0.2 — Зафетчи production

`WebFetch https://ais152.com` — что отдаётся в реальности (может отличаться от локального).

Если 404/timeout → используй Wayback Machine (`https://web.archive.org/web/2026*/ais152.com`).

## P0.3 — Зафетчи 6 проектов CEO (проверь что живые)

| Проект | URL | Если 404 |
|--------|-----|----------|
| StormGuard | https://www.stormguardprofessional.eu/ | пометь `archived` в roadmap |
| Eko-OYLIS | https://eco-oylis.info | пометь `archived` |
| RundUmsHaus | https://rundumshaus-littawe.de/ | пометь `archived` |
| StudioGlamour | https://aidancompton001.github.io/studioglamour/ | **известная проблема — был 404 на 2026-04-17**, если до сих пор 404 → статус `in-development` (НЕ удалять) |
| Provenly Homes | https://aidancompton001.github.io/provenly-homes | пометь `archived` |
| EDMI | https://aidancompton001.github.io/edmi-landing/ | prototype статус OK |

## P0.4 — Baseline Lighthouse

Через WebFetch получи https://pagespeed.web.dev/analysis?url=https%3A%2F%2Fais152.com (или эквивалент). Зафиксируй **числами, не на глаз**:

- Performance, Accessibility, Best Practices, SEO (mobile + desktop)
- LCP, CLS, TBT, TTI, Speed Index
- Размеры CSS / JS / шрифтов в KB

**Закон 05 (Numerical Verification, MainCore):** ни одного числа «из головы». Если PageSpeed недоступен — честно напиши «не смог замерить» и попроси CEO прогнать вручную.

## P0.5 — Что сломано (явный список)

Текущий ais152.com известно содержит:
- `cursor:none` на body (custom cursor может ломаться)
- Google Fonts CDN (`fonts.googleapis.com`) — **DSGVO violation в DE** (BGH 2022, Schrems-II), **обязательно self-host WOFF2**
- Жалобы CEO: «не все CTA кликаются», «WhatsApp не работает», «форма не отправляется»

Проверь и зафиксируй:
- Все `<a>` и `<button>` — реально ли работают (handler есть, target корректен)?
- Есть ли WhatsApp-кнопка вообще, какой `wa.me/` номер?
- Есть ли контактная форма, какой backend (если есть)?
- Шрифты — откуда грузятся?
- Аналитика — есть/нет (определит нужен ли cookie-banner)?

## P0.6 — Сделай roadmap-файл

Создай `c:\Projects\AiS152\docs\tasks\PX-002a_audit_and_roadmap.md` со структурой:

```markdown
# PX-002a — Audit & Redesign Roadmap

## Baseline (Lighthouse, проверено YYYY-MM-DD)
- Performance mobile: NN
- A11y: NN
- ... (числа из P0.4)

## Что работает
- ...

## Что сломано (с конкретикой)
- CTA "Hire me" → ссылка href="#" пустая
- WhatsApp-кнопка → нет
- Форма → нет / mailto / Formspree placeholder
- Шрифты → Google Fonts CDN (DSGVO violation)
- ... (всё что нашёл в P0.5)

## 6 проектов — статус
| Slug | URL | HTTP | Скриншот в assets/ | Статус |
|------|-----|------|-------------------|--------|
| stormguard | ... | 200 | stormguard-site.jpg | live |
| ...

## Open Questions для CEO (минимум 10)
1. WhatsApp номер для wa.me/{...}? (placeholder сейчас: {TODO_WHATSAPP})
2. Email для FormSubmit.co? (placeholder: {TODO_EMAIL_FORMSUBMIT})
3. Структура: SPA one-pager или multi-page?
4. Tone of voice: минимализм / инженерный / смелый?
5. StudioGlamour живой? Если 404 — статус "in-development"?
6. Подключаем ли аналитику (если да — нужен cookie-banner)?
7. Impressum/Datenschutz — есть тексты или заглушки?
8. Lighthouse цели: Perf 90 / A11y 95 / BP 100 / SEO 90 — принимаем?
9. Готов ли к data/projects.json (новый проект = 1 запись в JSON, без правки HTML)?
10. Шрифты: какая пара (sans/serif/mono)? Предложу 2-3 варианта в P1.

## Предложение по структуре редизайна
- Hero (1 экран, сильный stagger reveal заголовка)
- Selected Work (горизонтальный scroll-progress, 6 проектов из data/projects.json)
- About (короткий manifest, counter-анимация цифр: 9 проектов, N лет, etc.)
- Process (как работаю — 3-4 шага)
- Contact (форма + WhatsApp FAB)
- Footer (Impressum, Datenschutz, lang switch EN/DE)

## Архитектура «легко добавлять проекты» (требование CEO)
- Источник правды: `data/projects.json` (массив объектов)
- Схема в `data/projects.schema.json`
- README в `data/README.md`: «как добавить проект за 30 секунд»
- Vanilla JS читает JSON → клонирует <template id="project-card"> → рендерит сетку
- Добавление нового проекта = 1 запись + 2 скриншота (1x/2x) → коммит → push. Никаких правок HTML/CSS/JS.

## Performance Budget (целевой)
- CSS ≤ 60KB gzip
- JS ≤ 120KB gzip (вкл. GSAP+Lenis)
- LCP ≤ 2.5s (mid-tier mobile, Slow 4G)
- CLS ≤ 0.1
- TBT ≤ 200ms
- DOM ≤ 1500 nodes
- Шрифты ≤ 4 файла WOFF2, total ≤ 200KB

## KPI «next-level» (минимум, измеримо)
- ≥ 3 ScrollTrigger-сцены
- ≥ 1 pinned-section (горизонтальный scroll-progress)
- ≥ 1 SplitText / character-stagger reveal
- ≥ 1 magnetic-cursor элемент (hover)
- ≥ 1 smooth marquee / ticker
- ≥ 1 counter-анимация через RAF

## Browser matrix
Chrome ≥120, Edge ≥120, Firefox ≥120, Safari ≥17 (desktop), Safari iOS ≥17.
Особый пункт: тест Lenis на iOS Safari — known issue с overflow:hidden, workaround `body { overscroll-behavior: none }`.

## Breakpoints (стандарт Tailwind, tailwindcss.com/docs/responsive-design)
640 / 768 / 1024 / 1280 / 1536. Mobile-first.

## DSGVO / GDPR pre-merge gate
- Self-hosted WOFF2 (Google Fonts CDN запрещён, BGH 2022)
- Лицензии шрифтов: SIL OFL / Apache 2.0 / Free for commercial — копия в `assets/fonts/LICENSE-{name}.txt`
- WhatsApp: 2-click warning (DSGVO для embedding мессенджеров)
- Cookie-banner: только если подключена аналитика
- Impressum + Datenschutz обязательны в footer (требование TMG §5 / DDG)
- Owner: #14 Hans Landa подписывает DSGVO-секцию ДО merge

## Fallback-матрица
| Сбой | Резерв |
|------|--------|
| ais152.com 404/timeout в P0 | Wayback snapshot |
| FormSubmit лимит 50/мес free | Web3Forms 2-й провайдер + mailto: |
| GitHub Pages cache (≤10 мин) | ?v={git-short-hash} на CSS/JS |
| Нет WhatsApp на desktop | wa.me/ + parallel tel: link |
| StudioGlamour 404 | статус in-development в JSON |
| CEO молчит >24ч | пинг #1 + работа над не-блокирующими частями |
| Нет Filesystem MCP | STOP, инструкция CEO |
```

## P0.7 — STOP

После того как roadmap-файл создан и заполнен — выведи в чат **краткое резюме** (≤300 слов: что нашёл, что сломано, главные open questions) и заверши строкой:

```
=== WAITING_FOR_CEO_OK ===
```

**НЕ продолжай в P1 без явного «ОК» от CEO.**

---

# ФАЗА P1 — ДИЗАЙН (после ОК CEO на P0)

**Цель:** дать 2–3 варианта дизайн-токенов, чтобы CEO выбрал. **Без имплементации.**

## P1.1 — Сверка с CREATIVE_TOOLKIT.md (Закон 19)

Прочитай `c:\Projects\MainCore\core\CREATIVE_TOOLKIT.md`. Найди записи про GSAP, Lenis, ScrollTrigger. **Процитируй конкретные строки** где они одобрены. Без цитаты — STOP, не используй.

Если читать MainCore нет доступа — попроси CEO дать выписку.

## P1.2 — 3 варианта токенов

Оформи в roadmap-файле как 3 варианта `:root`:

**Вариант A — «Engineering Minimal»** (Linear-tone)
- BG: почти-чёрный `#0A0A0B`
- Text: `#EDEDEE`
- Accent: холодный синий `#3B82F6` или сдержанный
- Type: Inter / Inter Tight (sans, self-host)
- Mono: JetBrains Mono (для project tags)

**Вариант B — «Bold Tech»** (gsap-tone)
- BG: тёмно-зелёный/чёрный `#0E1410`
- Text: `#F5F5F0`
- Accent: ярко-зелёный `#00FF88` или текущий `#C8FF00`
- Type: Geist / Geist Mono или Outfit (self-host WOFF2)

**Вариант C — «Editorial Premium»** (vercel/awwwards)
- BG: off-white `#FAFAF8` (light theme!) либо deep `#101010`
- Text: контрастный
- Accent: graphite + один спот-цвет (магента/охра)
- Type: serif H1 (например Fraunces) + Inter body

Для каждого варианта дай:
- Палитру (5–7 ролей: bg, surface, border, text, muted, accent, accent-soft)
- Type scale (8 ступеней с rem)
- Spacing scale (8-pt grid)
- Motion scale (durations 150/300/600/1200ms, easings)
- Mood-картинку (опиши словами: «футуристичный лог-файл», «техническая монография», и т.д.)

## P1.3 — Wireframes секций (текстом)

Опиши каждую секцию: что видит пользователь, какие элементы, какая анимация. Без кода. ASCII-схемы допустимы.

## P1.4 — STOP

Заверши:
```
=== WAITING_FOR_CEO_OK ===
```

**НЕ начинай P2 без выбора варианта (A/B/C) и без ОК.**

---

# ФАЗА P2 — БИЛД (после ОК CEO на P1)

**Цель:** построить готовый сайт с data-driven каталогом проектов.

## P2.1 — Архитектура файлов

```
c:\Projects\AiS152\
├── index.html               (или index.html + projects.html + about.html — по решению CEO)
├── assets/
│   ├── css/
│   │   ├── tokens.css       (выбранный вариант A/B/C из P1)
│   │   ├── base.css         (reset + typography)
│   │   ├── layout.css
│   │   ├── components.css
│   │   └── motion.css       (только GSAP fallback стили + reduced-motion)
│   ├── js/
│   │   ├── main.js          (entry, init Lenis, init GSAP timelines)
│   │   ├── projects.js      (читает data/projects.json, рендерит карточки)
│   │   ├── form.js          (FormSubmit + Web3Forms fallback)
│   │   ├── whatsapp-fab.js  (DSGVO 2-click warning)
│   │   └── reduced-motion.js
│   ├── fonts/
│   │   ├── *.woff2          (self-hosted)
│   │   └── LICENSE-*.txt
│   └── projects/            (скриншоты, переезд из assets/*-site.jpg)
│       ├── stormguard.jpg
│       ├── stormguard@2x.jpg
│       └── ...
├── data/
│   ├── projects.json        (источник правды)
│   ├── projects.schema.json (JSON Schema для валидации)
│   └── README.md            (как добавить проект за 30 секунд)
├── CNAME                    (НЕ ТРОГАТЬ)
└── (старые concept-*.html — оставить или перенести в archive/)
```

## P2.2 — `data/projects.json` — схема

```json
[
  {
    "slug": "stormguard",
    "title": "StormGuard",
    "tagline": "E-commerce pet cosmetics",
    "year": 2026,
    "url": "https://www.stormguardprofessional.eu/",
    "status": "live",
    "tags": ["E-commerce", "Static", "Supabase", "Cloudflare Pages"],
    "summary": "Production e-commerce for premium pet cosmetics. Static site + Supabase backend, deployed on Cloudflare Pages.",
    "screenshot": "assets/projects/stormguard.jpg",
    "screenshot_2x": "assets/projects/stormguard@2x.jpg",
    "featured": true,
    "order": 1
  }
  // ... 6 объектов
]
```

`data/projects.schema.json` — валидный JSON Schema draft-07 со всеми полями `required`.

## P2.3 — `data/README.md` — для CEO

```markdown
# Как добавить новый проект в портфолио

1. Сделай скриншот сайта: 1280×800 (1x) и 2560×1600 (2x), формат JPG, оптимизированный (≤200KB на 1x)
2. Положи в `assets/projects/{slug}.jpg` и `assets/projects/{slug}@2x.jpg`
3. Открой `data/projects.json`, добавь новый объект в массив (см. схему в `projects.schema.json`)
4. Поля: slug (kebab-case), title, tagline (≤60 chars), year, url, status (live|in-development|archived), tags (1-5), summary (≤200 chars), screenshot, screenshot_2x, featured (true для главной), order (число для сортировки)
5. Коммит → push → GitHub Pages обновит сайт за ~2 мин

**Никаких правок HTML/CSS/JS не нужно.** Если что-то не работает — проверь JSON в https://jsonlint.com и схему в `projects.schema.json`.
```

## P2.4 — Рендер проектов (vanilla JS)

```js
// projects.js — псевдокод
fetch('./data/projects.json')
  .then(r => r.json())
  .then(projects => {
    const tpl = document.querySelector('#project-card-tpl');
    const grid = document.querySelector('#projects-grid');
    projects
      .filter(p => p.status !== 'archived' || ceoWantsArchived)
      .sort((a,b) => a.order - b.order)
      .forEach(p => {
        const node = tpl.content.cloneNode(true);
        // populate fields, src, srcset, href, status badge
        grid.appendChild(node);
      });
    // после рендера — init ScrollTrigger horizontal scroll
  });
```

Используй `<template>` элемент. Изображения с `loading="lazy"` + `srcset`.

## P2.5 — Анимации (GSAP + Lenis + ScrollTrigger)

Реализуй **минимум** (KPI из P0.6):
- ≥3 ScrollTrigger-сцены (hero reveal, projects pin/scrub, about counter)
- ≥1 pinned horizontal scroll в Selected Work — главная фишка
- ≥1 SplitText или character-stagger в Hero
- ≥1 magnetic cursor на главных CTA
- ≥1 smooth marquee (например в footer — список технологий)
- ≥1 counter (числа в About: «9 проектов», «N лет», etc.)

Lenis + GSAP интеграция — стандарт (см. CREATIVE_TOOLKIT.md строка 40).

**Reduced motion (обязательно):**
```js
if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
  // Не инициализируй Lenis, не запускай ST timelines
  // Оставь только opacity-fade на reveal
}
```

## P2.6 — WhatsApp FAB (DSGVO 2-click)

Sticky bottom-right на всех страницах. **Не сразу `wa.me/`** — сначала маленькое окошко: «Контакт через WhatsApp откроет сторонний сервис Meta Platforms Ireland Ltd. Datenschutz: …». После клика на «OK» → `wa.me/{TODO_WHATSAPP}`.

Для desktop без WhatsApp — параллельно `tel:` link и `mailto:`.

## P2.7 — Контактная форма (FormSubmit.co + Web3Forms fallback)

Основной endpoint — FormSubmit.co (проверено в Eko-OYLIS, см. `c:\Projects\MainCore\lessons\EKO_OYLIS_LESSONS.md`):

```html
<form action="https://formsubmit.co/{TODO_EMAIL_FORMSUBMIT}" method="POST">
  <input type="hidden" name="_captcha" value="false">
  <input type="hidden" name="_next" value="https://ais152.com/?sent=1">
  <input type="hidden" name="_honey" style="display:none">
  <!-- поля: name, email, message -->
</form>
```

Fallback (если FormSubmit рейт-лимит / down) — Web3Forms.com со своим access_key. UI states: idle / sending / success / error (`aria-live="polite"`).

CEO должен **подтвердить email** при первой отправке формы (FormSubmit пришлёт письмо с ссылкой).

## P2.8 — DSGVO

- Self-host WOFF2 — выбранные шрифты + копии лицензий в `assets/fonts/LICENSE-*.txt`
- Footer: ссылки на Impressum + Datenschutz (если текстов нет — заглушки с TODO для CEO)
- Cookie-banner: **по умолчанию НЕ подключаем** (нет аналитики). Если CEO в P0 ответил «нужна аналитика» — добавь cookie-consent (например vanilla-cookieconsent, не Cookiebot).

## P2.9 — A11Y

- WCAG AA, axe-core ≥ 95
- Semantic landmarks: `<header><main><nav><footer>`
- alt на всех `<img>`, aria-label на иконочных кнопках
- Focus-visible ring (custom, не дефолтный)
- Keyboard nav: Tab проходит весь сайт логично, Enter/Space активируют FAB и form submit
- Контраст ≥ 4.5:1 (проверь через ColorContrast tool)
- `prefers-reduced-motion` отключает GSAP/Lenis (см. P2.5)

## P2.10 — Cache busting

`<link href="assets/css/tokens.css?v={GIT_HASH}">` — на CSS/JS. Хеш можно подставить вручную при пуше (или скриптом). GitHub Pages кэширует до 10 мин — без `?v=` пользователи увидят старое.

## P2.11 — Финальный чеклист (выведи в конце как ✅/❌)

Для каждого пункта — реальный результат:

- [ ] Все 6 проектов отображаются с живыми ссылками
- [ ] StudioGlamour: статус `in-development` если 404 (не удалён)
- [ ] Добавлен 7-й тестовый проект через `data/projects.json` → появился без правок HTML/CSS/JS (демонстрация)
- [ ] WhatsApp FAB кликается → 2-click warning → wa.me/{TODO_WHATSAPP}
- [ ] Контактная форма отправляется → редирект на `_next` → email пришёл
- [ ] Lighthouse Performance ≥ 90 (mobile)
- [ ] Lighthouse A11y ≥ 95
- [ ] Lighthouse Best Practices = 100
- [ ] Lighthouse SEO ≥ 90
- [ ] Axe-core ≥ 95
- [ ] CSS ≤ 60KB gzip (число)
- [ ] JS ≤ 120KB gzip (число)
- [ ] LCP ≤ 2.5s, CLS ≤ 0.1, TBT ≤ 200ms (числа)
- [ ] Шрифты только self-hosted WOFF2 (никакого Google Fonts CDN)
- [ ] Лицензии шрифтов в `assets/fonts/LICENSE-*.txt`
- [ ] `prefers-reduced-motion` отключает все GSAP-анимации (проверено в DevTools)
- [ ] Keyboard tab-order логичен, focus-visible виден везде
- [ ] Mobile sticky CTA-bar работает на 360–640px
- [ ] iOS Safari тест Lenis: scroll плавный, нет jank на overflow
- [ ] ≥ 3 ScrollTrigger-сцены реализованы
- [ ] ≥ 1 pinned horizontal scroll в Selected Work
- [ ] ≥ 1 SplitText / stagger reveal
- [ ] ≥ 1 magnetic cursor
- [ ] ≥ 1 smooth marquee
- [ ] ≥ 1 counter с RAF
- [ ] Footer: Impressum + Datenschutz ссылки (даже если заглушки)
- [ ] Cache busting `?v=` на CSS/JS
- [ ] Стек НЕ изменён (Static HTML/CSS/JS, GitHub Pages, CNAME на месте)
- [ ] Никаких AI-баззвордов в копирайте («innovative», «AI-powered», «next-gen», «cutting-edge», «revolutionary»)
- [ ] Никаких stock-фото / lorem ipsum / фейковых отзывов
- [ ] Старые `concept-*.html` либо оставлены, либо перенесены в `archive/` (по решению CEO в P0)

## P2.12 — Open questions, оставшиеся к CEO

Если в процессе билда возникли решения, которые ты сделал по своему усмотрению — выведи их списком в конце. CEO решит оставлять или менять.

---

## ЗАПРЕЩЕНО (всю работу)

- Менять стек (никакого Next.js / React / Vue / Svelte / build-step)
- Подключать Framer Motion, AOS, ScrollMagic, Locomotive Scroll, Three.js heavy WebGL
- Использовать Google Fonts CDN (DSGVO violation)
- Stock-фото, AI-баззворды, lorem ipsum, фейковые отзывы
- Удалять CNAME
- Удалять `assets/*-site.jpg` (это базовые скриншоты, переноси в `assets/projects/{slug}.jpg`)
- Удалять `concept-*.html` без явного ОК CEO
- Запускать P1 без ОК на P0, P2 без ОК на P1
- Игнорировать `prefers-reduced-motion`
- «Срезать» KPI-минимум анимаций (≥3 ST + pinned + SplitText + magnetic + marquee + counter)

---

## ССЫЛКИ НА ИСТОЧНИКИ (для самопроверки в P2)

- Закон 19 / toolkit: `c:\Projects\MainCore\core\CREATIVE_TOOLKIT.md` — строки 35–40, 82+ (GSAP / Lenis / ScrollTrigger)
- FormSubmit lessons: `c:\Projects\MainCore\lessons\EKO_OYLIS_LESSONS.md` — строки 4, 33, 64
- DSGVO Google Fonts: BGH 2022 (LG München I, 20.01.2022, 3 O 17493/20)
- Tailwind breakpoints: https://tailwindcss.com/docs/responsive-design
- Lighthouse: https://pagespeed.web.dev/
- A11y: https://www.deque.com/axe/

---

## START

Начни с **PRE-FLIGHT** (toolset check). Затем **P0**. Не запускай P1 без ОК.

Удачи. CEO ждёт.
