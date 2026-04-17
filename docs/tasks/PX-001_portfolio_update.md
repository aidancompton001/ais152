# PX-001: Обновление портфолио — замена проектов на реальные сайты

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Дата:** 2026-04-17
**Статус:** P0 (анализ завершён, ожидает OK)
**Ответственный:** #1 Chief Methodologist
**Размер:** M
**Скилл:** writing-plans

**Цель:** Портфолио AiS152 отображает реальные завершённые проекты CEO с живыми ссылками, актуальными описаниями и скриншотами.

**Архитектура:** Single-file HTML (index.html). Проекты отображаются в секции `#cases` через bento-grid (12-колоночная CSS grid). Каждая карточка — `.bento-card` с изображением, мета-тегами, заголовком, описанием, метриками и ссылкой. Все тексты двуязычные (EN/DE через `data-lang-*`).

---

## АНАЛИЗ ТЕКУЩЕГО СОСТОЯНИЯ

### Что сейчас на портфолио (4 карточки в bento-grid):

| # | Проект | Тег | Год | Ссылка | Решение |
|---|--------|-----|-----|--------|---------|
| 1 | BauPreis AI | SaaS · AI | 2026 | baupreis.ais152.com | **ОСТАВИТЬ** (реальный проект) |
| 2 | MONO Men Only | Mobile · iOS · Android | 2026 | нет | **ОСТАВИТЬ** (реальный проект, нет public URL) |
| 3 | EDMI | Mobile · AI | 2026 | нет | **ОБНОВИТЬ** — в списке 6, добавить описание landing |
| 4 | Twitter 4.0 | Automation · n8n | 2026 | нет | **УДАЛИТЬ** — не сайт, не в списке 6 |

### Что нужно добавить (6 проектов CEO):

| # | Проект | URL | Статус URL | Описание |
|---|--------|-----|-----------|----------|
| 1 | StormGuard | https://www.stormguardprofessional.eu/ | ✅ Живой | E-commerce pet cosmetics (organic care, dogs & cats) |
| 2 | Eko-OYLIS | https://eco-oylis.info | ✅ Живой | Landing page — сбор/вывоз отработанных масел (Болгария) |
| 3 | RundUmsHaus | https://rundumshaus-littawe.de/ | ✅ Живой | Hausmeisterservice + Gartenpflege (Osnabrück) |
| 4 | StudioGlamour | https://glamour.ais152.com/ | ✅ Живой (custom domain) | Beauty salon — eyelash studio Munich (Next.js + Tailwind + shadcn/ui) |
| 5 | Provenly Homes | https://aidancompton001.github.io/provenly-homes | ✅ Живой | Short-term rental management (Köln, NRW) |
| 6 | EDMI | https://aidancompton001.github.io/edmi-landing/variant-d.html | ✅ Живой (final) | Dental microscope landing — Bento Grid (Variant D Final, CEO selected) |

### Итоговый состав портфолио (после изменений):

| Позиция | Проект | Grid class | Ссылка |
|---------|--------|-----------|--------|
| 1 | BauPreis AI | bc (span 7) | baupreis.ais152.com |
| 2 | MONO Men Only | bc2 (span 5) | нет |
| 3 | StormGuard | bc3 (span 5) | stormguardprofessional.eu |
| 4 | Eko-OYLIS | bc4 (span 7) | eco-oylis.info |
| 5 | RundUmsHaus | bc (span 7) | rundumshaus-littawe.de |
| 6 | Provenly Homes | bc2 (span 5) | provenly-homes (GitHub Pages) |
| 7 | EDMI (landing) | bc3 (span 5) | edmi-landing/variant-d.html (GitHub Pages) |
| 8 | StudioGlamour | bc4 (span 7) | glamour.ais152.com |

---

## БЛОКЕРЫ

### ~~BLOCKER-1: StudioGlamour~~ — РЕШЁН ✅

**Было:** URL `https://aidancompton001.github.io/studioglamour/` → 404 (lowercase, wrong case).
**Факт:** Сайт живёт на custom domain `https://glamour.ais152.com/` (CNAME настроен). Деплой работает, последний run успешен 2026-03-19.
**Рекомендация:** Включить HTTPS enforcement в настройках repo (Settings → Pages → Enforce HTTPS).

### ~~BLOCKER-2: Скриншоты~~ — РЕШЁН ✅

**Решение:** Puppeteer 24.41.0 (уже установлен) — автоматический скрипт, 6 скриншотов, 1600x900, JPG quality 85.

---

## АНАЛИЗ ПОСЛЕДСТВИЙ

### Какие файлы затронуты:
- `index.html` — секция `#cases` (строки ~757-846): HTML карточек
- `index.html` — CSS `.bc/.bc2/.bc3/.bc4` (строки ~363-367): возможно добавить `.bc5-.bc8` если более 4 карточек
- `index.html` — JS тilt-эффект на `.bento-card` (строки ~1068-1080): автоматически подхватит новые карточки через `querySelectorAll`
- `assets/` — новые изображения для 5 добавляемых проектов
- `index.html` — stat counter "4+" → "8+" (строка ~682)

### Что БЫЛО → что СТАНЕТ:
- **Секция Cases:** 4 карточки (BauPreis, MONO, EDMI, Twitter 4.0) → 7-8 карточек (+ StormGuard, Eko-OYLIS, RundUmsHaus, Provenly Homes, опционально StudioGlamour)
- **Bento grid:** 2 ряда → 4 ряда (паттерн 7/5 + 5/7 повторяется)
- **Stat "Projects Delivered":** `data-t="4"` → `data-t="8"` (или сколько карточек)
- **Twitter 4.0:** удалена из HTML
- **EDMI:** описание обновлено (landing вместо mobile app)

### Что может поплыть/сломаться:
- **Responsive (900px):** Все `.bc*` → `grid-column: span 1` — работает для любого количества карточек ✅
- **Responsive (1024px):** Все `.bc*` → `span 12` — каждая на всю ширину ✅
- **3D Tilt JS:** `querySelectorAll('.bento-card')` — подхватит автоматически ✅
- **Scroll Reveal:** `.rv` классы — нужно добавить на новые карточки
- **Bento grid gap:** 14px gap — без изменений ✅
- **Якоря/навигация:** `#cases` anchor — не затронут ✅
- **Lenis smooth scroll:** Не затронут ✅

### Breakpoints:
- **375px (mobile):** bento → single column, все ок
- **768px (tablet):** bento → single column (breakpoint 900px), все ок  
- **1440px (desktop):** bento → 12-column grid с 7/5 и 5/7 чередованием, нужно убедиться что CSS-классы корректны для 4 рядов

---

## ROADMAP

### Task 1: Скриншоты сайтов (автоматический скрипт Puppeteer)

**Инструмент:** Puppeteer 24.41.0 (установлен)
**Действие:** Node.js скрипт делает скриншоты 6 сайтов:

```js
// scripts/screenshots.mjs
import puppeteer from 'puppeteer';
import path from 'path';

const sites = [
  { name: 'stormguard-site',      url: 'https://www.stormguardprofessional.eu/' },
  { name: 'eko-oylis-site',       url: 'https://eco-oylis.info' },
  { name: 'rundumshaus-site',     url: 'https://rundumshaus-littawe.de/' },
  { name: 'provenly-homes-site',  url: 'https://aidancompton001.github.io/provenly-homes' },
  { name: 'edmi-landing-site',    url: 'https://aidancompton001.github.io/edmi-landing/variant-d.html' },
  { name: 'studioglamour-site',   url: 'https://glamour.ais152.com/' },
];

const browser = await puppeteer.launch({ headless: true });
const page = await browser.newPage();
await page.setViewport({ width: 1600, height: 900 });

for (const { name, url } of sites) {
  console.log(`📸 ${name} — ${url}`);
  await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
  await new Promise(r => setTimeout(r, 2000)); // wait for animations
  await page.screenshot({
    path: path.resolve('assets', `${name}.jpg`),
    type: 'jpeg',
    quality: 85,
    clip: { x: 0, y: 0, width: 1600, height: 900 },
  });
}

await browser.close();
console.log('✅ Done — 6 screenshots saved to assets/');
```

**Запуск:** `cd c:/Projects/AiS152 && node scripts/screenshots.mjs`
**Результат:** 6 файлов в `assets/` (JPG, 1600x900, quality 85)
**Проверка:** Открыть каждый файл, убедиться что контент корректный

### Task 2: Удалить Twitter 4.0 из index.html

**Files:** Modify: `index.html:828-845`
**Что:** Удалить блок `<!-- Twitter 4.0 -->` `.bento-card.bc4`
**Проверка:** Секция #cases показывает 3 карточки

### Task 3: Обновить EDMI карточку

**Files:** Modify: `index.html:809-825`
**Что:**
- Изменить тег: `Mobile · AI` → `Landing · Bento Grid`
- Обновить описание (EN/DE) — EDMI dental microscope landing (Variant D Final, Bento Grid)
- Добавить onclick → `https://aidancompton001.github.io/edmi-landing/variant-d.html`
- Описание EN: Apple-style bento grid landing for dental microscope & equipment store. 7 real microscopes (Zeiss, CJ-Optik), 11 accessories, AI configurator, product catalog with real pricing.
- Описание DE: Apple-Style Bento-Grid-Landing für Zahnmikroskop- und Geräteshop. 7 echte Mikroskope (Zeiss, CJ-Optik), 11 Zubehörteile, KI-Konfigurator, Produktkatalog mit realen Preisen.
- Добавить метрику "Visit site →"
- Заменить скриншот на `assets/edmi-landing-site.jpg`

### Task 4: Добавить StormGuard карточку

**Files:** Modify: `index.html` (после EDMI, новый `.bento-card.bc4`)
**Данные:**
- Тег: `E-commerce · Organic`
- Год: 2025
- Заголовок: StormGuard Professional
- Описание EN: Organic pet care e-commerce. Professional shampoos & conditioners for dogs and cats. Multi-language (EN/DE/BG), product catalog, order system.
- Описание DE: Bio-Tierpflege E-Commerce. Professionelle Shampoos & Conditioner für Hunde und Katzen. Mehrsprachig (EN/DE/BG), Produktkatalog, Bestellsystem.
- Ссылка: https://www.stormguardprofessional.eu/
- Метрики: "3 Languages" / "Organic" / "E-commerce"
- Изображение: `assets/stormguard-site.jpg`

### Task 5: Добавить Eko-OYLIS карточку

**Files:** Modify: `index.html` (новый `.bento-card.bc`)
**Данные:**
- Тег: `Landing · Business`
- Год: 2025
- Заголовок: Eko-OYLIS
- Описание EN: Business landing page for waste oil collection services. Custom design with contact form, service showcase, and mobile-optimized layout.
- Описание DE: Business-Landingpage für Altöl-Sammelservice. Individuelles Design mit Kontaktformular, Leistungsübersicht und mobil-optimiertem Layout.
- Ссылка: https://eco-oylis.info
- Метрики: "Bulgaria" / "Static Site" / "FormSubmit.co"
- Изображение: `assets/eko-oylis-site.jpg`

### Task 6: Добавить RundUmsHaus карточку

**Files:** Modify: `index.html` (новый `.bento-card.bc2`)
**Данные:**
- Тег: `Website · Service`
- Год: 2025
- Заголовок: RundUmsHaus Littawe
- Описание EN: Premium marketing website for house maintenance and garden care services. SEO-optimized, responsive design, service catalog with direct contact integration.
- Описание DE: Premium-Website für Hausmeister- und Gartenpflegedienste. SEO-optimiert, responsives Design, Leistungskatalog mit direkter Kontaktintegration.
- Ссылка: https://rundumshaus-littawe.de/
- Метрики: "Osnabrück" / "German" / "SEO"
- Изображение: `assets/rundumshaus-site.jpg`

### Task 7: Добавить Provenly Homes карточку

**Files:** Modify: `index.html` (новый `.bento-card.bc3`)
**Данные:**
- Тег: `Landing · Real Estate`
- Год: 2026
- Заголовок: Provenly Homes
- Описание EN: Short-term rental management platform. Property owner onboarding, three service tiers, automated pricing, guest communication — all from Cologne.
- Описание DE: Kurzzeitvermietungs-Management. Eigentümer-Onboarding, drei Servicestufen, automatisierte Preisgestaltung, Gästekommunikation — aus Köln.
- Ссылка: https://aidancompton001.github.io/provenly-homes
- Метрики: "Köln, NRW" / "3 Tiers" / "Rental Mgmt"
- Изображение: `assets/provenly-homes-site.jpg`

### Task 8: Добавить StudioGlamour карточку

**Files:** Modify: `index.html` (новый `.bento-card.bc4`)
**Данные:**
- Тег: `Website · Beauty`
- Год: 2026
- Заголовок: Studio of Glamour
- Описание EN: Eyelash extension studio website for Munich. Service catalog with pricing, online booking, gallery, and mobile-first design. Built with Next.js, Tailwind CSS, and shadcn/ui.
- Описание DE: Website für Wimpernstudio in München. Leistungskatalog mit Preisen, Online-Buchung, Galerie und Mobile-First-Design. Gebaut mit Next.js, Tailwind CSS und shadcn/ui.
- Ссылка: https://glamour.ais152.com/
- Метрики: "Munich" / "Next.js" / "shadcn/ui"
- Изображение: `assets/studioglamour-site.jpg`

### Task 9: Обновить статистику "Projects Delivered"

**Files:** Modify: `index.html:682`
**Что:** `data-t="4"` → `data-t="8"` (или 7 если без StudioGlamour)

### Task 10: Добавить CSS классы для дополнительных рядов bento

**Files:** Modify: `index.html` (CSS секция, ~строка 363)
**Что:** CSS классы `.bc`–`.bc4` уже определены и повторяются. Для 4 рядов используем тот же паттерн:
- Ряд 1: `.bc` (7) + `.bc2` (5) — BauPreis + MONO
- Ряд 2: `.bc3` (5) + `.bc4` (7) — EDMI + StormGuard
- Ряд 3: `.bc` (7) + `.bc2` (5) — Eko-OYLIS + RundUmsHaus  
- Ряд 4: `.bc3` (5) + `.bc4` (7) — Provenly Homes + StudioGlamour

Нового CSS не требуется — классы переиспользуются.

### Task 11: Тестирование

**Действия:**
1. Открыть index.html в браузере (desktop 1440px)
2. Проверить все карточки отображаются корректно
3. Проверить ВСЕ ссылки открывают живые сайты
4. Переключить язык EN → DE, проверить тексты
5. Проверить mobile (375px) — карточки в одну колонку
6. Проверить tablet (768px)
7. Проверить 3D tilt работает на новых карточках
8. Проверить scroll reveal анимация на новых карточках

### Task 12: Commit

```bash
git add index.html assets/
git commit -m "feat: replace portfolio with 7-8 real production projects

- Remove Twitter 4.0 placeholder
- Update EDMI with landing page link
- Add StormGuard, Eko-OYLIS, RundUmsHaus, Provenly Homes
- Add StudioGlamour (if unblocked)
- Update project count stat 4→8
- All links verified live"
```

---

## ЧЕКЛИСТ ПРИЁМКИ

- [ ] Twitter 4.0 удалён из портфолио
- [ ] BauPreis AI остался без изменений
- [ ] MONO Men Only остался без изменений
- [ ] EDMI обновлён с описанием landing + ссылкой
- [ ] StormGuard добавлен с живой ссылкой и скриншотом
- [ ] Eko-OYLIS добавлен с живой ссылкой и скриншотом
- [ ] RundUmsHaus добавлен с живой ссылкой и скриншотом
- [ ] Provenly Homes добавлен с живой ссылкой и скриншотом
- [ ] StudioGlamour добавлен с живой ссылкой glamour.ais152.com и скриншотом
- [ ] Скриншоты сделаны Puppeteer-скриптом (6 файлов в assets/)
- [ ] Статистика "Projects Delivered" обновлена
- [ ] Все ссылки открываются в новой вкладке
- [ ] Оба языка (EN/DE) корректны для всех карточек
- [ ] Desktop (1440px): bento-grid отображается корректно
- [ ] Mobile (375px): карточки в одну колонку
- [ ] 3D tilt и scroll reveal работают на новых карточках
- [ ] Общий дизайн/layout НЕ изменён
