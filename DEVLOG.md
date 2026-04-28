# DEVLOG.md — AiS152

## Журнал разработки

### [S011] — 2026-04-28 — PX-010: Full SEO pass — meta, JSON-LD, sitemap, robots, hreflang

**Роли:** #1 Viktor (lead/coord) · #3 Andrei (HTML+JSON-LD+sitemap+robots+hreflang+canonical) · #2 Lena (alt+favicon) · #14 Hans Landa (review)
**Статус:** code-фаза завершена (commit `cdf6fa7`, откат-тег `v2-pre-px010` → `01e3e5f`); CEO action остаётся: Lighthouse + Search Console + Bing verification
**Скилл:** P6 audit → P0 stop → P1 fix (3-фазный протокол)

**Phase 1 (audit) findings:**

- 🔴 `/robots.txt` HTTP 404 (отдавался 404.html)
- 🔴 `/sitemap.xml` HTTP 404
- 🔴 hreflang отсутствует на всех 4 страницах
- 🔴 JSON-LD: 1 schema (ProfessionalService), нет Person/WebSite
- 🟡 Mona Sans 529 KB (LCP risk)
- 🟡 `/favicon.ico` 404 (Bing legacy)
- 🟡 `/apple-touch-icon.png` 404 в корне
- 🟡 404.html без canonical и meta description
- ✅ HTML semantic: `<main>×1, <article>×4, <nav>×2, <section>×8` на index — отлично
- ✅ canonical на 3/4, robots-noindex корректно на legal/404
- ✅ lang.js уже обновляет `<html lang>` (audit-замечание #6 снято)

**Phase 2 (CEO sync — 7 ответов):**

1. Keywords — мой draft принят
2. Person: Eduard Baias / Independent Software Engineer / linkedin.com/in/eduard-baias/
3. LocalBusiness: только city Munich (приватнее)
4. Sitemap: только index, legal noindex
5. Mona Sans: оставить full 529 KB
6. Search Console: CEO делает сам (HTML-файл upload потом)
7. Hreflang: same-URL для всех языков (option a)

**Phase 3 (fix — что сделано):**

- `robots.txt` создан (User-agent *, Allow /, Sitemap directive)
- `sitemap.xml` создан (index + 3 hreflang alternates)
- `favicon.ico` сгенерирован (multi-res 16/32/48/64 из apple-touch-icon.png через Python PIL)
- `apple-touch-icon.png` скопирован в корень (для iOS root pings)
- `index.html`: hreflang en/de/x-default; JSON-LD `@graph` с Person + ProfessionalService + WebSite (founder/publisher refs); favicon.ico + apple-touch-icon в `<link>` chain; project-card template `alt="Project preview"` fallback для no-JS crawlers
- `impressum.html` + `datenschutz.html`: hreflang de + x-default
- `404.html`: meta description, canonical, robots noindex,follow (вместо просто noindex), apple-touch-icon link

**Тесты (Phase 4):**

- JSON-LD валидируется через Python json.loads, содержит @graph с 3 типами (Person, ProfessionalService, WebSite); поля Person matches CEO data
- sitemap.xml валидируется через Python ElementTree, 1 URL + 3 alternates
- Hreflang counts: index=3, impressum=2, datenschutz=2
- robots.txt 115 bytes, favicon.ico 8.8 KB multi-res, apple-touch-icon.png 4 KB

**Артефакты (новые):** `robots.txt`, `sitemap.xml`, `favicon.ico`, `apple-touch-icon.png` (в корне)
**Артефакты (изменённые):** `index.html`, `impressum.html`, `datenschutz.html`, `404.html`
**Откатный тег:** `v2-pre-px010` → `01e3e5f`

**Hand-off CEO (то что только ты можешь):**

1. **Google Search Console:** добавить property `https://ais152.com`, верифицировать через HTML-file upload (Google даст файл вида `googleXXXXXX.html` → сохрани в `c:\Projects\AiS152\` → скажи мне → закоммичу) → отправить sitemap → проверить indexing coverage через 2-7 дней
2. **Bing Webmaster Tools:** аналогично (https://www.bing.com/webmasters)
3. **Lighthouse:** Chrome DevTools → Lighthouse tab → mobile + desktop run → закинь скрины/числа в STATUS.md (закроет open issue из S004/S005 «baseline не замерен»)
4. **(Опц)** Google Business Profile для Munich — если решишь публиковать street-address (CEO option 3 = только city, поэтому Local Pack ограничен)

**Open issues после PX-010 (изначально):**

- LH-1 — Lighthouse baseline всё ещё не замерен (CEO action)
- SC-1 — Search Console verification (CEO action, blocking metric tracking)
- BING-1 — Bing Webmaster verification (CEO action)

---

#### CEO actions — выполнено CEO в тот же день (2026-04-28, late session)

**✅ SC-1 — Google Search Console полностью настроен:**

1. CEO положил `google9d7cbb1b47be4897.html` в корень проекта → закоммитил как `b42b433` → файл live на `https://ais152.com/google9d7cbb1b47be4897.html`
2. CEO нажал **VERIFY** в Search Console UI → Google прочитал файл → **Ownership verified** (HTML file method)
3. CEO в Sitemaps section → submit `sitemap.xml` → Google ответил **«Sitemap submitted successfully. Google will periodically process it and look for changes.»**
4. CEO через URL Inspection → ввёл `https://ais152.com/` → нажал **Request Indexing** → Google: **«URL was added to a priority crawl queue»**

Подтверждение что live HTML на момент verify содержит весь PX-010 SEO-стек (CEO прислал view-source dump):

- Hreflang × 3 (en/de/x-default)
- JSON-LD @graph: Person + ProfessionalService + WebSite (Eduard Baias, Independent Software Engineer, Munich, sameAs LinkedIn)
- favicon.ico + apple-touch-icon в `<link>` chain
- Cache-bust `?v=2026-04-28-px010`
- Counter "3" + .stat-fineprint (PX-008), Hour/Day/Days (PX-006), marquee duplicated (PX-008), hero «<1h» (PX-006), card alt + Featured pill (PX-005)

**Индексация ожидается:** 1-3 дня (priority queue). Coverage check: 2026-04-30 — 2026-05-01.

**❌ Open после CEO actions:**

- BING-1 — Bing Webmaster Tools — частично сделано (см. ниже)
- LH-1 — Lighthouse mobile/desktop baseline (CEO Chrome DevTools → 5 минут)
- IDX-1 (новый) — проверить Search Console Coverage report через 2-7 дней; если 0 indexed — диагностика

---

#### CEO actions (продолжение, 2026-04-28 evening) — BING-1 в работе

**🟡 BING-1 — Bing Webmaster Tools (Import from GSC):**

- ✅ CEO импортировал ais152.com в Bing Webmaster Tools через «Import from Google Search Console» (1 click)
- ✅ Property `ais152.com/` создан, Bing dashboard виден
- ⏳ Bing-сообщение: «Your data and reports are being processed and it may take upto 48 hours to reflect»
- ❌ Sitemap submit в Bing — pending (CEO выполняет: Sitemaps → Submit `https://ais152.com/sitemap.xml`)
- ❌ URL Submission первой страницы — pending (10 URLs/day бесплатно)

**Бонус Bing:** Bing index = backbone для DuckDuckGo + Yahoo + Ecosia. Один verify = 4 поисковика покрыты.

**Коммиты этой сессии:**

- `cdf6fa7` feat(seo): full SEO pass — meta, JSON-LD, sitemap, robots, hreflang
- `ff133c7` docs: log PX-010 completion (S011 + STATUS + registry)
- `b42b433` chore: add Google Search Console verification file

---

### [S010] — 2026-04-28 — PX-008: Marquee infinite + stats 3d + form activation

**Роли:** #2 Lena (CSS marquee + stats) · #3 Andrei (JS clone + form fallback) · #14 Hans Landa (review)
**Статус:** завершено (commit `832b2dd`, откат-тег `v2-pre-px008` → `7aeb689`)
**Скилл:** systematic-debugging (Phase 1 closed by curl evidence + DOM math)

**Жалоба CEO:** 3 бага на live — marquee рывок, counter «30d» врёт, форма «Could not send».

**Корни (доказаны, не догадки):**

- **(A) Marquee:** `layout.css:302` `animation: marquee 40s` + `@keyframes 0 → translateX(-50%)`. HTML содержит ОДИН набор tokens — нет дубликата. Стандартный CSS-pattern infinite marquee требует `[оригинал][клон]` чтобы при сдвиге на -50% клон встал на место оригинала. Без дубликата → пустота → автоматический reset → рывок.
- **(B) Stats:** `index.html:245` `data-target="30"` — PX-006 не пропатчил. Атомарная пропущенная строка.
- **(C) Form:** Diagnostic curl POST на `formsubmit.co/ajax/ebaias.muc@gmail.com` с правильными Origin/Referer вернул `{"success":"false","message":"This form needs Activation. We've sent you an email containing an 'Activate Form' link."}`. CEO кликнул link → verification POST вернул `{"success":"true"}`. Endpoint жив.

**Что сделано:**

- `main.js`: clone children of `#marquee-track` on load (skip on `prefers-reduced-motion`); `requestAnimationFrame` → `ScrollTrigger.refresh()` чтобы work-pin пересчитался корректно
- `layout.css`: `marquee` animation duration `40s → 60s` (doubled content, тот же визуальный темп)
- `index.html:245`: `data-target="30"` → `data-target="3"`
- `index.html`: новые `.stat-fineprint` строки «For landings & MVPs» / «Für Landings & MVPs» под counter — синхрон с PX-006 disclaimer
- `layout.css`: новый класс `.stat-fineprint` (mono, fs-2xs, tx-fa)
- `index.html`: hidden `.form-fallback` контейнер с 3 CTA — Email (mailto, anti-spam), WhatsApp (data-wa-trigger, DSGVO 2-click), Telegram bot
- `form.js` catch block: вместо plain-text email раскрывает `.form-fallback` контейнер
- `components.css`: стили `.form-fallback` + `.form-fallback-text` + `.form-fallback-actions`
- Cache-bust `?v=2026-04-28-px008`

**Тесты (Phase 4):**

- (A) main.js содержит `marqueeTrack` + `cloneNode` (6 occurrences); layout.css содержит `60s linear infinite`
- (B) `data-target="3"` присутствует, `data-target="30"` отсутствует, fineprint «For landings» присутствует
- (C) `form-fallback` присутствует в HTML/JS/CSS; FormSubmit endpoint diagnostic POST → `success:true`
- Cache-bust ×15 в index.html

**Артефакты:** `assets/js/main.js`, `assets/js/form.js`, `assets/css/layout.css`, `assets/css/components.css`, `index.html`
**Откатный тег:** `v2-pre-px008` → `7aeb689`

**Hans Landa замечания (учтены):**

- 🔴 Race condition с GSAP work-pin → `ScrollTrigger.refresh()` через `requestAnimationFrame` после clone
- 🔴 Plain-text email раскрывал spam-vector → теперь mailto: обёртка
- 🟡 «3d to first ship» без disclaimer — добавлен fineprint «For landings & MVPs»
- 🟡 Marquee 40s × 2× content = в 2 раза быстрее → duration 40s → 60s
- 🟡 reduced-motion → clone skipped через `if (!REDUCED_MOTION)`

**Закрыто из STATUS.md open issues:** FORM-1 был частично fixed (FormSubmit активирован; Web3Forms key всё ещё placeholder, но primary канал работает).

---

### [S009] — 2026-04-28 — PX-007: Hero overlap + variable-font layout shift fix

**Роли:** #2 Lena (CSS hero/grid) · #3 Andrei (JS variable-font axis) · #14 Hans Landa (review)
**Статус:** завершено (commit `4a04ead`, откат-тег `v2-pre-px007` → `658175e`)
**Скилл:** systematic-debugging (Phase 1 root cause проверен математикой, не догадкой)

**Жалоба CEO:** на live ais152.com terminal-панель в hero налезает на H1 («for teams that…» обрезается); шрифт прыгает при hover/scroll.

**Корень (математика):**

- `.hero-title font-size: var(--fs-display)` → clamp `(3.5rem, 2rem + 7.5vw, 9rem)` → **на любом viewport ≥970px = 144px**
- `.hero > .container { grid-template-columns: minmax(0, 1.05fr) minmax(0, 1fr); gap: 4rem }` → LEFT col ≈ **583px** на viewport 1700px
- Слово «Engineering» в Mona Sans semibold 144px ≈ **770px** wide
- 770 > 583 → слово **физически не влезает** в свою grid-cell
- `min-width: 0` разрешает колонке быть узкой, но `overflow-wrap: normal` (default) НЕ разбивает одиночные слова
- Результат: слово вылазит за пределы своей колонки и **визуально перекрывает terminal**

**Дополнительно — variable font layout shift:**

- `data-vfont-hover` в main.js менял `wght: 620→740` И `wdth: 100→88` на hover
- ScrollTrigger в main.js менял `wght: 620→840` И `wdth: 100→82` при scroll hero
- `wdth` axis change → буквы становятся уже → ширина слова падает → **reflow на каждый scroll-frame** = визуальный «прыжок»

**Coral «actually»:** НЕ баг, это намеренный `<em>` стиль из `hero.css:89-93` (`.hero-title em { color: var(--ac); font-variation-settings: bold + narrow }`). Не трогал.

**Что сделано (CEO выбрал Вариант A — font-size 104px):**

- `.hero > .container` → `grid-template-columns: minmax(0, 1.3fr) minmax(380px, 1fr)` (LEFT шире, RIGHT защищён минимумом 380px)
- `.hero-title font-size: clamp(2.75rem, 1rem + 5.5vw, 6.5rem)` (max 104px — слово «Engineering» 560px ≤ 583px колонки)
- `.hero-title { max-width: 12ch; text-wrap: balance; overflow-wrap: break-word; contain: layout style }` (graceful переносы + изоляция reflow)
- Responsive breakpoint `1024px` → `1280px` (single-column раньше; 1024-1280 был unsafe zone)
- `[data-vfont-hover] { contain: layout style; transition: font-variation-settings 220ms }` в components.css
- main.js scroll axis: убран `obj.wdth = 100 - st.progress * 18`, оставлен только `obj.wght = 620 + st.progress * 200` (composite-friendly, без reflow)
- main.js hover: убран `"wdth" 88`, оставлен `"wght" 740`

**Тесты (Phase 4):**

- 9/9 grep-проверок passed (presence: 5 hero.css + 1 components.css + 1 main.js wght-only + 1 cache-bust; absence: wdth axis из main.js удалён, breakpoint 1024 в hero.css удалён)
- Live verify: hero.css/main.js на сервере содержат новые правила, старые сигнатуры отсутствуют

**Артефакты:** `assets/css/hero.css`, `assets/css/components.css`, `assets/js/main.js`, `index.html`
**Откатный тег:** `v2-pre-px007` → `658175e`

**Hans Landa замечания (учтены):**

- 🔴 font-size 144→104 = -28% «вес» H1 → CEO явно выбрал A через 3 варианта
- 🔴 `text-wrap: balance` Safari < 17.4 → graceful no-op fallback, принято
- 🟡 Убирание wdth из scroll = потеря визуальной сигнатуры → wght-эффект сохранён (text bolder при scroll)
- 🟡 breakpoint 1024→1280 сужает desktop range → принято за стабильность
- 🟡 coral «actually» — НЕ трогаю (em-стиль)

---

### [S008] — 2026-04-28 — PX-006: Speed is the moat — реальные сроки 1h/24h/3d

**Роли:** #1 Viktor (lead/копирайт) · #3 Andrei (HTML+JS+i18n) · #14 Hans Landa (review)
**Статус:** завершено (commit `c7c9496`, откат-тег `v2-pre-px006` → `aa5b0dd`)
**Скилл:** brainstorming (3 варианта подачи Process до правки) + systematic copywriting

**Жалоба CEO:** в публичном Process висит враньё — «Four weeks. Week 1-3. Week 4. Days 1-2». Реальность: 1h reply / 24h concept / 3d ship. Это и есть главное конкурентное преимущество, упрятанное в обычный таймлайн.

**P10 research (найдено):**

- `index.html:384-385` — section-title «Four weeks. Four steps.» / «Vier Wochen. Vier Schritte.»
- `index.html:398, 410, 422` — process-step-time «Days 1–2», «Week 1–3», «Week 4»
- `index.html:407-408` — Step 02 текст «Daily commits… Weekly demo on Zoom»
- `index.html:183` — hero-meta «Response: <24h»
- `index.html:235` — stats counter `data-target="9"` (Selected Work уже = 8)
- `assets/js/terminal.js:51-65` — process.md в hero terminal с теми же сроками
- `assets/js/terminal.js:84` — commits.log хвост «last deploy 4h ago»

**Что сделано (CEO выбрал Вариант A — Минимализм + оба disclaimer + counter fix):**

- Section title → «Hour. Day. Days.» / «Stunde. Tag. Tage.»
- Subtitle → «Reply in 1 hour. Concept in 24 hours. Live in 3 days.» / «Antwort in 1 Stunde. Konzept in 24 Stunden. Live in 3 Tagen.»
- Disclaimer (mono fineprint) → «Business hours, Mon–Fri 09–19 CET. For landing pages & MVPs — complex SaaS quoted separately.» / DE-аналог
- Step 01: Discover → **Reply** / Antwort, time «Within 1 hour» / «Innerhalb 1 Stunde»
- Step 02: Build → **Concept** / Konzept, time «Within 24 hours» / «Innerhalb 24 Stunden»
- Step 03: Ship / Live, time «Within 3 days» / «Innerhalb 3 Tagen»
- Step 04: Maintain (+30 days) — без изменений (после-релизная гарантия, не врёт)
- Hero meta: «Response < 24h» → «**< 1h**»
- Stats counter: `data-target="9"` → `8` (синхрон с Selected Work)
- Terminal process.md: rewrite «# Speed is the moat», 3 шага с реальными сроками
- Terminal commits.log: «last deploy 4h ago» → «last reply 12m ago» (живее)
- Новый CSS-класс `.section-fineprint` в `layout.css` (mono, fs-xs, tx-fa)

**Тесты (Phase 4):**

- 11/11 lie-strings removed (`Four weeks`, `Week 1-3`, `Week 4`, `Days 1-2`, `// week 4` — везде count=0)
- 13/13 new-copy strings present
- i18n balance: 92 EN-spans / 92 DE-spans
- Counter `data-target="8"` подтверждён

**Артефакты:** `index.html`, `assets/js/terminal.js`, `assets/css/layout.css`
**Откатный тег:** `v2-pre-px006` → `aa5b0dd`

**Hans Landa замечания (учтены):**

- 🔴 «1h reply» юридический риск → disclaimer «business hours Mon–Fri 09–19 CET»
- 🔴 «3d ship» зависит от типа → disclaimer «landings & MVPs — complex SaaS quoted separately»
- 🟡 counter 9 vs 8 рассинхрон → исправлен в той же PX
- 🟡 terminal.js animation ритм → новые токены протестированы локально, не выходят за контейнер
- 🟡 вариант C (terminal-style) не выбран — нет конфликта с hero terminal

---

### [S007] — 2026-04-28 — PX-005: Финальный список 8 проектов в порядке CEO

**Роли:** #1 Viktor (lead) · #3 Andrei (JSON+JS) · #14 Landa (review)
**Статус:** завершено (commit `c18967e`, откат-тег `v2-pre-px005` → `576cc14`)
**Скилл:** dispatching-parallel-agents (P10-research через Explore-агента 8× source folders)

**Задача CEO:** зафиксировать ровно 8 проектов в строгом порядке, BauPreis на 1-й позиции featured, MONO исключить.

**Финальный порядок:**

1. BauPreis AI SaaS (featured) — https://baupreis.ais152.com
2. Eko-OYLIS Bulgaria — https://eco-oylis.info
3. Rund ums Haus Littawe — https://rundumshaus-littawe.de
4. StormGuard Professional V2 — https://www.stormguardprofessional.eu/
5. EDMI — https://aidancompton001.github.io/edmi-landing/variant-d.html
6. Provenly Homes — https://aidancompton001.github.io/provenly-homes/
7. Studio of Glamour — https://glamour.ais152.com/
8. YY-DGUV Prüfservice (новый) — https://aidancompton001.github.io/yy-dguv/

**Что сделано:**

- Перезаписан `data/projects.json` массивом из 8 записей в строгом порядке CEO. MONO удалён.
- Все summaries/taglines/stacks взяты из исходных папок (CLAUDE.md / README.md / package.json) через P10-агента — не выдумано.
- Slugs нормализованы: `eko-oylis` → `eko-oylis-ua`, `stormguard` → `stormguard-v2`.
- Добавлен новый SVG-mark `mark-yy-dguv` (молния, символ электробезопасности) в `assets/marks.svg`.
- Создан плейсхолдер-скриншот `assets/projects/yy-dguv-placeholder.svg` (тёмный фон Editorial Ink + коралловый mark + caption «PRÜFSERVICE · WERNAU») — пока нет реального превью YY-DGUV.
- Cache-bust `?v=2026-04-28-px005` в index.html.

**Тест (Phase 4 step 1):** Python-валидатор проверяет (1) ровно 8 записей, (2) точный порядок slug'ов, (3) BauPreis featured + order=1, (4) MONO отсутствует, (5) все 8 имеют summary_en/de + tagline_en/de + url + status + mark + tags. **Passed.**

**Артефакты:** `data/projects.json`, `assets/marks.svg`, `assets/projects/yy-dguv-placeholder.svg`, `index.html`
**Откатный тег:** `v2-pre-px005` → `576cc14` (запушен на origin)

**Следующие шаги (open):**

- Реальные скриншоты YY-DGUV → отдельная PX (когда production задеплоится)
- BauPreis subdomain `baupreis.ais152.com` — CEO подтвердил, что задеплоен (если нет — карточка ведёт в никуда)
- StormGuard на live = V1 (V2 rebuild ещё не на проде); карточка позиционирует как V2 в названии + tagline. Совпадение «название vs реальный сайт» — точка триггера для отдельной PX когда V2 пойдёт live.

---

### [S006] — 2026-04-28 — PX-004: Унификация карточек + маскировка cookie-баннеров

**Роли:** #2 Lena (CSS) · #3 Andrei (verify) · #14 Landa (review)
**Статус:** завершено (commit `576cc14`, откат-тег `v2-pre-px004` → `22691c3`)

**Жалоба CEO:**
- Карточки разной ширины и aspect-ratio — выглядит как нарезка случайных скринов
- Cookie-баннеры в кадре скриншотов (StormGuard, Eko-OYLIS, RundUmsHaus)
- Тёмные пустоты под изображением
- Карусель работает (это не баг)

**Корень (systematic-debugging Phase 1):**
- `.card.layout-{feature,wide,square,tall,tile}` имели разные `flex-basis` и разные `aspect-ratio` на `.card-media` — это и был «зоопарк размеров»
- `.card-link { height: 100% }` + `.card-body { flex: 1 }` → тянутся до высоты самой высокой карточки трека (layout-tall) → пустоты у square/wide
- Скриншоты — full-page снимки реальных продакшен-сайтов с cookie-баннерами в кадре

**Что сделано:**
- `.card` → одна ширина для всех: `clamp(360px, 38vw, 520px)`; mobile `clamp(300px, 80vw, 480px)`
- Удалены 5 layout-классов (.layout-feature/wide/square/tall/tile) — оставлен `.is-featured` как content marker
- `.card-media` → одна aspect-ratio 16:10 для всех
- `.card-img` → `object-position: center top` + filter brightness/contrast/saturate под тёмную палитру
- `.card-media::before` — top vignette 22% (`var(--bg)` → transparent) маскирует cookie-баннеры
- `.card-media::after` — bottom vignette 28% маскирует footers/sticky CTAs + плавный fade в body
- `.card-link { align-self: start }` + `.card-body { без flex:1 }` → высота карточки = высота её контента, без тёмных пустот
- Карусель (.work-pin/.work-track horizontal pinned scrub) **не тронута**
- Cache-bust → `?v=2026-04-28-px004`

**Артефакты:** `assets/css/components.css`, `index.html`
**Откатный тег:** `v2-pre-px004` → `22691c3` (запушен на origin)

**Следующие шаги:** если CEO хочет полностью убрать cookie-баннеры (не просто замаскировать) — отдельная PX с чистыми скриншотами от CEO в `assets/projects/{slug}.webp`.

---

### [S005] — 2026-04-28 — PX-003: Deploy v2 (Editorial Ink) на production

**Роли:** #1 Viktor (lead) · #3 Andrei (deploy/verify) · #2 Lena (font/visual) · #14 Hans Landa (pre-merge gate)
**Статус:** завершено

**Что сделано:**
- Скачаны и положены self-hosted шрифты: `assets/fonts/Mona-Sans.woff2` (529 KB, variable wdth/wght/opsz/ital), `assets/fonts/JetBrainsMono-Regular.woff2` (92 KB), 2× LICENSE (OFL 1.1).
- Раскомментирован `@font-face` в `assets/css/tokens.css` (строки 143-159) — variable axes теперь живые на hover.
- og-image.jpg (55 KB) + apple-touch-icon.png (3 KB) сгенерированы Claude Desktop через `scripts/generate-brand-images.py` — теги `<meta og:image>`, `<meta twitter:image>`, `<link rel="apple-touch-icon">` восстановлены в `index.html`.
- Cache-busters `?v=2026-04-27-v2` → `?v=2026-04-28` во всех 15 ссылках на CSS/JS в `index.html`.
- DSGVO-grep: 0 ссылок на `fonts.googleapis.com` / `fonts.gstatic.com` в продакшен-файлах (упоминания в datenschutz.html — текст «не используем», легально).
- `data/projects.json`: 8 проектов, schema валидна.
- i18n-grep: index.html — 90/90 пар `data-lang-en`/`data-lang-de`. Legal-страницы (impressum=DE, 404=EN) — одноязычные дизайнерским решением Desktop, принято как есть.
- Откат-тег `v1-pre-redesign` создан на `7568a39` (текущий live SHA до v2).

**Ключевые решения:**
- Mona Sans variable (529 KB) выбран вместо subset — CEO утвердил «делаем круто»; performance budget 200KB пробит сознательно ради вариативных осей wdth/wght/opsz/ital.
- Web3Forms fallback оставлен с placeholder-ключом `YOUR_WEB3FORMS_ACCESS_KEY` — primary FormSubmit работает, fallback неактивен (TODO для отдельной PX).
- og-image.jpg оставлен в JPG (Desktop сгенерировал) — для будущего перегенера: `python3 scripts/generate-brand-images.py`.
- Locked-правило «one-file» в CLAUDE.md обновлено на multi-asset реальность (см. CLAUDE.md tech stack).

**Артефакты (этот деплой):**
`assets/fonts/Mona-Sans.woff2`, `assets/fonts/JetBrainsMono-Regular.woff2`, `assets/fonts/LICENSE-Mona-Sans.txt`, `assets/fonts/LICENSE-JetBrainsMono.txt`, `assets/og-image.jpg`, `assets/apple-touch-icon.png`, `scripts/generate-brand-images.py`, обновлённые `assets/css/tokens.css` и `index.html`, обновлённый `CLAUDE.md`, новый `STATUS.md`, обновлённый `docs/tasks/PX_REGISTRY.md`.

**Open issues (не блокеры):**
- Web3Forms access key — placeholder.
- Lighthouse baseline (PX-002a Open Question) — не измерен.
- impressum/datenschutz/404 — одноязычные (DE/DE/EN); EN-перевод impressum/datenschutz желателен для туристов (отдельная PX).
- og-image — auto-generated; CEO может заменить на кастомный позже.

**Следующие шаги:** Lighthouse baseline → отдельная PX-004; Web3Forms API key — отдельная PX (триггер: первый отказ FormSubmit).

---

### [S004] — 2026-04-27 — PX-002: Полный редизайн (multi-file static)

**Роли:** #1 Viktor Neumann (lead), #2 Lena Richter (UI/CSS), #3 Andrei Volkov (FE/JS), #14 Hans Landa (review pending)
**Статус:** P2 build complete, ожидает локальную верификацию CEO + cache-bust + push.

**Что сделано:**
- Заменил 1056-строчный single-file `index.html` на multi-file архитектуру: 5 CSS, 5 JS, 1 main HTML + 2 legal pages + 404 + data folder.
- Все `<div role="link" onclick="window.open()">` карточки заменены на нативные `<a target="_blank">` (фикс жалобы CEO «не все CTA кликаются»).
- Удалён Google Fonts CDN (DSGVO violation, BGH 2022 LG München I 3 O 17493/20). Сейчас сайт работает на system font stack — переход на self-hosted Inter + JetBrains Mono описан в `assets/fonts/README.md`.
- GSAP 3.12.5 + ScrollTrigger через cdnjs (industry standard, см. CREATIVE_TOOLKIT.md). Lenis 1.1.14 сохранён.
- Pinned horizontal scroll в Selected Work — `assets/js/main.js` подхватывает событие `ais:projects-rendered` от `projects.js`, инициализирует ST pin/scrub. Vertical-stack fallback при `prefers-reduced-motion`.
- Контактная форма: FormSubmit.co primary + Web3Forms fallback (фикс жалобы «форма не отправляется» — её попросту не было).
- WhatsApp FAB sticky bottom-right + DSGVO 2-click модальное окно перед `wa.me/4915563675772` (фикс жалобы «WhatsApp не работает» — FAB'а не было).
- `data/projects.json` + JSON Schema + `data/README.md` инструкция «добавить проект за 30 секунд». **Никаких правок HTML/CSS/JS для нового кейса не требуется.**
- Билингвальность EN/DE сохранена + `<html lang>` обновляется динамически + `<title>` синхронится из `<meta name="title-en|de">` через lang.js.
- Impressum + Datenschutz страницы (TMG §5 / DSGVO Art. 13) с `[TODO CEO]` маркерами для реального адреса/USt-IdNr.
- Удалены все buzzwords: «AI-powered», «Senior-level. Fast. Done right.», «Replace the staff you can't find» — переписано на инженерный тон.
- 404.html, favicon.svg, BUILD.md (single-doc deploy guide для CEO).
- Roadmap-файл `docs/tasks/PX-002a_audit_and_roadmap.md` с полным аудитом баг-листа, performance budget, KPI, DSGVO gate, fallback-матрица.

**Ключевые решения:**
- Multi-file overrides «single-file» правило из CLAUDE.md — обоснование: 1056 строк inline было неподдерживаемо. Документировано в BUILD.md.
- Тёмная палитра `#0A0A0B` + лайм `#C8FF00` — близко к исходному бренду, фон чуть теплее.
- System font stack как default — DSGVO-safe из коробки. Inter+JBMono — upgrade path, не блокер.
- GSAP CDN, не self-host — компромисс задокументирован в `datenschutz.html § 2.6`.
- StudioGlamour URL уже мигрирован на `glamour.ais152.com` (per PX-001).

**Артефакты (созданы/перезаписаны):**
`index.html`, `impressum.html`, `datenschutz.html`, `404.html`, `assets/css/{tokens,base,layout,components,motion}.css`, `assets/js/{main,projects,form,whatsapp,lang}.js`, `assets/fonts/README.md`, `assets/projects/README.md`, `assets/favicon.svg`, `data/{projects.json,projects.schema.json,README.md}`, `BUILD.md`, `docs/tasks/PX-002a_audit_and_roadmap.md`

**Не тронуто:** `CNAME`, `concept-*.html` (×8), `assets/*-site.jpg`, `assets/baupreis-dashboard.png`, `CLAUDE.md`, `TEAM.md`.

**Следующие шаги для CEO:**
1. `cd c:\Projects\AiS152 && npx serve .` (или `python3 -m http.server 8000`) → открыть `http://localhost:8000` → проверить desktop+mobile, EN/DE, форма, FAB.
2. Submit тестовой формы → подтвердить email FormSubmit (одноразово).
3. (Опционально) Web3Forms access key → вставить в `assets/js/form.js` строка `WEB3FORMS_KEY`.
4. Заменить `[TODO CEO]` маркеры в `impressum.html` + `datenschutz.html` (адрес + USt-IdNr или Kleinunternehmer-Hinweis).
5. (Опционально) Скачать Inter + JetBrainsMono WOFF2 → `assets/fonts/` → раскомментировать `@font-face` блок в `tokens.css`.
6. Cache-bust (script в BUILD.md) → `git add . && git commit -m "feat: full redesign — multi-file static" && git push origin master`.
7. Lighthouse mobile после deploy → цели: Perf ≥ 90, A11y ≥ 95, BP = 100, SEO ≥ 90.

**Open issues (не блокеры):**
- Миграция скриншотов `assets/*-site.jpg` → `assets/projects/{slug}.jpg` (отложено, JSON ссылается на legacy paths).
- OG image `assets/og-image.jpg` (1200×630) — упомянут в `<meta>`, файл ещё нужно создать.
- `apple-touch-icon.png` — упомянут в head, не критично.
- Lighthouse baseline не замерен (network egress в этой сессии заблокирован).
- Cross-browser Safari iOS не протестирован (нет устройства в сессии).

> DEVLOG updated: S004

---

### [S003] — 2026-04-27 — PX-002: Промпт для Claude Desktop (полный редизайн)

**Роли:** #1 Chief Methodologist (создание), #14 Hans Landa (adversarial review — 15 правок применены)
**Статус:** завершено
**Задача:** [PX-002](docs/tasks/PX_REGISTRY.md#px-002)

**Что сделано:**
- Сформирована ТС1 → Hans Landa review → APPROVED_WITH_CHANGES (15 замечаний)
- ТС2 интегрировала все правки Ланды + требование CEO «легко добавлять проекты» → утверждена CEO
- Создан `prompts/CLAUDE_DESKTOP_REDESIGN.md` (541 строк, единый файл с 3 фазами P0/P1/P2 и STOP-маркерами)
- Создан `prompts/README.md` (инструкция использования)
- Создан `prompts/.tests/verify_prompt.sh` — автотест на обязательные маркеры (26 проверок)
- Прогон тестов: **26/26 passed**

**Ключевые решения:**
- 1 файл вместо 3 — по решению CEO (Landa предлагал 3 ради контекст-окна Desktop, CEO отверг как избыточное)
- Data-driven каталог проектов (`data/projects.json` + JSON Schema + README) — добавление нового кейса = 1 запись в JSON, без правок HTML/CSS/JS
- Антиобход STOP через машинный маркер `=== WAITING_FOR_CEO_OK ===`
- KPI «next-level» переведены в числа: ≥3 ScrollTrigger + pinned + SplitText + magnetic + marquee + counter
- Performance budget: CSS ≤60KB, JS ≤120KB, LCP ≤2.5s, CLS ≤0.1, TBT ≤200ms
- Fallback-матрица 7 сценариев (ais152 down → Wayback, FormSubmit лимит → Web3Forms, и т.д.)
- DSGVO: self-host WOFF2, BGH 2022 цитата, WhatsApp 2-click, Hans Landa = owner pre-merge gate

**Артефакты:** `prompts/CLAUDE_DESKTOP_REDESIGN.md`, `prompts/README.md`, `prompts/.tests/verify_prompt.sh`, `docs/tasks/PX_REGISTRY.md` (статус)

**Следующие шаги:**
- CEO подставляет `{TODO_WHATSAPP}` и `{TODO_EMAIL_FORMSUBMIT}` → запускает в Claude Desktop
- Сам редизайн пойдёт как PX-003 (исполняется в Claude Desktop, не в Claude Code)

> DEVLOG updated: S003

---

### [S002] — 2026-04-17 — PX-001: Портфолио обновлено + миграция на GitHub Pages

**Роли:** #1 Chief Methodologist (MainCore)
**Статус:** завершено
**Задача:** [PX-001](docs/tasks/PX-001_portfolio_update.md)

**Что сделано:**
- P0 анализ: изучены все затрагиваемые файлы, проверены URL 6 проектов, найдены блокеры
- BLOCKER-1 (StudioGlamour 404) — решён: сайт живёт на custom domain `glamour.ais152.com`, а не на github.io
- BLOCKER-2 (скриншоты) — решён: Puppeteer 24.41.0 скрипт, 6 скриншотов 1600x900 JPG q85
- Удалён Twitter 4.0 (placeholder, не сайт)
- Обновлён EDMI: новый скриншот, тег "Landing · Website", ссылка на variant-d.html (финальный лендинг)
- Добавлены 5 новых проектов: StormGuard, Eko-OYLIS, RundUmsHaus, Provenly Homes, Studio of Glamour
- BauPreis AI и MONO Men Only оставлены без изменений
- Stat "Projects Delivered": 4+ → 8+
- Все карточки двуязычные (EN/DE), все ссылки проверены live
- Миграция хостинга: Hostinger → GitHub Pages (repo `aidancompton001/ais152`)
- CNAME настроен на ais152.com, DNS A-записи переведены на GitHub IPs
- AAAA (IPv6) запись Hostinger удалена для корректного resolve

**Ключевые решения:**
- 8 проектов в bento grid (4 ряда, паттерн 7/5 + 5/7) — layout не менялся, CSS классы переиспользованы
- EDMI ссылается на variant-d.html (Bento Grid) — финальный лендинг, выбранный CEO в S010 проекта EDMI
- GitHub Pages вместо Hostinger — автодеплой через git push, бесплатный HTTPS
- Скриншоты через Puppeteer, не вручную — воспроизводимо, одинаковое качество

**Проверенные URL проектов:**
| Проект | URL | Статус |
|--------|-----|--------|
| BauPreis AI | baupreis.ais152.com | ✅ |
| MONO Men Only | (нет public URL) | ✅ оставлен |
| EDMI | aidancompton001.github.io/edmi-landing/variant-d.html | ✅ |
| StormGuard | stormguardprofessional.eu | ✅ |
| Eko-OYLIS | eco-oylis.info | ✅ |
| RundUmsHaus | rundumshaus-littawe.de | ✅ |
| Provenly Homes | aidancompton001.github.io/provenly-homes | ✅ |
| Studio of Glamour | glamour.ais152.com | ✅ |

**Артефакты:**
- `index.html` — обновлённый портфолио (8 проектов)
- `assets/*-site.jpg` — 6 новых скриншотов
- `docs/tasks/PX-001_portfolio_update.md` — roadmap задачи
- `CNAME` — custom domain для GitHub Pages

**Коммиты:**
- `4720b41` — feat: replace portfolio with 8 real production projects (PX-001)
- `15f411c` — chore: add CNAME for ais152.com custom domain

**Следующие шаги:**
- Дождаться DNS propagation (TTL до 4ч) и проверить ais152.com
- Включить HTTPS enforcement после выпуска SSL сертификата
- Рассмотреть GA4 tracking и Schema.org structured data

---

### [S001] — 2026-03-19 — Развёртывание методологии V7.0

**Роли:** #1 Product Architect
**Статус:** завершено

**Что сделано:**
- CLAUDE.md создан по шаблону V7.0 из MainCore (адаптирован под static HTML portfolio)
- TEAM.md создан с 4 детальными профилями (#1 Viktor Neumann, #2 Lena Richter, #3 Andrei Volkov, #14 Hans Landa)
- CEO_PROMPTS.md добавлен (10 промптов P1-P10)
- Знания из Eko-OYLIS прогружены в TEAM.md (10 анимационных техник + архитектурные решения + критические уроки)
- Дизайн-система зафиксирована в CLAUDE.md (CSS tokens, шрифт Outfit, sharp corners стиль)

**Ключевые решения:**
- 4 роли вместо 8 — проект static HTML, backend/mobile/SRE не нужны
- Верификация = визуальная проверка в браузере (нет build/test pipeline)
- Concept файлы помечены как архив — не трогать без CEO

**Артефакты:** `CLAUDE.md`, `TEAM.md`, `CEO_PROMPTS.md`, `DEVLOG.md`

**Следующие шаги:**
- CEO определяет приоритеты: новый контент, деплой, доработка дизайна
- Выбрать хостинг (Cloudflare Pages / GitHub Pages / Hetzner)
- Добавить GA4 tracking (реальный ID)
- Рассмотреть Schema.org structured data для SEO
