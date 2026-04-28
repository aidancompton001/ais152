# Task Registry — AiS152

> Пронумерованный реестр всех PX-задач от CEO.

## Как пользоваться

1. Перед добавлением — посмотри последний номер PX-NNN
2. Нумерация — продолжай с последнего + 1
3. Формат — копируй PX-формулировку AS IS
4. Статус — обновляй при завершении

---

## PX-001

**Дата:** 2026-04-17
**Статус:** новая
**DEVLOG:** —
**Источник:** чат MainCore, PX-формулировка CEO

**Задача:** Обновление портфолио AiS152 — замена проектов на реальные сайты с живыми ссылками и скриншотами
**Контекст:** `C:\Projects\AiS152` — портфолио-сайт на ais152.com. Данные проектов (JSON/HTML), секция портфолио, изображения.
**Проблема:** Сейчас на портфолио устаревшие или placeholder-проекты. У CEO уже есть 6 реальных завершённых сайтов на production, но портфолио на них не ссылается и не показывает их.
**Цель:** Портфолио отображает 6 реальных проектов с живыми ссылками, актуальными описаниями и скриншотами каждого сайта.
**Скоуп:**
- Изучить текущее состояние ais152.com — какие проекты сейчас показаны, какая структура данных
- Определить формат карточек проектов (заголовок, описание, ссылка, скриншот, теги/стек)
- Заменить/добавить 6 реальных проектов:
  1. **StormGuard** — e-commerce pet cosmetics (URL уточнить из проекта)
  2. **Eko-OYLIS** — landing page (GitHub Pages)
  3. **RundUmsHaus** — Hausmeisterservice сайт
  4. **StudioGlamour** — beauty salon (GitHub Pages)
  5. **Provenly Homes** — aidancompton001.github.io/provenly-homes
  6. **EDMI** — лендинг (URL уточнить из проекта)
- Сделать скриншоты каждого сайта (desktop + mobile, или как подходит под текущий дизайн портфолио)
- Для каждого проекта: название, краткое описание, стек/теги, живая ссылка, скриншот
- Убрать старые/фейковые проекты которых больше нет
**Ограничения:**
- НЕ менять общий дизайн/layout портфолио — только контент проектов
- URL каждого сайта проверить что он живой перед добавлением
- Скриншоты должны быть актуальными (с текущего production)
- Если на портфолио есть проекты которые реально существуют — оставить, не удалять
**Рекомендуемый промпт:** P0 (сначала анализ текущего состояния + roadmap, потом исполнение)

---

## PX-002

**Дата:** 2026-04-27
**Статус:** ✅ выполнено 2026-04-27
**DEVLOG:** AiS152 DEVLOG.md + MainCore DEVLOG.md S016
**Артефакт:** `prompts/CLAUDE_DESKTOP_REDESIGN.md` (541 строк, 26/26 тестов passed)
**Источник:** чат MainCore, PX-формулировка CEO

**Задача:** Создать deployment-style промпт для Claude Desktop (skills: ui-ux-pro-max + design:user-research) на полный редизайн портфолио AiS152 — next-level визуал уровня gsap.com + рабочая интерактивность (клики, WhatsApp, форма)
**Контекст:**
- Проект **AiS152** — портфолио CEO, production: https://ais152.com, исходники: `c:\Projects\AiS152`
- Стек: Static HTML/CSS/JS, хостинг GitHub Pages (менять НЕЛЬЗЯ — иначе ломается деплой)
- Контент: 6 реальных проектов из PX-001 (StormGuard, Eko-OYLIS, RundUmsHaus, StudioGlamour, Provenly Homes, EDMI) — данные актуальны, проблема в подаче
- Артефакт PX-002 = **сам длинный промпт-документ** для Claude Desktop (по образцу DGUV-примера), а не редизайн. Редизайн пойдёт отдельной задачей через готовый промпт.
**Проблема:**
- Текущий дизайн ais152.com обычный — не передаёт уровень CEO как создателя 9 production-проектов
- Интерактив сломан: не все кнопки/ссылки кликаются, WhatsApp-кнопка не работает, контактная форма не отправляется
- Нет «вау-эффекта» уровня gsap.com (горизонтальный scroll-progress, инженерная плавность анимаций)
**Цель:** Готовый промпт-документ (`prompts/CLAUDE_DESKTOP_REDESIGN.md` или аналог), который при вставке в Claude Desktop запустит:
1. **P0-этап:** аудит текущего ais152.com — анализ структуры, стека, что работает / что сломано → roadmap-файл → стоп до ОК CEO
2. **Дизайн-этап:** концепт уровня gsap.com / Linear / Vercel в индивидуальном стиле AiS152 (палитра, типографика, lay-out)
3. **Реализация:** GSAP + Lenis (Закон 19 разрешённый toolkit), горизонтальный scroll-progress как ключевая фишка, hover-микроинтеракции, reveal — уровень L2
4. **Починка интерактива:** каждая ссылка/CTA кликается, WhatsApp FAB → `wa.me/{TODO_номер_CEO}`, контактная форма через бесплатный сервис без backend (рекомендуется FormSubmit.co — проверено в Eko-OYLIS)
**Скоуп (что промпт должен содержать):**
- Роль исполнителя (ведущий дизайнер + frontend-архитектор, ui-ux-pro-max + design:user-research skills)
- Амбиция (next-level портфолио инженера, не «шаблон Webflow»)
- Reference: https://gsap.com (горизонтальный scroll-progress + Lenis-плавность) — впитать тон, не копировать
- Стилевые ориентиры: gsap.com, Linear, Vercel (только техника типографики/spacing, не визуал)
- Обязательный аудит текущего сайта перед редизайном (P0-логика: roadmap → ОК → исполнение)
- Структура страниц портфолио (hero / проекты / обо мне / контакты — точное содержание уточнит CEO в P0)
- Анимации: стек GSAP + Lenis + ScrollTrigger; горизонтальный progress-scroll, stagger reveal, hover-микроинтеракции, counter-анимация; `prefers-reduced-motion` обязателен
- Палитра + типографика: 2-3 варианта токенов в `:root` для выбора CEO
- Интерактив:
  - WhatsApp FAB sticky (правый низ, все страницы), `wa.me/{TODO_номер_CEO}` с placeholder
  - Контактная форма через FormSubmit.co (или аналог без оплаты/backend)
  - Все ссылки на 6 проектов из PX-001 — живые, проверенные
- a11y: WCAG AA, semantic landmarks, alt, aria-label, focus states, keyboard nav 100%, prefers-reduced-motion
- Responsive: mobile-first, breakpoints 640/1024/1440, sticky-CTA-bar на mobile
- DSGVO-минимум: self-hosted шрифты WOFF2 (Google Fonts CDN запрещён в DE), cookie-banner только если подключается аналитика, WhatsApp 2-click-warning по DSGVO
- Запрещения для Claude Desktop: Framer Motion, AOS, ScrollMagic, Locomotive, тяжёлый WebGL — только Закон 19 toolkit
- Запрещения по контенту: stock-фото, AI-баззворды («innovative», «AI-powered», «next-gen»), фейковые отзывы
- Стек НЕ менять: Static HTML/CSS/JS + GitHub Pages
- Формат вывода Claude Desktop: README + структура папок + карта применённых техник + open questions для CEO
**Ограничения:**
- Промпт пишется под возможности **Claude Desktop** (не Code) — учитывать его tool-set: WebFetch для аудита ais152.com, Filesystem MCP для чтения `c:\Projects\AiS152`, design-skills (ui-ux-pro-max, design:user-research)
- Стек AiS152 фиксирован (Static HTML/CSS/JS, GitHub Pages) — никакого Next.js/React
- Контент 6 проектов из PX-001 НЕ удалять — только репрезентация меняется
- WhatsApp номер = placeholder `{TODO_номер_CEO_подставит}`
- Форма = бесплатный сервис (FormSubmit.co рекомендуется), без платных backend
**Рекомендуемый промпт:** P1 (исполнение по чёткому ТЗ — написание длинного промпт-документа как артефакта)

---

## PX-003

**Дата:** 2026-04-28
**Статус:** ✅ выполнено 2026-04-28
**DEVLOG:** AiS152 DEVLOG.md S005
**Откат-тег:** `v1-pre-redesign` → `7568a39`
**Источник:** чат AiS152, PX-формулировка CEO (после реверса задачи: v2-сайт от Claude Desktop уже на диске)

**Задача:** Деплой нового v2-сайта AiS152 на production (ais152.com) + локальная верификация + настройка вариативного шрифта Mona Sans + создание/наполнение Obsidian-папки проекта
**Контекст:**
- **Проект:** `c:\Projects\AiS152` — Claude Desktop уже перезаписал `index.html` + `impressum.html` + `datenschutz.html` + `404.html` новой v2-версией (Editorial Ink палитра, terminal-панель в hero, dot grid canvas, magazine-layout карточек, custom SVG marks-sprite)
- **Новая структура assets:** `assets/css/{tokens,base,layout,components,motion,hero,marks}.css`, `assets/js/{lang,dotgrid,terminal,projects,form,whatsapp,main}.js`, `assets/fonts/README.md`, `assets/marks.svg`, `assets/favicon.svg`
- **Данные:** `data/projects.json` (v2 — добавлены поля `layout`, `mark`), `data/projects.schema.json`
- **Документы:** `BUILD.md` (deploy guide от Desktop), `DEVLOG.md` обновлён, `docs/tasks/PX-002a_audit_and_roadmap.md` создан
- **Не тронуты:** `concept-*.html × 8` (архив дизайн-итераций), `CLAUDE.md`, `TEAM.md`, `CNAME`, скриншоты проектов в `assets/*-site.jpg` + `baupreis-dashboard.png`
- **Деплой:** GitHub Pages, домен `ais152.com` (CNAME уже настроен — коммит `15f411c chore: add CNAME for ais152.com custom domain`)
- **Старый сайт:** перезаписан, доступен только через git-историю
- **Obsidian:** папка `01_Projects/AiS152/` отсутствует — создать с нуля
**Проблема:**
- v2 лежит на диске, но **не задеплоен** — production (ais152.com) до сих пор показывает старую версию
- v2 **не верифицирован визуально** — никто не открывал `npx serve .` и не проверял что hero terminal печатает код, dot grid реагирует на курсор, magazine-layout рендерится корректно, EN/DE переключение работает, формы и WhatsApp кнопка не сломаны
- Mona Sans (вариативный шрифт) **не установлен** — без него `font-variation-settings` hover-эффекты no-op, сайт смотрится беднее задуманного
- Obsidian-папка проекта отсутствует — некуда складывать артефакты, Task Registry не синхронизирован с проектным
**Цель:**
- v2-сайт верифицирован локально (desktop + mobile, EN + DE, все интеракции живые) — без визуальных багов и сломанной функциональности
- Mona Sans (Mona-Sans.woff2) скачан, положен в `assets/fonts/`, `@font-face` в `assets/css/tokens.css` раскомментирован, hover-эффекты с variable axes работают
- v2 задеплоен на production — `https://ais152.com` показывает новую версию (Editorial Ink + terminal hero + magazine grid)
- Obsidian-папка `01_Projects/AiS152/` создана со структурой-зеркалом проектной (Tasks, Design, Plans, Reports, Research, Inbox), индексной заметкой `AiS152.md`, и `Task Registry.md` синхронизированным с `docs/tasks/PX_REGISTRY.md` (PX-001, PX-002, PX-002a, PX-003)
- Финальный отчёт CEO: чек-лист верификации + ссылка на live + diff Obsidian
**Скоуп:**
1. **Локальная верификация v2 (перед деплоем):**
   - запустить `npx serve .` в `c:\Projects\AiS152`, открыть `http://localhost:3000`
   - desktop (1440px) + mobile (375px) viewport: hero terminal печатает код, тики переключают файлы, dot grid реагирует на курсор, magazine layout (featured → square → tall → wide → 2 tile → square → wide final) рендерится, coral-glyphs наклоняются на hover карточек, H1 уплотняется при скролле
   - переключение EN ↔ DE на всех страницах (`index.html`, `impressum.html`, `datenschutz.html`, `404.html`)
   - все CTA кликаются, формы валидируются, WhatsApp-кнопка открывает корректный `wa.me/{номер}` (CEO подтверждает номер если placeholder)
   - проверка консоли браузера на JS-ошибки
   - чек-лист с галочками
2. **Установка Mona Sans:**
   - скачать `Mona-Sans.woff2` с https://github.com/github/mona-sans/releases
   - положить в `assets/fonts/Mona-Sans.woff2`
   - раскомментировать `@font-face` в `assets/css/tokens.css`
   - повторно проверить hover-эффекты (вариативные оси работают)
   - аналогично для JetBrains Mono если в `assets/fonts/README.md` указан (для terminal-панели)
3. **Деплой на production:**
   - `git status` → закоммитить только релевантные файлы (исключить случайный мусор)
   - conventional commit `feat: deploy v2 site (editorial ink + terminal hero + magazine grid)`
   - `git push` в `master` → GitHub Pages подхватит
   - проверить `https://ais152.com` через 2-5 минут — live совпадает с локалью
   - проверить `https://ais152.com/impressum.html`, `https://ais152.com/datenschutz.html`, `https://ais152.com/404.html` (последний через несуществующий путь)
4. **Obsidian-папка проекта:**
   - через MCP Obsidian: создать `01_Projects/AiS152/` с подпапками `Tasks/`, `Design/`, `Plans/`, `Reports/`, `Research/`, `Inbox/`
   - индексная заметка `AiS152.md`: обзор проекта, ссылка на live (ais152.com), стек, ссылка на репозиторий, текущий статус, контакты
   - `Task Registry.md` — копия `docs/tasks/PX_REGISTRY.md` AS IS (PX-001, PX-002, PX-003) + структура заголовков
   - найти и перенести в `Inbox/` или соответствующие подпапки разбросанные AiS152-заметки в vault, если такие есть
5. **Регистрация PX-003:**
   - `docs/tasks/PX_REGISTRY.md` (проект) + `01_Projects/AiS152/Task Registry.md` (Obsidian) — обе записи под одним PX-003
6. **Финальный отчёт:** чек-лист верификации (все галочки), ссылка на live, ссылка на коммит, скриншот-обзор Obsidian-папки, список открытых вопросов если что-то не сработало
**Ограничения:**
- **НЕ трогать дизайн/контент v2.** Реализация Claude Desktop остаётся как есть. Только верификация + шрифт + деплой.
- **НЕ трогать `concept-*.html` × 8** — это архив.
- **НЕ удалять старые ассеты** (`assets/baupreis-dashboard.png`, `assets/*-site.jpg`) — они используются в v2 через `data/projects.json`.
- **`CLAUDE.md` правило «one-file locked»** — фактически уже нарушено новой структурой `assets/css/`+`assets/js/`. Обновить `CLAUDE.md` под новую multi-asset реальность КОРОТКО, в рамках этой PX (без полного переосмысления).
- **WhatsApp номер:** если в `assets/js/whatsapp.js` стоит placeholder — перед деплоем CEO должен подтвердить реальный номер либо явно ОК запустить с placeholder.
- **FormSubmit/Web3Forms endpoint:** если в `assets/js/form.js` placeholder — то же самое, ОК CEO до деплоя.
- **Двуязычность EN/DE** обязана работать на всех 4 страницах (index, impressum, datenschutz, 404) — блокер для деплоя.
- **DSGVO:** проверить что Google Fonts CDN не используется, шрифты self-hosted (`assets/fonts/`).
- **Откат:** перед деплоем — пометить текущий live-коммит тегом `v1-pre-redesign` для быстрого роллбэка.
- **Obsidian:** НИКОГДА не перезаписывать существующие заметки — только создавать новые / добавлять.
**Рекомендуемый промпт:** **P1** (исполнение по чёткому плану — сайт уже готов, нужны конкретные шаги: проверить → положить шрифт → закоммитить → запушить → завести Obsidian → отчитаться). Размер: **L**.

---

<!-- Последний номер: PX-003 -->
