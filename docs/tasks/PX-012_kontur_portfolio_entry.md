# PX-012 — KONTUR Portfolio Entry (Selected Work #1)

**Дата:** 2026-05-22
**Статус:** в работе → завершено
**Формализация:** self-formalized по запросу CEO (2026-05-22)
**Сложность:** S (один JSON-entry + SVG mark + count-update, по контракту секции Selected Work)

---

## Цель

Добавить новый проект **KONTUR** (`https://kontur.ais152.com`) в портфолио AiS152, поставить **первым** в Selected Work, написать описание EN/DE, обновить счётчик проектов 9 → 10, чтобы посетители ais152.com сразу видели и могли открыть новый кейс.

## Контекст

- KONTUR создан 2026-05-22 — кастомная WordPress + WooCommerce тема для вымышленной немецкой specialty-кофейной Rösterei. Production-сайт, портфолио-кейс. Рождён из MainCore PX-021 / T028, концепт A «KONTUR» (Editorial Roastery).
- Сайт **уже LIVE** на `https://kontur.ais152.com` (KONTUR STATUS.md S011, T001 завершён, go-live смоук пройден, SSL валиден).
- AiS152 — статический портфолио-сайт. Source of truth для проектов: `data/projects.json`, рендер `assets/js/projects.js`. Счётчик «9» захардкожен в `index.html` в нескольких местах.

## Проблема

- KONTUR отсутствует в `data/projects.json` → не виден на ais152.com
- Счётчик проектов в `index.html` показывает 9 (hero lead, hero-meta, terminal, stats counter, work section title, about-параграф) — после добавления должно быть 10

## Скоуп

**Включено:**
- Свежий чистый hero-скриншот kontur.ais152.com → `assets/kontur-site.jpg` (✅ снят Playwright, верифицирован: 0 console errors, 0 placeholders, production-quality)
- Новый entry в `data/projects.json` — `order: 1`, `featured: true`, `layout: "feature"`; остальные 9 проектов сдвигаются `order +1`
- Новый SVG-symbol `mark-kontur` в спрайте `index.html`
- Обновление счётчика 9 → 10 во всех местах `index.html` (EN + DE)

**НЕ включено:**
- Изменения на самом сайте KONTUR (он отдельный проект, уже live)
- Изменение `projects.js` логики рендера (контракт «один JSON-entry» соблюдается)

## Технические требования

- `data/projects.json` соответствует `data/projects.schema.json`
- Описания EN + DE — реальные, из STATUS/CLAUDE.md KONTUR (WordPress, WooCommerce, кастомная тема, кофе-Abo, немецкое e-commerce-право)
- Скриншот ≤ ~150 KB (как другие карточки)

## Критерии приёмки

- [x] `assets/kontur-site.jpg` существует, чистый hero, без cookie-баннера
- [x] `data/projects.json` — KONTUR `order:1`, остальные сдвинуты, валидный JSON
- [x] `mark-kontur` symbol добавлен в `index.html` sprite
- [x] Счётчик 9 → 10 обновлён везде: hero lead EN/DE, hero-meta, terminal commits-строка, stats `data-target`, work section title EN/DE, about параграф EN/DE
- [x] Локальная проверка рендера — KONTUR первой карточкой
- [x] Commit + push → GitHub Pages deploy

## Артефакты

- `data/projects.json` (MODIFY)
- `index.html` (MODIFY — sprite + 8 count-мест)
- `assets/kontur-site.jpg` (CREATE)
- `assets/kontur-fullpage-reference.png` (CREATE — reference, не на сайте)
- `docs/tasks/PX-012_kontur_portfolio_entry.md` (этот файл)
- `docs/tasks/PX_REGISTRY.md` (MODIFY — запись PX-012)

## DEVLOG

S-запись после завершения.
