# Сверка кратких описаний проектов на ais152.com с файлами проектов — 2026-09-11

Источник текстов: `C:\Projects\AiS152\data\projects.json`. Взяты записи со status `live`, кроме stormguard-v2 и edmi: 13 проектов.
Проверены поля tagline_de, tagline_en, summary_de, summary_en, tags и url. Одинаковые DE/EN-утверждения объединены в одну строку, в колонке «поле» указано, где оно встречается.
Источники подтверждения: CLAUDE.md, STATUS.md, DEVLOG.md, docs/, verify/ и код проекта. Переписку client-communication как источник не использовали. Пути в колонке «источник» даны относительно папки проекта, если не указан абсолютный путь.
Коды url получены так: `curl -s -o /dev/null -L --max-time 25 -w "%{http_code} %{num_redirects} %{url_effective}" <url>`, 11.09.2026, с машины CEO (Windows, Git Bash curl).
Вердикты посчитаны скриптом `gen_audit.py` по строкам таблицы ниже. Файлы проектов не менялись.

## Сводка

| slug | папка | утверждений | CONFIRMED | CONTRADICTED | NOT_FOUND |
|---|---|---|---|---|---|
| staskiewitz | `C:\Projects\Staskiewitz` | 17 | 17 | 0 | 0 |
| hennerheede | `C:\Projects\HennerHeede-Site` | 23 | 15 | 8 | 0 |
| taxi-moennigmann | `C:\Projects\Taxi-Moennigmann` | 21 | 17 | 2 | 2 |
| sorrysara | `C:\Projects\SorrySara` | 23 | 17 | 4 | 2 |
| silkekleinart | `C:\Projects\SilkeKleinArt` | 18 | 15 | 1 | 2 |
| ofnstube | `C:\Projects\Ofnstube` | 17 | 12 | 4 | 1 |
| elektrocheck-stuttgart | `C:\Projects\ElektroCheck-Stuttgart` | 18 | 14 | 3 | 1 |
| kontur | `C:\Projects\KONTUR` | 18 | 15 | 2 | 1 |
| pomp | `C:\Projects\POMP` | 19 | 18 | 1 | 0 |
| baupreis | `C:\Projects\BauPreis AI SaaS` | 16 | 12 | 3 | 1 |
| eko-oylis-ua | `C:\Projects\Eko-Oylis-UA` | 16 | 14 | 2 | 0 |
| rundumshaus | `C:\Projects\RundUmsHaus` | 17 | 16 | 1 | 0 |
| provenly-homes | `C:\Projects\fr_02_Provenly Homes` | 18 | 13 | 2 | 3 |
| **Итого** | | **241** | **195** | **33** | **13** |

## Таблица утверждений

| slug | поле | утверждение | вердикт | источник / выдержка |
|---|---|---|---|---|
| staskiewitz | tagline_de+en, summary_de+en | Клиент — пасека (Imkerei) | CONFIRMED | CLAUDE.md:5 "**Клиент:** Imkerei Staskiewitz «The Crazy Bee» (Michael & Marcel Staskiewitz), пасека" |
| staskiewitz | summary_de+en | Семейная пасека (Familien-Imkerei) | CONFIRMED | wp-theme/dist/thecrazybee/front-page.php:192 "Familiengeführter Betrieb" |
| staskiewitz | tagline_de+en, summary_de+en | Spessart / Naturpark Spessart | CONFIRMED | CLAUDE.md:5 "Am Sülzberg 12, 63857 Waldaschaff, Naturpark Spessart" |
| staskiewitz | tagline_de+en, summary_de+en, tags | WordPress | CONFIRMED | CLAUDE.md:6 "перенос дизайна в WordPress + Goldenbee" |
| staskiewitz | tagline_de+en, summary_de+en, tags | WooCommerce | CONFIRMED | CLAUDE.md:6 "2 WooCommerce-магазина (B2C Genießer-Shop + B2B Imkerei-Bedarf)" |
| staskiewitz | summary_de+en | 26 Inhaltsseiten | CONFIRMED | STATUS.md:52 "**Содержание.** 26 страниц перенесены"; 25 в P0_ROADMAP.md:21 — ранняя цифра, исправлена DEVLOG.md:86 "было 25, оказалось 26" |
| staskiewitz | summary_de+en | Перенесены 1:1 со старого сайта | CONFIRMED | CLAUDE.md:28 "Тексты/цены 1:1 со старого сайта, ничего не выдумывать"; оговорка STATUS.md:52 "18 записей в `docs/migration/deviations.json`" — есть 18 записанных отклонений |
| staskiewitz | summary_de+en | Проверены блок за блоком | CONFIRMED | STATUS.md:33 "Содержание 26 страниц \| `node verify/verify-migration.mjs` \| **405 из 405**" |
| staskiewitz | summary_de+en | Honig-Shop | CONFIRMED | STATUS.md:86 "шесть банок мёда в разделе"; реально шире: STATUS.md:54 "126 товаров", CLAUDE.md:6 B2C + B2B |
| staskiewitz | summary_de+en | Оплата: Rechnung и Vorkasse | CONFIRMED | STATUS.md:56 "Оплата: Kauf auf Rechnung, Vorkasse."; DEVLOG.md:1431-1432 (11.09) "ровно два способа оплаты — Kauf auf Rechnung · Vorkasse" |
| staskiewitz | summary_de+en | 203 старых адреса перенаправлены | CONFIRMED | STATUS.md:46 "Карта вшита в тему. В ней 203 строки"; DEVLOG.md:1427 (11.09) "карта из 203 адресов"; redirects.php — 203 записи "=>" |
| staskiewitz | summary_de+en | Чтобы не потерять ранжирование | CONFIRMED | DEVLOG.md:328 "После переключения домена это были бы 404 ровно на тех адресах…" (цель; сработает при смене домена) |
| staskiewitz | tags | Shop | CONFIRMED | STATUS.md:56 "**Магазин.** EUR, Германия, налоги 19 % и 7 % разнесены." |
| staskiewitz | tags | Migration | CONFIRMED | CLAUDE.md:6 "миграция контента со Strato" |
| staskiewitz | tags | Handwerk | CONFIRMED | DEVLOG.md:161 "слоган «Traditionelles Handwerk aus dem Herzen des Naturparks Spessart»" |
| staskiewitz | tags | DE | CONFIRMED | STATUS.md:56 "Заграницу не возим — указание клиента." |
| staskiewitz | url | https://thecrazybee.de открывается и это боевой адрес | CONFIRMED | curl 200, 0 редиректов; STATUS.md:3 "**Сайт:** https://thecrazybee.de (открыт для посетителей)". Финальный по файлам — www.imkerei-staskiewitz.de: T001_pereezd_all-inkl.md:12-13 "`thecrazybee.de` — только 301 на главный" (переезд в фазе Ф5, ещё не сделан) |
| hennerheede | tagline_de+en, summary_de+en | Должность — Design Director | CONTRADICTED | DEVLOG.md:423 "Должность `Design Director` → `Creative Director` везде, включая название сайта"; wp-theme/hennerheede/header.php:16 "<span class=\"role\">Creative Director</span>" |
| hennerheede | tagline_de+en, summary_de+en | Бренды BOSS, MANGO, Baldessarini, Mustang | CONFIRMED | CLAUDE.md:5 "Бренды: BOSS, MANGO, Baldessarini, Mustang." |
| hennerheede | summary_de+en | ALPHATAURI в одном ряду с брендами-работодателями | CONTRADICTED | docs/tasks/T009_PX006_Client_Fixes_0408_part3.md:87 "it does not belong to a company I worked for. Pls keep it only in CASE STUDIES"; STATUS.md:91 "Концепты убраны из полосы FORMER BRANDS — там только работодатели" |
| hennerheede | tagline_de+en, summary_de+en, tags | Portfolio | CONFIRMED | CLAUDE.md:5 "Портфолио-сайт **Henner Heede**" |
| hennerheede | summary_de+en | Мюнхен | CONFIRMED | CLAUDE.md:5 "(Fashion & Lifestyle, München)" |
| hennerheede | summary_de+en, tags | Fashion & Lifestyle | CONFIRMED | CLAUDE.md:5 "(Fashion & Lifestyle, München)" |
| hennerheede | summary_de+en, tags | WordPress | CONFIRMED | DEVLOG.md:560 "WordPress 6.6.2 установлен, постоянные ссылки `/%postname%/`" |
| hennerheede | summary_de+en | Handgeschriebenes Theme | CONFIRMED | DEVLOG.md:561 "**Кастомная тема `hennerheede`** — 15 файлов PHP, вся вёрстка своя" |
| hennerheede | summary_de+en, tags | ACF | CONTRADICTED | wp-theme/hennerheede/functions.php:4 "Поля контента сделаны нативными метабоксами: без ACF Pro и без платных плагинов,"; DEVLOG.md:562 "ACF Pro не нужен" |
| hennerheede | summary_de+en | 11 Seiten | CONTRADICTED | verify/hrc_ledger_px011.json:92 "ITOG: stranic=12 v_karte=12 raznyh_opisanij=12 problem=0"; 11 из STATUS.md:249 включали Leadership, позже снятую в черновик (CLAUDE.md:38) |
| hennerheede | summary_de+en | Четыре кейса | CONTRADICTED | docs/tasks/T013_P0_i18n_prod_migration.md:21 "case_study \| boss:11, mango:12, baldessarini:13, mustang:14, alphatauri:131, neon:132" — 6 кейсов; NEON в тексте нет |
| hennerheede | summary_de+en | Кейсы с mood-изображениями | CONFIRMED | docs/tasks/T010_PX007_Client_Fixes_0508.md:45 "`Unbenannt.JPG` встаёт как mood — так же, как у BOSS и Baldessarini" (для MANGO подтверждения нет) |
| hennerheede | summary_de+en | Кейсы с loop-видео | CONTRADICTED | verify/hrc_ledger_px010.json:88 "На странице MANGO нет ни одного видео"; видео есть у 3 из 4: single-case_study.php:65 "autoplay loop muted playsinline" |
| hennerheede | summary_de+en | Philosophy | CONFIRMED | CLAUDE.md:36 "Philosophy · About · CV (Stationen) · Contact" |
| hennerheede | summary_de+en | CV-Zeitleiste | CONFIRMED | wp-theme/hennerheede/functions.php:73 "'name'          => 'CV — Stationen'," |
| hennerheede | summary_de+en | About | CONFIRMED | CLAUDE.md:36 "Philosophy · About · CV (Stationen) · Contact" |
| hennerheede | summary_de+en | Contact | CONFIRMED | CLAUDE.md:36 "Philosophy · About · CV (Stationen) · Contact" |
| hennerheede | summary_de+en, tags | Enge Editorial-Typografie | CONFIRMED | CLAUDE.md:25 "**Типографика** — editorial: тесный letter-spacing, крупные headlines" |
| hennerheede | summary_de+en | Оригинальные логотипы 1:1 | CONFIRMED | CLAUDE.md:24 "**Лого брендов** — только оригинальные, 1:1, чёрные, SVG." |
| hennerheede | summary_de+en | Self-hosted шрифты | CONFIRMED | wp-theme/hennerheede/assets/css/main.css:2 "Шрифт Prata подключается локально: Google Fonts с внешнего CDN нарушает DSGVO." |
| hennerheede | summary_de+en | DSGVO-konform | CONTRADICTED | docs/tasks/T015_NEON_de_text_and_footer.md:17 "Страниц **Imprint нет**, **privacy-policy = draft**"; живой замер 11.09: /imprint/ 200, /privacy-policy/ 404, /datenschutz/ 404, в футере только ссылка /imprint/ — Datenschutzerklärung на сайте нет |
| hennerheede | tags | DE/EN (двуязычный) | CONFIRMED | verify/hrc_ledger_i18nprod.json:38 "Немецкие страницы на проде отдаются на /de/-URL с кодом 200" |
| hennerheede | url | https://henner.ais152.com — финальный адрес | CONTRADICTED | curl: 301 → https://hennerheede.com/ (200). verify/hrc_ledger_i18nprod.json:88 "henner.ais152.com 301-редиректит на hennerheede.com с сохранением пути" |
| taxi-moennigmann | tagline_de+en, summary_de+en | Такси в Leer (Ostfriesland) | CONFIRMED | src/data/contact.json:22 "\"city\": \"Leer (Ostfriesland)\"," |
| taxi-moennigmann | summary_de+en | Для всей Ostfriesland (ganz / all) | NOT_FOUND | На сайте только src/data/i18n/de.json:16 "in Leer und Ostfriesland"; «ganz/all» нигде нет (искал src/data/i18n, CLAUDE.md, DEVLOG.md) |
| taxi-moennigmann | tagline_de+en | Tag und Nacht / day and night | CONFIRMED | src/data/i18n/de.json:15 "\"claim\": \"Ihr Taxi in Leer — Tag und Nacht\","; de.json:101 "\"heroBadge\": \"24/7 erreichbar\"," |
| taxi-moennigmann | tagline_de+en | Seit über 20 Jahren | CONFIRMED | src/data/i18n/de.json:16 "Seit über 20 Jahren, alles was Taxi kann, in Leer und Ostfriesland" (формулировка клиента, DEVLOG.md:149) |
| taxi-moennigmann | summary_de+en, tags | Corporate / Firmenwebsite | CONFIRMED | CLAUDE.md:21 "**Тип:** Корпоративный сайт таксомоторной компании" |
| taxi-moennigmann | summary_de+en, tags | Astro static build | CONFIRMED | astro.config.mjs:10 "output: 'static'," |
| taxi-moennigmann | summary_de+en | Git-CMS для новостей | CONTRADICTED | public/admin/index.html:16 "News-Verwaltung — Einrichtung erfolgt beim Deployment (Decap CMS)."; public/admin/config.yml:4 "⚠️ Фаза 5 (deploy): настроить backend + OAuth-провайдер" — не подключён; новости = Markdown при сборке (NewsPage.astro:13) |
| taxi-moennigmann | summary_de+en | Self-hosted WOFF2 | CONFIRMED | DEVLOG.md:234 "Шрифты: self-hosted **Bricolage Grotesque** (500/600/700) + **Manrope** (400/600/700)" |
| taxi-moennigmann | summary_de+en, tags | Hero-Video | CONFIRMED | src/components/HomePage.astro:55 "<source src=\"/videos/hero.mp4\" type=\"video/mp4\" />" |
| taxi-moennigmann | summary_de+en | 8 Leistungsbereiche | CONTRADICTED | src/data/services.json: 6 × "type": "service" + 1 × "blog" (стр. 56) + 1 × "contact" (стр. 64); DEVLOG.md:279 "услуги 6×3" — услуг 6, а не 8 |
| taxi-moennigmann | summary_de+en | Названия: Krankenfahrten, Inklusionstaxi, Flughafentransfers, Schülertransporte, Zeitlosreisen | CONFIRMED | src/data/i18n/de.json:21-25 "\"zeitlosreisen\": \"Zeitlosreisen\"," и др. |
| taxi-moennigmann | summary_de+en, tags | WCAG 2.1 AA | CONFIRMED | CLAUDE.md:134 "### WCAG 2.1 AA — Barrierefreiheit (наш стандарт качества + дифференциатор)"; DEVLOG.md:237 "контраст AA — все боевые пары PASS с запасом" (полного a11y-аудита в файлах нет) |
| taxi-moennigmann | summary_de+en | Барьерность как дифференциатор | CONFIRMED | CLAUDE.md:27 "**WCAG 2.1 AA** (Barrierefreiheit — наш стандарт качества + дифференциатор;" |
| taxi-moennigmann | summary_de+en | Phone-first Mobile-UX | CONFIRMED | CLAUDE.md:90 "модуль «Anrufen», Facebook-иконка, mobile-first, короткая загрузка" |
| taxi-moennigmann | summary_de+en, tags | Трёхъязычный DE/EN/Plattdeutsch | CONFIRMED | astro.config.mjs:13 "locales: ['de', 'en', 'nds'],"; вычитка носителем не сделана (STATUS.md:4) |
| taxi-moennigmann | summary_de+en | Plattdeutsch по желанию клиента | CONFIRMED | CLAUDE.md:25 "**Plattdeutsch** (региональный — требование клиента)" |
| taxi-moennigmann | summary_de+en, tags | DSGVO-konform | CONFIRMED | src/pages/datenschutz.astro:41 "Analyse-Dienste und keine Tracking-Cookies eingesetzt."; DEVLOG.md:19 "Grundsatz (0 CDN/трекеров/куки)" |
| taxi-moennigmann | summary_de+en | TTDSG-konform | CONFIRMED | src/pages/datenschutz.astro:15 "<p class=\"sub\">DSGVO und TTDSG</p>" — термин устарел, с 14.05.2024 закон называется TDDDG |
| taxi-moennigmann | summary_de+en | Хостинг ALL-INKL | CONFIRMED | CLAUDE.md:29 "**Хостинг:** ALL-INKL (Kasserver.com)"; DEVLOG.md:41 S016 «Публикация на боевой домен клиента (ALL-INKL)» |
| taxi-moennigmann | summary_de+en | Хостинг в Германии | NOT_FOUND | Страна хостинга в файлах не названа (искал CLAUDE.md, DEVLOG.md, STATUS.md, docs/) |
| taxi-moennigmann | url | https://taxi-moennigmann.de — финальный адрес | CONFIRMED | curl 200, 0 редиректов; astro.config.mjs:8 "site: 'https://taxi-moennigmann.de',"; DEVLOG.md:43 "**Статус:** LIVE на https://taxi-moennigmann.de/" |
| sorrysara | tagline_de+en, summary_de+en | Коктейль- и фрай-бар | CONFIRMED | CLAUDE.md:15 "Сайт-визитка коктейль- и фрай-бара «Sorry Sara»" |
| sorrysara | tagline_de+en, summary_de+en | Бургас | CONFIRMED | CLAUDE.md:16 "ул. Калофер 3, Бургас, Болгария" |
| sorrysara | tagline_de+en, summary_de+en, tags | Управление через Telegram-бот (в проде) | CONFIRMED | STATUS.md:4 "T002 (CMS-бот) LIVE В ПРОДЕ" |
| sorrysara | summary_de+en | Управляет сама владелица | CONFIRMED | DEVLOG.md:188 "переключил `ADMIN_CHAT_ID` ... → 474563258 (Анна)" |
| sorrysara | summary_de+en | С телефона (vom Handy aus) | NOT_FOUND | Прямо нигде не сказано; следует из Telegram как инструмента (субъективно) |
| sorrysara | summary_de+en | Без классической админки | CONFIRMED | STATUS.md:52 "CMS = Telegram-бот (Вариант A), Strapi НЕ используется" |
| sorrysara | summary_de+en | Бот ведёт весь сайт (komplette Pflege / entire site) | CONTRADICTED | DEVLOG.md:149 "обработчики разделов `home:menu`,`home:events`" — только меню и события; часы, контакты, UI-тексты и legal живут в web/messages/*.json, web/src/data/contacts.json, legalContent.ts |
| sorrysara | summary_de+en | Бот: меню | CONFIRMED | STATUS.md:22 "меню-флоу: CRUD категорий/позиций кликами" |
| sorrysara | summary_de+en | Бот: события | CONFIRMED | STATUS.md:23 "события-флоу ... draft→publish→archive" |
| sorrysara | summary_de+en | Бот: фото | CONFIRMED | STATUS.md:25 "Меню (`photo_url`) + событие host-фото/галерея" |
| sorrysara | summary_de+en | Бот: цены | CONFIRMED | bot/src/menu-flow.ts:200 ".text('💶 Цена', `iprice:${it.id}`)" |
| sorrysara | summary_de+en | Бот: переводы | CONFIRMED | bot/src/menu-flow.ts:126-131 "Да обновя ли преводите EN/UK/DE?" — только перезапуск автоперевода |
| sorrysara | summary_de+en | Клик-клик, вводится только значение | CONFIRMED | STATUS.md:22 "CRUD категорий/позиций кликами ... строгий парсер («20 лв» отклонён)" |
| sorrysara | tagline_de+en, summary_de+en, tags | Билеты на платные события через Stripe | CONFIRMED | web/src/app/api/stripe/webhook/route.ts:242 "case 'checkout.session.completed'" |
| sorrysara | summary_de+en | Stripe в боевом режиме | CONFIRMED | docs/CREDENTIALS.md:77 "## Stripe — LIVE (подключено 2026-07-16, env sorrysara-web)"; реальной покупки картой не было (STATUS.md:4 "Осталось: реальный e2e-тест покупки картой") |
| sorrysara | summary_de+en, tags | Без овербукинга, race-safe | CONFIRMED | web/src/lib/seats.ts:132 "SELECT event_id FROM ss_event_seatlock WHERE event_id = $1 FOR UPDATE" |
| sorrysara | summary_de+en | «garantiert» überbuchungsfrei | CONFIRMED | STATUS.md:24 "тест `Σpaid+seats_taken≤capacity` под конкуренцией (10 раундов)" |
| sorrysara | summary_de+en | Возврат денег автоматически освобождает место | CONTRADICTED | Код есть: route.ts:267 "case 'charge.refunded':"; но боевой вебхук подписан только на docs/CREDENTIALS.md:82 "события: checkout.session.completed, checkout.session.expired" — charge.refunded не доходит; живого возврата не тестировали |
| sorrysara | summary_de+en | Claude переводит BG → EN/UK/DE (в проде) | CONFIRMED | docs/CREDENTIALS.md:28 "авто-перевод BG→EN/UK/DE активен (env контейнера `sorrysara-bot`)" |
| sorrysara | summary_de+en | Ручные правки владелицы не перезаписываются | NOT_FOUND | Защита есть в bot/src/i18n.ts:214 "if (src === 'manual' && !opts.overwriteManual)", но потока ручной правки перевода в боте нет — setManual( вызывается только в i18n.ts и тестах |
| sorrysara | summary_de+en, tags | Мультиязычный сайт, 4 языка | CONTRADICTED | web/src/i18n/config.ts:2 "locales = ['bg', 'en', 'uk', 'de']", но UI-тексты DE/UK = английские: скрипт сравнения web/messages/{de,uk}.json с en.json → de 121 из 123, uk 121 из 123 строк идентичны EN; legalContent.ts:270 "uk: privacyEn, de: privacyEn"; CLAUDE.md:17 "запуск на BG+EN, UK/DE по мере переводов Hanna" |
| sorrysara | tags | GDPR | CONTRADICTED | Consent Mode есть (DEVLOG.md:445), но данные оператора — заглушки: 12 × "TODO_§16" в web/src/components/sections/legalContent.ts; на живой /privacy видны "TODO_§16" |
| sorrysara | url | https://sorrysara.space — финальный адрес | CONFIRMED | curl 200, 0 редиректов; STATUS.md:7 "**https://sorrysara.space** — Clouding.io `187.33.159.205`" |
| silkekleinart | tagline_de+en, summary_de+en | Художница (Malerin) | CONFIRMED | docs/tasks/PX-030_TS1.md:28 "Künstler-Website (Malerei) Silke Klein, Kiel." |
| silkekleinart | tagline_de+en, summary_de+en | Kiel | CONFIRMED | CLAUDE.md:16 "**Локация:** Kiel (клиент)"; docs/content/legal/impressum.md:11 "24146 Kiel" |
| silkekleinart | tagline_de+en, tags | Портфолио (не магазин) | CONFIRMED | docs/design/CDP_SilkeKleinArt_Design.md:113 "Сегмент B2C — арт-портфолио/презентация. Сайт НЕ магазин" |
| silkekleinart | tagline_de+en, summary_de+en | Neubau существующего сайта | CONFIRMED | docs/adr/ADR-001-stack-and-scope.md:12 "Сайт художницы Silke Klein (silkekleinart.com) живёт на IONOS + WordPress + Elementor" |
| silkekleinart | tagline_de+en, summary_de+en, tags | Handgeschriebenes WordPress-Theme | CONFIRMED | CLAUDE.md:58 "Кастомная WP-тема (PHP templates + vanilla JS/CSS)" |
| silkekleinart | summary_de+en, tags | Advanced Custom Fields | CONFIRMED | wp-content-plugin/silkekleinart-core/includes/acf-fields.php:25 "'key'      => 'group_skart_ausstellung'" |
| silkekleinart | summary_de+en, tags | CPT для работ и выставок | CONFIRMED | wp-content-plugin/silkekleinart-core/includes/post-types.php:13 "Registriert die CPTs „ausstellung“ und „werk“." |
| silkekleinart | summary_de+en | Художница сама ведёт работы и выставки через WP-формы | CONFIRMED | docs/tasks/PX-033_AUDIT_REPORT.md:26 "**Editor-Rolle `silke-klein`**: sieht Werke/Ausstellungen/Seiten/Medien + ACF-Felder" |
| silkekleinart | summary_de+en | Страницы тоже через «aufgeräumte WP-Formulare» | NOT_FOUND | Для страниц ACF-форма только у одного шаблона: acf-fields.php:179-181 "'page-templates/galerie-rubrik.php'"; остальные страницы — обычный WP-редактор |
| silkekleinart | summary_de+en | Ohne Page-Builder | CONFIRMED | docs/tasks/PX-033_AUDIT_REPORT.md:27 "kein Elementor/Pro-Elements" |
| silkekleinart | summary_de+en | Premium | CONFIRMED | CLAUDE.md:15 "**дизайн — премиальный редизайн**" (субъективно, цель проекта) |
| silkekleinart | summary_de+en | Editorial-Typografie | CONFIRMED | docs/design/CDP_SilkeKleinArt_Design.md:139 "Editorial serif (Playfair Display как класс заголовков)" |
| silkekleinart | summary_de+en | Responsive галерея | CONFIRMED | wp-theme/silkekleinart/assets/css/gallery.css:72 "@media (max-width: 900px) { .hang { columns: 2 240px; } }" |
| silkekleinart | summary_de+en | Vollständig DSGVO-konform | CONTRADICTED | docs/tasks/PX-030_AUDIT_REPORT.md:79 "**LOW — Datenschutz Hosting-Klausel kaputt**"; docker/seed/seed.json:405 "Wir haben Wordfence auf dieser Website eingebunden" — Wordfence на новом сайте нет (PX-033:12,27); исправление нигде не записано |
| silkekleinart | summary_de+en | Self-hosted Schriften | CONFIRMED | wp-theme/silkekleinart/assets/css/base.css:3 "DSGVO: Schriften self-hosted (KEIN Google-CDN, LG München 2022)." |
| silkekleinart | summary_de+en | Barrierefreiheit (BFSG 2025) | NOT_FOUND | BFSG только как цель брифа: CDP_SilkeKleinArt_Design.md:252 "a11y (BFSG 2025 / WCAG AA — КРИТИЧНО…)"; аудита нет, только Lighthouse DEVLOG.md:144 "a11y 96–98" |
| silkekleinart | tags | DE | CONFIRMED | CLAUDE.md:17 "**Языки:** Deutsch (сайт)" |
| silkekleinart | url | https://silkekleinart.com — финальный адрес | CONFIRMED | Домен подтверждён: STATUS.md:3 "LIVE auf KUNDIN-Hosting — https://silkekleinart.com jetzt auf **IONOS Webhosting Plus**". Открытие нестабильно: 6 запросов curl → 4 × "Recv failure: Connection was reset", с -v — 200 после TLS-renegotiation; www и http → 301 на https://silkekleinart.com/ |
| ofnstube | tagline_de+en, summary_de+en | Мюнхен | CONFIRMED | CLAUDE.md:20 "**Локация:** Мюнхен, Германия" |
| ofnstube | tagline_de+en, summary_de+en | Реальный ресторан-клиент | CONTRADICTED | CLAUDE.md:15 "Ofnstube — Munich Craft-Burger (fictional brand, баварский Stube-feel)"; pages/reservation.html:327 "Ofnstube — fiktives Demo-Projekt, alle Angaben sind Platzhalter" |
| ofnstube | tagline_de+en, summary_de+en | Landing | CONFIRMED | CLAUDE.md:16 "restaurant landing с in-house reservation" |
| ofnstube | tagline_de+en, summary_de+en | Работающая In-House-Reservierung | CONTRADICTED | pages/reservation.html:192 "<form class=\"form\" action=\"#\" method=\"post\""; :246 "Der Versand des Formulars wird in einer späteren Prototyp-Stufe angebunden" |
| ofnstube | summary_de+en, tags | Vanilla HTML5 + CSS3 + JS | CONFIRMED | CLAUDE.md:16 "Static website (Vanilla HTML5 + CSS3 + JS)" |
| ofnstube | summary_de+en | Multi-Page, 10 страниц | CONFIRMED | README.md:20 "Vanilla HTML5, multi-page (10 страниц)"; в pages/ ровно 10 .html |
| ofnstube | summary_de+en | Self-hosted Fraunces + Inter | CONFIRMED | assets/css/base.css:9 "src: url('../fonts/fraunces-variable.woff2')" |
| ofnstube | summary_de+en, tags | GSAP + Lenis | CONFIRMED | CLAUDE.md:64 "self-hosted UMD в `assets/vendor/`, НЕ CDN"; gsap.min.js: "GSAP 3.12.5" |
| ofnstube | summary_de+en | Allergen-Kennzeichnung | CONFIRMED | pages/menu.html:170 "Pflichtangaben nach Anhang II der Verordnung (EU) 1169/2011"; данные мок: data/menu.json:3 "MOCK-Daten" |
| ofnstube | summary_de+en | Ссылка «LMIV §1169» | CONTRADICTED | pages/menu.html:170 "Verordnung (EU) 1169/2011" — 1169 это номер регламента, а не параграф |
| ofnstube | summary_de+en | JuSchG | CONFIRMED | pages/agb.html:126 "Gemäß § 9 JuSchG werden Bier und Wein nur an Personen ab 16 Jahren abgegeben" |
| ofnstube | summary_de+en | BFSG 2025 Barrierefreiheit | NOT_FOUND | Меры есть (base.css:109 "Focus (BFSG …)"), но аудит открыт: README.md:112 "⬜ BFSG-Audit mit Screenreader + Lighthouse vor Launch" |
| ofnstube | summary_de+en | Vollständig DSGVO-konform | CONTRADICTED | pages/datenschutz.html:112 "Diese Datenschutzerklärung ist ein Platzhalter für den R&D-Prototyp."; README.md:109 "⬜ Impressum / Datenschutz / AGB — anwaltlich zu finalisieren" |
| ofnstube | tags | Restaurant | CONFIRMED | CLAUDE.md:17 "Сайт fictional craft-burger ресторана в Мюнхене" |
| ofnstube | tags | Bilingual DE/EN | CONFIRMED | assets/js/lang.js:2 "DE (primary) / EN (secondary) switch" (JS-переключатель; legal только DE) |
| ofnstube | tags | DSGVO (техническая часть) | CONFIRMED | README.md:96 "✅ Self-hosted WOFF2-Fonts — keine Verbindung zu Google Fonts CDN" |
| ofnstube | url | https://ofnstube.ais152.com — финальный адрес | CONFIRMED | curl 200, 0 редиректов; CNAME:1 "ofnstube.ais152.com" |
| elektrocheck-stuttgart | tagline_de+en, summary_de+en | DGUV V3 Prüfungen | CONFIRMED | design/desktop/phase-3/index.html:52 "DGUV V3-Prüfungen für ortsveränderliche und ortsfeste elektrische Geräte in Stuttgart und Umgebung." |
| elektrocheck-stuttgart | tagline_de+en, summary_de+en | Region Stuttgart | CONFIRMED | design/desktop/phase-3/index.html:58 "Stuttgart und Umgebung" |
| elektrocheck-stuttgart | summary_de+en | Landing-Site | CONFIRMED | design/desktop/master-prompt/MASTER_PROMPT.md:108 "одностраничник DE-only" |
| elektrocheck-stuttgart | summary_de | Elektromeister | CONTRADICTED | design/desktop/phase-3/impressum.html:57 "Berufsbezeichnung: Elektrofachkraft / Befähigte Person nach TRBS 1203" — «Meister» в проекте нет |
| elektrocheck-stuttgart | summary_de+en | Для предприятий | CONFIRMED | design/desktop/phase-3/index.html:555 "Prüfungen für Unternehmen und Gewerbekunden in Stuttgart und Umgebung" |
| elektrocheck-stuttgart | summary_de+en | Для частных клиентов (Privatkunden) | CONTRADICTED | index.html:555 — только "Unternehmen und Gewerbekunden"; script.js:163 "Privatvermieter ohne Beschäftigte = nicht DGUV V3-pflichtig" |
| elektrocheck-stuttgart | summary_en | legally required | CONFIRMED | index.html:150 "Einordnung der DGUV V3-Prüfpflicht für Gewerbebetriebe" (верно только для бизнеса) |
| elektrocheck-stuttgart | summary_de+en | Festpreis-Angebot | CONFIRMED | index.html:625 "Wir erstellen ein verbindliches Festpreis-Angebot binnen 24 Stunden nach Anfrage." |
| elektrocheck-stuttgart | summary_de+en, tags | Немецкий сайт и форма | CONFIRMED | index.html:2 "<html lang=\"de\">"; CLAUDE.md:20 "Languages: DE only" |
| elektrocheck-stuttgart | summary_de+en, tags | Форма через FormSubmit | CONFIRMED | index.html:664 "action=\"https://formsubmit.co/info@elektrocheckstuttgart.de\"" (ящик info@ по HANGING_ITEMS.md:17 H-11 "POSTPONED_CEO") |
| elektrocheck-stuttgart | summary_de+en | Vollständig DSGVO-konform | NOT_FOUND | Перенос в США только по datenschutz.html:114 "Art. 49 Abs. 1 lit. b DSGVO"; AVV с FormSubmit нет; юрист не подтвердил (HANGING_ITEMS.md:14 H-08); impressum.html:66 "Steuernummer: Wird nach Erteilung durch Finanzamt ergänzt" |
| elektrocheck-stuttgart | tags | DSGVO (есть Impressum и Datenschutz) | CONFIRMED | datenschutz.html:99 "Die Verarbeitung erfolgt auf Grundlage des Art. 6 Abs. 1 lit. b DSGVO" |
| elektrocheck-stuttgart | summary_de+en, tags | Vanilla HTML+CSS+JS | CONFIRMED | CLAUDE.md:16 "Static HTML/CSS/JS (vanilla, 0 зависимостей …)" |
| elektrocheck-stuttgart | summary_de+en | GitHub Pages | CONTRADICTED | DEVLOG.md:113 "23 files uploaded → перемещены в `/public/` (IONOS требует subfolder)"; scripts/sftp_upload.py:3 "SFTP upload phase-3/ → IONOS Webhosting Standard"; GitHub Pages — только исходный план CLAUDE.md:18 |
| elektrocheck-stuttgart | summary_de+en | Eigene Domain | CONFIRMED | DEVLOG.md:111 "Domain elektrocheckstuttgart.de registered FREE Y1" |
| elektrocheck-stuttgart | tags | Service | CONFIRMED | index.html:447 "Was wir leisten" |
| elektrocheck-stuttgart | tags | B2B | CONFIRMED | index.html:555 "für Unternehmen und Gewerbekunden" |
| elektrocheck-stuttgart | url | https://elektrocheckstuttgart.de — финальный адрес | CONFIRMED | Домен подтверждён: design/desktop/phase-3/index.html:11 "<link rel=\"canonical\" href=\"https://elektrocheckstuttgart.de/\">". curl apex: 3 из 4 запросов 200, 1 обрыв; www — 2 из 2 "Connection was reset". Go-live в DEVLOG не записан (последняя запись DEVLOG.md:135-136 «site недоступен») |
| kontur | tagline_de+en | Specialty-Kaffeerösterei (тема) | CONFIRMED | wp-content/themes/kontur/front-page.php:27 "Spezialitätenkaffee · Rösterei" (бренд вымышленный) |
| kontur | summary_de+en | Shop для реальной немецкой обжарочной (клиентский проект) | CONTRADICTED | CLAUDE.md:14 "Портфолио-кейс."; CLAUDE.md:15 "Онлайн-магазин specialty-кофе вымышленной немецкой Kaffeerösterei «KONTUR»"; docs/tasks/T004_faza_d_kontent_foto.md:37 "Реальной компании нет" |
| kontur | tagline_de+en, tags | Individueller Shop / Custom Theme | CONFIRMED | wp-content/themes/kontur/style.css:5 "Kastom-Theme für die KONTUR Kaffeerösterei — WooCommerce-Shop für Spezialitätenkaffee … Kein Page-Builder." |
| kontur | summary_de+en | Handgeschriebenes Theme, kein Page-Builder | CONFIRMED | CLAUDE.md:58 "Кастомная тема (НЕ page-builder, НЕ Elementor/Divi) \| Locked" |
| kontur | summary_de+en, tags | WordPress + WooCommerce | CONFIRMED | DEVLOG.md:348 "WordPress 7.0 (de_DE) + WooCommerce активны" |
| kontur | summary_de+en | Katalog | CONFIRMED | DEVLOG.md:285 "`woocommerce/archive-product.php` + `content-product.php` — каталог" |
| kontur | summary_de+en | Produktseiten | CONFIRMED | DEVLOG.md:249 "`woocommerce/single-product.php` — PDP" |
| kontur | summary_de+en | Warenkorb | CONFIRMED | DEVLOG.md:250 "`woocommerce/cart/cart.php` + `cart-empty.php` — корзина" |
| kontur | summary_de+en | Checkout | CONFIRMED | DEVLOG.md:223 "оформлен тестовый заказ **#271** → `thankyou.php` (Gesamt 49,00 €)" (только Vorkasse/Rechnung) |
| kontur | summary_de+en | Kaffee-Abo (подписка) | CONTRADICTED | docs/tasks/T003_faza_c_woocommerce_integraciya.md:95 "обычный WC-товар «Abo» с мета-данными, без рекуррентных платежей, без платного плагина" — конфигуратор, не подписка |
| kontur | summary_de+en | Editorial-Design | CONFIRMED | CLAUDE.md:15 "Concept A «KONTUR» (Editorial Roastery) выбран" |
| kontur | summary_de+en | DSGVO (меры) | CONFIRMED | template-parts/cookie-banner.php:18-20 "Einstellungen" / "Ablehnen" / "Akzeptieren"; шрифты локально |
| kontur | summary_de+en | PAngV (Grundpreis) | CONFIRMED | inc/woocommerce.php:67 "PAngV: Grundpreis je Kilogramm." |
| kontur | summary_de+en | LMIV | CONFIRMED | inc/woocommerce.php:122-126 "'_kontur_lmiv_zutaten' … '_kontur_lmiv_mhd'" |
| kontur | summary_de+en | Konform mit deutschem E-Commerce-Recht | NOT_FOUND | Только внутренний чек-лист DEVLOG.md:165 "Юр-чеклист: … все PASS"; T004:87 "Данные компании — плейсхолдеры (… USt DE000000000)"; юр. проверки нет (T004:37) |
| kontur | tags | E-commerce | CONFIRMED | CLAUDE.md:14 "кастомная WordPress + WooCommerce тема (онлайн-магазин)" |
| kontur | tags | DE | CONFIRMED | CLAUDE.md:19 "**Рынок:** Германия" (живой сайт отдаёт <html lang="en-US">) |
| kontur | url | https://kontur.ais152.com — финальный адрес | CONFIRMED | curl 200, 0 редиректов; Caddyfile:5 "kontur.ais152.com {"; STATUS.md:6 "сайт LIVE и магазин РАБОТАЕТ." |
| pomp | tagline_de+en, tags | Markenidentität / Brand | CONFIRMED | C:\Projects\MainCore\vault\02_Knowledge\Brands\POMP.md:10 "# POMP — Brand Pack" (в репо POMP гайдлайна нет) |
| pomp | tagline_de+en, tags | Landing | CONFIRMED | app/page.tsx — один маршрут: Hero, Story, FlavoursCarousel, Tasting, Nutrition, SignUp, Footer |
| pomp | tagline_de+en | Farbenfroh / colourful | CONFIRMED | Brands/POMP.md:24 "**Category** \| Colourful sparkling water" |
| pomp | tagline_de+en, summary_de+en | Sparkling Water | CONFIRMED | app/layout.tsx:23 "Sparkling water with a personality, in six bold flavors." |
| pomp | summary_de+en | Komplettes / full Brand-Paket | CONTRADICTED | Brands/POMP.md:101 "OG flat-lay (deferred) … ⏸️"; :102 "Lifestyle shots × 3 (deferred)"; public/og-image.jpg отсутствует при ссылке в layout.tsx:26 |
| pomp | summary_de+en | Produktions-Landing | CONFIRMED | Brands/POMP.md:175 "## Production Deployment (PX-012, 2026-05-05)" (подписка не подключена к почте, STATUS.md:161) |
| pomp | summary_de+en | Konzept (не реальный бренд) | CONFIRMED | Brands/POMP.md:7 "status: active-pilot" |
| pomp | summary_de+en | Шесть вкусов | CONFIRMED | lib/flavors.ts:29,44,59,74,89,104 — 6 id (mango-chili … black-cherry-cola) |
| pomp | summary_de+en | Hero-Video | CONFIRMED | components/Hero.tsx:59 "<source src=\"/videos/hero.mp4\" type=\"video/mp4\" />" |
| pomp | summary_de+en | Scroll-pinned карусель на десктопе | CONFIRMED | components/FlavoursCarousel.tsx:57 "pin: true," |
| pomp | summary_de+en | Нативный snap-scroll на мобильном | CONFIRMED | components/FlavoursCarousel.tsx:7 "Mobile / touch: native CSS scroll-snap horizontal carousel" |
| pomp | summary_de+en | Freigestellte Produkt-Shots | CONFIRMED | git 7637714 "Convert PNG -> WebP @ q88 with transparency"; альфа у всех 6 public/images/cans/*.webp |
| pomp | summary_de+en | Dunkel-/Cream-Rhythmus | CONFIRMED | git aab804e "Nutrition section: bg-cream -> bg-ink, text inverted (visual rhythm break)" |
| pomp | summary_de+en, tags | Next.js 16 | CONFIRMED | package.json:19 "\"next\": \"16.2.4\"," |
| pomp | summary_de+en | Tailwind 4 | CONFIRMED | package.json:33 "\"tailwindcss\": \"^4.0.0\"" |
| pomp | summary_de+en, tags | GSAP | CONFIRMED | package.json:17 "\"gsap\": \"^3.12.5\"," |
| pomp | summary_de+en | Lenis | CONFIRMED | package.json:18 "\"lenis\": \"^1.1.20\","; lib/lenis-provider.tsx:4 "import Lenis from 'lenis';" |
| pomp | tags | Motion | CONFIRMED | package.json:16 "\"framer-motion\": \"^11.15.0\","; импорт в 7 компонентах |
| pomp | url | https://pomp-landing.vercel.app — финальный адрес | CONFIRMED | curl 200, 0 редиректов; docs/tasks/T001_carousel_mobile_lag.md:16 "\| Live URL \| https://pomp-landing.vercel.app \|"; своего домена нет (STATUS.md:249 "pomp.com domain \| ⏸️ Deferred") |
| baupreis | tagline_de+en | KI-Prognosen | CONFIRMED | app/src/app/api/cron/analyze/route.ts:245 "model: \"claude-3-haiku-20240307\""; :188 forecast_json 7d/30d/90d (без ключа — статистический fallback, lib/forecast-baseline.ts:2) |
| baupreis | tagline_de+en | Intelligentere Baubudgets / smarter budgets | NOT_FOUND | Функции бюджетов нет; продукт — мониторинг цен и рекомендация buy_now/wait/watch (analyze/route.ts:183) (субъективно) |
| baupreis | summary_de+en | KI-gestützte Überwachung von Baustoffpreisen | CONFIRMED | CLAUDE.md:15 "Мониторинг цен 16 стройматериалов, AI-анализ трендов, прогнозы, алерты" |
| baupreis | summary_de | Für deutsche Handwerksbetriebe | CONTRADICTED | CLAUDE.md:15 "Платформа для немецких строительных компаний (Bauunternehmen, Einkäufer, Projektleiter)"; app/src/i18n/de.ts:12 "für deutsche Bauunternehmen" |
| baupreis | summary_en | For German contractors | CONFIRMED | app/src/i18n/de.ts:521 "Für kleine Bauunternehmen" |
| baupreis | summary_de+en | 16+ Materialien | CONTRADICTED | Скрипт по init.sql (INSERT INTO materials) → 16 строк, в migrations/ новых нет; с данными 15: STATUS.md:33 "Diesel: нет TANKERKOENIG_API_KEY (15/16 материалов)" |
| baupreis | summary_de+en | Preisvorhersagen | CONFIRMED | app/src/lib/forecast-baseline.ts:116-118 "forecast7d … forecast30d … forecast90d" |
| baupreis | summary_de+en, tags | Multi-Tenant-SaaS | CONFIRMED | DEVLOG.md:1256 "Phase 3: Multi-tenant (organizations, plan gating Basis/Pro/Team)" |
| baupreis | summary_de+en | Три тарифа | CONFIRMED | app/src/lib/plans.ts:55-58 "basis: { monthly: 49 … pro: { monthly: 149 … team: { monthly: 299" |
| baupreis | summary_de+en | Claude-Trendanalyse | CONFIRMED | analyze/route.ts:173 "Du bist ein Analyst für Baustoffpreise"; :182 "\"trend\": \"rising\" \| \"falling\" \| \"stable\"" (активность в проде не проверяема: STATUS.md:34 "Anthropic API: низкий баланс") |
| baupreis | tags | SaaS | CONFIRMED | DEVLOG.md:1248 "от нуля до рабочего SaaS" |
| baupreis | tags | AI | CONFIRMED | analyze/route.ts:4 "import Anthropic from \"@anthropic-ai/sdk\"" |
| baupreis | tags | Next.js | CONFIRMED | CLAUDE.md:38 "Frontend \| Next.js 14 (App Router) + TypeScript + Tailwind + shadcn/ui \| Locked" |
| baupreis | tags | Stripe | CONTRADICTED | DEVLOG.md:547 "Billing на сервере = PayPal+Paddle, НЕ Stripe (CREDENTIALS.md drift)"; STATUS.md:35 "Stripe: test mode" |
| baupreis | summary_de+en | Немецкий рынок | CONFIRMED | README.md:3 "KI-gestützte Baustoff-Preisplattform für Deutschland" |
| baupreis | url | https://baupreis.ais152.com — финальный адрес | CONFIRMED | curl 200, 0 редиректов; app/src/app/layout.tsx:58 "canonical: \"https://baupreis.ais152.com\""; /api/health → {"status":"ok"} |
| eko-oylis-ua | tagline_de+en, summary_de+en | Сбор отработанного масла (UCO) | CONFIRMED | src/_data/timeline.json:9 "EKO-OYLIS founded as a specialised operator for used vegetable oil collection in Ukraine." |
| eko-oylis-ua | summary_de+en | Украинская компания | CONFIRMED | CLAUDE.md:15 "…отработанного растительного масла (UCO) на территории Украины"; site.json:14 "\"country\": \"UA\"" |
| eko-oylis-ua | tagline_de+en, summary_de+en | Выход в ЕС через Болгарию | CONFIRMED | src/_data/timeline.json:80-81 "Opening of EKO-OYLIS representation in Bulgaria" |
| eko-oylis-ua | summary_de+en, tags | Corporate | CONFIRMED | CLAUDE.md:14 "Тип: Corporate Website Redesign (материнский сайт группы компаний)" |
| eko-oylis-ua | summary_de+en, tags | Двуязычный UA/EN | CONFIRMED | src/_data/site.json:5 "\"locales\": [\"uk\", \"en\"]"; CLAUDE.md:20 "Языки: UA + EN" |
| eko-oylis-ua | summary_de+en | 11 вех | CONFIRMED | Скрипт node по src/_data/timeline.json → count=11; about.njk:73 "{% for m in timeline.milestones %}" |
| eko-oylis-ua | summary_de+en | 2008 → 2026 | CONFIRMED | timeline.json:4 "\"year\": 2008" … timeline.json:94 "\"year\": 2026" |
| eko-oylis-ua | summary_de+en | 2500+ HoReCa-партнёров | CONFIRMED | src/_data/site.json:8 "\"partnersCount\": 2500"; i18n/ua.json:97 "2500+ партнерів у громадському харчуванні" |
| eko-oylis-ua | summary_de+en | Собственный автопарк | CONFIRMED | i18n/ua.json:111 "Власний автопарк" |
| eko-oylis-ua | summary_de+en, tags | Eleventy | CONFIRMED | package.json:23 "\"@11ty/eleventy\": \"^3.1.5\"" |
| eko-oylis-ua | summary_de+en, tags | GSAP | CONFIRMED | package.json:39 "\"gsap\": \"~3.12.5\"" |
| eko-oylis-ua | summary_de+en | Lenis | CONFIRMED | package.json:40 "\"lenis\": \"~1.1.14\"" |
| eko-oylis-ua | summary_de+en | schema.org | CONFIRMED | src/_includes/head.njk:84 "<script type=\"application/ld+json\">"; schema.js:113 "\"@type\": \"LocalBusiness\"" |
| eko-oylis-ua | summary_de+en | Vollständig self-hosted | CONTRADICTED | Шрифты и скрипты локальные, но форма уходит в Cloudflare Worker: src/_data/site.json:19 "\"formEndpoint\": \"https://eko-form.eko-oylis.workers.dev\"" |
| eko-oylis-ua | tags | DSGVO | CONTRADICTED | Меры есть (согласие contacts.njk:59 "name=\"gdpr_consent\" required"), но privacy.njk:14 "Цей документ — заглушка. Перед публікацією підлягає юридичній перевірці." |
| eko-oylis-ua | url | https://eko-oylis.com.ua — финальный адрес | CONFIRMED | curl 200, 0 редиректов; src/_data/site.json:3 "\"url\": \"https://eko-oylis.com.ua\"" |
| rundumshaus | summary_de+en | Osnabrück | CONFIRMED | site/src/data/site.json:5-6 "\"street\": \"Bramscher Str. 161\", \"city\": \"Osnabrück\"" |
| rundumshaus | summary_de+en | Lokales Handwerk / handyman services | CONFIRMED | CLAUDE.md:14 "Коммерческий сайт для клиента (Hausmeister & Gartenpflege)" (формулировка «Handwerk» неточная) |
| rundumshaus | summary_de+en | Пять категорий услуг | CONFIRMED | site/src/data/services.json:7,17,31,41,55 — 5 id: garten-landschaftsbau, gartenpflege, entruempelung, hausmeisterservice, dacharbeiten |
| rundumshaus | summary_de+en | WhatsApp-интеграция | CONFIRMED | site/src/components/layout/WhatsAppButton.tsx:5 "https://wa.me/4915239603175" |
| rundumshaus | summary_de+en | KI-generierte Bildwelt | CONFIRMED | DEVLOG.md:28 "Фото AI по стилю макета (решение CEO)"; позже добавлены реальные фото (referenzen.json:6-33) |
| rundumshaus | summary_de+en | Mobile Sticky-CTA | CONFIRMED | site/src/components/layout/Navbar.tsx:45 "<header className=\"sticky top-0 z-50 bg-white"; WhatsAppButton.tsx:48 "fixed bottom-6 right-6" |
| rundumshaus | summary_de+en | DSGVO-konform | CONTRADICTED | site/src/app/datenschutz/page.tsx:68-70 "Es werden keine Tracking-Cookies, Analyse-Tools oder Drittanbieter-Skripte eingesetzt." — при этом site/src/app/layout.tsx:250 "src=\"https://plausible.io/js/script.js\""; datenschutz/page.tsx:77 "(Lora, Plus Jakarta Sans)" — сайт уже на Inter |
| rundumshaus | tags | Next.js | CONFIRMED | site/package.json:19 "\"next\": \"16.2.3\"" |
| rundumshaus | tags | GSAP | CONFIRMED | site/package.json:16 "\"gsap\": \"^3.15.0\"" |
| rundumshaus | tags | SEO | CONFIRMED | docs/SEO_RESULTS.md:18 "Total programmatic landing pages \| 490" |
| rundumshaus | tags | DE | CONFIRMED | CLAUDE.md:17 "Deutsch (единственный язык сайта)" |
| rundumshaus | tags | Website | CONFIRMED | .github/workflows/deploy.yml:1 "Deploy to GitHub Pages" |
| rundumshaus | summary_de+en | Premium | CONFIRMED | CLAUDE.md:15 "Премиум-сайт" (субъективно, цель проекта) |
| rundumshaus | tagline_de | Komplettlösung für Hausmeisterservice und Garten | CONFIRMED | site/src/data/homepage.json:52 "Viele Dienstleistungen aus einer Hand" (из 5 услуг названы 2) |
| rundumshaus | tagline_en | Complete home care | CONFIRMED | site/src/data/homepage.json:22 "bei allen Arbeiten rund um Haus, Garten, Dach und Grundstück" |
| rundumshaus | tagline_en | Fast and reliable | CONFIRMED | site/src/components/sections/Hero.tsx:25 "const BADGES = [\"Zuverlässig\", \"Schnell\", \"Preiswert\", \"Persönlich\"]" (собственный текст клиента; DE- и EN-tagline говорят разное) |
| rundumshaus | url | https://rundumshaus-littawe.de — финальный адрес | CONFIRMED | curl 200, 0 редиректов; site/public/CNAME:1 "rundumshaus-littawe.de" |
| provenly-homes | tagline_de+en | Motion-Design | CONFIRMED | site/package.json:15,17 "\"gsap\": \"^3.14.2\"", "\"motion\": \"^12.38.0\"" |
| provenly-homes | tagline_de+en | Premium | NOT_FOUND | Только в собственном брендинге проекта: branding/BRAND_GUIDE.md:91 "With \"Premium Property Management\" subtitle"; в текстах сайта нет (субъективно) |
| provenly-homes | tagline_de+en | Бизнес — «Kurzzeitvermietung / short-term rentals» | CONTRADICTED | CLAUDE.md:15 "Новый сайт для компании по управлению краткосрочной арендой недвижимости в NRW"; site/src/data/homepage.json:4 "Wir übernehmen Betrieb, Gäste, Zustand und Ertrag" — это управление арендой для собственников |
| provenly-homes | summary_de+en | Corporate-Website | CONFIRMED | CLAUDE.md:14 "**Тип:** Corporate website (static, SSG)" |
| provenly-homes | summary_de+en | Сделан «für ein Unternehmen» (сданный клиентский проект) | NOT_FOUND | Договора/приёмки нет; STATUS.md:47 "- [ ] Final walkthrough + sign-off"; префикс fr_02 — питч; отношения с клиентом знает только CEO |
| provenly-homes | summary_de+en | Компания по управлению краткосрочной арендой | CONFIRMED | CLAUDE.md:15 "компании по управлению краткосрочной арендой недвижимости в NRW" |
| provenly-homes | summary_de+en | Köln | CONFIRMED | CLAUDE.md:16 "**Локация:** Köln, NRW, Germany" |
| provenly-homes | summary_de+en | Awwwards-Effekte / Awwwards-level | NOT_FOUND | Только цель: CLAUDE.md:15 "Целевой уровень — Awwwards"; приёмочные пункты T004_awwwards_design_gap.md:100-118 не отмечены (субъективно) |
| provenly-homes | summary_de+en | Scroll-анимации | CONFIRMED | site/src/components/sections/Hero.tsx:5 "import { ScrollTrigger } from \"gsap/ScrollTrigger\";" |
| provenly-homes | summary_de+en | GSAP + Motion hybrid | CONFIRMED | DEVLOG.md:142 "`docs/ANIMATION_RULES.md` — GSAP vs Motion responsibilities" |
| provenly-homes | summary_de+en | JSON-getriebener Inhalt | CONFIRMED | DEVLOG.md:133 "**JSON data:** 10 files from content/"; Hero.tsx:7 "import homepageData from \"@/data/homepage.json\";" |
| provenly-homes | summary_de+en | GitHub Pages | CONFIRMED | site/.github/workflows/deploy.yml:1 "name: Deploy to GitHub Pages"; next.config.ts:7 "output: \"export\"" |
| provenly-homes | tags | Website | CONFIRMED | CLAUDE.md:14 "Corporate website (static, SSG)" |
| provenly-homes | tags | Real Estate | CONFIRMED | CLAUDE.md:15 "управлению краткосрочной арендой недвижимости" |
| provenly-homes | tags | Next.js | CONFIRMED | site/package.json:18 "\"next\": \"16.2.3\"" |
| provenly-homes | tags | GSAP | CONFIRMED | site/package.json:15 "\"gsap\": \"^3.14.2\"" |
| provenly-homes | tags | Motion | CONFIRMED | site/package.json:17 "\"motion\": \"^12.38.0\"" |
| provenly-homes | url | github.io/provenly-homes — живой сайт компании / финальный домен | CONTRADICTED | curl 200, но это превью: финальный домен по файлам provenlyhomes.de, переключение не сделано — STATUS.md:45 "- [ ] DNS: CNAME provenlyhomes.de -> GitHub Pages"; на provenlyhomes.de сейчас старый сайт: curl → <meta name="generator" content="Framer 3db8496"> |

## CONTRADICTED и NOT_FOUND по проектам, с правкой текста

### staskiewitz

**Предлагаемая правка:**

Опровергнутых и ненайденных утверждений нет. Две правки по желанию, для точности:

- «1:1» (18 записанных отклонений) — DE: «26 Inhaltsseiten vom alten Auftritt übernommen und Block für Block geprüft» / EN: «26 content pages moved from the old site and checked block by block»
- «Honig-Shop» (126 товаров, B2C + B2B) — DE: «Shop für Honig und Imkereibedarf mit Rechnung und Vorkasse» / EN: «a shop for honey and beekeeping supplies with invoice and prepayment»
- url: после переезда (T001, фаза Ф5) заменить на https://www.imkerei-staskiewitz.de

### hennerheede

- **CONTRADICTED** — tagline_de+en, summary_de+en: Должность — Design Director. DEVLOG.md:423 "Должность `Design Director` → `Creative Director` везде, включая название сайта"; wp-theme/hennerheede/header.php:16 "<span class=\"role\">Creative Director</span>"
- **CONTRADICTED** — summary_de+en: ALPHATAURI в одном ряду с брендами-работодателями. docs/tasks/T009_PX006_Client_Fixes_0408_part3.md:87 "it does not belong to a company I worked for. Pls keep it only in CASE STUDIES"; STATUS.md:91 "Концепты убраны из полосы FORMER BRANDS — там только работодатели"
- **CONTRADICTED** — summary_de+en, tags: ACF. wp-theme/hennerheede/functions.php:4 "Поля контента сделаны нативными метабоксами: без ACF Pro и без платных плагинов,"; DEVLOG.md:562 "ACF Pro не нужен"
- **CONTRADICTED** — summary_de+en: 11 Seiten. verify/hrc_ledger_px011.json:92 "ITOG: stranic=12 v_karte=12 raznyh_opisanij=12 problem=0"; 11 из STATUS.md:249 включали Leadership, позже снятую в черновик (CLAUDE.md:38)
- **CONTRADICTED** — summary_de+en: Четыре кейса. docs/tasks/T013_P0_i18n_prod_migration.md:21 "case_study | boss:11, mango:12, baldessarini:13, mustang:14, alphatauri:131, neon:132" — 6 кейсов; NEON в тексте нет
- **CONTRADICTED** — summary_de+en: Кейсы с loop-видео. verify/hrc_ledger_px010.json:88 "На странице MANGO нет ни одного видео"; видео есть у 3 из 4: single-case_study.php:65 "autoplay loop muted playsinline"
- **CONTRADICTED** — summary_de+en: DSGVO-konform. docs/tasks/T015_NEON_de_text_and_footer.md:17 "Страниц **Imprint нет**, **privacy-policy = draft**"; живой замер 11.09: /imprint/ 200, /privacy-policy/ 404, /datenschutz/ 404, в футере только ссылка /imprint/ — Datenschutzerklärung на сайте нет
- **CONTRADICTED** — url: https://henner.ais152.com — финальный адрес. curl: 301 → https://hennerheede.com/ (200). verify/hrc_ledger_i18nprod.json:88 "henner.ais152.com 301-редиректит на hennerheede.com с сохранением пути"

**Предлагаемая правка:**

CONTRADICTED: Design Director, ALPHATAURI как бренд-работодатель, ACF, 11 Seiten, четыре кейса, loop-видео во всех кейсах, DSGVO-konform, url. Полная правка:

- tagline_de: Creative-Director-Portfolio — BOSS, MANGO, Baldessarini, Mustang
- tagline_en: Creative Director portfolio — BOSS, MANGO, Baldessarini, Mustang
- summary_de: Editorial-Portfolio für einen Münchner Creative Director in Fashion & Lifestyle (BOSS, MANGO, Baldessarini, Mustang). Handgeschriebenes WordPress-Theme mit eigenen Eingabefeldern im Admin — 12 Seiten, zweisprachig EN/DE: sechs Case Studies (vier Marken plus die Konzepte ALPHATAURI und NEON), teils mit Mood-Bildern und Loop-Video, Philosophy, CV-Zeitleiste, About, Contact. Enge Editorial-Typografie, Original-Markenlogos 1:1, self-hosted Schrift ohne externe CDNs.
- summary_en: Editorial portfolio for a Munich-based Creative Director in fashion & lifestyle (BOSS, MANGO, Baldessarini, Mustang). Hand-coded WordPress theme with custom admin fields — 12 pages, bilingual EN/DE: six case studies (four brands plus the ALPHATAURI and NEON concepts), some with mood imagery and looped video, Philosophy, CV timeline, About, Contact. Tight editorial typography, original brand logos 1:1, self-hosted font with no external CDNs.
- tags: Portfolio, Fashion, WordPress, Custom Theme, Editorial, DE/EN (ACF → Custom Theme)
- url: https://hennerheede.com
- «DSGVO-konform» можно вернуть, когда на сайте появится Datenschutzerklärung (сейчас /privacy-policy/ и /datenschutz/ → 404).

### taxi-moennigmann

- **NOT_FOUND** — summary_de+en: Для всей Ostfriesland (ganz / all). На сайте только src/data/i18n/de.json:16 "in Leer und Ostfriesland"; «ganz/all» нигде нет (искал src/data/i18n, CLAUDE.md, DEVLOG.md)
- **CONTRADICTED** — summary_de+en: Git-CMS для новостей. public/admin/index.html:16 "News-Verwaltung — Einrichtung erfolgt beim Deployment (Decap CMS)."; public/admin/config.yml:4 "⚠️ Фаза 5 (deploy): настроить backend + OAuth-провайдер" — не подключён; новости = Markdown при сборке (NewsPage.astro:13)
- **CONTRADICTED** — summary_de+en: 8 Leistungsbereiche. src/data/services.json: 6 × "type": "service" + 1 × "blog" (стр. 56) + 1 × "contact" (стр. 64); DEVLOG.md:279 "услуги 6×3" — услуг 6, а не 8
- **NOT_FOUND** — summary_de+en: Хостинг в Германии. Страна хостинга в файлах не названа (искал CLAUDE.md, DEVLOG.md, STATUS.md, docs/)

**Предлагаемая правка:**

CONTRADICTED: Git-CMS, 8 Leistungsbereiche. NOT_FOUND: «ganz Ostfriesland», хостинг «in Deutschland».

- summary_de: Firmenwebsite eines Taxiunternehmens in Leer und Ostfriesland. Astro-Static-Build mit Markdown-basiertem News-Bereich, self-hosted WOFF2-Schriften, Hero-Video, 6 Leistungsbereiche (Stadttaxi, Krankenfahrten, Inklusionstaxi, Flughafentransfers, Schülertransporte, Zeitlosreisen) plus News und Kontakt. WCAG 2.1 AA Barrierefreiheit als Differenzierungsmerkmal, Phone-first Mobile-UX, dreisprachig DE/EN/Plattdeutsch (Plattdeutsch auf Kundenwunsch), DSGVO-konform ohne Cookies und Tracking, Hosting bei ALL-INKL.
- summary_en: Corporate website for a taxi company in Leer serving Leer and Ostfriesland. Astro static build with a Markdown-based news section, self-hosted WOFF2 fonts, hero video, 6 service sections (Stadttaxi, Krankenfahrten, Inklusionstaxi, Flughafentransfers, Schülertransporte, Zeitlosreisen) plus news and contact. WCAG 2.1 AA accessibility as a differentiator, phone-first mobile UX, trilingual DE/EN/Plattdeutsch (Plattdeutsch on client request), DSGVO compliant with no cookies or tracking, hosted on ALL-INKL.
- «TTDSG» заменён на «ohne Cookies und Tracking»: закон с 2024 называется TDDDG. На самом сайте (datenschutz.astro:15) тоже стоит TTDSG — это отдельная правка сайта.

### sorrysara

- **NOT_FOUND** — summary_de+en: С телефона (vom Handy aus). Прямо нигде не сказано; следует из Telegram как инструмента (субъективно)
- **CONTRADICTED** — summary_de+en: Бот ведёт весь сайт (komplette Pflege / entire site). DEVLOG.md:149 "обработчики разделов `home:menu`,`home:events`" — только меню и события; часы, контакты, UI-тексты и legal живут в web/messages/*.json, web/src/data/contacts.json, legalContent.ts
- **CONTRADICTED** — summary_de+en: Возврат денег автоматически освобождает место. Код есть: route.ts:267 "case 'charge.refunded':"; но боевой вебхук подписан только на docs/CREDENTIALS.md:82 "события: checkout.session.completed, checkout.session.expired" — charge.refunded не доходит; живого возврата не тестировали
- **NOT_FOUND** — summary_de+en: Ручные правки владелицы не перезаписываются. Защита есть в bot/src/i18n.ts:214 "if (src === 'manual' && !opts.overwriteManual)", но потока ручной правки перевода в боте нет — setManual( вызывается только в i18n.ts и тестах
- **CONTRADICTED** — summary_de+en, tags: Мультиязычный сайт, 4 языка. web/src/i18n/config.ts:2 "locales = ['bg', 'en', 'uk', 'de']", но UI-тексты DE/UK = английские: скрипт сравнения web/messages/{de,uk}.json с en.json → de 121 из 123, uk 121 из 123 строк идентичны EN; legalContent.ts:270 "uk: privacyEn, de: privacyEn"; CLAUDE.md:17 "запуск на BG+EN, UK/DE по мере переводов Hanna"
- **CONTRADICTED** — tags: GDPR. Consent Mode есть (DEVLOG.md:445), но данные оператора — заглушки: 12 × "TODO_§16" в web/src/components/sections/legalContent.ts; на живой /privacy видны "TODO_§16"

**Предлагаемая правка:**

CONTRADICTED: «вся» поддержка через бот, возврат автоматически освобождает место, 4 языка / мультиязычный, GDPR. NOT_FOUND: «с телефона», ручные правки перевода сохраняются.

- summary_de: Eine Website für eine Cocktail- & Fry-Bar in Burgas (Oberfläche BG/EN, Menü und Events zusätzlich auf UK/DE), deren Inhaberin Inhalte per Telegram pflegt. Statt klassischem Admin-Panel laufen Menü und Events — samt Fotos, Preisen und Übersetzungen — über einen Telegram-Bot: klick-klick, tippen nur den Wert. Bezahl-Events verkaufen Tickets über Stripe mit garantiert überbuchungsfreier Platzsteuerung. Auf Bulgarisch geschriebene Inhalte werden von Claude automatisch nach EN/UK/DE übersetzt.
- summary_en: A website for a Burgas cocktail & fry bar (BG/EN interface, menu and events also in UK/DE) whose owner manages content through Telegram. Instead of a classic admin panel, the menu and events — including photos, prices and translations — are managed through a Telegram bot: tap-tap, type only the value. Paid events sell tickets via Stripe with race-safe, no-overbooking seat control. Content written in Bulgarian is auto-translated to EN/UK/DE by Claude.
- tags: Telegram-CMS, Stripe Ticketing, BG/EN + UK/DE-Inhalte (EN: BG/EN + UK/DE content), Anti-Overbooking, Consent Mode v2 (вместо GDPR, пока в legal-тексте стоят TODO_§16)
- Фразу про возврат можно вернуть, когда на боевом вебхуке Stripe подпишут charge.refunded.

### silkekleinart

- **NOT_FOUND** — summary_de+en: Страницы тоже через «aufgeräumte WP-Formulare». Для страниц ACF-форма только у одного шаблона: acf-fields.php:179-181 "'page-templates/galerie-rubrik.php'"; остальные страницы — обычный WP-редактор
- **CONTRADICTED** — summary_de+en: Vollständig DSGVO-konform. docs/tasks/PX-030_AUDIT_REPORT.md:79 "**LOW — Datenschutz Hosting-Klausel kaputt**"; docker/seed/seed.json:405 "Wir haben Wordfence auf dieser Website eingebunden" — Wordfence на новом сайте нет (PX-033:12,27); исправление нигде не записано
- **NOT_FOUND** — summary_de+en: Barrierefreiheit (BFSG 2025). BFSG только как цель брифа: CDP_SilkeKleinArt_Design.md:252 "a11y (BFSG 2025 / WCAG AA — КРИТИЧНО…)"; аудита нет, только Lighthouse DEVLOG.md:144 "a11y 96–98"

**Предлагаемая правка:**

CONTRADICTED: «vollständig DSGVO-konform». NOT_FOUND: страницы через WP-формы, BFSG 2025.

- summary_de: Premium-Neubau der Website einer Kieler Malerin. Handgeschriebenes WordPress-Theme mit Advanced Custom Fields und Custom Post Types — die Künstlerin pflegt Werke und Ausstellungen über aufgeräumte WP-Formulare, Seiten im WP-Editor, ohne Page-Builder. Editorial-Typografie, responsive Galerie, self-hosted Schriften, Cookie-Banner ohne Tracking und barrierearme Umsetzung.
- summary_en: Premium rebuild of a Kiel-based painter's website. Hand-coded WordPress theme with Advanced Custom Fields and Custom Post Types — the artist manages works and exhibitions through clean WP forms and pages in the WP editor, no page builder. Editorial typography, responsive gallery, self-hosted fonts, a tracking-free cookie banner and an accessibility-minded build.
- Datenschutzerklärung на живом сайте всё ещё содержит Wordfence и сломанную клаузулу о хостинге (PX-030:79) — это отдельная правка сайта.

### ofnstube

- **CONTRADICTED** — tagline_de+en, summary_de+en: Реальный ресторан-клиент. CLAUDE.md:15 "Ofnstube — Munich Craft-Burger (fictional brand, баварский Stube-feel)"; pages/reservation.html:327 "Ofnstube — fiktives Demo-Projekt, alle Angaben sind Platzhalter"
- **CONTRADICTED** — tagline_de+en, summary_de+en: Работающая In-House-Reservierung. pages/reservation.html:192 "<form class=\"form\" action=\"#\" method=\"post\""; :246 "Der Versand des Formulars wird in einer späteren Prototyp-Stufe angebunden"
- **CONTRADICTED** — summary_de+en: Ссылка «LMIV §1169». pages/menu.html:170 "Verordnung (EU) 1169/2011" — 1169 это номер регламента, а не параграф
- **NOT_FOUND** — summary_de+en: BFSG 2025 Barrierefreiheit. Меры есть (base.css:109 "Focus (BFSG …)"), но аудит открыт: README.md:112 "⬜ BFSG-Audit mit Screenreader + Lighthouse vor Launch"
- **CONTRADICTED** — summary_de+en: Vollständig DSGVO-konform. pages/datenschutz.html:112 "Diese Datenschutzerklärung ist ein Platzhalter für den R&D-Prototyp."; README.md:109 "⬜ Impressum / Datenschutz / AGB — anwaltlich zu finalisieren"

**Предлагаемая правка:**

CONTRADICTED: реальный ресторан (по файлам — вымышленный демо-проект), работающая резервация, «LMIV §1169», «vollständig DSGVO-konform». NOT_FOUND: BFSG 2025.

- tagline_de: Fiktives Münchner Craft-Burger-Restaurant — Konzept-Site mit Reservierungsseite
- tagline_en: Fictional Munich craft-burger restaurant — concept site with reservation page
- summary_de: Konzept-Website für ein fiktives Münchner Craft-Burger-Restaurant. Vanilla HTML5 + CSS3 + JS, Multi-Page (10 Seiten), self-hosted Fraunces + Inter, GSAP + Lenis. Reservierungsseite (Quandoo-2-Klick-Platzhalter, Anfrageformular ohne Backend), Allergen-Kennzeichnung nach LMIV (VO (EU) Nr. 1169/2011), JuSchG-Altershinweise, barrierearm umgesetzt, Datenschutz by Design (self-hosted Assets, 2-Klick-Embeds, keine Analytics).
- summary_en: Concept website for a fictional Munich craft-burger restaurant. Vanilla HTML5 + CSS3 + JS, multi-page (10 pages), self-hosted Fraunces + Inter fonts, GSAP + Lenis. Reservation page (Quandoo two-click placeholder, request form without backend), allergen labelling under LMIV (Regulation (EU) No 1169/2011), JuSchG age notes, accessibility-minded build, privacy by design (self-hosted assets, two-click embeds, no analytics).

### elektrocheck-stuttgart

- **CONTRADICTED** — summary_de: Elektromeister. design/desktop/phase-3/impressum.html:57 "Berufsbezeichnung: Elektrofachkraft / Befähigte Person nach TRBS 1203" — «Meister» в проекте нет
- **CONTRADICTED** — summary_de+en: Для частных клиентов (Privatkunden). index.html:555 — только "Unternehmen und Gewerbekunden"; script.js:163 "Privatvermieter ohne Beschäftigte = nicht DGUV V3-pflichtig"
- **NOT_FOUND** — summary_de+en: Vollständig DSGVO-konform. Перенос в США только по datenschutz.html:114 "Art. 49 Abs. 1 lit. b DSGVO"; AVV с FormSubmit нет; юрист не подтвердил (HANGING_ITEMS.md:14 H-08); impressum.html:66 "Steuernummer: Wird nach Erteilung durch Finanzamt ergänzt"
- **CONTRADICTED** — summary_de+en: GitHub Pages. DEVLOG.md:113 "23 files uploaded → перемещены в `/public/` (IONOS требует subfolder)"; scripts/sftp_upload.py:3 "SFTP upload phase-3/ → IONOS Webhosting Standard"; GitHub Pages — только исходный план CLAUDE.md:18

**Предлагаемая правка:**

CONTRADICTED: Elektromeister, Privatkunden, GitHub Pages. NOT_FOUND: «vollständig DSGVO-konform».

- summary_de: Landing-Site für einen DGUV V3-Prüfdienst im Raum Stuttgart (Elektrofachkraft, in die Handwerksrolle eingetragen), der Prüfungen für Unternehmen und Gewerbekunden anbietet. Verbindliches Festpreis-Angebot, deutsches Kontaktformular über FormSubmit, Impressum und Datenschutzerklärung nach DSGVO. Vanilla HTML+CSS+JS, IONOS Webhosting, eigene Domain.
- summary_en: Landing site for a Stuttgart-area DGUV V3 inspection service (qualified electrician, registered with the Chamber of Crafts) offering legally required safety inspections for businesses and commercial clients. Binding fixed-price quotes, German contact form via FormSubmit, imprint and DSGVO privacy policy. Vanilla HTML+CSS+JS, IONOS web hosting, custom domain.
- Taglines без изменений.

### kontur

- **CONTRADICTED** — summary_de+en: Shop для реальной немецкой обжарочной (клиентский проект). CLAUDE.md:14 "Портфолио-кейс."; CLAUDE.md:15 "Онлайн-магазин specialty-кофе вымышленной немецкой Kaffeerösterei «KONTUR»"; docs/tasks/T004_faza_d_kontent_foto.md:37 "Реальной компании нет"
- **CONTRADICTED** — summary_de+en: Kaffee-Abo (подписка). docs/tasks/T003_faza_c_woocommerce_integraciya.md:95 "обычный WC-товар «Abo» с мета-данными, без рекуррентных платежей, без платного плагина" — конфигуратор, не подписка
- **NOT_FOUND** — summary_de+en: Konform mit deutschem E-Commerce-Recht. Только внутренний чек-лист DEVLOG.md:165 "Юр-чеклист: … все PASS"; T004:87 "Данные компании — плейсхолдеры (… USt DE000000000)"; юр. проверки нет (T004:37)

**Предлагаемая правка:**

CONTRADICTED: магазин для реальной обжарочной (по файлам — вымышленный бренд, портфолио-кейс), Kaffee-Abo. NOT_FOUND: «konform mit deutschem E-Commerce-Recht».

- tagline_de: Specialty-Kaffeerösterei (Konzept) — individueller WooCommerce-Shop
- tagline_en: Specialty coffee roastery concept — custom WooCommerce store
- summary_de: Konzept-Shop für eine fiktive deutsche Specialty-Kaffeerösterei (Portfolio-Case). Handgeschriebenes WordPress-Theme — kein Page-Builder — mit WooCommerce: Katalog, Produktseiten, Warenkorb, Checkout und Abo-Konfigurator. Editorial-Design mit eingebauten Pflichtangaben nach deutschem E-Commerce-Recht (DSGVO, PAngV, LMIV).
- summary_en: Concept store for a fictional German specialty coffee roastery (portfolio case). Hand-coded WordPress theme — no page builder — with WooCommerce: catalog, product pages, cart, checkout and a subscription configurator. Editorial design with German e-commerce disclosures built in (DSGVO, PAngV, LMIV).
- На живой /abo/ (page-abo.php:77, :97) обещано «jederzeit im Konto kündbar» — такой функции нет. Это правка сайта.

### pomp

- **CONTRADICTED** — summary_de+en: Komplettes / full Brand-Paket. Brands/POMP.md:101 "OG flat-lay (deferred) … ⏸️"; :102 "Lifestyle shots × 3 (deferred)"; public/og-image.jpg отсутствует при ссылке в layout.tsx:26

**Предлагаемая правка:**

CONTRADICTED: «komplettes / full Brand-Paket».

- summary_de: Brand-Paket (Wortmarke, Farb- und Typo-System, Tonalität) und Produktions-Landing für ein Sparkling-Water-Konzept mit sechs Sorten. Hero-Video, scroll-gepinntes Sorten-Karussell auf Desktop, natives Snap-Scrollen mobil, freigestellte Produkt-Shots, Dunkel-/Cream-Rhythmus. Next.js 16, Tailwind 4, GSAP, Lenis.
- summary_en: Brand pack (wordmark, colour and type system, tone of voice) and production landing for a sparkling water concept with six flavours. Hero video, scroll-pinned flavour carousel on desktop, native snap-scroll on mobile, transparent product shots, dark/cream colour rhythm. Next.js 16, Tailwind 4, GSAP, Lenis.
- Попутно исправлена грамматика: «scroll-gepinnte Sorten-Karussell» → «scroll-gepinntes Sorten-Karussell».

### baupreis

- **NOT_FOUND** — tagline_de+en: Intelligentere Baubudgets / smarter budgets. Функции бюджетов нет; продукт — мониторинг цен и рекомендация buy_now/wait/watch (analyze/route.ts:183) (субъективно)
- **CONTRADICTED** — summary_de: Für deutsche Handwerksbetriebe. CLAUDE.md:15 "Платформа для немецких строительных компаний (Bauunternehmen, Einkäufer, Projektleiter)"; app/src/i18n/de.ts:12 "für deutsche Bauunternehmen"
- **CONTRADICTED** — summary_de+en: 16+ Materialien. Скрипт по init.sql (INSERT INTO materials) → 16 строк, в migrations/ новых нет; с данными 15: STATUS.md:33 "Diesel: нет TANKERKOENIG_API_KEY (15/16 материалов)"
- **CONTRADICTED** — tags: Stripe. DEVLOG.md:547 "Billing на сервере = PayPal+Paddle, НЕ Stripe (CREDENTIALS.md drift)"; STATUS.md:35 "Stripe: test mode"

**Предлагаемая правка:**

CONTRADICTED: Handwerksbetriebe, «16+» материалов, тег Stripe. NOT_FOUND: «intelligentere Baubudgets».

- tagline_de: KI-Prognosen für Baustoffpreise
- tagline_en: AI forecasts for construction material prices
- summary_de: KI-gestützte Überwachung von Baustoffpreisen für deutsche Bauunternehmen. 16 Materialien, Preisvorhersagen, Multi-Tenant-SaaS mit drei Tarifebenen und Claude-Trendanalyse.
- summary_en: AI-powered construction material price monitoring for German construction companies. 16 materials, price forecasts, multi-tenant SaaS with three pricing tiers and Claude-driven trend analysis.
- tags: SaaS, AI, Next.js, Claude API, Multi-tenant (вместо Stripe)

### eko-oylis-ua

- **CONTRADICTED** — summary_de+en: Vollständig self-hosted. Шрифты и скрипты локальные, но форма уходит в Cloudflare Worker: src/_data/site.json:19 "\"formEndpoint\": \"https://eko-form.eko-oylis.workers.dev\""
- **CONTRADICTED** — tags: DSGVO. Меры есть (согласие contacts.njk:59 "name=\"gdpr_consent\" required"), но privacy.njk:14 "Цей документ — заглушка. Перед публікацією підлягає юридичній перевірці."

**Предлагаемая правка:**

CONTRADICTED: «vollständig self-hosted» (форма уходит на Cloudflare Worker), тег DSGVO (privacy — заглушка).

- summary_de: Firmenwebsite eines ukrainischen Altspeisefett-Sammlers mit EU-Expansion über Bulgarien. Zweisprachig UA/EN, 11 Meilensteine (2008→2026, 2500+ HoReCa-Partner, eigene Flotte), Eleventy + GSAP + Lenis, schema.org, Schriften und Skripte self-hosted (kein CDN).
- summary_en: Corporate site for a Ukrainian used cooking oil collector with EU expansion via Bulgaria. Bilingual UA/EN, 11-milestone history (2008→2026, 2500+ HoReCa partners, own fleet), Eleventy + GSAP + Lenis, schema.org, self-hosted fonts and scripts (no CDN).
- tags: Corporate, Bilingual, Eleventy, GSAP, Privacy by Design (вместо DSGVO)

### rundumshaus

- **CONTRADICTED** — summary_de+en: DSGVO-konform. site/src/app/datenschutz/page.tsx:68-70 "Es werden keine Tracking-Cookies, Analyse-Tools oder Drittanbieter-Skripte eingesetzt." — при этом site/src/app/layout.tsx:250 "src=\"https://plausible.io/js/script.js\""; datenschutz/page.tsx:77 "(Lora, Plus Jakarta Sans)" — сайт уже на Inter

**Предлагаемая правка:**

CONTRADICTED: «DSGVO-konform» (Datenschutzerklärung отрицает аналитику, а сайт грузит Plausible; названы старые шрифты).

- summary_de: Premium-Website für einen Hausmeister- und Gartenservice in Osnabrück. Fünf Leistungskategorien mit WhatsApp-Integration, KI-generierte Bildwelt, Mobile-Sticky-CTA, Impressum, Datenschutzerklärung und Cookie-Hinweis.
- summary_en: Premium website for a caretaking and garden service in Osnabrück. Five service categories with WhatsApp integration, AI-generated imagery, mobile sticky CTA, imprint, privacy policy and cookie notice.
- По желанию, чтобы DE- и EN-tagline говорили одно и то же — DE: Hausmeisterservice, Garten, Dach und Entrümpelung aus einer Hand / EN: Caretaking, garden, roof and clear-outs from one provider
- «DSGVO-konform» можно вернуть после исправления datenschutz/page.tsx (Plausible, Inter). Это правка сайта клиента.

### provenly-homes

- **NOT_FOUND** — tagline_de+en: Premium. Только в собственном брендинге проекта: branding/BRAND_GUIDE.md:91 "With \"Premium Property Management\" subtitle"; в текстах сайта нет (субъективно)
- **CONTRADICTED** — tagline_de+en: Бизнес — «Kurzzeitvermietung / short-term rentals». CLAUDE.md:15 "Новый сайт для компании по управлению краткосрочной арендой недвижимости в NRW"; site/src/data/homepage.json:4 "Wir übernehmen Betrieb, Gäste, Zustand und Ertrag" — это управление арендой для собственников
- **NOT_FOUND** — summary_de+en: Сделан «für ein Unternehmen» (сданный клиентский проект). Договора/приёмки нет; STATUS.md:47 "- [ ] Final walkthrough + sign-off"; префикс fr_02 — питч; отношения с клиентом знает только CEO
- **NOT_FOUND** — summary_de+en: Awwwards-Effekte / Awwwards-level. Только цель: CLAUDE.md:15 "Целевой уровень — Awwwards"; приёмочные пункты T004_awwwards_design_gap.md:100-118 не отмечены (субъективно)
- **CONTRADICTED** — url: github.io/provenly-homes — живой сайт компании / финальный домен. curl 200, но это превью: финальный домен по файлам provenlyhomes.de, переключение не сделано — STATUS.md:45 "- [ ] DNS: CNAME provenlyhomes.de -> GitHub Pages"; на provenlyhomes.de сейчас старый сайт: curl → <meta name="generator" content="Framer 3db8496">

**Предлагаемая правка:**

CONTRADICTED: «Kurzzeitvermietung» как бизнес (на деле управление арендой), url как живой сайт компании. NOT_FOUND: Premium, сданный клиентский проект, Awwwards.

- tagline_de: Kurzzeitvermietungs-Management mit Motion-Design
- tagline_en: Short-term rental management with motion design
- summary_de: Relaunch-Entwurf der Corporate-Website eines Kurzzeitvermietungs-Managements aus Köln. An Awwwards-Referenzen orientierte Scroll-Animationen, GSAP + Motion hybrid, JSON-getriebener Inhalt, Vorschau auf GitHub Pages.
- summary_en: Relaunch draft of the corporate website of a short-term rental management company in Cologne. Scroll animations modelled on Awwwards references, GSAP + Motion hybrid, JSON-driven content, preview on GitHub Pages.
- status «live»: по файлам сайт не переключён на provenlyhomes.de (там работает Framer), приёмки нет. Показывать как концепт или превью, пока CEO не подтвердит отношения с клиентом.
