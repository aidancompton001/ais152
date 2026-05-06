# PX-011 — Quiz Landing «Какие соцсети нужны вашему бизнесу»

**Дата:** 2026-05-03
**Статус:** P0 (roadmap, ждёт ОК CEO)
**Ответственный:** #1 Product Architect
**Скилл:** ui-ux-pro-max + brainstorming
**Размер:** L (20 итераций)
**Источник:** [PX-011 в PX_REGISTRY](PX_REGISTRY.md#px-011), ТЗ [quiz-spec.md](quiz-spec.md)

---

## Анализ последствий

### Затрагиваемые файлы

**Создаётся (новое):**
- `quiz.html` — новая страница, доступная по `/quiz` (через GitHub Pages clean URL)
- `assets/css/quiz.css` — стили только для квиза (не загружаются на главной)
- `assets/js/quiz.js` — логика квиза (state, scoring, render)
- `data/quiz-questions.json` — 15 вопросов + варианты ответов (вынесено для отдельного редактирования)
- `data/quiz-matrix.json` — 4 матрицы промежуточных выводов
- `data/quiz-platforms.json` — 11 карточек платформ + минимальные требования
- `data/quiz-scoring.json` — таблицы баллов Q1-Q15 × 11 платформ
- `assets/js/quiz-telegram.js` — обработка Telegram Login Widget callback
- `apps-script/Code.gs` — Apps Script Web App (хранится в репо для версии, деплой вручную)

**Модифицируется:**
- `index.html` — добавить ссылку «Quiz» в навигацию (один `<a>`)
- `datenschutz.html` — параграф о сборе данных через квиз (Telegram ID + ответы) для GDPR
- `sitemap.xml` — добавить `/quiz` URL
- `robots.txt` — без изменений (Allow всё)

**Не трогается:**
- `concept-*.html` (8 концептов), `404.html`, `impressum.html`
- Существующие CSS/JS (`base.css`, `hero.css`, `tokens.css`, `main.js`, `form.js`, etc.)
- `data/projects.json`

### БЫЛО → СТАНЕТ

| Что | БЫЛО | СТАНЕТ |
|-----|------|--------|
| Страниц на сайте | 4 (index, impressum, datenschutz, 404) | 5 (+ quiz) |
| Каналов лидогенерации | 1 (форма на index → FormSubmit) | 2 (форма + квиз → Telegram + Sheets) |
| Telegram-ботов проекта | 0 | 1 (`AisQuizBot`) |
| Backend-зависимостей | 0 (FormSubmit external) | 1 (Apps Script Web App) |
| GDPR-документ | Покрывает только форму | Покрывает форму + квиз |

### Риски / что может сломаться

1. **Lighthouse score** — новая страница не должна тянуть тяжёлые скрипты на главной (изоляция CSS/JS)
2. **Telegram Login Widget script** — внешний `https://telegram.org/js/telegram-widget.js` подгружается только на `/quiz`, не на index (CSP/privacy)
3. **Apps Script CORS** — Web App должен отдавать правильные заголовки для POST из браузера
4. **Apps Script rate limit** — 20k вызовов/день (бесплатный лимит) — для квиза с заполнением раз в N минут хватит надолго
5. **GDPR** — без обновления `datenschutz.html` и явного opt-in рискуем нарушением (Google Sheets — US-резидентность данных)
6. **Состояние при F5** — потеря прогресса; решение: localStorage (опционально, не блокер для MVP)

### Breakpoints (адаптив)

- **375px** (mobile) — основная цель: текст вопроса читается, варианты по 1 в столбец, кнопки 44px+
- **768px** (tablet) — 2 варианта в строку, увеличенные карточки платформ
- **1024px** (desktop) — централизованный контейнер max-width 720px (читаемость)
- **1440px+** (large) — без изменений (контейнер не растягивается)

### Затронутые системы (якоря, навигация, JS, анимации)

- ✅ Навигация index.html — добавляется ссылка `/quiz` (минимальный риск)
- ✅ JS квиза изолирован в `quiz.js` (не загружается на главной)
- ✅ Анимации перехода между вопросами (CSS transitions, no GSAP — экономим вес)
- ✅ Lenis smooth scroll — НЕ нужен на /quiz (квиз = пошаговый, без скролла)
- ✅ Tokens из `tokens.css` переиспользуются (Editorial Ink palette)

### Тесты

- **Unit-уровня:** скоринг (валидация для 6 ниш Q1 × 5 типов Q2 = 30 комбинаций минимум)
- **Trigger-тесты:** триггер каждого выхода (A, B, C) минимум по разу
- **Manual UAT:** проход по всем 15 вопросам в браузере + проверка Telegram-уведомления
- **Mobile responsive:** Chrome DevTools на 375 / 768 / 1024
- **GDPR:** прохождение БЕЗ согласия → ошибка / прохождение С согласием → норм

---

## Roadmap (28 шагов)

### Фаза 1 — Подготовка backend (Telegram + Sheets)

1. Создать Telegram-бота `AisQuizBot` через @BotFather → получить bot token
2. Привязать домен `ais152.com` к боту через @BotFather (`/setdomain` для Login Widget)
3. Получить chat_id CEO (через @userinfobot или getUpdates)
4. Создать Google Sheet «AisQuizLeads» с колонками: timestamp, telegram_user_id, telegram_username, name, photo_url, q1-q15, exit_type, top_platforms
5. Создать Apps Script проект, привязанный к этому Sheet
6. Написать Web App endpoint POST: верификация Telegram-подписи + запись в Sheet + отправка уведомления CEO
7. Деплой Apps Script как Web App (Anyone access, новая версия)
8. Записать Web App URL + bot token в `.env.local` и в `data/quiz-config.json` (только bot username и Web App URL — без секретов)

### Фаза 2 — Frontend HTML/CSS

9. Создать `quiz.html` — структура: `<head>` (meta, OG, Plausible) + `<body>` с одним контейнером `#app`
10. Создать `assets/css/quiz.css` — переиспользует `tokens.css` (Editorial Ink), стили для: hero, lead capture, question screen, progress bar, intermediate screen, final screens A/B/C, platform cards
11. Адаптив 375 / 768 / 1024 — flex/grid с media queries
12. Hero-секция: заголовок «Какие соцсети нужны вашему бизнесу», подзаголовок, кнопка «Пройти квиз»
13. Lead capture screen: Telegram Login Widget + чекбокс GDPR + privacy policy ссылка

### Фаза 3 — Frontend JS логика

14. Создать `assets/js/quiz.js` — модуль с state object: `{currentScreen, answers, scoring, telegramUser}`
15. Загрузка `data/quiz-questions.json`, `data/quiz-matrix.json`, `data/quiz-scoring.json`, `data/quiz-platforms.json` через fetch
16. Render question screen: блок, прогресс-бар (1/15), вопрос, варианты single-choice, кнопки Назад/Далее
17. Render intermediate screen: вычисление по матрицам (Q1+Q2 / Q5+Q6 / Q9 / Q11+Q12+Q13)
18. Скоринг engine: накопление баллов по 11 платформам через все 15 ответов
19. Финал-логика: проверка C → B → A (по спеке секция «ПОРЯДОК ПРОВЕРКИ»)
20. Render final screen: 3 варианта (A/B/C) с топ-2 карточками платформ + первый шаг
21. Кнопка «Пройти заново» → reset state
22. POST в Apps Script Web App: timestamp + telegram_user + answers + scoring + exit_type
23. Plausible analytics events: `quiz_started`, `question_N_answered`, `quiz_completed`, drop-off на каждом вопросе

### Фаза 4 — Интеграция и тесты

24. Прогон всех 6 ниш Q1 × несколько Q2 → проверка скоринга и матриц промежуточных выводов
25. Триггер каждого выхода (A, B, C) по тестовым комбинациям
26. Mobile responsive проверка (Chrome DevTools 375 / 768 / 1024)
27. Прохождение полного цикла: лид в Sheet записан + CEO получил Telegram-уведомление

### Фаза 5 — Деплой и документация

28. Update `index.html` (ссылка nav), `datenschutz.html` (GDPR параграф), `sitemap.xml` (+/quiz). Push в main → GitHub Pages auto-deploy → DEVLOG запись + KB update

---

## Чеклист приёмки

- [ ] `quiz.html` доступен по `https://ais152.com/quiz`
- [ ] Hero + кнопка «Пройти квиз» работают
- [ ] Telegram Login Widget виден, авторизация работает (логин в @AisQuizBot)
- [ ] GDPR чекбокс блокирует старт без согласия
- [ ] 15 вопросов отображаются с прогресс-баром
- [ ] Кнопка «Назад» работает на каждом вопросе (кроме блока 1 Q1)
- [ ] Кнопка «Далее» неактивна без выбора ответа
- [ ] 4 промежуточных экрана показывают корректные тексты по матрицам
- [ ] Финал триггерит выход C при условии (Q14=sales + Q15=now + Q12=b_zero + Q11=t_low)
- [ ] Финал триггерит выход B когда платформа из top-2 требует > ресурса
- [ ] Финал триггерит выход A в остальных случаях с топ-2 карточками
- [ ] POST в Apps Script записал лид в Google Sheet (timestamp, tg_user, all 15 answers, exit, top-2)
- [ ] CEO получил Telegram-уведомление в чате с резюме лида
- [ ] Mobile 375 / tablet 768 / desktop 1024 — адаптив без горизонтального скролла
- [ ] Lighthouse mobile ≥ 90 на всех 4 KPI (Performance / Accessibility / Best Practices / SEO)
- [ ] `datenschutz.html` обновлён (раздел про квиз)
- [ ] `sitemap.xml` содержит `/quiz`
- [ ] `index.html` имеет ссылку на квиз в навигации
- [ ] DEVLOG запись + Obsidian KB update (Tasks and Roadmap + Problems and Decisions при необходимости)
- [ ] Тег отката `v2-pre-px011` создан до деплоя

---

## Открытые риски / TODO

1. **Apps Script secrets** — bot token хранится в Apps Script Properties (не в репо). Документировать процесс ротации.
2. **Telegram Login Widget без HTTPS на dev** — локальная разработка через `localtunnel` или тестировать прямо на проде через preview branch
3. **localStorage для прогресса** — опционально, не в скоупе MVP. Если CEO захочет — отдельная PX
4. **EN-перевод квиза** — отдельная PX (сейчас только RU)
5. **Privacy policy update** — нужно согласование с CEO формулировки (GDPR-compliant)

---

> KB: updated [[01_Projects/AiS152/Tasks and Roadmap]]
