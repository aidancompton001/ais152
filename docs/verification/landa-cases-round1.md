# Ревью #14 Hans Landa — тексты кейсов, круг 1 из 2 (AIS152-IDX-001)

Дата: 2026-09-11. Вердикт: **REJECTED** — все 14 FIX. Сито `case_text_rules.py`: CASE_RULES_OK files=14 (ловит только шаблоны).
Сверено 583 выдержки со строкой источника (±3): одна мимо — baupreis `consents.json:18` → на деле 78.

## CRITICAL
- baupreis: «auf einem Server in Deutschland» — ложь, сервер Clouding.io, Barcelona; `CLAUDE.md:45` (Hetzner) устарел → удалить предложение
- provenly-homes: сайт подан как принятый клиентом, а provenlyhomes.de на Framer; публично перечислены дефекты живого сайта названной фирмы («kein Cookie-Hinweis») → правки ниже, публикация кейса — решение CEO

## Правки по проектам (цитата → что не так → правка)

**baupreis**
1. CRITICAL «Betrieben wird die Anwendung auf einem Server in Deutschland.» → удалить
2. HIGH «Abonnements über Stripe» → Stripe в test mode, биллинг PayPal+Paddle (`DEVLOG.md:547`) → «Die Anmeldung läuft per E-Mail oder Google-Konto, und Funktionen werden je nach Tarif freigeschaltet.»
3. MEDIUM [не проверено] «BauPreis läuft produktiv … KI-Prognosen» → низкий баланс Anthropic API → «BauPreis ist unter baupreis.ais152.com erreichbar.»
4. MEDIUM конкуренты по именам (Mintec, Fastmarkets, BKI, SIRADOS) — § 6 UWG → «Die vorhandenen Werkzeuge passen nicht zu ihnen. Baupreis-Nachschlagewerke sind statisch und arbeiten ohne KI, professionelle Rohstoff-Datendienste sind für den Mittelstand zu teuer, und Bausoftware für die Projektabwicklung beobachtet keine Preise.»
5. LOW «Sieben Cron-Jobs sammeln Preise, …» → «Sieben Cron-Jobs übernehmen den Betrieb: Sie sammeln Preise, …»; источник `consents.json:18` → `:78`

**edmi**
1. MEDIUM «Gewählt wurde die helle Glass-Variante» → «Gewählt wurde die helle Fassung von Glass Prism, die ich anschließend ausgebaut habe:»
2. LOW «Im Rahmen eines Projekts, zu dem auch eine mobile App gehört» → «Zusätzlich zum Shop sollte eine eigenständige Landingpage entstehen.»

**eko-oylis-ua**
1. LOW «alte Adressen leiten per 301 auf die neuen weiter» → «alte Adressen wie /sertifikation leiten per 301 auf die neuen weiter.»

**elektrocheck-stuttgart**
1. MEDIUM [не проверено] «Die Anfrage geht zusammen mit diesem Ergebnis an den Betrieb» → подтверждения FormSubmit нет → удалить предложение (или тестовая заявка с записью результата)
2. LOW «reines HTML, CSS und JavaScript ohne externe Abhängigkeiten» → «ohne externe Bibliotheken»
3. LOW источники ведут на черновик `design/desktop/phase-3/index.html` → перевести на опубликованный код

**hennerheede**
1. MEDIUM «Sein Portfolio zeigt er potenziellen Arbeitgebern» → раскрывает поиск работы → «… Baldessarini und Mustang. Entsprechend genau mussten Bild und Typografie in seinem Portfolio sitzen.»
2. MEDIUM «Weil Theme und Schriften auf dem eigenen Server liegen, hängt die Seite an keiner Baukasten-Plattform und an keinem Abo.» → «Theme und Schriften liegen auf dem Webserver der Seite, eine Baukasten-Plattform mit Abo braucht sie nicht.»

**kontur** (решение CEO: Konzeptprojekt)
1. «KONTUR ist eine fiktive deutsche Specialty-Kaffeerösterei. Ich habe das Projekt als Portfolio-Fallstudie angelegt, mit dem Anspruch eines echten Produktivshops.» → «KONTUR ist ein Konzeptprojekt: eine erfundene deutsche Specialty-Kaffeerösterei, für die ich einen Onlineshop mit dem Anspruch eines echten Produktivshops gebaut habe. Einen realen Auftraggeber gibt es nicht.»; «Beispielinhalte der Fallstudie» → «Beispielinhalte des Konzeptprojekts»
2. «Der Shop ist unter einer eigenen Subdomain öffentlich erreichbar und bildet den ganzen Kaufweg ab:» → «Der Konzept-Shop ist unter einer eigenen Subdomain öffentlich erreichbar und zeigt den ganzen Kaufweg:»
3. HIGH «Die Vorgaben aus DSGVO, PAngV, LMIV, § 312j BGB und BFSG sind direkt im Theme umgesetzt» → «Grundpreis und „inkl. MwSt.“ nach PAngV, die LMIV-Pflichtangaben, die Bestellschaltfläche nach § 312j BGB und ein Cookie-Banner mit gleichwertigen Schaltflächen sind direkt im Theme umgesetzt, dazu Grundlagen der Barrierefreiheit wie Sprachauszeichnung, Sprunglink, Alternativtexte und Landmarken.»
4. LOW «Die Seite läuft in einem Docker-Container mit SSL-Zertifikat von Let's Encrypt.» → удалить

**ofnstube** (решение CEO: Konzeptprojekt)
1. «Ofnstube ist kein realer Betrieb, sondern eine fiktive Marke: … Ich habe das Projekt als eigene Fallstudie umgesetzt, veröffentlicht unter einer Subdomain meines Portfolios.» → «Ofnstube ist ein Konzeptprojekt: ein erfundenes Craft-Burger-Restaurant in München mit bayerischer Stuben-Atmosphäre. Einen realen Betrieb gibt es nicht. Veröffentlicht ist die Website unter einer Subdomain meines Portfolios.»
2. «Aus drei Markenvarianten wurde eine ausgewählt» → «Aus drei Markenvarianten habe ich eine ausgewählt»
3. «weil Alkohol nur vor Ort ausgeschenkt wird» → «weil das Konzept Alkohol nur zum Verzehr vor Ort vorsieht.»
4. HIGH «Die Reservierungsseite bündelt drei Wege: Quandoo-Widget, WhatsApp und Telefon. Das Widget des externen Anbieters wird erst nach Einwilligung geladen.» → «Die Reservierungsseite zeigt drei Wege, alle mit Beispieldaten: WhatsApp, Telefon und einen Platzhalter für das Reservierungs-Widget von Quandoo. Wie bei einem echten Widget erscheint er erst nach Einwilligung.»
5. «14 Gerichten» → «14 Beispielgerichten»; «vollständige Restaurant-Website» → «vollständige Website für ein Konzept-Restaurant»
6. MEDIUM Закон 27 §7 «ihr Gesamtgewicht sank von 48,8 MB auf 1,2 MB» → «Die Bilder habe ich vor der Veröffentlichung komprimiert.»
7. MEDIUM «Alkoholische Getränke tragen einen Hinweis „ab 16“» → «Bier und Radler tragen einen Hinweis „ab 16“.» (данные drinks.json уточнить отдельно: «Spezi mit Schuss» 4,0 % vol помечен «ab 16»)
8. LOW «Die Abfolge der Abschnitte folgt keinem Präsentationsschema.» → удалить
9. LOW «ab 1920 Pixel» → «mit 1920 Pixel Breite»

**provenly-homes**
1. CRITICAL «Provenly Homes hat einen vollständig neu gebauten Auftritt … erhalten, veröffentlicht auf GitHub Pages», «Der bisherige Auftritt lief auf Framer» → «Der Auftritt des Unternehmens läuft auf Framer.» и «Entstanden ist ein vollständig neu gebauter Auftritt mit 20 Seitenrouten, veröffentlicht als Vorschau auf GitHub Pages.»
2. CRITICAL абзац «Bei der Bestandsaufnahme fielen mehrere Mängel auf: … kein Cookie-Hinweis.» → удалить целиком, оставить «Ziel war ein neu gebauter Auftritt mit aufwendigen Animationen, der die vorhandenen Inhalte vollständig übernimmt: Leistungen, drei Pakete, Referenzobjekte, Kundenstimmen, FAQ und den Ratgeber.»; убрать «die Tippfehler bereinigt»; «der Cookie-Hinweis ist vorhanden» → «ein Cookie-Hinweis ist eingebaut»
3. MEDIUM «Alle 39 im Designplan festgelegten Effekte sind umgesetzt» → удалить; оставить «Die Effekte laufen auf dem Smartphone teils in einer eigenen mobilen Fassung.»
4. LOW «auf Awwwards-Niveau» → входит в п.2

**rundumshaus**
1. MEDIUM цифры Search Console (5→46, 163) → удалить предложение «Nach dem Start der Ortsseiten stieg … bei 163.»
2. LOW «2026 folgte ein Redesign» → «Im Sommer 2026 folgte ein Redesign»
3. LOW «Die Domain rundumshaus-littawe.de war bereits registriert.» → удалить
4. LOW «Schema.org-Daten mit den Google-Bewertungen» → «Schema.org-Daten»

**silkekleinart**
1. MEDIUM Lighthouse 98/97/100 → удалить предложение
2. LOW «Für eine Künstlerin ohne technischen Hintergrund … immer wieder durcheinander» → «Ohne technisches Vorwissen war das schwer zu pflegen, besonders die Seite mit den Ausstellungen geriet dabei durcheinander.»

**sorrysara**
1. HIGH «die gesetzlich geforderte Umrechnung in Lewa übernimmt ein Skript mit festem Kurs» → «Preise gibt sie in Euro ein.»
2. MEDIUM «Tickets verkauft die Seite über Stripe im Live-Betrieb» → «Der Ticketkauf ist über Stripe im Live-Modus angebunden, Rückerstattungen eingeschlossen.»
3. LOW «Inhaberin» → подтвердить у CEO (в CLAUDE.md «заказчик Hanna»)

**staskiewitz**
1. HIGH «Der bisherige Auftritt lief als ePages-Shop», «Jede alte Adresse leitet per 301 auf die passende neue Seite weiter.» → «Der bisherige Auftritt ist ein ePages-Shop.» и «Für jede Adresse des alten Shops ist eine 301-Weiterleitung auf die passende neue Seite hinterlegt.»
2. MEDIUM разбивка старого магазина (133/33/25) рядом с 126/30/26 → удалить разбивку старого; после «126 Produkte in 30 Kategorien» добавить «Einzelne Artikel hat die Imkerei bewusst nicht übernehmen lassen.» (`STATUS.md:93`)
3. LOW «für Besucher geöffnet» → «Der Shop ist unter thecrazybee.de online.»

**stormguard-v2**
1. HIGH оба предложения про BORICA удалить; «mit Schnellansicht und Warenkorb-Schublade» → «mit Schnellansicht»
2. HIGH /de/impressum.html отдаёт 404 вживую → решение CEO: придержать кейс или без ссылки на /de/
3. LOW «Änderungen sind nach jedem Deployment sofort beim Besucher sichtbar, weil …» → оставить «Die Inhalte bleiben auch ohne JavaScript sichtbar.»

**taxi-moennigmann**
1. HIGH «Beim Inklusionstaxi ist der Betrieb in der Region allein» → «Unter den neun Wettbewerbern aus Leer und Ostfriesland, die ich vorab ausgewertet habe, bot keiner ein Inklusionstaxi an. Diese Stärke sollte die neue Website klar zeigen.»; повтор про девять конкурентов в Umsetzung удалить
2. LOW «Das Impressum erfüllt § 5 DDG vollständig.» → «Das Impressum enthält alle Angaben nach § 5 DDG.»

## Вопрос 6
- RundUmsHaus, Search Console 5→46/163 — недопустимо (служебный показатель, снимок до редизайна, 163 из 617 бьёт по нам) → удалить
- SilkeKleinArt, Lighthouse 98/97/100 — недопустимо (Закон 27 §7, стейджинг, конфигурации больше нет, один прогон) → удалить

## Сквозное
- Сито: проверять строку выдержки; шаблоны `Server in`, `erfüllt`, `allein|einzig`, `Lighthouse`, `\d+[,.]?\d* MB`, `indexiert`, `live`
- `data/projects.json` как источник замыкает круг (sorrysara, staskiewitz, taxi, elektrocheck, silke)
- `CASE_TEXT_RULES.md`: раздел «Technik» не соответствует трём разделам JSON
- KONTUR: на kontur.ais152.com нужна видимая плашка «Konzeptprojekt – keine echten Bestellungen»
- после правок — сито на 300+ слов (ближе к порогу provenly-homes, taxi-moennigmann)
