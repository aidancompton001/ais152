# DEVLOG.md — AiS152

## Журнал разработки

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
