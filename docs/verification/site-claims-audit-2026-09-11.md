# Сверка фактических утверждений ais152.com — 2026-09-11

Только отчёт, на сайте ничего не менялось.

**Метод.** Страницы сняты `curl -s https://ais152.com/<путь>` 11.09.2026 (все 200), текст извлечён без JS (html.parser, script/style/svg вырезаны; JSON-LD разобран отдельно). Карточки проектов на главной пропущены (сверяются отдельно). Английская главная — только утверждения, которые отличаются от DE или имеют собственный источник; остальное — дословное зеркало DE с тем же вердиктом.

**Приборы, которыми сняты ключевые доказательства:**

- Сервер n8n: `nslookup n8n.ais152.com` → `187.33.159.205`; `curl -s https://ipinfo.io/187.33.159.205/json` → `"city": "Barcelona", "country": "ES", "org": "AS49635 CLOUDI NEXTGEN SL", hostname *.clouding.host`
- Живость проектов: `curl -s -o /dev/null -L -m 20 -w "%{http_code}"` по 15 адресам из `data/projects.json` → 14×200 сразу; elektrocheckstuttgart.de по умолчанию `curl: (35) Recv failure: Connection was reset`, с `-4 --http1.1 --tlsv1.2` → 200
- Число коммитов: `git -C C:/Projects/AiS152 rev-list --count HEAD` → 173; авторы: `git log --format='%an <%ae>' | sort | uniq -c` → `172 aidancompton001`, `1 Claude`
- Самый ранний коммит по всем репозиториям `C:/Projects/*/.git`: `git log --reverse --format=%ad --date=short | head -1`, минимум → `2026-02-14 BauPreis AI SaaS`
- Трекеры на главной: `grep -c 'googletagmanager\|google-analytics\|gtag(\|plausible\|matomo\|hotjar\|clarity'` → 0 (DE и EN)
- Счётчики на главной (без JS показывают 0): `data-target="15"`, `"85"`, `"3"` — `index.html:300/305/310`, исходник `_src/index.src.html:315/320/325`

Коды страниц: HOME = `/`, EN = `/en/`, LST = `/leistungen/`, N8N = n8n-automatisierung, KIA = ki-automatisierung, PRZ = prozessautomatisierung, KII = ki-integration-bestandssysteme, NHW = n8n-hosting-wartung, WML = website-erstellen-lassen-muenchen, HWK = website-handwerk, ARZ = website-arztpraxis, SHP = onlineshop-erstellen, WRT = wartung.html, IMP = impressum.html (дополнительно, сведения о владельце).

## Таблица

| ID | страница | утверждение (дословно) | вердикт | источник / выдержка |
|---|---|---|---|---|
| H01 | HOME | «15 Projekte sind live.» / «Projekte 15 live» | CONFIRMED | `data/projects.json`: 15 записей `"status": "live"`, Studio of Glamour `"archived"` (:371); curl 15/15 адресов → 200 (ElektroCheck только по IPv4/TLS1.2) |
| H02 | HOME | «Websites für kleine Betriebe und Praxen, Festpreis ab 390 €» | PROMISE | условие бизнеса; совпадает с `docs/KLEINANZEIGEN_STRATEGIE.md:399` «EINSEITER — 390 €» |
| H03 | HOME | «Festpreis, kein Abo» | PROMISE | условие бизнеса |
| H04 | HOME | «Antwort selber Werktag» | PROMISE | условие бизнеса |
| H05 | HOME | «172 commits · 15 projects» | CONFIRMED | `git rev-list --count HEAD` (AiS152) = 173 — число вписано руками (`index.src.html`, hero-терминал), отстаёт на 1 |
| H06 | HOME | Лента стека: «Next.js · Node · Tailwind · GSAP» | CONFIRMED | `projects.json:210-215` POMP «Next.js 16, Tailwind 4, GSAP, Lenis»; :282 Rund ums Haus «Next.js, GSAP» |
| H07 | HOME | Лента стека: «Postgres» | CONFIRMED | `MainCore/CLAUDE.md:545` BauPreis «PostgreSQL 16 (multi-tenant)»; :555 StartupProfi «PostgreSQL (таблица startup_profi_leads)» |
| H08 | HOME | Лента стека: «Supabase» | CONFIRMED | `StormGuard-V2/CLAUDE.md:5` «Eleventy … + Supabase + GSAP» |
| H09 | HOME | Лента стека: «n8n» | CONFIRMED | `StartupProfi-Automation/CLAUDE.md:44` «Воронка LIVE на проде, протестирована вживую» |
| H10 | HOME | Лента стека: «Anthropic» | CONFIRMED | `projects.json:92` SorrySara «auto-translated … by Claude»; `StartupProfi-Automation/CLAUDE.md:31` «Claude Haiku» |
| H11 | HOME | Лента стека: «shadcn/ui» | CONFIRMED | `MainCore/CLAUDE.md:542` BauPreis «Tailwind + shadcn/ui» (единственный живой проект; второй — Studio of Glamour, снят) |
| H12 | HOME | Лента стека: «Cloudflare» | CONFIRMED | `StormGuard/DEVLOG.md:691,700` «Миграция хостинга: Netlify → Cloudflare Pages … stormguard.pages.dev — LIVE» (2026-03-13) |
| H13 | HOME | Лента стека: «GitHub Actions» | CONFIRMED | `StormGuard-V2/CLAUDE.md:6` «Deploy: Hetzner via GitHub Actions SFTP» |
| H14 | HOME | Лента стека «React Native»; тег карточки «iOS / Android» | NOT_FOUND | ни одного выпущенного мобильного приложения: `MONO/STATUS.md:21` «[ ] Публикация в App Store / Google Play»; RMS, EDMI-app — только планы в CLAUDE.md |
| H15 | HOME | Лента стека «OpenAI»; карточка 03 «n8n, OpenAI, Anthropic»; тег «OpenAI / Anthropic» | NOT_FOUND | ни в одном сданном проекте: `EDMI/CLAUDE.md:98` (Whisper — план), `LKW/CLAUDE.md:61` «OpenAI (резерв)», `PersonalAssistant/docs/ЛИЧНОЕ_ДЕЛО.md:155` — навык, не проект |
| H16 | HOME | «15 Production-Projekte» (счётчик) | CONTRADICTED | `projects.json:130,141` Ofnstube «Konzeptprojekt mit fiktiver Marke»; :179,191 KONTUR — то же; :322,331 EDMI «Prototyp»; решение 11.09 (`DEVLOG.md:1534,1536`) |
| H17 | HOME | «85 % Ø Kostensenkung» | NOT_FOUND | замера нет; число — заготовка `docs/tasks/PX-002a_audit_and_roadmap.md:128` «60-85% savings», `docs/tasks/PX_REGISTRY.md:475` «85% AVG. COST REDUCTION» без источника |
| H18 | HOME | «3 T Bis Launch — Für Landings & MVPs» | PROMISE | обещание сроков, стоит в ряду статистики как измеренное; замера нет. Для сравнения Henner Heede: `HennerHeede-Site/DEVLOG.md` S002 24.07 → S024 06.08 |
| H19 | HOME | «24/7 Systeme im Betrieb» | CONFIRMED | curl 15/15 адресов → 200 (11.09) |
| H20 | HOME | Блок «Was Kunden bei Google schreiben» | CONFIRMED | блок `hidden`, `data/reviews.json:9,15` `"ratingCount": 0`, `"reviews": []` — отзывов на сайте не показано. В HTML остаётся «(Stand: )» с пустой датой |
| H21 | HOME | «Fünfzehn Projekte aus München, kürzlich ausgeliefert» | CONTRADICTED | из Мюнхена только Henner Heede (`projects.json:43`) и вымышленная Ofnstube (:141). Остальные: Spessart, Leer, Burgas, Kiel, Stuttgart, Osnabrück, Köln, Украина; Ofnstube/KONTUR не «ausgeliefert» — клиента нет (`consents.json:31,43`) |
| H22 | HOME | «Alles live, alles produktiv.» | CONTRADICTED | см. H16: 2 концепта + прототип EDMI |
| H23 | HOME | «KI-Automatisierung, Apps, Plattformen, drei Dinge, die ich gut mache» | CONTRADICTED | ниже 4 карточки: App-Entwicklung, Websites, Prozessautomatisierung, Website-Wartung |
| H24 | HOME | «Kein Agenturaufschlag, keine Junior-Schicht. Direkte Arbeit, Ende zu Ende.» | CONFIRMED | `vault/05_Cases/2026-08_gewerbeanmeldung-ais152/SUMMARY.md:31` «1 Beteiligter, 0 Mitarbeiter» |
| H25 | HOME | «SaaS-Dashboards, B2C-Plattformen, interne Tools» | CONFIRMED | `projects.json:238` BauPreis (SaaS); :92 SorrySara (Stripe-билеты, B2C); `PersonalAssistant/CLAUDE.md:61` (внутренний инструмент) |
| H26 | HOME | «Die Domain läuft auf Ihren Namen, alle Zugänge bekommen Sie, kein Abo.» | PROMISE | условие бизнеса |
| H27 | HOME | Тег «Cloudflare Pages» (Websites) | CONFIRMED | `StormGuard/DEVLOG.md:700` |
| H28 | HOME | «E-Mail-Triage, Lead-Scoring» | CONFIRMED | `StartupProfi-Automation/CLAUDE.md:44` «score 85 hot vs 5 cold»; `PersonalAssistant/CLAUDE.md:61` «AI-классификация писем (Claude Haiku)» |
| H29 | HOME | «Content-Pipelines, Reporting» | NOT_FOUND | ни одного живого проекта; `LKW/STATUS.md:30` (content factory) — черновик |
| H30 | HOME | «Website-Wartung — ab 39 €/Mon. … Monatlich kündbar, keine Bindung.» | PROMISE | согласуется с `agb.html:153` «Es besteht keine Mindestlaufzeit» |
| H31 | HOME | «Alle Preise sind Endpreise. Gemäß § 19 UStG wird keine Umsatzsteuer erhoben» | CONFIRMED | `SUMMARY.md:29` «Kleinunternehmer §19 UStG» |
| H32 | HOME | «Domaingebühr etwa 15 € im Jahr, Hosting etwa 5 bis 10 € im Monat» | PROMISE | оценка для клиента |
| H33 | HOME | «Antwort am selben Werktag. Konzept in 24 Stunden. Live in 3 Tagen.» | PROMISE | обещание сроков |
| H34 | HOME | «Geschäftszeiten, Mo–Fr 09–19 MEZ» | PROMISE | условие бизнеса |
| H35 | HOME | «30 Tage Gewährleistung inklusive.» | CONTRADICTED | `agb.html:191-193` «Es gelten die gesetzlichen Mängelrechte. Zusätzlich beseitigt der Auftragnehmer innerhalb von 30 Tagen nach Abnahme kostenfrei auch solche Abweichungen, die keinen Mangel im Rechtssinne darstellen.» — гарантия законная, 30 дней — это дополнительная бесплатная доработка |
| H36 | HOME | «n8n-Automatisierung aus München · ein Ingenieur, nur Produktion» | CONTRADICTED | `PersonalAssistant/docs/ЛИЧНОЕ_ДЕЛО.md:150` «2008–2012: Tourismusmanagement»; :24 цель «Учёба в университете — KI Ingenieurwesen». В Баварии «Ingenieur» — защищённое звание (BayIngG). «nur Produktion» — см. H16 |
| H37 | HOME | «Ich sitze in München und schreibe Code, für den andere bezahlen.» | CONFIRMED | `SUMMARY.md:48` (счета 2026-001 и 2026-002); `rechnungen/Rechnung-2026-001-Moennigmann.pdf` |
| H38 | HOME | «funktionierende Software in Repos mit meinem Namen auf den Commits» | CONTRADICTED | `git log` AiS152: 172 коммита от `aidancompton001`, 1 от `Claude`; имени владельца в коммитах нет |
| H39 | HOME | «Manche haben hundert Nutzer, manche zehntausend.» | NOT_FOUND | нигде нет чисел пользователей |
| H40 | HOME | «Alle wurden im zugesagten Zeitrahmen ausgeliefert.» | NOT_FOUND | срок записан только у Henner Heede (`HennerHeede-Site/CLAUDE.md:8` «дедлайн середина августа», последние правки `DEVLOG.md:1` 06.08 — не противоречит); по остальным 11 клиентским проектам записей нет; у концептов клиента нет |
| H41 | HOME | «Der Name «AIS.152» ist ein leises Tribut an AISI 52100» | CONFIRMED | `SUMMARY.md:27` «AIS.152 (Anspielung an AISI 52100 bearing steel)» |
| H42 | HOME | «Munich, DE · EN · DE · RU» | CONFIRMED | `SUMMARY.md:62` (адрес Мюнхен); `ЛИЧНОЕ_ДЕЛО.md:160-165` RU родной, EN B2, DE B1 |
| H43 | HOME | «Einzelunternehmer · Kleinunternehmer §19 UStG» | CONFIRMED | `SUMMARY.md:12` «nicht eingetragenes Einzelunternehmen», :29 |
| H44 | HOME | «2024–now» | NOT_FOUND | стоит рядом с «Einzelunternehmer», читается как «работаю с 2024». Gewerbe с 12.08.2026 (`SUMMARY.md:17`); самый ранний коммит всех проектов 2026-02-14; `ЛИЧНОЕ_ДЕЛО.md:147` «2024–2025: Full-Stack & AI» — это обучение |
| H45 | HOME | «Ich lese jede Nachricht und antworte innerhalb eines Werktages, meist schneller.» | PROMISE | условие бизнеса |
| H46 | HOME | «+49 155 636 75 772 · ais152.business@gmail.com» | CONFIRMED | `SUMMARY.md:63` телефон; Impressum на живом сайте — те же данные |
| H47 | HOME | «Engineering-Studio für KI-Automatisierung, n8n und Produktionssoftware. München, weltweit tätig.» | CONFIRMED | клиенты в BG (`projects.json:80`, :309), UA (:251) |
| H48 | HOME | «Mit Vanilla-HTML + GSAP gebaut. Keine Frameworks, keine Tracker.» | CONFIRMED | grep трекеров в home.html = 0 |
| H49 | HOME | meta: «Apps und Plattformen im produktiven Einsatz» | CONFIRMED | BauPreis, SorrySara — `projects.json:229,83`, оба 200 |
| H50 | HOME | JSON-LD Person `"name": "Eduard Baias"` | CONTRADICTED | Impressum и Gewerbe: «Eduard Morocho Baias» (`SUMMARY.md:57`); тот же блок во всех 9 страницах услуг |
| H51 | HOME | JSON-LD `knowsAbout: "Mobile Development", "React Native"`; `"description": "…AI systems, mobile applications…"` | NOT_FOUND | см. H14 |
| E01 | EN | «Reply in 1 hour. Concept in 24 hours. Live in 3 days.» / «One real human, one hour … I read it the same hour» / «Within 1 hour» | CONTRADICTED | противоречит той же EN-странице: hero «Response — same working day», Kontakt «reply within one business day»; DE-версия «Am selben Werktag» |
| E02 | EN | meta: «Production AI systems, mobile platforms, and automation» | CONTRADICTED | мобильных платформ в работе нет: `MONO/STATUS.md:7,21` |
| E03 | EN | «Fifteen things I shipped recently» | CONTRADICTED | см. H21 (концепты не «shipped» клиенту) |
| E04 | EN | «All live, all production.» | CONTRADICTED | см. H16 |
| E05 | EN | «Three things I do well» | CONTRADICTED | 4 карточки |
| E06 | EN | «One engineer · Production-only» | CONTRADICTED | «Production-only» — см. H16 (в портфолио концепты и прототип) |
| E07 | EN | «Some have a hundred users, some have ten thousand.» | NOT_FOUND | см. H39 |
| E08 | EN | «All of them were shipped on the timelines I quoted.» | NOT_FOUND | см. H40 |
| E09 | EN | «30 days of warranty included.» | CONTRADICTED | см. H35 |
| E10 | EN | «85 % Avg. cost reduction» | NOT_FOUND | см. H17 |
| E11 | EN | «15 Production projects» | CONTRADICTED | см. H16 |
| E12 | EN | «…just working software in repositories with my name on the commits» | CONTRADICTED | см. H38 |
| L01 | LST | meta «Fünf Leistungen, jede einzeln beschrieben» / «Fünf Sachen, die ich regelmäßig baue» | CONTRADICTED | на той же странице 9 ссылок на услуги |
| L02 | LST | «n8n Hosting und Wartung, Betrieb auf einem Server in Deutschland» | CONTRADICTED | n8n.ais152.com → 187.33.159.205 → ipinfo: Barcelona, ES (Clouding); `KONTUR/docs/CREDENTIALS.md:31` «Clouding.io (shared-сервер n8n-main)»; `MainCore/CLAUDE.md:558` |
| L03 | LST | «Fünfzehn ausgelieferte Projekte stehen unter Ausgewählte Arbeiten» | CONTRADICTED | 2 из 15 — концепты с вымышленным брендом (`consents.json:31,43`), не сданы клиенту |
| N01 | N8N | meta: «…mit Daten, die in Deutschland bleiben.» | CONTRADICTED | см. L02 |
| N02 | N8N | «Ich betreibe die Instanz auf einem Server in Deutschland» | CONTRADICTED | см. L02 |
| N03 | N8N | «trenne Zugänge, protokolliere Läufe … steht das im Verzeichnis der Verarbeitungstätigkeiten, mit Auftragsverarbeitungsvertrag» | PROMISE | порядок работы; реестра обработок ни в одном проекте не найдено |
| N04 | N8N | «Systeme, die nicht miteinander reden, bekommen eine Brücke: DATEV, Shopware, Google Workspace, Telefonie» | NOT_FOUND | DATEV/Shopware упомянуты только в `HausBot/DEVLOG.md`, `RMS/DEVLOG.md` — не сданные проекты, не в портфолио |
| N05 | N8N | «Ein Workflow zuerst … läuft er zwei Wochen ohne Nacharbeit, kommt der nächste» | PROMISE | порядок работы |
| N06 | N8N | «Ich übergebe alles dokumentiert.» / «Bezahlt wird, was gebaut ist und läuft.» | PROMISE | условие бизнеса |
| N07 | N8N | «Fünfzehn ausgelieferte Projekte stehen unter» | CONTRADICTED | см. L03 |
| K01 | KIA | «Da baue ich einen Menschen in den Ablauf ein» / «Ich sage vorher, wenn eine Aufgabe für ein Sprachmodell ungeeignet ist» | PROMISE | порядок работы |
| K02 | KIA | «n8n für die Abläufe, Claude oder ein vergleichbares Modell für den Sprachteil, PostgreSQL für Daten» | CONFIRMED | `StartupProfi-Automation/CLAUDE.md:31` «Claude Haiku»; `MainCore/CLAUDE.md:555` PostgreSQL; n8n — H09 |
| K03 | KIA | «…ein Server in Deutschland für den Betrieb» | CONTRADICTED | см. L02 |
| K04 | KIA | «Kein Aufbau, der ohne einen einzelnen Anbieter zusammenbricht.» | PROMISE | принцип |
| K05 | KIA | «Fünfzehn ausgelieferte Projekte stehen unter» | CONTRADICTED | см. L03 |
| P01 | PRZ | «Ich schreibe auf, welcher Ablauf welche Felder anfasst, wo sie liegen und wie lange.» | PROMISE | порядок работы |
| P02 | PRZ | «Fünfzehn ausgelieferte Projekte stehen unter» | CONTRADICTED | см. L03 |
| I01 | KII | «Offene Schnittstelle … Anbindung in Tagen» | PROMISE | обещание сроков |
| I02 | KII | «Ich verdiene an beidem gleich. Deshalb rate ich zu dem, was weniger kostet.» | PROMISE | принцип |
| I03 | KII | «Fünfzehn ausgelieferte Projekte stehen unter» | CONTRADICTED | см. L03 |
| W01 | NHW | meta «n8n selbst gehostet auf einem Server in Deutschland» | CONTRADICTED | см. L02 |
| W02 | NHW | «Eigene n8n-Instanz auf einem Server in Deutschland, getrennt von anderen Kunden» | CONTRADICTED | сервер в ES (L02); нынешняя инстанция общая с BauPreis/KONTUR/MONO (`KONTUR/docs/CREDENTIALS.md:31`) |
| W03 | NHW | «Updates … Überwachung … Sicherung von Workflows und Daten, mit geprüfter Wiederherstellung … Zugänge getrennt nach Person» | PROMISE | состав услуги |
| W04 | NHW | «In beiden Fällen bekommen Sie Zugänge und Dokumentation.» | PROMISE | условие бизнеса |
| W05 | NHW | «Fünfzehn ausgelieferte Projekte stehen unter» | CONTRADICTED | см. L03 |
| M01 | WML | meta «…schnell, DSGVO-konform. Ein Ingenieur, direkte Arbeit» | CONTRADICTED | «Ein Ingenieur» — см. H36; «DSGVO-konform» — обещание |
| M02 | WML | «Sie reden mit der Person, die den Code schreibt.» | CONFIRMED | `SUMMARY.md:31` 0 Mitarbeiter |
| M03 | WML | «Handgeschriebener Code statt Baukasten oder gekauftes Theme» / «WordPress mit ACF» | CONFIRMED | `projects.json:44` Henner «Handgeschriebenes WordPress-Theme mit ACF»; :118 Silke Klein Art — то же |
| M04 | WML | «Zweisprachig … jede Sprache auf eigener Adresse» | CONFIRMED | ais152.com и /en/; `projects.json:69` Taxi DE/EN/Plattdeutsch |
| M05 | WML | «Ich sage ab, wenn ein Projekt bei mir schlechter aufgehoben wäre.» | PROMISE | принцип |
| M06 | WML | «nach dem ersten Gespräch bekommen Sie eine Summe und einen Umfang, an die ich mich halte» / «Das Gespräch kostet nichts.» | PROMISE | условие бизнеса |
| M07 | WML | «Persönlich in München oder per Video» | PROMISE | условие бизнеса |
| M08 | WML | «Fünfzehn ausgelieferte Projekte stehen unter» | CONTRADICTED | см. L03 |
| R01 | HWK | «Nach der Arbeit an Websites für Elektro, Hausmeisterservice, Garten und Prüfservice» | CONFIRMED | `projects.json:167` ElektroCheck «Elektromeister … DGUV V3 Prüfungen»; :287 Rund ums Haus «Hausmeisterservice und Garten»; согласия `consents.json:36,58` |
| R02 | HWK | «Deshalb baue ich statisch» | CONFIRMED | `projects.json:166` ElektroCheck «Vanilla HTML+CSS+JS, GitHub Pages» |
| R03 | HWK | meta «DSGVO-konform»; «Schriften vom eigenen Server …, Formular ohne Weitergabe an Dritte» | PROMISE | принцип. Замечание: у референса ElektroCheck форма идёт через FormSubmit, то есть через третью сторону (`projects.json:167`) |
| R04 | HWK | «Fünfzehn ausgelieferte Projekte stehen unter» | CONTRADICTED | см. L03 |
| A01 | ARZ | «Website für Arztpraxis in München — 690 € Festpreis» | PROMISE | согласуется с `docs/KLEINANZEIGEN_STRATEGIE.md:767` (690) |
| A02 | ARZ | «Eine Praxiswebsite, die das sauber beantwortet, entlastet den Empfang messbar.» | NOT_FOUND | ни одного сайта практики в работе и ни одного замера; сама страница пишет «Eine Praxis ist noch nicht dabei» |
| A03 | ARZ | «den Auftragsverarbeitungsvertrag können Sie lesen, bevor Sie mir schreiben» / «Mein Muster liegt offen: ais152.com/avv.html» | CONFIRMED | curl https://ais152.com/avv.html → 200 |
| A04 | ARZ | Состав пакета «bis zu 6 Seiten … Auftragsverarbeitungsvertrag nach Art. 28 DSGVO, unterschrieben» | PROMISE | состав услуги |
| A05 | ARZ | «Mehr als 10 Seiten, zweisprachig oder mit Online-Terminvergabe: 990 bis 1.200 €» | PROMISE | цена. Замечание: 7–10 страниц без цены |
| A06 | ARZ | «Ich bin Kleinunternehmer nach § 19 UStG» | CONFIRMED | `SUMMARY.md:29` |
| A07 | ARZ | «im ersten Jahr ändere ich das ohne Berechnung» / «Kein Abo, keine Mindestlaufzeit» | PROMISE | условие бизнеса |
| A08 | ARZ | «taxi-moennigmann.de — dreisprachig» | CONFIRMED | `Taxi-Moennigmann/CLAUDE.md:25` «Deutsch + English + Plattdeutsch» |
| A09 | ARZ | «…barrierefrei nach WCAG 2.1 AA» | NOT_FOUND | соответствие не проверено: `Taxi-Moennigmann/CLAUDE.md:27` — только «наш стандарт качества»; в `verify/acceptance.json:14` из доступности проверяется только skip-link; аудита (axe/контраст) нет |
| A10 | ARZ | «elektrocheckstuttgart.de — Prüfservice, B2B» | CONFIRMED | `projects.json:153,160` «DGUV V3 … B2B»; живой (200 по IPv4/TLS1.2) |
| A11 | ARZ | «rundumshaus-littawe.de — Hausmeisterservice» | CONFIRMED | `projects.json:274`; 200 |
| A12 | ARZ | «ais152.com — meine eigene Seite mit Impressum, Datenschutz, Widerruf und AVV» | CONFIRMED | sitemap.xml: impressum/datenschutz/widerruf; avv.html 200 |
| A13 | ARZ | «Eine Praxis ist noch nicht dabei» | CONFIRMED | Praxis-Stadtpark — только демо `praxis-demo.ais152.com` с noindex (`Praxis-Stadtpark/STATUS.md:10-19`) |
| A14 | ARZ | «Sie bekommen innerhalb eines Werktages eine ehrliche Einschätzung und einen Festpreis» | PROMISE | условие бизнеса |
| A15 | ARZ | «Fünfzehn ausgelieferte Projekte stehen unter» | CONTRADICTED | см. L03 |
| S01 | SHP | meta «WooCommerce oder handgeschrieben, Zahlung, Versand, Rechtstexte» | CONFIRMED | `projects.json:19` The Crazy Bee «WooCommerce-Shop … Honig-Shop mit Rechnung und Vorkasse» |
| S02 | SHP | «Zahlung: Karte, PayPal, Rechnung, Vorkasse» / «Versandkosten … auch nach Österreich und in die Schweiz» / «Rechtstexte an den vorgeschriebenen Stellen» | PROMISE | состав услуги |
| S03 | SHP | «Deshalb gehört Überwachung dazu» / «Bestellungen wandern automatisch in die Buchhaltung» | PROMISE | состав услуги |
| S04 | SHP | «Fünfzehn ausgelieferte Projekte stehen unter» | CONTRADICTED | см. L03 |
| T01 | WRT | «BASIS — 39 € / STANDARD — 59 € / PRAXIS & KANZLEI — 79 € / Monat» | PROMISE | цены |
| T02 | WRT | «Verfügbarkeits-Monitoring alle 5 Minuten», «Wöchentliches verschlüsseltes Backup», «Antwort … innerhalb eines Werktags» | PROMISE | состав услуги |
| T03 | WRT | «Auftragsverarbeitungsvertrag nach Art. 28 DSGVO, unterschrieben — Muster vorab lesen» | CONFIRMED | avv.html → 200 |
| T04 | WRT | «Bewusst nicht enthalten (§ 3 AGB, gesondert nach Aufwand)» | CONFIRMED | `agb.html:90-93` «§ 3 Leistungsumfang … Positionen sind abschließend» |
| T05 | WRT | «Ich schaue mir deine Website 15 Minuten an — kostenlos» | PROMISE | условие бизнеса |
| T06 | WRT | «Rechnungen werden gemäß § 34a UStDV … Muster unter rechnungen/muster» | CONFIRMED | файл `rechnungen/muster.html` есть |
| T07 | WRT | «Eduard Morocho Baias — AIS.152, Oefelestraße 19, 81543 München» | CONFIRMED | `SUMMARY.md:57,62` |
| T08 | WRT | «Kleinunternehmer nach § 19 UStG — keine Umsatzsteuer.» | CONFIRMED | `SUMMARY.md:29` |
| T09 | WRT | «Gewerbeanmeldung KVR München vom 12.08.2026.» | CONFIRMED | `SUMMARY.md:17,70` «Geltungszeitpunkt: 12.08.2026» |
| T10 | WRT | «Wartungsverträge sind monatlich mit 14 Tagen zum Monatsende kündbar (§ 6 AGB).» | CONFIRMED | `agb.html:156-157` «mit einer Frist von 14 Tagen zum Ende eines Kalendermonats in Textform kündigen» |
| T11 | WRT | «E-Mail: ais152.business@gmail.com · Telefon: +49 155 636 75 772» | CONFIRMED | `SUMMARY.md:63` |
| X01 | IMP | «Gewerbeanzeige beim Kreisverwaltungsreferat … am 12.08.2026. Aktenzeichen: 8220-26-14125.» | CONFIRMED | `SUMMARY.md:9,48` «Aktenzeichen `8220-26-14125`» |
| X02 | IMP | «Die Steuernummer wurde beim Finanzamt München beantragt» | NOT_FOUND | подачи нет в записях: `SUMMARY.md:88` «[ ] Fragebogen zur steuerlichen Erfassung ausfüllen»; `2026-08_jc-aenderungsmitteilung-lts-selbstaendigkeit/CHECKLIST_Selbststaendigkeit.md:52-54` — анкету ещё ждут |

## Проекты на страницах услуг

Упоминания проектов в текстах 9 страниц услуг, `/leistungen/` и wartung (`grep -oniE` по сохранённому HTML всех 11 страниц):

- **website-arztpraxis.html** — единственная страница с проектами: taxi-moennigmann.de, elektrocheckstuttgart.de, rundumshaus-littawe.de, ais152.com. Все четыре существуют, отвечают 200 и соответствуют описанию (A08, A10–A12). Исключение — «barrierefrei nach WCAG 2.1 AA» у Taxi (A09): не доказано
- **website-handwerk.html** — проекты не названы, но «Websites für Elektro, Hausmeisterservice, Garten und Prüfservice» — это ElektroCheck и Rund ums Haus: реальные клиенты с согласием (R01)
- **Studio of Glamour, Ofnstube, KONTUR, StormGuard, EDMI, «Konfigurator», «Dashboard»** — 0 вхождений на всех 11 страницах. Решениям 11.09 страницы не противоречат
- Косвенный конфликт с решением 11.09: фраза «Fünfzehn ausgelieferte Projekte» стоит в подвале всех 9 страниц услуг и на `/leistungen/`, а «Fünfzehn Projekte aus München, kürzlich ausgeliefert» / «Alles live, alles produktiv» / счётчик «15 Production-Projekte» — на главной. Все они считают Ofnstube и KONTUR (концепты) и EDMI (прототип) сданными рабочими проектами

## CONTRADICTED — точные правки

1. **Server in Deutschland (L02, N01, N02, K03, W01, W02).** Правда: n8n на Clouding, Барселона (ES). Вариант А — поменять текст: «Server in der EU (Spanien)»; «Daten, die in der EU bleiben»; «Eigene n8n-Instanz auf einem Server in der EU». Вариант Б — перенести n8n на сервер в Германии и оставить текст. Где править:
   - `_src/leistungen_index.html:16`
   - `_src/leistungen/n8n-automatisierung.json:5`, `:29`
   - `_src/leistungen/ki-automatisierung.json:36`
   - `_src/leistungen/n8n-hosting-wartung.json:5`, `:12` — также убрать «getrennt von anderen Kunden» или назвать это условием для нового клиента: «für jeden Kunden eine eigene Instanz»
   - Попутно: `BauPreis AI SaaS/CLAUDE.md:261` называет тот же IP «Hetzner CX32, Nuremberg» — это ложь во внутренней документации
2. **«ausgelieferte Projekte» ×10 (L03, N07, K05, P02, I03, W05, M08, R04, A15, S04).** Заменить на «Fünfzehn Projekte, davon zwei Konzeptprojekte, stehen unter …»; либо считать без `concept`. Где править: `scripts/build_services.py:121` (все 9 страниц услуг), `_src/leistungen_index.html:31`. Счёт — в `_projects_word()` (`build_services.py:130-138`), нужен фильтр по `consents.json` → `concept`
3. **«Fünfzehn Projekte aus München, kürzlich ausgeliefert» / «{{WORD_EN}} things I shipped recently» (H21, E03).** Заменить на «Fünfzehn Projekte, zwei davon Konzeptprojekte» / «Fifteen projects, two of them concept work». Где править: `_src/index.src.html:347` (DE), `:346` (EN)
4. **«Alles live, alles produktiv.» / «All live, all production.» (H22, E04).** Заменить на «Alle live. Zwei Konzeptprojekte und ein Prototyp sind als solche markiert.» / «All live. Two concept projects and one prototype are labelled as such.» Где править: `_src/index.src.html:355`, `:354`
5. **Счётчик «15 Production-Projekte» (H16, E11).** Подпись «Projekte live» / «Projects live» при `{{N}}`; либо число без концептов и прототипа. Где править: `_src/index.src.html:315-317`
6. **«drei Dinge» / «Three things» (H23, E05).** Заменить на «vier Dinge» / «Four things» либо убрать число. Где править: `_src/index.src.html:423`, `:422`
7. **«Fünf Leistungen» / «Fünf Sachen» (L01).** Заменить на «Neun Leistungen» / «Neun Sachen» либо убрать число. Где править: `scripts/build_services.py:184`, `_src/leistungen_index.html:8`
8. **«30 Tage Gewährleistung» / «30 days of warranty» (H35, E09).** Заменить на «Gesetzliche Gewährleistung, dazu 30 Tage kostenlose Nachbesserung ab Abnahme.» / «Statutory warranty, plus 30 days of free fixes after acceptance.» Где править: `_src/index.src.html:559`, `:558`
9. **«ein Ingenieur» (H36, M01).** Заменить на «ein Entwickler» (DE). EN «engineer» можно оставить. Где править: `_src/index.src.html:576`, `_src/leistungen/website-erstellen-lassen-muenchen.json:5`. «nur Produktion» / «Production-only» (H36, E06) → «Code statt Folien» / «Code, not slides»: `_src/index.src.html:576`, `:575`
10. **«Repos mit meinem Namen auf den Commits» (H38, E12).** Заменить на «in Repos, die ich selbst schreibe» / «in repositories I write myself»; либо переписать автора коммитов на своё имя. Где править: `_src/index.src.html`, абзац About (соседний с `:583`/`:584`)
11. **EN «Reply in 1 hour» / «one hour … the same hour» / «Within 1 hour» (E01).** Заменить на «Reply the same working day.» / «I read it the same working day …» / «Same working day». Где править: `_src/index.src.html:507`, `:522`, `:525`
12. **EN meta «mobile platforms» (E02).** Заменить на «Independent studio in Munich. Websites, automation with n8n and AI, and platforms running in production.» Где править: `scripts/build_langs.py:56-57`. JSON-LD там же, где H51: `_src/index.src.html:76`, `:110`
13. **JSON-LD `"name": "Eduard Baias"` (H50).** Заменить на `"Eduard Morocho Baias"`. Где править: `_src/index.src.html:62`. На страницы услуг блок попадает через `shell()` в `build_services.py` — проверить после сборки

## NOT_FOUND — точные правки

1. **«85 % Ø Kostensenkung» (H17, E10).** Убрать карточку; либо заменить проверяемым числом («Festpreis ab 390 €»). Где править: `_src/index.src.html:320-322`
2. **«Manche haben hundert Nutzer, manche zehntausend.» (H39, E07).** Удалить предложение. Где править: `_src/index.src.html:584`, `:583`
3. **«Alle wurden im zugesagten Zeitrahmen ausgeliefert.» (H40, E08).** Удалить; либо «Termine, die ich zusage, halte ich» — это уже PROMISE. Где править: `_src/index.src.html:584`, `:583`
4. **«2024–now» (H44).** Заменить на «seit 08/2026 selbstständig» либо «Code seit 2024». Где править: `_src/index.src.html:597`
5. **«React Native», «iOS / Android», JSON-LD «Mobile Development»/«mobile applications» (H14, H51).** Убрать из ленты и тегов, пока нет выпущенного приложения. Где править: `_src/index.src.html` лента стека (район `:300`), `:452`, `:76`, `:110`
6. **«OpenAI» (H15).** Убрать из ленты (`_src/index.src.html:300`), из текста карточки 03 (`:471-472`) и тега (`:474`); оставить «Anthropic»
7. **«Content-Pipelines, Reporting» (H29).** Сократить до «E-Mail-Triage, Lead-Scoring» / «Email triage, lead scoring». Где править: `_src/index.src.html:471-472`
8. **«DATEV, Shopware, Google Workspace, Telefonie» (N04).** Заменить на «etwa Buchhaltung, Shop, Kalender, Telefonie» (без марок) либо «z. B. …» как пример без опыта. Где править: `_src/leistungen/n8n-automatisierung.json` (абзац «Was n8n Automatisierung konkret übernimmt»)
9. **«entlastet den Empfang messbar» (A02).** Заменить на «…soll den Empfang entlasten». Где править: `_src/leistungen/website-arztpraxis.json:7`
10. **«barrierefrei nach WCAG 2.1 AA» у Taxi (A09).** Заменить на «barrierearm gebaut, Ziel WCAG 2.1 AA»; либо сначала провести аудит (axe + контраст) и сохранить отчёт. Где править: `_src/leistungen/website-arztpraxis.json`, блок «Arbeiten, die Sie selbst ansehen können»
11. **Impressum «Die Steuernummer wurde beim Finanzamt München beantragt» (X02).** Правда по записям: анкету ещё не подавали. Либо подать Fragebogen в ELSTER, либо заменить на «Die Steuernummer wird nach Vergabe durch das Finanzamt München ergänzt.» Где править: `impressum.html` (раздел «Steuernummer»; в `_src` нет — править корневой файл)

## Попутно (вне вердиктов)

- `/`: «Stand: )» — пустая дата в скрытом блоке отзывов (`index.html:337`); при открытии блока будет видна
- ARZ: цена для 7–10 страниц не определена (690 € — до 6 страниц, 990–1.200 € — больше 10)
- elektrocheckstuttgart.de: по умолчанию `curl: (35) Connection was reset`, с `--tlsv1.2 -4` → 200; DNS указывает на 217.160.0.22 (IONOS), в `projects.json:166` написано «GitHub Pages» — это касается карточки, передать в сверку карточек
