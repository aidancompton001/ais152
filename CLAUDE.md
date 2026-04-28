# CLAUDE.md — AiS152

## Владелец проекта

**Пользователь = CEO проекта.** Его слово — закон. Все решения CEO имеют абсолютный приоритет. Команда выполняет указания CEO без обсуждения.

**Второй после CEO: #1 Product Architect** — правая рука CEO, координатор команды. Несёт персональную ответственность за качество всех задач.

---

## Проект

**Название:** AiS152 — AI Systems & Automation Portfolio
**Тип:** Portfolio / Landing Page
**Описание:** Персональный сайт-портфолио фрилансера/студии AiS1.52 — разработка AI-powered приложений, мобильных платформ и автоматизация процессов. Showcasing: BauPreis AI, MONO, EDMI, Twitter 4.0. Двуязычный (EN/DE), тёмная тема, кастомный курсор, Aurora-эффекты, scroll-анимации.
**Локация:** Мюнхен, Германия
**Языки:** English (основной) + Deutsch
**Домен:** https://ais152.com
**Контакт:** ebaias.muc@gmail.com, +49 155 636 75 772

---

## Документация

| Файл | Назначение | Когда читать |
|------|-----------|--------------|
| `CLAUDE.md` | Главный управляющий документ | Всегда (загружается автоматически) |
| `TEAM.md` | Команда: роли, страйки, увольнения | При запуске любого агента |
| `DEVLOG.md` | Журнал разработки | Старт/завершение сессии |
| `CEO_PROMPTS.md` | 10 промптов CEO для задач | При каждой задаче CEO |

---

## Tech Stack

| Слой | Технология | Статус |
|------|-----------|--------|
| Markup | HTML5 (multi-file: index + impressum + datenschutz + 404) | Locked v2 (PX-002/PX-003) |
| Стили | Vanilla CSS, разнесён в `assets/css/{tokens,base,layout,components,motion,hero,marks}.css` | Locked v2 |
| Скрипты | Vanilla JS, разнесён в `assets/js/{lang,dotgrid,terminal,projects,form,whatsapp,main}.js` | Locked v2 |
| Smooth Scroll + Animations | Lenis + GSAP + ScrollTrigger (CDN) | Locked v2 |
| Шрифты | Self-hosted WOFF2 — Mona Sans (variable wdth/wght/opsz/ital) + JetBrains Mono | Locked v2 (DSGVO) |
| Хостинг | GitHub Pages, домен ais152.com (CNAME) | Live |
| Языки | EN/DE на index, DE-only legal, EN-only 404 | Locked v2 |
| Данные | `data/projects.json` (8 проектов, JSON Schema валидация) | Locked v2 |

---

## Структура проекта

```
AiS152/
├── CLAUDE.md                # Главный управляющий документ
├── TEAM.md                  # Команда
├── DEVLOG.md                # Журнал разработки
├── CEO_PROMPTS.md           # Промпты CEO
├── index.html               # Основная страница (production)
├── concept-a.html           # Концепт A (архив дизайн-итераций)
├── concept-b.html           # Концепт B
├── concept-c.html           # Концепт C
├── concept-d.html           # Концепт D
├── concept-d-plus.html      # Концепт D+
├── concept-e.html           # Концепт E
├── concept-f.html           # Концепт F
├── concept-g.html           # Концепт G (Dark Aurora — основа для index.html)
└── assets/
    ├── baupreis-dashboard.png
    ├── edmi-1.jpg / edmi-2.jpg / edmi-3.jpg
    ├── mono-app-*.jpg
    ├── mono-p*.jpg
    ├── mono-slide-*.jpg
    └── twitter-screen.jpg
```

---

## ПРОТОКОЛ ФОРМАЛИЗАЦИИ ЗАДАЧ

> **CEO ставит задачу -> агент ОБЯЗАН выполнить протокол из промпта CEO.**
> **Без промпта CEO — агент читает этот раздел как минимальный стандарт.**

### 5-шаговый протокол (ЧИТАЙ -> ФОРМАЛИЗУЙ -> ДЕЛАЙ -> ПРОВЕРЬ -> ЗАПИШИ)

```
1. ЧИТАЙ    — Прочитай CLAUDE.md и TEAM.md. Изучи затрагиваемые файлы.
2. ФОРМАЛИЗУЙ — Назначь ответственного. Сформируй ТС. Покажи CEO, жди ОК.
3. ДЕЛАЙ    — Выполняй строго по ТС. Не расширяй скоуп.
4. ПРОВЕРЬ  — Открой в браузере. Desktop + Mobile. Проверь оба языка (EN/DE).
5. ЗАПИШИ   — Результат в DEVLOG.md. Покажи итог CEO.
```

**Нарушение любого шага = страйк. 2 страйка = увольнение.**

### Шаблон ТС (M / L / XL)

```
## ТС: [Краткое название]

**Ответственный:** #N — [Имя] — [Роль]
**Размер:** S / M / L / XL
**Скилл:** {какой скилл применён}

### Цель
[Одно предложение: что и зачем]

### Скоуп
**Включено:** [что входит]
**НЕ включено:** [что явно исключено]

### Критерии приёмки
- [ ] [Проверяемый критерий 1]
- [ ] [Проверяемый критерий N]

### Файлы
- [файлы для создания/изменения]

### Верификация
Открыть в браузере → desktop (1440px) → mobile (375px) → EN → DE
```

### Шаблон ТС (S)

```
## ТС: [Название]
**Ответственный:** #N | **Размер:** S
**Что сделать:** [1-2 предложения]
**Критерий:** [1 строка]
**Файлы:** [список]
```

### Размеры задач

| Размер | Описание | Бюджет итераций | ОК от CEO | Тесты |
|--------|---------|----------------|-----------|-------|
| **S** | 1 файл, <50 строк, CSS-правка, текст | 3 | Нет | Нет |
| **M** | Новая секция, компонент, i18n-блок | 7 | Да | Визуальная проверка |
| **L** | Редизайн секции, новая страница, новый case | 15 | Да | Desktop + Mobile + EN/DE |
| **XL** | Полный редизайн, новый стек, миграция | 25 | Да + Landa Review | Полный аудит |

**Бюджет превышен -> СТОП -> ждать CEO.**

---

## ВЕРИФИКАЦИЯ

| Размер | Что проверить | Готово когда |
|--------|-------------|-------------|
| **S** | Визуально в браузере | Нет ломаных стилей |
| **M** | Desktop + Mobile | Оба viewport корректны |
| **L** | Desktop + Mobile + EN/DE + Performance | Lighthouse 90+ Performance |
| **XL** | Всё от L + Landa ревью + Cross-browser | Chrome + Safari + Firefox OK |

**Нет галочек = не готово. Пропуск верификации = страйк.**

---

## ПРАВИЛА

### Команда
- Каждая задача = один ответственный из TEAM.md
- #1 Product Architect = правая рука CEO. Ведёт реестр замечаний
- 2 замечания = увольнение (без обсуждения)
- #14 Hans Landa = критический ревьюер (вызывается на XL и по запросу CEO)

### Скиллы (выбирает #1)
- UI/Дизайн/CSS -> `ui-ux-pro-max`
- Баг -> `systematic-debugging`
- Ревью -> `requesting-code-review`
- Параллельная работа -> `dispatching-parallel-agents`
- Перед "готово" -> `verification-before-completion`

### Числа (ЖЕЛЕЗНОЕ ПРАВИЛО)
> ВСЕ расчёты через скрипт (Python/Node.js). НИКОГДА в голове. Нарушение = увольнение.

### Git
- Conventional Commits: `type(scope): description`
- Типы: `feat`, `fix`, `refactor`, `style`, `docs`, `chore`
- Co-Authored-By: `Claude <noreply@anthropic.com>`

### Специфика проекта (Static HTML)
- **Один файл = один артефакт.** index.html содержит ВСЕ: HTML + CSS + JS (кроме Lenis CDN)
- **Нет сборки.** Нет npm, нет bundler. Файл открывается в браузере напрямую
- **Concept файлы = архив.** НЕ трогать concept-*.html без указания CEO
- **Двуязычность:** `data-lang-en` / `data-lang-de` атрибуты. Каждый текстовый элемент = 2 span
- **Анимации:** CSS @keyframes + IntersectionObserver scroll reveal. Respect `prefers-reduced-motion`
- **Кастомный курсор:** `.cur` + `.cur-ring` (desktop only, hidden on mobile)
- **Aurora-эффекты:** 4 orb gradient backgrounds с CSS animations
- **Performance:** Inline everything. Единственный внешний ресурс = Google Fonts + Lenis CDN

### ЗАПРЕЩЕНО (без исключений)
- Менять index.html без ТС (M+ задачи)
- Удалять concept файлы без указания CEO
- Добавлять npm/node_modules/build tools
- Менять цветовую палитру (--bg, --ac, --tx) без одобрения CEO
- Добавлять внешние JS-библиотеки без одобрения CEO
- Ломать двуязычность (каждый текст = EN + DE)
- Решать за CEO (хостинг, домен, контент, дизайн)

---

## ЖУРНАЛ (DEVLOG)

### Формат записи

```
### [SNNN] — ГГГГ-ММ-ДД — Заголовок (макс 60 символов)

**Роли:** #N Роль
**Статус:** завершено | частично | заблокировано

**Что сделано:**
- Результат 1 (не процесс!)

**Ключевые решения:**
- Решение — причина

**Артефакты:** `файл1`, `файл2`

**Следующие шаги:**
- Конкретное действие
```

---

## Риски

| # | Риск | Владелец | Стратегия |
|---|------|---------|-----------|
| 1 | Сломанные стили после правки inline CSS | #2 UI/CSS | Проверка desktop + mobile после каждого изменения |
| 2 | Потеря двуязычности (забыли DE или EN) | #3 Frontend | Чеклист: каждый текст = 2 span (en + de) |
| 3 | Тяжёлые изображения в assets/ | #2 UI/CSS | WebP, lazy loading, max 200KB per image |
| 4 | JS-ошибка блокирует весь сайт | #3 Frontend | Graceful degradation, CSS-only fallbacks |
| 5 | Нарушение протокола | #1 | Strike System: 2 страйка = увольнение |
| 6 | Потеря контекста | #1 | DEVLOG каждую сессию |

---

## Дизайн-система (Design Tokens)

```css
:root {
  --bg:   #070810;                    /* Фон: почти чёрный с синим оттенком */
  --sf:   rgba(255,255,255,0.04);     /* Surface: карточки, секции */
  --sf2:  rgba(255,255,255,0.07);     /* Surface hover */
  --bd:   rgba(255,255,255,0.07);     /* Border: разделители */
  --bdg:  rgba(200,255,0,0.28);       /* Border green: hover borders */
  --tx:   #F0F0F2;                    /* Text: основной текст */
  --mu:   rgba(240,240,242,0.42);     /* Muted: вторичный текст */
  --ac:   #C8FF00;                    /* Accent: лайм, CTA, выделения */
  --acd:  rgba(200,255,0,0.1);        /* Accent dim: фоны иконок */
}
```

**Шрифт:** Outfit (200-900), Google Fonts
**Border-radius:** 0px (sharp edges everywhere)
**Стиль:** Dark, brutalist-minimalist, sharp corners, lime accent

---

## CREATIVE ARSENAL — Протокол анимации и дизайна (Закон 19 MainCore)

> При ЛЮБОЙ задаче на дизайн, анимацию, визуал, UI/UX — обязательно сверься с арсеналом.

### Как использовать

1. **Прочитай справочник:** `Read c:\Projects\MainCore\core\CREATIVE_TOOLKIT.md`
2. **Определи уровень** по Decision Tree в справочнике:
   - L1 (GSAP + Lenis + Rive) — scroll, hover, transitions, kinetic typography
   - L2 (Three.js / R3F) — 3D модели, WebGL галереи
   - L3 (шейдеры, Blender, WebGPU) — полные 3D-миры
3. **Выбери инструменты** из арсенала (НЕ придумывай свои)
4. **Подключи** по рецепту из toolkit

### Быстрый старт (L1 — подходит для 90% задач)

```bash
npm i gsap lenis
```

```js
import Lenis from 'lenis'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
gsap.registerPlugin(ScrollTrigger)
const lenis = new Lenis()
lenis.on('scroll', ScrollTrigger.update)
gsap.ticker.add((time) => lenis.raf(time * 1000))
```

### 4 сценария

| CEO говорит | Агент делает |
|-------------|-------------|
| "Scroll-анимации" | Toolkit → GSAP + Lenis + ScrollTrigger. Рецепт 1-3 из toolkit |
| "Хочу как на этом сайте" | Toolkit → секция D (реверс-инжиниринг). AI Cloner или DevTools |
| "Крутой лендинг с нуля" | Toolkit → секция B (стартеры). Клонировать gcolombi/nextjs-starter |
| "3D модель продукта" | Toolkit → Spline (no-code) или Three.js/R3F |

### Guard

**Установка анимационной библиотеки НЕ из арсенала без обоснования = замечание.**

> Полный протокол: `c:\Projects\MainCore\laws\19_CREATIVE_ARSENAL.md`
> Полный справочник (30+ репо): `c:\Projects\MainCore\core\CREATIVE_TOOLKIT.md`
