# PX-015 — ElektroCheck Stuttgart portfolio entry (11 → 12)

**Дата:** 2026-05-25
**Статус:** P0 (roadmap, ждёт ОК CEO)
**Ответственный:** #1 Product Architect
**Скилл:** writing-plans
**Размер:** M (12 итераций)
**Источник:** [PX-015 в PX_REGISTRY](PX_REGISTRY.md#px-015)
**Шаблон:** [PX-014 Ofnstube](PX-014_ofnstube_portfolio_entry.md) + [PX-012 KONTUR](PX-012_kontur_portfolio_entry.md)

---

## Анализ последствий

### Затрагиваемые файлы

**Создаётся:**
- `assets/elektrocheck-site.jpg` — Playwright clean hero (live `https://elektrocheckstuttgart.de`)
- `verify/acceptance.json` — критерии приёмки PX-015 (полная замена под текущую задачу)

**Модифицируется:**
- `data/projects.json` — новый entry `order:2`, существующие 10 проектов сдвигаются `order +1`
- `index.html` — SVG-symbol `mark-elektrocheck` (Blitz/молния) + счётчик 11 → 12 в 6 локациях

**Не трогается:**
- `quiz.html`, `quiz.css`, `quiz.js`, `quiz-engine.js`, остальные страницы
- Ofnstube entry (PX-014) — `order:1` сохраняется
- Стили, шрифты, скрипты вне счётчика

### БЫЛО → СТАНЕТ

| Что | БЫЛО (после PX-014) | СТАНЕТ (после PX-015) |
|-----|----------------------|------------------------|
| Всего проектов | 11 | **12** |
| order:1 | Ofnstube | Ofnstube (без изменений) |
| order:2 | KONTUR | **ElektroCheck Stuttgart** (новый) |
| order:3..12 | POMP..YY_DGUV | KONTUR..YY_DGUV (сдвинуты +1) |
| Hero lead EN | «Eleven live projects» | «Twelve live projects» |
| Hero lead DE | «Elf Live-Projekte» | «Zwölf Live-Projekte» |
| Hero meta | «11 live» | «12 live» |
| Stats counter | `data-target="11"` | `data-target="12"` |
| Terminal | «11 projects» | «12 projects» |
| Work title EN | «Eleven things I shipped recently» | «Twelve things I shipped recently» |
| Work title DE | «Elf Dinge, kürzlich ausgeliefert» | «Zwölf Dinge, kürzlich ausgeliefert» |

### Риски

| Риск | Митигация |
|------|-----------|
| Lighthouse score падает из-за тяжёлой картинки | Hero JPEG quality 80, размер < 250 KB (как Ofnstube 208 KB) |
| Опечатка «Twelve»/«Zwölf» | AC14-AC15 в verify (точная сверка) |
| Случайно тронуть Ofnstube `order:1` | AC2 в verify (проверка order=1 для Ofnstube) |
| Пропуск 6-й локации счётчика | AC16 (старая цифра 11 не должна остаться) |
| Период в новом heading (Global Typography Rule) | AC17 (`check_no_periods_in_headings.py`) |
| 404 на новый URL | AC18 (fetch returns 200) |

### Breakpoints
- 375 (mobile) — карточка не ломает grid, тег `featured:true` корректно занимает первую строку
- 768 (tablet) — 2 столбца
- 1024+ (desktop) — стандартный grid

### Анимации / Якоря / JS
- Stats counter — JS читает `data-target` динамически; смена 11→12 безопасна
- Лента карточек строится из `projects.json` динамически (если есть js-генерация) — порядок берётся из `order`

### Тесты
17 критериев в `verify/acceptance.json` — структурные + типографика + live URL 200.

---

## Roadmap (15 шагов)

### Фаза 1 — Подготовка

1. `git tag v2-pre-px015` (rollback point до правок)
2. Прочитать `C:\Projects\ElektroCheck-Stuttgart\CLAUDE.md` + `DEVLOG.md` — извлечь: tagline DE/EN, summary DE/EN ≤280, tags, бренд-палитра
3. Открыть live `https://elektrocheckstuttgart.de/` через Playwright, проверить 200 + clean (no cookie banner mid-screen, no placeholders)
4. Сделать hero-скриншот → `assets/elektrocheck-site.jpg` (jpeg q90, < 250 KB)

### Фаза 2 — Данные

5. Прочитать `data/projects.json` целиком
6. Добавить новый entry ElektroCheck с `order:2, featured:true, layout:"feature"`
7. Сдвинуть существующие 10 entries (Ofnstube остаётся `order:1`; KONTUR 2→3, POMP 3→4, ..., YY_DGUV 11→12). Проверить через Node-скрипт: orders=[1..12], slug 'ofnstube' имеет order=1, 'elektrocheck' имеет order=2

### Фаза 3 — index.html

8. Найти и заменить 6 счётчиков 11 → 12:
   - Hero lead EN: `Eleven live projects` → `Twelve live projects`
   - Hero lead DE: `Elf Live-Projekte` → `Zwölf Live-Projekte`
   - Hero meta: `11 live` → `12 live`
   - Stats: `data-target="11"` → `data-target="12"`
   - Terminal: `11 projects` → `12 projects`
   - Work title EN: `Eleven things I shipped recently` → `Twelve things I shipped recently`
   - Work title DE: `Elf Dinge, kürzlich ausgeliefert` → `Zwölf Dinge, kürzlich ausgeliefert`
9. Добавить SVG-symbol `mark-elektrocheck` в `<defs>` (Blitz/молния — niche: Elektroprüfungen). Пример: `<symbol id="mark-elektrocheck" viewBox="0 0 24 24"><path d="M13 2 L4 14 L11 14 L10 22 L20 9 L13 9 L13 2 Z"/></symbol>`

### Фаза 4 — Верификация

10. Создать `verify/acceptance.json` с 17 критериями (см. Чеклист ниже)
11. Запустить `python verify/verify.py` — добиться **17/17 PASSED (100%)**, exit 0
12. Если FAIL → починить, перезапустить (без 100% задача не закрывается — Закон 21)

### Фаза 5 — Деплой

13. `git push origin v2-pre-px015` (tag)
14. `git add data/projects.json index.html assets/elektrocheck-site.jpg verify/acceptance.json && git commit -m "feat(portfolio): add ElektroCheck Stuttgart as #2, bump counter 11 → 12 (PX-015)" && git push origin master`
15. Через 60 сек проверить `https://ais152.com/` — карточка ElektroCheck видна на позиции `02 / 12`, ссылка ведёт на `https://elektrocheckstuttgart.de/`

---

## Чеклист приёмки (17 AC для verify/acceptance.json)

- [ ] **AC1** entry ElektroCheck в `data/projects.json` (slug)
- [ ] **AC2** Ofnstube остался `order:1` (не сломали PX-014)
- [ ] **AC3** ElektroCheck — `order:2`
- [ ] **AC4** Всего 12 проектов
- [ ] **AC5** Все order = 1..12 без пропусков и дубликатов
- [ ] **AC6** Tagline EN ≤ 280
- [ ] **AC7** Summary EN ≤ 280
- [ ] **AC8** Summary DE ≤ 280
- [ ] **AC9** URL = `https://elektrocheckstuttgart.de` (root, без `#main`)
- [ ] **AC10** Screenshot существует, > 10 KB
- [ ] **AC11** SVG-symbol `mark-elektrocheck` в index.html
- [ ] **AC12** Stats `data-target="12"`
- [ ] **AC13** Hero meta «12 live»
- [ ] **AC14** Terminal «12 projects»
- [ ] **AC15** Work title — Twelve / Zwölf (оба варианта)
- [ ] **AC16** Hero lead — Twelve / Zwölf (оба)
- [ ] **AC17** Старая цифра 11 не осталась нигде (data-target, «11 live», «Eleven», «Elf», «11 projects»)
- [ ] **AC18** Live `https://elektrocheckstuttgart.de` → 200
- [ ] **AC19** Типографика: 0 точек в h1-h4 (Global Rule, check_no_periods_in_headings.py)

(финальное число AC = 19; первоначальная оценка 17 уточнена в чеклисте)

---

## Открытые вопросы (закрыты CEO 2026-05-25)

1. ✅ «Обнови инфу на сайте» = счётчик 11→12 + всё связанное (стандартный паттерн PX-014)
2. ✅ SVG mark — #1 Product Architect решает (выбор: Blitz/молния как иконка Elektroprüfungen)
3. ✅ PX-014 Ofnstube — закрыта, deployed, счётчик уже = 11

---

> KB: skip — state-only update (P0 = roadmap-файл, не knowledge)
