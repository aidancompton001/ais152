# Kleinanzeigen-Strategie AIS.152 — München

> Erstellt: 12.08.2026 · Grundlage: Live-Recherche kleinanzeigen.de (Playwright, 12.08.2026),
> Preis-Benchmarks (Quellen в §10), Rechtsrecherche §5 DDG / §312g BGB / PAngV / §19 UStG.
> Alle Zahlen mit Quelle. Nicht verifizierte Punkte sind in Abschnitt 9 gesammelt.

---

## 0. Executive Summary

**Начни с варианта A — Website-Wartung.** Не с создания сайтов.

Причина одна и она измеримая: поиск `website wartung` в München на Kleinanzeigen возвращает **ноль результатов** — дословно «Es wurden keine Ergebnisse». То же самое по `website umzug` (0), `barrierefreiheit website` (0), `ki agentur` (0). При этом рынок за Wartung платит 50–250 €/мес (два независимых источника, §10), и это **рекуррентная** выручка, а не разовая.

Параллельно — рынок создания сайтов в München на Kleinanzeigen забит: 15 объявлений по запросу `webdesign`, все gewerblich, приватных ноль. Заходить туда пятым одинаковым «Website erstellen lassen» — значит соревноваться ценой с 25-евровым студентом снизу и с Kecke Lösungen GbR за 1.999 € сверху.

Ключевая асимметрия рынка, которую никто не использует: **из 15 объявлений в выдаче München физически в München сидят только ~7.** Остальные — Nürnberg, Augsburg, Waiblingen, Würzburg, Regensburg с пометкой «+ 200 km · Kommt zu dir». Слово «München» в заголовке стоит ровно у одного конкурента. Локальность — свободный аргумент.

**Рекомендованный порядок запуска:**

| Приоритет | Вариант | Обоснование |
|---|---|---|
| 1 | **A — Wartung & Betreuung** | 0 конкурентов, рекуррентные 39–79 €/мес, низкий порог входа для клиента |
| 2 | **B — Praxis-Website (DSGVO + AVV)** | 0 объявлений в нише, у тебя live AVV-Muster (Art. 28 DSGVO) — ни у кого нет |
| 3 | **C — KI/Automatisierung** | 1 реальное объявление по `n8n` во всём München, лучшая маржа на час |
| 4 | **E — Website-Umzug/Rettung** | 0 конкурентов, дешёвый вход (149 €) → апселл в Wartung |
| 5 | **D — Landingpage** | Самая конкурентная ниша, идти туда последним и только по цене-качеству |

Бесплатных объявлений в категории Dienstleistungen — **2 или 3 в 30 дней** (источники расходятся, см. §9). Значит физически стартуем с **A + B**, остальное докупаем по ~4–5 €/шт. или ротируем.

**Три вещи, которые надо сделать ДО первой публикации** (детали в §8):
1. Убрать ссылку на OS-Plattform из `impressum.html` — платформа выключена 20.07.2025, живая ссылка на неё сама по себе Abmahn-повод.
2. Настроить блок «Rechtliche Angaben» в Anzeigen-Manager (один раз — применяется ко всем объявлениям).
3. Починить расхождение 10 vs 16 проектов в About на ais152.com.

---

## 1. Wettbewerber-Research

### 1.1 Структура категорий — важная поправка

**Отдельной категории «Webdesign», «IT» или «Softwareentwicklung» на Kleinanzeigen не существует.** Веб-услуги размазаны по двум веткам:

| Ветка | ID | URL-шаблон | Доля |
|---|---|---|---|
| Dienstleistungen → **Weitere Dienstleistungen** | c298 | `/s-sonstige/muenchen/c298l6411` | ~85% объявлений |
| Elektronik → **Büro, IT & EDV-Dienstleistungen** | c226 | `/s-dienstleistungen-edv/muenchen/c226l6411` | остальное |

München = `l6411`. Верхний уровень Dienstleistungen = `c297`.

Практический вывод: **трафик приходит через keyword-поиск, а не через дерево категорий.** Заголовок несёт двойную нагрузку — он и рекламный текст, и SEO-запрос. Отсюда keyword-спам у конкурентов. Мы пойдём другим путём (см. §3).

**Рекомендация по категории — уточнена по живой форме размещения 12.08.2026:**
В ветке `Dienstleistungen` подкатегории «Büro, IT & EDV» **нет** — там только Altenpflege, Auto/Rad/Boot, Babysitter, Elektronik, Haus & Garten, Künstler/Musiker, Reise & Event, Tierbetreuung, Umzug & Transport, **Weitere Dienstleistungen**. Категория c226 «Büro, IT & EDV-Dienstleistungen» лежит под верхним уровнем `Elektronik`, а не под `Dienstleistungen`.

Поэтому **все пять вариантов идут в `Dienstleistungen → Weitere Dienstleistungen` (c298)** — именно там сидят ~85% веб-объявлений München.

### 1.2 Объём рынка (h1 живой выдачи, 12.08.2026)

| Запрос в München | Результатов |
|---|---|
| `webdesign` в Dienstleistungen c297 | 15 (**gewerblich 15 из 15, privat 0**) |
| `webseite erstellen` | 15 |
| `softwareentwicklung` | 13 — **почти все вакансии** (stepstone/xing), реально услугу предлагает 1 |
| c226 «Büro, IT & EDV» целиком | 235 |
| c297 Dienstleistungen целиком | 5.396 |

### 1.3 Топ-конкуренты

**№1 — Kecke Lösungen GbR — самый сильный, эталон для битья**
`1.999 €` Festpreis · 80331 Altstadt-Lehel · 01.08.2026 · 118 просмотров · gewerblich с 17.11.2025.
Заголовок: «Professionelle Business Website erstellen lassen inkl (DSGVO + SEO + Branding & Logo + kostenloser chatbot) | Homepage | Webdesign | ...»
Дословно: «Direkt, transparent, ohne unnötiges Agentur-Blabla» · «✅ Individuelles, responsives Design (kein 0815-Template)» · «✅ DSGVO-ready (Impressum, Datenschutz & Cookie-Banner)» · «KI-Chatbot kostenlos inklusive (Wert 297 €)» · «⚡ Fertigstellung: 9 Tage» · «(Optional) Wartung: 39 €/Monat».
**Единственный, кто собрал полный пакет:** DSGVO + чатбот + Wartung + жёсткий срок + внешняя форма заказа.
*Слабость:* GbR из двух человек, но подаётся как агентство; 1.999 € — верхняя граница для Kleinanzeigen-аудитории; чатбот «бесплатно» обесценивает KI как продукт.

**№2 — STBR Solutions (Niclas)** — `499 €`, 80995 Feldmoching, аккаунт с 29.06.2026.
Трёхуровневая сетка в тексте: «ESSENTIAL – 499 €» / «GROWTH – 899 € ⭐ BELIEBT» / «SCALE – 1.699 €» + «WARTUNG & PFLEGE – 49 €/Monat». «Fertig in 3–7 Werktagen», «Kein Abo, keine versteckten Kosten».
*Слабость:* **портфолио отсутствует полностью.** Легитимация — «Seit meinem 16. Lebensjahr beschäftige ich mich mit digitalem Business». Аккаунт 6 недель. Для Praxis или Handwerk это не аргумент.

**№3 — Logo-Homepage.de / logo2buy.de** — `790 € VB`, 81925 Bogenhausen, аккаунт с 26.05.2022, бейджи «TOP Zufriedenheit».
Сильнейший по доверию: «5,0 ⭐ Google Bewertungen · 6 Jahre Erfahrung · Ratenzahlung möglich», **16 доменов-референсов списком** (naturheilpraxis-verde.de, hausmeister-kosta.de, stadler-reinigungsservice.de …), «DSGVO-konform inkl. Impressum».
*Слабость:* заголовок — свалка из 20 keyword'ов; позиционирование размыто между веб-разработкой и полиграфией (Fahnen, Leuchtkästen, Visitenkarten).

**№4 — «Moe» / alpine-dev.de** — `VB` без цены, 81673 Berg-am-Laim, аккаунт с 24.11.2024.
Единственный, кто явно бьёт по нашей целевой: «Zu meinem Portfolio gehören u.a. Praxen, Anwälte, Bauunternehmen, Gastronomen, Immobilienfirmen, NGOs». Играет на личном контакте: «Mir ist ein persönliches Treffen wichtig… oder wir besprechen deine Wünsche bei einem Kaffee».
**Позиционируется явно ПРОТИВ AI:** «in einer Qualität, die man sonst eher von teuren Agenturen kennt, nur ohne deren Preis und ohne AI-Slops».
*Слабость:* «ich studiere derzeit Cybersecurity» — студент; ни одной цены; список услуг слишком широкий.

**№5 — List & Sell GmbH München** — `VB`, 81249 Allach-Untermenzing.
Стоковый заход: «Warum brauchen Sie eine Webseite? Ohne eine Webseite können Sie Ihr Geschäft und Ihre Ideen nicht optimal präsentieren…». Длинный список галочек, CMS-перечисление (WordPress, Joomla, Drupal).
*Слабость:* GmbH, а портфолио упомянуто **без ссылки** — «Auf unserer Webseite finden Sie im Portfolio». Цены нет. DSGVO не упомянут вообще.

**№6 — «IT-Student erstellt professionelle Webseiten»** — `25 € VB`, ценовое дно, висит с 18.06.2026 (~2 месяца без результата).

**Иногородние с «+200 km»:** Nürnberg 599 €, Regensburg 999 € (без PRO-бейджа в выдаче — статус не подтверждён на детальной странице), Augsburg 299 € VB («Top Dienstleister 23-2024»), Waiblingen 1.000 € VB («5,0 ⭐ (124) Google Rezensionen»).

### 1.4 Систематические слабости конкурентов — наша карта атаки

| Слабость | Насколько распространена | Наш ответ |
|---|---|---|
| **Нет цены (только «VB»)** | 3 из 7 локальных, включая GmbH | Конкретная якорная цена в заголовке |
| **Заголовок — keyword-свалка 15–25 слов** | почти все | Читаемый заголовок из одного обещания |
| **Портфолио отсутствует или без ссылки** | 5 из 7 | 16 live-URL, которые клиент откроет и проверит |
| **DSGVO упоминают только 3 из 15** | — | DSGVO + AVV как отдельный продукт |
| **Сроки не называет почти никто** | искл. 9 Tage / 3–7 Werktage | Жёсткий срок в заголовке |
| **Wartung продают 2 из 15** | 39 € и 49 €/мес | Wartung как **основной** продукт |
| **Отзывы копипастой без ссылки** | «5,0 ⭐ (124)» текстом | Не имитировать, работать проверяемыми URL |
| **Локальность не используется** | «München» в заголовке у 1 из 15 | München в каждом заголовке |

### 1.5 Непокрытые ниши (проверено, живая выдача München)

| Ниша | Конкурентов | Комментарий |
|---|---|---|
| `website wartung` | **0** | «Es wurden keine Ergebnisse» |
| `website umzug` | **0** | |
| `barrierefreiheit website` | **0** | но см. §9 — как аргумент применять осторожно |
| `ki agentur` | **0** | |
| `make automatisierung` | **0** | |
| `n8n` | **1** реальное | «Büroarbeit automatisieren – KI & n8n Workflows» |
| `chatbot` | **2** | одно — чатбот как бесплатный бонус (Kecke) |
| Praxis-Website как отдельное объявление | **0** | только упоминание в списке у Moe |
| Softwareentwicklung как услуга | **1** | остальные 12 — вакансии |

---

## 2. Стратегия позиционирования

### 2.1 USP — три опоры, каждая проверяема

**Опора 1: «Ich baue nicht nur, ich betreibe.»**
Конкуренты продают сборку и исчезают — Wartung есть у 2 из 15. Это разворачивает всю коммуникацию: не «сделаю сайт», а «беру сайт на себя». Продукт входа дешёвый (39 €/мес), удержание долгое, и он же — канал для апселла.

**Опора 2: Проверяемое портфолио вместо прилагательных.**
У нас 16 live-проектов с URL, которые клиент откроет прямо сейчас. Из них для Kleinanzeigen-аудитории ценнее всего именно немецкие локальные бизнесы, а не SaaS:

| Проект | URL | Почему релевантен |
|---|---|---|
| Taxi Mönnigmann | taxi-moennigmann.de | локальный DE-бизнес, WCAG 2.1 AA, DSGVO |
| ElektroCheck Stuttgart | elektrocheckstuttgart.de | Handwerk/B2B-услуга, DSGVO |
| Rund ums Haus Littawe | rundumshaus-littawe.de | Handwerk, SEO |
| Silke Klein Art | silkekleinart.com | Solo-Selbstständige, WordPress |
| Henner Heede | henner.ais152.com | портфолио-сайт, WordPress + ACF |

Пять ссылок бьют любое «professionell & zuverlässig». Против конкурента, у которого портфолио вообще нет (STBR за 499 €) или упомянуто без URL (List & Sell GmbH), это решающий аргумент.

**Опора 3: Готовый юридический пакет.**
На ais152.com уже live: Impressum, Datenschutz, **AVV-Muster по Art. 28 DSGVO**, Rechnungsmuster. AVV — это то, чего нет ни у одного конкурента в München, и то, что Praxis обязана иметь, отдавая доступ к сайту с данными пациентов. Наш AVV прямо содержит в § 4: «ggf. Patienten oder Klienten (bei medizinischen/therapeutischen Praxen)».

Это превращает юридическую формальность в товар: клиент получает не только сайт, но и подписываемый документ, который закрывает его собственную обязанность по Art. 28.

### 2.2 AISI 52100 storytelling — на Kleinanzeigen НЕ использовать

**Рекомендация: отказаться.** Обоснование:

Метафора подшипниковой стали требует двух шагов объяснения — что такое AISI 52100 и почему это про софт. На сайте, где у читателя есть время и контекст, она работает и придаёт имя смысл. На Kleinanzeigen у объявления есть ~3 секунды на скан заголовка и первых двух строк, и читатель — Praxisinhaberin или мастер-электрик, а не инженер. Там метафора занимает место, которое должно нести цену, срок и доказательство.

Хуже того: рядом стоят конкуренты, которые бьют прямо — «Fertig in 3–7 Werktagen», «1.999 € Festpreis». Поэтичный заход на их фоне читается как уход от конкретики.

**Где storytelling остаётся:** на ais152.com (уже там), в презентации при личной встрече, в коммерческом предложении после первого контакта. То есть — на втором шаге воронки, когда внимание уже куплено.

Единственная допустимая форма на Kleinanzeigen — сухая подпись в конце: `AIS.152 · Eduard Morocho Baias · ais152.com`. Название работает как знак, без объяснения.

### 2.3 Einzelunternehmer + Kleinunternehmer — играть ЗА, и жёстко

Оба статуса — актив, не оправдание. Но по разным причинам.

**Einzelunternehmer** — конкуренты сами продают это как преимущество («ohne unnötiges Agentur-Blabla», «Direkter Ansprechpartner – kein Agentur-Overhead»). Значит рынок аргумент уже принял, и мы не изобретаем, а исполняем его лучше: у нас за спиной 16 реальных проектов, а не «с 16 лет занимаюсь digital business».

**Kleinunternehmer §19 UStG — здесь есть аргумент, который не использует никто, и он сильнее, чем кажется.**

Логика: Heilberufe (Ärzte, Physiotherapeuten, Heilpraktiker) оказывают услуги, освобождённые от НДС по §4 Nr. 14 UStG. Прямое следствие освобождения — **у них нет права на Vorsteuerabzug**. То есть НДС, который им выставляет подрядчик, они вернуть не могут, и он для них чистая переплата.

Что это значит на цифрах: конкурент выставляет Praxis 1.999 € netto → с 19% НДС это 2.378,81 € реальных расходов. Наши 690 € — это 690 € расходов, без надбавки. Разница для клиента не 1.309 €, а **1.688,81 €**.

Та же логика работает для: Vereine, частных лиц, Kleinunternehmer-коллег, врачей, психотерапевтов, некоммерческих организаций — всех, кто не vorsteuerabzugsberechtigt.

**Как формулировать в объявлении** (осторожно, см. §4.4 — «inkl. MwSt.» писать запрещено):
> «Kein Ausweis von Umsatzsteuer gemäß § 19 UStG. Für Praxen, Vereine und Privatpersonen ohne Vorsteuerabzug bedeutet das: der genannte Preis ist Ihr tatsächlicher Endpreis.»

Где статус — минус: крупный B2B-клиент с Vorsteuerabzug на нём ничего не выигрывает, а лимит 25.000 €/год читается как «мелкий». Вывод: в B2B-объявлениях (вариант C, KI/Automation) §19 не выпячивать — упомянуть один раз в юридическом блоке и всё.

### 2.4 Целевые аудитории — приоритет

| # | Аудитория | Почему | Через какой вариант |
|---|---|---|---|
| 1 | **Kleine Praxen** (Ärzte, Physio, Heilpraktiker, Zahnärzte, Psychotherapeuten) | DSGVO-давление реальное, AVV обязателен, §19-эффект максимальный, конкурентов 0, кейс Greta уже в работе | B, затем A |
| 2 | **Handwerk / lokale Dienstleister** (Elektriker, Hausmeister, Reinigung, Taxi, Gastro) | Уже есть 3 прямых референса; платят за результат, не за дизайн; мало кто из них умеет сам обслуживать сайт | A, D |
| 3 | **Solo-Selbstständige и Vereine** | не vorsteuerabzugsberechtigt → §19-эффект; бюджет малый → Wartung заходит лучше, чем новый сайт | A, E |
| 4 | **KMU 5–50 человек** для автоматизации | лучшая маржа, ниша пуста, но цикл сделки длиннее | C |
| 5 | Startups | самая конкурентная ниша, платят мало, торгуются много | D — последним |

**Отдельно про «Alte-Etablierte»:** это не отдельная аудитория, а состояние внутри 1 и 2 — фирма с сайтом 2013 года на устаревшем хостинге. Именно они — целевая для варианта E (Umzug/Rettung), и заходить к ним надо не через «новый сайт», а через «ваш сайт под угрозой».

---

## 3. Объявления

> Общие правила для всех: заголовок ≤ 65 знаков (проверено скриптом), Sie-Form,
> без буллет-спама эмодзи, юридический блок в конце (§4).
> Если «—» отображается битым — заменить на «·».

---

### ВАРИАНТ A — Website-Wartung (ПРИОРИТЕТ 1)

**Titel** (61 знак):
```
Website-Wartung München — Updates, Backups, DSGVO ab 39 €/Monat
```

**Kategorie:** Dienstleistungen → Weitere Dienstleistungen (c298), Ort: München (Firmensitz)

**Preis:** `39 €` — в поле цены; в тексте разворачивается в три пакета

**Beschreibung:**

Ihre Website läuft. Aber wer kümmert sich darum, wenn sie es nicht mehr tut?

Die meisten Websites werden einmal gebaut und dann sich selbst überlassen. Updates bleiben liegen, Backups gibt es nicht, das Kontaktformular schickt seit Monaten ins Leere — und niemand merkt es, bis ein Kunde anruft.

Ich übernehme den laufenden Betrieb Ihrer Website. Monatlich kündbar, ohne Mindestlaufzeit.

**BASIS — 39 €/Monat**
· Updates für CMS, Plugins und Themes
· Wöchentliches Backup, extern gespeichert
· Monitoring der Erreichbarkeit
· Wiederherstellung nach Ausfall
· Kurzbericht per E-Mail, einmal im Monat

**STANDARD — 59 €/Monat**
· alles aus BASIS
· Updates erst auf einer Testkopie, dann live — kein Blindflug
· Bis zu 2 Stunden Inhaltsänderungen pro Monat (Texte, Bilder, Öffnungszeiten, Team)
· Prüfung von Impressum, Datenschutzerklärung und Einwilligungsverwaltung
· Antwort innerhalb eines Werktages

**PRAXIS & KANZLEI — 79 €/Monat**
· alles aus STANDARD
· Auftragsverarbeitungsvertrag nach Art. 28 DSGVO, unterschrieben
· Jährliche Prüfung der Datenschutz-Dokumente
· Vertraulichkeit auch gegenüber Dritten schriftlich zugesichert

Was ich betreue: WordPress, WooCommerce, statische Seiten, Next.js, Astro, Eleventy. Hosting bei Ihrem bisherigen Anbieter oder bei einem deutschen Hoster — Sie behalten die Zugänge, ich bekomme nur, was ich brauche.

Kein Abo-Zwang. Wenn Sie aufhören wollen, hören Sie zum Monatsende auf, und ich übergebe alle Zugänge und ein vollständiges Backup.

**Wer ich bin**

Eduard Morocho Baias, Softwareentwickler aus München, Einzelunternehmer. Sie sprechen mit mir — nicht mit einem Account Manager, der Ihr Anliegen weiterleitet.

Sechzehn abgeschlossene Projekte seit 2025. Fünf davon können Sie direkt ansehen:
· taxi-moennigmann.de — Taxiunternehmen, Ostfriesland
· elektrocheckstuttgart.de — Elektro-Prüfservice, B2B
· rundumshaus-littawe.de — Hausmeisterservice
· silkekleinart.com — Künstlerin, WordPress
· ais152.com — meine eigene Seite

**So läuft es an**

Schreiben Sie mir kurz, welche Website es ist. Ich schaue sie mir an und sage Ihnen ehrlich, was sie braucht — auch dann, wenn die Antwort „nichts, das läuft sauber“ lautet. Diese erste Einschätzung kostet nichts.

---

### ВАРИАНТ B — Praxis-Website mit DSGVO & AVV (ПРИОРИТЕТ 2)

**Titel** (62 знака):
```
Website für Praxis — DSGVO, AVV, Festpreis ab 690 €, München
```

**Kategorie:** Dienstleistungen → Weitere Dienstleistungen (c298), Ort: München

**Preis:** `390 €`

**Beschreibung:**

Eine Praxis-Website hat zwei Aufgaben, die nichts miteinander zu tun haben: Patienten sollen Sie finden — und der Datenschutz muss stimmen. Die meisten Anbieter lösen die erste Aufgabe und lassen Sie mit der zweiten allein.

Ich mache beides und gebe Ihnen die Unterlagen dazu schriftlich.

**Was Sie bekommen — Festpreis 690 €**

· Website mit bis zu 6 Seiten (Start, Leistungen, Team, Anfahrt, Kontakt, Rechtliches)
· Für Smartphones optimiert — dort suchen Patienten
· Öffnungszeiten, Anfahrt mit ÖPNV, Kontaktformular, Rückrufwunsch
· Impressum und Datenschutzerklärung, auf Ihre Praxis zugeschnitten
· Kontaktformular ohne Weitergabe an Dritte — kein Google, kein US-Dienstleister
· Selbst gehostete Schriften und Karten statt eingebundener Google-Dienste
· Hosting in Deutschland, auf Wunsch bei Ihrem bisherigen Anbieter
· **Auftragsverarbeitungsvertrag nach Art. 28 DSGVO — unterschrieben, nicht nur erwähnt**
· 30 Tage kostenlose Nachbesserung nach Übergabe — zusätzlich zur gesetzlichen Gewährleistung

Erweiterung auf 10+ Seiten, mehrsprachig oder mit Online-Terminvergabe: 890 € bis 1.200 €. Genauer Preis nach einem Gespräch, vorher schriftlich fixiert.

**Warum der AVV wichtig ist**

Sobald jemand Zugriff auf Ihre Website erhält, über die Patientenanfragen laufen, verarbeitet er personenbezogene Daten in Ihrem Auftrag. Art. 28 DSGVO verlangt dafür einen schriftlichen Vertrag — und in der Verantwortung stehen Sie, nicht der Dienstleister.

Mein AVV-Muster liegt öffentlich einsehbar unter ais152.com/avv.html. Sie können es lesen, bevor Sie mich überhaupt anschreiben. Die Endfassung passe ich auf Ihre Praxis an und unterschreibe sie vor Projektbeginn.

**Zum Preis**

Ich bin Kleinunternehmer nach § 19 UStG und weise keine Umsatzsteuer aus. Für eine Praxis ist das kein Formaldetail: Ärztliche Heilbehandlungen sind nach § 4 Nr. 14 UStG umsatzsteuerfrei, weshalb Sie in der Regel nicht vorsteuerabzugsberechtigt sind. Umsatzsteuer, die Ihnen ein anderer Anbieter berechnet, bekommen Sie also nicht zurück — sie ist für Sie echter Aufwand.

690 € sind bei mir 690 €. Bei einem Anbieter mit Umsatzsteuerausweis kommen auf den genannten Nettopreis noch 19 % obendrauf, die Sie nicht zurückholen können.

Ob Sie tatsächlich nicht vorsteuerabzugsberechtigt sind, klärt Ihre Steuerberatung — ich rechne hier nur vor, was der Unterschied bedeutet.

**Wer ich bin**

Eduard Morocho Baias, Softwareentwickler in München, Einzelunternehmer. Sechzehn abgeschlossene Projekte seit 2025. Direkt ansehen können Sie unter anderem:
· taxi-moennigmann.de — dreisprachig, WCAG 2.1 AA barrierefrei
· elektrocheckstuttgart.de — Prüfservice, B2B
· silkekleinart.com — WordPress, eigenes Theme
· ais152.com — meine eigene Seite mit Impressum, Datenschutz, AVV und Rechnungsmuster

**Nächster Schritt**

Schreiben Sie mir, was für eine Praxis Sie führen und ob es schon eine Website gibt. Sie bekommen von mir innerhalb eines Werktages eine ehrliche Einschätzung und einen Festpreis — kein Beratungstermin, keine Warteschleife.

---

### ВАРИАНТ C — KI-Automatisierung (ПРИОРИТЕТ 4)

**Titel** (61 знак):
```
Büro automatisieren mit KI — n8n, Chatbot, Festpreis ab 390 €
```

**Kategorie:** Dienstleistungen → Weitere Dienstleistungen (c298), Ort: München

**Preis:** `390 €`

**Beschreibung:**

In jedem kleinen Unternehmen gibt es Arbeit, die jeden Tag gleich abläuft: Anfragen aus dem Postfach sortieren und weiterleiten. Rechnungen aus PDFs abtippen. Termine bestätigen. Daten von einem System ins andere übertragen. Berichte zusammenstellen, die niemand gerne macht.

Das lässt sich automatisieren, und zwar ohne dass Sie Ihre bestehende Software austauschen müssen.

**Womit ich arbeite**

n8n (auf Ihrem eigenen Server oder in der Cloud), Anbindung an OpenAI oder Anthropic, eigene Python-Bausteine dort, wo Standardlösungen nicht reichen. Verbindungen zu Outlook, Google Workspace, DATEV-Exporten, Webshops, CRM-Systemen und praktisch allem, was eine Schnittstelle hat.

**Beispiele mit Preisen**

· **E-Mail-Triage — ab 390 €**
  Eingehende Nachrichten werden gelesen, einsortiert, an die richtige Person weitergeleitet, dringende sofort gemeldet.

· **Dokumente auslesen — ab 490 €**
  Rechnungen, Lieferscheine, Formulare werden per KI ausgewertet und landen strukturiert in Ihrer Tabelle oder Datenbank, statt abgetippt zu werden.

· **Chatbot für Ihre Website — ab 590 €**
  Beantwortet Fragen aus Ihren eigenen Unterlagen — nicht aus dem allgemeinen Internetwissen. Erfasst Anfragen auch nachts und am Wochenende. Wenn er etwas nicht weiß, sagt er das, statt sich etwas auszudenken.

· **Berichte und Auswertungen — ab 390 €**
  Zahlen aus mehreren Quellen laufen automatisch zusammen, jeden Montag im Postfach.

· **Größere Abläufe über mehrere Systeme — nach Aufwand, 45 €/Stunde**
  Umfang und Preis werden vorher schriftlich festgelegt. Sie bekommen eine Obergrenze, keine offene Rechnung.

**Was dazukommt**

Laufende Kosten für Server und KI-Schnittstellen liegen je nach Menge typischerweise zwischen 15 und 90 € im Monat. Den konkreten Rahmen rechne ich Ihnen vor der Beauftragung vor. Diese Kosten laufen über Ihre eigenen Zugänge — Sie zahlen direkt beim Anbieter und behalten die Kontrolle. Ich schlage nichts auf.

Betreuung der laufenden Automatisierungen auf Wunsch ab 59 €/Monat.

**Datenschutz**

Wenn personenbezogene Daten durch die Automatisierung laufen, schließen wir vorher einen Auftragsverarbeitungsvertrag nach Art. 28 DSGVO. Mein Muster liegt offen unter ais152.com/avv.html. Auf Wunsch läuft alles auf europäischen Servern oder vollständig bei Ihnen im Haus.

**Wer ich bin**

Eduard Morocho Baias, Softwareentwickler aus München. Sechzehn abgeschlossene Projekte seit 2025, darunter mehrere mit KI-Komponenten — unter anderem baupreis.ais152.com (Kalkulations-SaaS mit KI) und sorrysara.space (Ticketverkauf mit automatisierter Buchungslogik).

**Nächster Schritt**

Beschreiben Sie mir eine Aufgabe, die bei Ihnen jede Woche wiederkehrt. Ich sage Ihnen, ob sich die Automatisierung rechnet — und wenn nicht, sage ich Ihnen das auch. Diese Einschätzung ist kostenlos und unverbindlich.

---

### ВАРИАНТ D — Landingpage / Website (ПРИОРИТЕТ 5)

**Titel** (62 знака):
```
Website in 5 Tagen — Festpreis ab 390 €, Entwickler aus München
```

**Kategorie:** Dienstleistungen → Weitere Dienstleistungen (c298), Ort: München

**Preis:** `390 €`

**Beschreibung:**

Eine Seite, die eine Sache tut: aus Besuchern Anfragen machen. In der Regel fertig in fünf Werktagen ab Auftragsbestätigung, zum Festpreis, der vorher schriftlich feststeht.

**Die Pakete**

· **EINSEITER — 390 €**
  Eine Seite, die trägt: Angebot, Belege, Antworten auf die üblichen Einwände, Kontaktformular. Für Produkteinführungen, Kampagnen und Selbstständige, die schnell sichtbar sein müssen.

· **WEBSITE — 590 €**
  Bis zu 6 Seiten, Kontaktformular, Grundlagen für Google-Auffindbarkeit, Impressum und Datenschutzerklärung.

· **WEBSITE+ — 990 €**
  Bis zu 12 Seiten, zweisprachig, Blog oder News-Bereich, erweiterte Auffindbarkeit, Anbindung an Ihre bestehenden Systeme.

In jedem Paket enthalten: für Smartphones optimiert, schnelle Ladezeiten, Einrichtung Ihrer Domain, SSL, deutsches Hosting, 30 Tage kostenlose Nachbesserung nach Übergabe — zusätzlich zur gesetzlichen Gewährleistung.

**Warum fünf Tage realistisch sind**

Weil ich keine Abstimmungsschleifen durch drei Abteilungen habe. Tag 1: Sie schreiben mir, was die Seite leisten soll, ich schicke Preis und Ablauf. Tag 2: Sie sehen einen klickbaren Entwurf auf einer nicht öffentlichen Adresse. Tag 3 und 4: Ihre Änderungen. Tag 5: live.

Das gilt für Einseiter und Websites. Größere Anwendungen mit Datenbank, Login oder Zahlungsabwicklung dauern länger — dann sage ich Ihnen vorher, wie lange.

**Kein Baukasten**

Ihre Seite wird geschrieben, nicht zusammengeklickt. Sie bekommen den vollständigen Quellcode und alle Zugänge. Keine Bindung an einen Anbieter, keine monatliche Gebühr für die Seite selbst — Sie zahlen nur Domain und Hosting, direkt bei Ihrem Anbieter.

**Zum Ansehen**

· rundumshaus-littawe.de — Hausmeisterservice
· elektrocheckstuttgart.de — Prüfservice, B2B
· taxi-moennigmann.de — Taxiunternehmen, dreisprachig, barrierefrei
· glamour.ais152.com — Beauty-Studio
· ais152.com — meine eigene Seite

Insgesamt sechzehn abgeschlossene Projekte seit 2025.

**Nächster Schritt**

Schreiben Sie mir in zwei Sätzen, was die Seite erreichen soll. Sie bekommen innerhalb eines Werktages einen Festpreis und einen Termin — oder eine ehrliche Absage, wenn ich nicht der Richtige bin.

---

### ВАРИАНТ E — Website-Umzug & Rettung (МОЁ ПРЕДЛОЖЕНИЕ, ПРИОРИТЕТ 3)

> Это и есть «Вариант Г» (ПРИОРИТЕТ 3). Обоснование: `website umzug` → 0 конкурентов
> в München, вход дешёвый (149 €), а клиент после переезда естественным образом
> переходит в Wartung. Это лучший канал набора для варианта A.

**Titel** (62 знака):
```
Website umziehen ohne Ausfall — Hosterwechsel München ab 149 €
```

**Kategorie:** Dienstleistungen → Weitere Dienstleistungen (c298), Ort: München

**Preis:** `149 €`

**Beschreibung:**

Ihr Hoster wird teurer, langsamer oder antwortet nicht mehr. Der Dienstleister, der die Seite gebaut hat, ist nicht mehr erreichbar. Oder Sie wissen schlicht nicht mehr, wo Ihre Website eigentlich liegt und wem die Domain gehört.

Das lässt sich klären, und die Seite lässt sich umziehen — ohne dass sie dabei offline geht.

**Umzug — ab 149 €**

· Bestandsaufnahme: wo liegt die Seite, wem gehört die Domain, was hängt daran
· Vollständige Sicherung vor dem ersten Handgriff
· Aufbau beim neuen Anbieter, Test auf einer Vorschau-Adresse
· Umschaltung außerhalb Ihrer Geschäftszeiten
· E-Mail-Postfächer wandern mit, ohne Verlust
· SSL-Zertifikat, Weiterleitungen, Prüfung nach dem Umzug
· Umschaltung außerhalb Ihrer Öffnungszeiten — Ausfallzeit üblicherweise unter 15 Minuten

Umfangreiche Seiten, Onlineshops oder viele Postfächer: 290 bis 490 €. Preis steht vor Beginn fest.

**Rettung — ab 90 €**

Wenn es schon brennt: Zugang verloren, Seite offline, Hoster gekündigt, Domain droht auszulaufen, Ex-Dienstleister rückt nichts heraus. Ich schaue mir das an und sage Ihnen, was noch geht.

**Notfall-Prüfung: kostenlos.** Sie erfahren vorher, ob Ihr Fall lösbar ist — und wenn ich ihn nicht lösen kann, sage ich das, bevor Sie zahlen.

**Alt-Website übernehmen — ab 190 €**

Ihr bisheriger Dienstleister ist weg, die Seite läuft aber noch. Ich übernehme sie: Zugänge sichern, Updates nachziehen, Sicherheitslücken schließen, Impressum und Datenschutzerklärung auf Stand bringen. Danach wissen Sie wieder, wem was gehört.

Anschließende Betreuung auf Wunsch ab 39 €/Monat — nötig ist sie nicht.

**Womit ich umgehen kann**

WordPress, WooCommerce, TYPO3, Joomla, statische Seiten, Next.js, Astro. Hoster: All-Inkl, Strato, IONOS, Hetzner, Netcup, Cloudflare, Vercel und die meisten anderen.

**Wer ich bin**

Eduard Morocho Baias, Einzelunternehmer aus München, Softwareentwickler. Sechzehn abgeschlossene Projekte seit 2025, unter anderem taxi-moennigmann.de, elektrocheckstuttgart.de und rundumshaus-littawe.de.

Wenn ich Zugriff auf personenbezogene Daten bekomme — bei einem Umzug ist das die Regel — schließen wir vorher einen Auftragsverarbeitungsvertrag nach Art. 28 DSGVO. Mein Muster liegt offen unter ais152.com/avv.html.

**Nächster Schritt**

Schreiben Sie mir die Adresse Ihrer Website. Ich sehe mir von außen an, wo sie liegt und in welchem Zustand sie ist, und melde mich innerhalb eines Werktages mit einer Einschätzung und einem Festpreis. Die Einschätzung kostet nichts.

---

### 3.6 Рекомендации по картинкам

Kleinanzeigen позволяет до 20 изображений. Первое — решает, кликнут или нет; оно показывается в выдаче маленьким.

**Общий принцип:** не стоковые фото людей в костюмах и не абстрактные «digital»-градиенты. У конкурентов именно они, и они не читаются в мелком размере.

| Позиция | Что показать | Зачем |
|---|---|---|
| **1 (обложка)** | Тёмная плашка 1200×900, крупно цена и одно обещание: «Website-Wartung · ab 79 €/Monat · München». Шрифт крупный, читаемый в 200 px | В выдаче видно только это. Цена в картинке отрабатывает даже когда заголовок обрезан |
| 2 | Скриншот-коллаж из 3–4 реальных проектов с подписанными доменами | Единственное настоящее доказательство. У большинства конкурентов его нет |
| 3 | Скриншот страницы ais152.com/avv.html | Показывает, что AVV существует, а не обещан. Для варианта B — обязательно |
| 4 | Таблица пакетов и цен как изображение | Читается быстрее текста; кто скроллит картинки, не читая описание, всё равно увидит цену |
| 5 | Скриншот Impressum на ais152.com | Сигнал легитимности: настоящее Gewerbe, настоящий адрес |
| 6 | Портрет — нейтральный, при хорошем свете, без костюма | Локальный клиент покупает у человека. Конкуренты прячутся за логотипами |

Для варианта C вместо скриншотов сайтов — схема потока данных (Postfach → Sortierung → Weiterleitung), нарисованная просто, без технического жаргона.

**Что не делать:** не ставить логотипы чужих брендов (BOSS, MANGO из портфолио Henner Heede) — это чужие товарные знаки, и на Kleinanzeigen это лишний риск. В описании проекта словами — можно, логотипом — нет.

---

## 4. Юридическое оформление

> **Дисклеймер:** я не адвокат. Ниже — результат исследования первоисточников (законы,
> справка Kleinanzeigen, публикации IT-Recht Kanzlei и Händlerbund). Muster-тексты
> взяты из Anlage 1 и 2 EGBGB. Перед первой публикацией стоит один раз проверить
> пакет у Händlerbund или профильной канцелярии — это дешевле одного Abmahnung.

### 4.1 Архитектура: настроить один раз, не повторять в каждом объявлении

Kleinanzeigen даёт в Anzeigen-Manager поле **«Rechtliche Angaben»**. IT-Recht Kanzlei: «Die unter 'rechtliche Angaben' eingefügten Rechtstexte werden automatisch in alle aktiven und künftigen Inserate übernommen».

Туда идут полные тексты: Impressum, Widerrufsbelehrung, Muster-Widerrufsformular, Datenschutzhinweis, AGB.

**Но этого недостаточно.** Händlerbund предупреждает: тексты видны только после клика по кнопке, что может быть расценено как «versteckt». Поэтому **в теле каждого объявления** ставится короткий блок-указатель.

### 4.2 Блок в конец каждого объявления (копировать дословно)

```
────────────────────────
ANBIETER

Eduard Morocho Baias
Einzelunternehmer — AIS.152
Oefelestraße 19, 81543 München
Telefon: +49 155 636 75 772
E-Mail: ais152.business@gmail.com
Gewerbeanmeldung: KVR München

Kein Ausweis von Umsatzsteuer gemäß § 19 UStG (Kleinunternehmerregelung).

Impressum, Widerrufsbelehrung, Muster-Widerrufsformular und
Datenschutzhinweise finden Sie vollständig unter der Schaltfläche
„Rechtliche Angaben". Impressum zusätzlich unter ais152.com/impressum.html

Verbraucher haben bei Fernabsatzverträgen ein Widerrufsrecht von
14 Tagen. Auf ausdrücklichen Wunsch beginne ich vor Ablauf dieser
Frist mit der Arbeit — in diesem Fall gelten §§ 356 Abs. 5, 357a
Abs. 2 BGB. Einzelheiten in der Widerrufsbelehrung.

Ich bin nicht bereit und nicht verpflichtet, an Streitbeilegungs-
verfahren vor einer Verbraucherschlichtungsstelle teilzunehmen (§ 36 VSBG).
────────────────────────
```

**Три замечания к этому блоку:**

1. **USt-IdNr. не указывается** — она у тебя её нет, а по §5 DDG она обязательна только «sofern vorhanden». Писать «keine USt-IdNr.» не нужно.
2. **Steuernummer в объявление не выносится** — она в Impressum появится после присвоения Finanzamt. По §5 DDG в Impressum обязательна USt-IdNr., а не Steuernummer.
3. **Ссылка на OS-Plattform отсутствует намеренно** — см. §4.5.

### 4.3 Widerrufsbelehrung — в «Rechtliche Angaben»

Widerrufsrecht для Dienstleistungen из Fernabsatz **обязательно** (§312g Abs. 1 BGB). Исключения §312g Abs. 2 к веб-разработке не применяются: Nr. 9 — только о Beherbergung/Beförderung/Mietwagen/Speisen/Freizeit, Nr. 1 (индивидуальное изготовление) — только о **Waren**, не об услугах.

Оговорка «Verkauf nur an Gewerbetreibende» без реальной проверки статуса сама по себе Abmahn-риск. Держим Widerrufsbelehrung всегда.

**Важно:** Gesetzlichkeitsfiktion работает только при **дословном, неизменённом** использовании Muster из Anlage 1 EGBGB (Art. 246a §1 Abs. 2 S. 2 EGBGB). Любая «улучшенная» самодельная редакция — потеря защиты.

```
WIDERRUFSBELEHRUNG

Widerrufsrecht

Sie haben das Recht, binnen vierzehn Tagen ohne Angabe von Gründen
diesen Vertrag zu widerrufen.

Die Widerrufsfrist beträgt vierzehn Tage ab dem Tag des Vertragsabschlusses.

Um Ihr Widerrufsrecht auszuüben, müssen Sie uns (Eduard Morocho Baias,
Oefelestraße 19, 81543 München, Telefon: +49 155 636 75 772,
E-Mail: ais152.business@gmail.com) mittels einer eindeutigen Erklärung
(z. B. ein mit der Post versandter Brief oder E-Mail) über Ihren Entschluss,
diesen Vertrag zu widerrufen, informieren. Sie können dafür das beigefügte
Muster-Widerrufsformular verwenden, das jedoch nicht vorgeschrieben ist.

Zur Wahrung der Widerrufsfrist reicht es aus, dass Sie die Mitteilung über
die Ausübung des Widerrufsrechts vor Ablauf der Widerrufsfrist absenden.

Folgen des Widerrufs

Wenn Sie diesen Vertrag widerrufen, haben wir Ihnen alle Zahlungen, die wir
von Ihnen erhalten haben, einschließlich der Lieferkosten (mit Ausnahme der
zusätzlichen Kosten, die sich daraus ergeben, dass Sie eine andere Art der
Lieferung als die von uns angebotene, günstigste Standardlieferung gewählt
haben), unverzüglich und spätestens binnen vierzehn Tagen ab dem Tag
zurückzuzahlen, an dem die Mitteilung über Ihren Widerruf dieses Vertrags
bei uns eingegangen ist. Für diese Rückzahlung verwenden wir dasselbe
Zahlungsmittel, das Sie bei der ursprünglichen Transaktion eingesetzt haben,
es sei denn, mit Ihnen wurde ausdrücklich etwas anderes vereinbart; in keinem
Fall werden Ihnen wegen dieser Rückzahlung Entgelte berechnet.

Haben Sie verlangt, dass die Dienstleistungen während der Widerrufsfrist
beginnen sollen, so haben Sie uns einen angemessenen Betrag zu zahlen, der
dem Anteil der bis zu dem Zeitpunkt, zu dem Sie uns von der Ausübung des
Widerrufsrechts hinsichtlich dieses Vertrags unterrichten, bereits erbrachten
Dienstleistungen im Vergleich zum Gesamtumfang der im Vertrag vorgesehenen
Dienstleistungen entspricht.

─────────────────────

MUSTER-WIDERRUFSFORMULAR

(Wenn Sie den Vertrag widerrufen wollen, dann füllen Sie bitte dieses
Formular aus und senden Sie es zurück.)

An: Eduard Morocho Baias, Oefelestraße 19, 81543 München,
E-Mail: ais152.business@gmail.com

Hiermit widerrufe(n) ich/wir (*) den von mir/uns (*) abgeschlossenen
Vertrag über den Kauf der folgenden Waren (*) / die Erbringung der
folgenden Dienstleistung (*)

_____________________________________________

Bestellt am (*) / erhalten am (*): _______________

Name des/der Verbraucher(s): _______________

Anschrift des/der Verbraucher(s): _______________

Unterschrift des/der Verbraucher(s) (nur bei Mitteilung auf Papier):

_______________

Datum: _______________

(*) Unzutreffendes streichen.
```

### 4.4 Wertersatz — механика, которую надо соблюдать на практике

Если клиент хочет начать раньше, чем истекут 14 дней (а он всегда хочет), нужны **три условия одновременно** (§357a Abs. 2 BGB), иначе за уже сделанную работу не получишь ничего:

1. Клиент **явно потребовал** начать до истечения срока — «ausdrücklich verlangt hat»
2. При договоре вне помещений — это требование на «dauerhafter Datenträger»
3. Клиент был надлежаще информирован по Art. 246a §1 Abs. 2 S. 1 Nr. 1 и 3 EGBGB

**Практика:** перед началом работы клиент присылает письменно (e-mail достаточно) фразу:

> «Ich verlange ausdrücklich, dass Sie mit der Erbringung der Dienstleistung vor Ablauf der Widerrufsfrist beginnen. Mir ist bekannt, dass mein Widerrufsrecht mit vollständiger Vertragserfüllung erlischt.»

Эти две фразы закрывают и §356 Abs. 5 (Erlöschen), и §357a Abs. 2 (Wertersatz). Расчёт при отзыве — pro rata temporis от согласованной общей цены (BGH, Urteil v. 26.11.2020, I ZR 169/19).

Включить в шаблон подтверждения заказа — см. §7.

### 4.5 Preisangabe и §19 UStG

**PAngV не обязывает называть цену вообще.** §3 PAngV включается, когда есть Angebot (Aufforderung zum Kauf) или реклама **с указанием цен**. Судебная практика по «Preis auf Anfrage» расходится: LG München I признал нарушением, OLG München в апелляции — не признал для konfigurationsbedürftige услуг.

**Но нам это безразлично, потому что цену мы называем осознанно** — три из семи локальных конкурентов её не называют, и это их слабость, а не наша. Якорная цена в заголовке снимает и вопрос PAngV, и вопрос конверсии.

**Kleinunternehmer — запрет, который легко нарушить по привычке:**
писать «inkl. MwSt.» или «zzgl. MwSt.» **нельзя**. НДС не начисляется, надпись вводит в заблуждение (§5 UWG; аргументация со ссылкой на OLG Hamm, Urteil v. 19.11.2013, Az. 4 U 65/13 — цитируется по IT-Recht Kanzlei, сам текст решения не читан).

Правильно: `Kein Ausweis von Umsatzsteuer gemäß § 19 UStG (Kleinunternehmerregelung).`

В **Rechnung** это уже жёсткая обязанность — §34a UStDV с 01.01.2025 требует «Hinweis auf die Steuerbefreiung». BMF-Schreiben от 18.03.2025 допускает и разговорную форму.

### 4.6 OS-Plattform — СРОЧНО убрать с живого сайта

Платформа ЕС по онлайн-урегулированию споров **выключена 20.07.2025**, ODR-VO отменена Verordnung (EU) 2024/3228. Ссылка на несуществующую платформу — вводящее в заблуждение действие по §§3, 5 UWG, потому что создаёт у потребителя впечатление работающей процедуры. Канцелярии предупреждают о волне Abmahnungen именно по этому поводу с лета 2025.

**На ais152.com/impressum.html этот блок сейчас есть** — строки 94–99, раздел «Streitschlichtung» со ссылкой на `ec.europa.eu/consumers/odr/`.

Убрать **ссылку и первый абзац**, оставив только второй:

```html
<h2>Verbraucherstreitbeilegung</h2>
<p>
  Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer
  Verbraucherschlichtungsstelle teilzunehmen (§ 36 VSBG).
</p>
```

Обязанность по §36 VSBG сохраняется — её оставляем.

### 4.7 Правила площадки, за нарушение которых блокируют

| Правило | Формулировка | Что это значит для нас |
|---|---|---|
| **Дубликаты запрещены** | объявление размещается один раз; дубликатами считаются и объявления, которые «trotz Abweichungen dasselbe Angebot enthalten», и удалённые-переразмещённые | 5 наших вариантов должны быть **действительно разными услугами**, а не одним оффером в пяти обёртках. Они разные — но текст переписывать при ротации нельзя формально, а по сути надо |
| **Место = Firmensitz** | «Dabei richtest du dich nach dem Ort, an dem sich dein Firmensitz befindet» | Только München. Размещать тот же оффер в Berlin/Hamburg — двойное нарушение. «Bundesweit» пишется **в тексте**, а не размещением в других городах |
| **Один аккаунт** | мультиаккаунты — прямая причина блокировки | Один gewerblich-аккаунт `ais152.business@gmail.com`. Не смешивать с личным |

---

## 5. Pricing-Strategie

### 5.1 Что писать в поле цены — решение

**Festpreis-якорь, не «VB» и не «auf Anfrage».**

Обоснование по фактам: из 7 локальных München-конкурентов трое (включая GmbH) не указывают цену вообще — только «VB». Клиент не может сравнить и не пишет. Те, кто указывает Festpreis (Kecke 1.999 €, STBR 499 €), выглядят увереннее и получают просмотры — у Kecke 118 просмотров за 11 дней.

Формат: в поле цены — нижняя граница пакета числом. В тексте — три пакета с точными ценами. Слово «ab» — в заголовке, не в поле цены (поле принимает число).

«Nach Aufwand» оставляем только для одной позиции — крупных автоматизаций в варианте C, где объём действительно неизвестен. И там сразу даём почасовую ставку и обещание потолка: «Sie bekommen eine Obergrenze, keine offene Rechnung».

### 5.2 Итоговая сетка и её обоснование рынком

| Услуга | Рынок (источники §9) | Kleinanzeigen München | Наша цена | Позиция |
|---|---|---|---|---|
| Wartung Basis | 50–100 €/мес | 39 € и 49 € (2 объявления) | **39 €/мес** | по дну площадки — это вход, не заработок |
| Wartung Standard | 100–250 €/мес | нет | **59 €/мес** | ниже рынка |
| Wartung Praxis | 50–150 €/мес (Praxis) | нет | **79 €/мес** | ниже рынка, оправдана AVV |
| Praxis-Website | 1.500–3.000 € фрилансер | нет объявлений | **690 €** | твой уровень + надбавка за AVV |
| Praxis-Website erweitert | 3.000–6.000 € индивид. | нет | **890–1.200 €** | сильно ниже рынка |
| Einseiter | 500–1.800 € фрилансер | 499–1.999 € | **390 €** | твой текущий чек |
| Website 6 стр. | 1.200–3.500 € фрилансер | 599–1.999 € | **590 €** | твой текущий чек |
| Website 12 стр. 2 языка | 1.500–5.000 € | 1.699 € (SCALE) | **990 €** | верх твоей вилки |
| Umzug | 100 € — несколько тысяч | **нет конкурентов** | **149–490 €** | ниша, цена свободна |
| n8n Workflow простой | 500–800 € | нет | **390–490 €** | ниже рынка |
| Chatbot | от 3.000 € у консультантов | нет | **590 €** | резко ниже рынка |
| Stundensatz | медиана 90 €/ч (DE, IT-фриланс) | не указывает никто | **45 €/ч** | твой уровень |

**Оговорка честно:** эта сетка построена не по рыночным benchmark, а по твоему реальному чеку 300–600 € (Stephan — 400 €, план 4–5 клиентов × 400–500 €). Рынок платит в 2–4 раза больше, и портфолио из 16 live-проектов объективно стоит дороже. Но цена, в которую сам не веришь, разваливается на первом же торге, поэтому стартуем отсюда. Как поднимать — в §5.3.

### 5.3 Premium или Volume — ответ

**Ни то, ни другое в чистом виде. Правильная модель — низкий вход и рекуррентная база.**

Против premium прямо сейчас: премиальная цена требует доказательств, которых на Kleinanzeigen пока нет — отзывов на аккаунте ноль, аккаунт создан 12.08.2026, бейджей «TOP Zufriedenheit» нет. Kecke держит 1.999 € имея аккаунт с ноября 2025. Портфолио у нас сильнее, но на Kleinanzeigen сначала смотрят на профиль, потом на портфолио.

Против volume-дискаунта: 25-евровый студент показывает, чем это кончается — его объявление висит два месяца без результата. Цена ниже рынка на такой площадке читается как сигнал качества, а не как выгода.

**Модель:** дешёвый и честный вход (бесплатная оценка → Umzug 149 € → Wartung 39 €/мес), и уже внутри отношений — разработка по твоей вилке.

**Почему Wartung важнее чека за сайт.** Твой текущий потолок посчитан скриптом:

| клиентов/мес | × 400 € | × 450 € | × 500 € | × 600 € |
|---|---|---|---|---|
| 3 | 1.200 | 1.350 | 1.500 | 1.800 |
| 4 | 1.600 | 1.800 | 2.000 | 2.400 |
| 5 | 2.000 | 2.250 | 2.500 | 3.000 |
| 6 | 2.400 | 2.700 | 3.000 | 3.600 |

Это работает, пока крутишь педали. Перестал искать клиентов — доход ноль в тот же месяц.

Wartung накапливается:

| клиентов | × 39 € | × 49 € | × 79 € |
|---|---|---|---|
| 5 | 195 | 245 | 395 |
| 10 | 390 | 490 | 790 |
| 15 | 585 | 735 | 1.185 |
| 20 | 780 | 980 | 1.580 |

Если из четырёх клиентов в месяц один остаётся на обслуживании за 49 €, через год это 12 клиентов = **588 €/мес**, приходящих без единой новой продажи. Плюсом к году: **3.822 €**.

**Как поднимать цену.** Не сейчас. Через 5 оценок на аккаунте Kleinanzeigen — +20% по всей сетке без изменения текстов (390 → 490, 690 → 830). Ещё через 5 — ещё раз. Оценки на площадке весят больше портфолио: у Kecke аккаунт с ноября 2025 и он держит 1.999 €, у тебя аккаунт с 12.08.2026 и оценок ноль. Это единственное, чем он реально сильнее.

### 5.4 Что не делать с ценой

Не имитировать приёмы конкурентов, которые не подкреплены: «5,0 ⭐⭐⭐⭐⭐ (124) Google Rezensionen» текстом без ссылки на профиль — это то, что нельзя проверить, и то, чего у нас нет. Копирование такого приёма — прямой репутационный риск при первом же вопросе клиента.

Не писать «Wert 297 € — kostenlos» в стиле Kecke. Приём работает, но обесценивает KI-продукт, который мы собираемся продавать за 590 €.

---

## 6. Publish-Plan

### 6.1 Лимиты — главное ограничение плана

Категория Dienstleistungen у gewerbliche Nutzer: **2 бесплатных объявления в 30 дней** (данные с 03.03.2025), при этом с 11.05.2026 лимиты пересмотрены и часть источников говорит про «bis zu drei Anzeigen in 30 Tagen kostenfrei». **Источники противоречат друг другу, официальная страница тарифов не отдаётся** (см. §9).

Каждое следующее — 3,99–4,99 €. Verlängerung стоит столько же, сколько первичное размещение. Окно скользящее, 30 дней, и в него засчитываются **уже удалённые** объявления.

**Что делать:** при размещении первого объявления Kleinanzeigen показывает стоимость на шаге публикации. Там и увидишь реальный лимит. Планируй на 2, обрадуешься если 3.

Даже худший вариант не страшен: 3 дополнительных объявления = ~15 €/мес. При среднем чеке 450 € это не расход, а округление.

### 6.2 План запуска

**Неделя 1 — фундамент (до первой публикации):**
1. Убрать OS-ссылку из impressum.html, задеплоить
2. Заполнить «Rechtliche Angaben» в Anzeigen-Manager полными текстами из §4.3
3. Заполнить профиль gewerblich: название AIS.152, München, ссылка на ais152.com
4. Подготовить обложки для A и B

**Неделя 1, публикация — 2 объявления бесплатно:**
- **A (Wartung)** — категория c226
- **B (Praxis-Website)** — категория c298

Почему именно эти два: A — пустая ниша с рекуррентной выручкой, B — пустая ниша с готовым кейсом (Greta) и уникальным активом (AVV). Они не конкурируют между собой и бьют по разным аудиториям.

**Неделя 2 — докупить третье:**
- **E (Umzug)** за ~4 € — это канал набора в A

**Неделя 4 — по результатам:**
- Если A и B дают отклики → добавить C (KI)
- Если тишина → см. §6.5

**D (Landingpage) — не раньше второго месяца.** Это самая конкурентная ниша, туда идём, когда на аккаунте появятся первые оценки.

### 6.3 Время публикации

**Оговорка честно: точных данных по оптимальному времени именно для Kleinanzeigen в категории Dienstleistungen я не нашёл, и выдумывать их не буду.** Ниже — рассуждение от свойств аудитории, а не измеренный факт.

Целевая аудитория A и B — владельцы практик и мелких фирм. Сайтом они занимаются не в рабочее время, когда идёт приём, а вечером или в начале недели, когда разбирают накопившееся.

Разумная гипотеза: **вторник–четверг, 18:00–21:00.** Понедельник — разбор завала после выходных, пятница после обеда — уже никто ничего не начинает.

Это гипотеза, а не знание. Проверяется просто: у Kleinanzeigen видно число просмотров объявления. Публикуем A во вторник вечером, E — через неделю в воскресенье днём, и через две недели сравниваем просмотры на объявление в сутки. Это и будет твой собственный измеренный ответ вместо чужого совета.

### 6.4 Refresh-цикл

Объявления опускаются в выдаче по мере появления новых. Наблюдение из research: объявления конкурентов в этой категории живут месяцами (25-евровый студент висит с 18.06), то есть поток новых объявлений слабый — 15 штук на всю München. Значит выпадение из топа медленное, и агрессивный refresh не нужен.

Verlängerung стоит как новое размещение — то есть 3,99–4,99 €. Делать это раз в неделю бессмысленно.

**Ритм:** проверять позицию раз в 7–10 дней. Обновлять, только когда объявление физически ушло со второй страницы выдачи по своему ключевому запросу.

**Важно:** удалять и переразмещать вместо продления — прямое нарушение правила о дубликатах, и удалённое всё равно засчитывается в лимит 30 дней. Не делать.

### 6.5 Что делать при успехе и при провале

**Успех — приходят отклики, есть первые заказы:**
- Просить оценку на профиле Kleinanzeigen у каждого довольного клиента. Оценки на площадке весят больше, чем портфолио — именно их не хватает нам против Kecke
- После 5 оценок поднять цены на 15–20%
- Расширять не количество объявлений, а глубину: тот же A, но с двумя-тремя реальными кейсами обслуживания внутри текста

**Провал — 3 недели, откликов нет:**

Диагностировать по числу просмотров, а не по ощущению. Kleinanzeigen показывает просмотры на каждом объявлении.

| Симптом | Диагноз | Что менять |
|---|---|---|
| Просмотров мало (< 30 за 2 недели) | Не находят | Заголовок — ключевые слова не совпадают с тем, что ищут. Проверить, по каким запросам объявление вообще всплывает |
| Просмотров много, откликов ноль | Находят, но не убеждает | Цена или первые 3 строки описания. Первым делом — обложка и цена |
| Отклики есть, заказов нет | Проблема на follow-up | См. §7 — скорее всего слишком длинный или слишком дорогой первый ответ |

Менять **по одному элементу за раз**, иначе непонятно, что сработало. Сначала обложку, через неделю — заголовок, потом цену. Цену — в последнюю очередь, потому что снизить легко, а вернуть обратно нельзя.

---

## 7. Follow-Up-System

### 7.1 Принцип

Kleinanzeigen — площадка, где отвечают быстро или не получают заказ. На сайте ais152.com обещано «Antwort innerhalb 1 Stunde» — это обещание надо держать и здесь, оно само по себе конкурентное преимущество: у конкурентов-агентств между запросом и ответом сидит менеджер.

Первый ответ **не должен содержать цену**, если запрос был неконкретным. Цена без понимания задачи либо отпугнёт, либо загонит в невыгодные рамки.

### 7.2 Шаблон первого ответа — общий

```
Guten Tag,

danke für Ihre Nachricht.

Damit ich Ihnen einen verbindlichen Festpreis nennen kann und keine
Hausnummer, brauche ich drei Angaben:

1. Um welche Website geht es? (Adresse genügt — falls es noch keine
   gibt, sagen Sie mir kurz, was Sie anbieten)
2. Was soll sich ändern? Ein Satz reicht.
3. Bis wann brauchen Sie das?

Danach bekommen Sie von mir innerhalb eines Werktages einen Festpreis
und einen Terminvorschlag — schriftlich, ohne Beratungstermin.

Meine bisherigen Arbeiten können Sie sich jederzeit ansehen:
ais152.com

Viele Grüße
Eduard Morocho Baias
AIS.152 — Softwareentwicklung
München · +49 155 636 75 772
```

### 7.3 Шаблон первого ответа — Praxis (вариант B)

```
Guten Tag,

danke für Ihre Anfrage.

Vier Fragen, dann kann ich Ihnen einen Festpreis nennen:

1. Was für eine Praxis führen Sie, und wie viele Behandelnde sind Sie?
2. Gibt es schon eine Website? Wenn ja: welche Adresse?
3. Sollen Patienten online Termine buchen können, oder reicht
   Telefon und Kontaktformular?
4. Wer betreut die Seite bisher — und kommen Sie an die Zugänge?

Zum Datenschutz: sobald ich Zugriff auf eine Seite bekomme, über die
Patientenanfragen laufen, verarbeite ich personenbezogene Daten in Ihrem
Auftrag. Dafür schließen wir vor Projektbeginn einen Auftragsverarbeitungs-
vertrag nach Art. 28 DSGVO. Mein Muster können Sie vorab lesen:
ais152.com/avv.html

Sie bekommen von mir innerhalb eines Werktages einen Festpreis, schriftlich.

Viele Grüße
Eduard Morocho Baias
AIS.152 — Softwareentwicklung
München · +49 155 636 75 772
```

### 7.4 Квалификация — что выяснить до предложения

Пять вопросов, которые решают, стоит ли браться:

| Вопрос | Что проверяем | Красный флаг |
|---|---|---|
| Кто решает? | Дойдёт ли до сделки | «Ich muss noch mit meinem Partner sprechen» на третьем письме |
| Есть ли доступы к домену и хостингу? | Выполнимость | «Das hatte damals mein Neffe gemacht» — заложить время на розыск |
| Какой бюджет представляли? | Совпадение ожиданий | «Ich dachte so an 150 Euro» — вежливо отказать сразу |
| Срок | Реалистичность | «Bis übermorgen» — либо наценка, либо нет |
| Что не устраивает сейчас? | Настоящая задача | «Alles» — задача не сформулирована, нужен звонок |

**Правило:** если бюджет расходится с ценой больше чем вдвое — отказывать сразу и вежливо, не торгуясь. Это экономит недели.

```
Guten Tag,

danke für die Offenheit. In diesem Rahmen kann ich die Arbeit nicht
seriös anbieten — dafür müsste ich an der Substanz sparen, und das
würde Ihnen nichts bringen.

Was in Ihrem Budget realistisch ist: [Wartung 39 €/Monat / Umzug 149 € /
eine einzelne Seite statt einer vollständigen Website].

Falls sich der Rahmen später ändert, melden Sie sich gerne.

Viele Grüße
Eduard Morocho Baias
```

### 7.5 Конверсия в заказ — письмо с предложением

```
Guten Tag [Name],

wie besprochen, hier mein Angebot.

LEISTUNG
[конкретно, 3–5 строк — что именно будет сделано]

NICHT ENTHALTEN
[что не входит — честно, это снимает 90% споров потом]

PREIS
[Summe] € — Festpreis
Kein Ausweis von Umsatzsteuer gemäß § 19 UStG (Kleinunternehmerregelung).

ZAHLUNG
50 % bei Auftragsbestätigung, 50 % nach Abnahme.

TERMIN
Start: [Datum] · Übergabe: [Datum]

DANACH
30 Tage kostenlose Nachbesserung, zusätzlich zur gesetzlichen Gewährleistung. Laufende Betreuung optional ab 39 €/Monat,
monatlich kündbar — kein Muss.

────────────────────────
Zum Ablauf: Als Verbraucher haben Sie ein Widerrufsrecht von 14 Tagen
ab Vertragsschluss. Wenn Sie möchten, dass ich sofort anfange und nicht
erst in zwei Wochen, brauche ich dafür Ihre ausdrückliche Bestätigung.
Antworten Sie in diesem Fall bitte mit diesem Satz:

„Ich verlange ausdrücklich, dass Sie mit der Erbringung der Dienstleistung
vor Ablauf der Widerrufsfrist beginnen. Mir ist bekannt, dass mein
Widerrufsrecht mit vollständiger Vertragserfüllung erlischt."

Die vollständige Widerrufsbelehrung mit Muster-Widerrufsformular
schicke ich Ihnen mit der Auftragsbestätigung zu; sie steht außerdem
in meinem Kleinanzeigen-Profil unter „Rechtliche Angaben".
────────────────────────

Wenn das so passt, antworten Sie einfach mit „Einverstanden" — dann
schicke ich die Auftragsbestätigung und lege los.

Viele Grüße
Eduard Morocho Baias
AIS.152 — Softwareentwicklung
Oefelestraße 19, 81543 München
+49 155 636 75 772 · ais152.com
```

**Почему именно так:** блок с Widerruf выглядит как забота о клиенте, а не как юридическая защита — но выполняет ровно требование §357a Abs. 2 BGB. Без этой фразы при отзыве через 13 дней работы ты не получишь ничего.

### 7.6 Ритм follow-up

| Когда | Что |
|---|---|
| В течение 1 часа | Первый ответ с вопросами |
| В течение 1 рабочего дня после ответов | Предложение с ценой |
| +3 дня тишины | Одно короткое напоминание |
| +7 дней тишины | Закрыть. Больше не писать |

Напоминание — коротко, без давления:

```
Guten Tag [Name],

kurze Nachfrage zu meinem Angebot von [Datum] — ist es noch aktuell?

Falls Sie sich anders entschieden haben, ist das völlig in Ordnung,
sagen Sie einfach kurz Bescheid. Dann halte ich den Termin nicht frei.

Viele Grüße
Eduard
```

Третьего письма нет. Оно не приносит заказов и портит впечатление.

---

## 8. Действия перед первой публикацией

| # | Действие | Почему | Кто |
|---|---|---|---|
| 1 | **Убрать OS-ссылку из impressum.html** и задеплоить | Живой Abmahn-риск, §§3, 5 UWG. Объявление ссылается на Impressum — конкурент проверит первым делом | требует твоего решения (деплой живого сайта) |
| 2 | Заполнить «Rechtliche Angaben» в Anzeigen-Manager текстами из §4.3 | Применяется автоматически ко всем объявлениям, настраивается один раз | ты, вручную в аккаунте |
| 3 | Починить «zehn Projekte» → «sechzehn» в About на ais152.com | На сайте одновременно стоят 16 в Hero и 10 в About. Клиент, который пришёл по объявлению с «sechzehn Projekte», увидит расхождение | правка на 2 строки |
| 4 | Решить, какой e-mail в Impressum | Сейчас в Impressum `ebaias.muc@gmail.com`, а gewerblich-аккаунт на `ais152.business@gmail.com`. Расхождение адресов между объявлением и Impressum выглядит небрежно | твоё решение |
| 5 | Проверить реальный лимит бесплатных объявлений на шаге публикации | Источники противоречат: 2 или 3 | ты, при первой публикации |
| 6 | Опционально: показать пакет юридических текстов Händlerbund или канцелярии | Дешевле одного Abmahnung | твоё решение |

---

## 9. Что НЕ проверено — читать перед использованием

Раздел обязательный. Всё ниже — либо не подтверждено первоисточником, либо подтверждено косвенно.

**9.1 BFSG / Barrierefreiheit — аргумент НЕ использовать в том виде, в каком он напрашивается.**
Ниша `barrierefreiheit website` в München пуста (0 объявлений), и соблазн продавать «обязанность с 28.06.2025» велик. **Но по §3 Abs. 3 BFSG Kleinstunternehmen, оказывающие услуги, из закона исключены** — критерий: менее 10 сотрудников И не более 2 млн € оборота, оба условия одновременно. Типичная маленькая Praxis под исключение попадает, то есть **не обязана**.
Поэтому в тексты вариантов A–E аргумент BFSG **не включён**. Если использовать — только в честной форме: «Praxen ab zehn Beschäftigten sind seit 28.06.2025 verpflichtet — kleinere nicht, gewinnen aber trotzdem Patienten dazu». Пугать несуществующей обязанностью — быстрый способ потерять клиента, который спросит своего Steuerberater.
Источники: [Bundesfachstelle Barrierefreiheit FAQ](https://www.bundesfachstelle-barrierefreiheit.de/DE/Fachwissen/Produkte-und-Dienstleistungen/Barrierefreiheitsstaerkungsgesetz/FAQ/faq_node.html), [Händlerbund BFSG](https://www.haendlerbund.de/de/ratgeber/recht/barrierefreiheitsstaerkungsgesetz-bfsg), [Händlerbund — Kleinstunternehmen-Ausnahme](https://ohn.haendlerbund.de/recht/rechtsfragen/kleinstunternehmen-bfsg-ausnahme)

**9.2 Точный лимит бесплатных объявлений в Dienstleistungen — 2 или 3, не установлено.**
Официальная страница `themen.kleinanzeigen.de/hilfe-gewerblich/gewerbe/gebuehrengewerbliche/` не отвечает ботам (timeout 60 с, 6 попыток с двух сторон). Справочная статья про gewerblich за логином Zendesk. Цифры «2 бесплатно, 3,99–4,99 € далее» — из вторичных источников (Händlerbund/OHN, wortfilter.de). С 11.05.2026 структура изменена, источники противоречат друг другу. **Проверяется только в живом аккаунте на шаге публикации.**

**9.3 Цены PRO-пакетов** — полной таблицы не публикует ни один источник. Подтверждено только: спецтариф 15 €/мес (до 10 товаров ≤25 €) и что мелкие пакеты 1–5 объявлений не подорожали.

**9.4 Оптимальное время публикации** — измеренных данных для Kleinanzeigen нет. Рекомендация вторник–четверг 18–21 в §6.3 помечена как гипотеза и подлежит проверке твоими же цифрами просмотров.

**9.5 OLG Hamm, Urteil v. 19.11.2013, Az. 4 U 65/13** (запрет «inkl. MwSt.» для Kleinunternehmer) — цитируется по IT-Recht Kanzlei, сам текст решения не читан.

**9.6 Тексты конкурентов №7–10** (Nürnberg, Regensburg, Augsburg, Waiblingen) — сняты со страницы выдачи, детальные страницы не открывались. Заголовки, цены и даты точны; полные тексты описаний не проверены.

**9.7 Правила Kleinanzeigen про дубликаты** — страница `themen.kleinanzeigen.de/policy/` напрямую не открылась, формулировки реконструированы из поисковых сниппетов. Смысл правила подтверждается несколькими источниками, дословность — нет.

**9.8 Даты публикации ряда ценовых источников** (LINDTEC, cconnect, dsgvo-nord) на страницах не указаны — это живые коммерческие предложения на дату проверки 12.08.2026.

**9.9 Расчёт 2.378,81 €** в варианте B: 1.999 × 1,19 = 2.378,81. Арифметика проверена скриптом. Вывод «Praxis не vorsteuerabzugsberechtigt» верен как общее правило (§4 Nr. 14 UStG → освобождение → нет права на вычет), но у конкретной практики могут быть и облагаемые обороты (Selbstzahlerleistungen, IGeL, продажа товаров). Поэтому в тексте объявления стоит оговорка «Ob Sie tatsächlich nicht vorsteuerabzugsberechtigt sind, klärt Ihre Steuerberatung».

**9.10 Kleinanzeigen-статистика по числу просмотров** — есть только у одного объявления (118 у Kecke). Утверждение «Kecke получает просмотры» опирается на одну точку данных.

---

## 10. Источники

**Конкуренты и площадка:** живая выдача kleinanzeigen.de через Playwright, 12.08.2026 — `/s-dienstleistungen/muenchen/webdesign/k0c297l6411`, `/s-sonstige/muenchen/c298l6411`, `/s-dienstleistungen-edv/muenchen/c226l6411`

**Цены:** [magnet-seiten.de](https://magnet-seiten.de/blog/website-erstellen-lassen-kosten) · [saschafix.de — Arztpraxis](https://saschafix.de/wissen/blog-articles/homepage-fuer-arztpraxis-erstellen/) · [freelancermap Stundensatz](https://www.freelancermap.de/blog/stundensatz-it-freelancer/) · [Freelancer-Kompass 2025 PDF](https://www.freelancermap.de/media/press_release/PM-Freelancer-Kompass-2025.pdf) · [codeaeffchen.de — Wartung](https://codeaeffchen.de/insights/wordpress-wartung-kosten/) · [dein-wp-doktor.de — Wartung](https://dein-wp-doktor.de/wordpress-wartung-kosten/) · [davidkeiser.de — Relaunch](https://davidkeiser.de/wissen/website-relaunch-kosten/) · [niklasbern.de — KI-Automation](https://niklasbern.de/wissen/ki-automation-leitfaden/) · [snutig.de — Chatbot](https://www.snutig.de/blogbeitrage/chatbot-entwickeln-lassen-kosten-beispiele/) · [dsgvo-nord.de — Website-Check](https://dsgvo-nord.de/externe-datenschutzbeauftragte-it-sicherheitsbeauftragte/internetseiten-check/)

**Право:** [§312g BGB](https://www.gesetze-im-internet.de/bgb/__312g.html) · [§356 BGB](https://dejure.org/gesetze/BGB/356.html) · [§357a BGB](https://www.gesetze-im-internet.de/bgb/__357a.html) · [Anlage 1 EGBGB](https://www.buzer.de/Anlage_1_EGBGB.htm) · [PAngV 2022](https://www.gesetze-im-internet.de/pangv_2022/BJNR492110021.html) · [§19 UStG](https://www.gesetze-im-internet.de/ustg_1980/__19.html) · [§34a UStDV](https://dejure.org/gesetze/UStDV/34a.html) · [BMF-Schreiben 18.03.2025](https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Steuerarten/Umsatzsteuer/Umsatzsteuer-Anwendungserlass/2025-03-18-sonderregelung-kleinunternehmer.pdf?__blob=publicationFile&v=3)

**Практика:** [IT-Recht Kanzlei — Kleinanzeigen Abmahngefahr](https://www.it-recht-kanzlei.de/ebay-kleinanzeigen-handlungsanleitung-minimierung-abmahngefahr.html) · [IT-Recht Kanzlei — Kleinunternehmer MwSt.](https://www.it-recht-kanzlei.de/kleinunternehmer-mehrwertsteuer-umsatzsteuer.html) · [Händlerbund — Rechtstexte Kleinanzeigen](https://ohn.haendlerbund.de/recht/rechtsfragen/140160-rechtstexte-kleinanzeigen) · [Händlerbund — Gebühren gewerblich](https://ohn.haendlerbund.de/themen/marktplaetze/gewerbliche-verkaeufer-kleinanzeigen-kostenlose-anzeigen) · [WBS.LEGAL — OS-Plattform](https://www.wbs.legal/it-und-internet-recht/eu-streitbeilegungsplattform-os-plattform-eingestellt-jetzt-impressum-aktualisieren-83428/) · [Kleinanzeigen Hilfe — Impressum](https://hilfe.kleinanzeigen.de/hc/de/articles/17101949468572-Was-geh%C3%B6rt-in-ein-Impressum) · [Kleinanzeigen Hilfe — Ort der Dienstleistung](https://hilfe.kleinanzeigen.de/hc/de/articles/17089202962588-An-welchem-Ort-darf-ich-meine-Produkte-Dienstleistungen-oder-Jobangebote-einstellen)
