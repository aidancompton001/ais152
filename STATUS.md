# STATUS — AiS152

**Live:** https://ais152.com
**Production версия:** v2 (Editorial Ink, multi-asset)
**Last deploy:** 2026-04-28 (PX-010 — `cdf6fa7` + verification file `b42b433`)
**Откат-теги:** `v2-pre-px010` (`01e3e5f`), `v2-pre-px008` (`7aeb689`), `v2-pre-px007` (`658175e`), `v2-pre-px006` (`aa5b0dd`), `v2-pre-px005` (`576cc14`), `v2-pre-px004` (`22691c3`), `v1-pre-redesign` (`7568a39`)

## SEO infrastructure (PX-010)
- ✅ `/robots.txt` (Allow + Sitemap directive)
- ✅ `/sitemap.xml` (1 URL + 3 hreflang alternates)
- ✅ `/favicon.ico` (multi-res 16/32/48/64 для Bing legacy)
- ✅ `/apple-touch-icon.png` (root для iOS pings)
- ✅ Hreflang en/de/x-default на index, de+x-default на impressum/datenschutz
- ✅ JSON-LD @graph: Person + ProfessionalService + WebSite (linked via @id refs)
- ✅ canonical на всех 4 страницах
- ✅ 404.html: meta description + canonical + noindex,follow

## CEO actions
- ✅ **SC-1** Google Search Console — **DONE 2026-04-28**: verification HTML-file (`google9d7cbb1b47be4897.html`) live + Ownership verified + Sitemap submitted + URL Inspection → Request Indexing added to priority queue. Coverage check expected 2026-04-30 → 2026-05-01.
- 🟡 **LH-1** Lighthouse mobile/desktop run → закинуть числа в STATUS (Perf/A11y/BP/SEO)
- 🟡 **BING-1** Bing Webmaster Tools — import+verify ✅ + URL Submission ✅ DONE 2026-04-28; pending optional: Sitemap submit в Bing UI (но GSC import уже передал sitemap reference)
- 🟡 **IDX-1** (новый) проверить Coverage report в Search Console через 2-7 дней; если 0 indexed — диагностика

## Текущая активная задача
— нет (последняя завершена: PX-008 marquee infinite + stats 3d + form activation)

## ✅ Resolved (PX-008)
- **FormSubmit активирован** CEO 2026-04-28 (Activate-link clicked, endpoint verified live `success:true`)
- Marquee теперь infinite loop (cloned content)
- Stats counter синхронен с PX-006 (3d)
- Form fallback с 3 graceful CTA (mailto + WhatsApp + Telegram)

## Brand-сообщение (PX-006)
- Process: «Hour. Day. Days.» — Reply 1h / Concept 24h / Live 3d / Maintain +30d
- Disclaimer: business hours Mon-Fri 09-19 CET; landings & MVPs only (complex SaaS quoted separately)
- Hero meta «Response < 1h»
- Terminal process.md = «# Speed is the moat»

## Состав портфолио (PX-005, 8 проектов в порядке CEO)
1. BauPreis AI SaaS *(featured)* — https://baupreis.ais152.com
2. EKO-OYLIS UA — https://eko.ais152.com/en/
3. Rund ums Haus Littawe — https://rundumshaus-littawe.de
4. StormGuard Professional V2 — https://www.stormguardprofessional.eu/
5. EDMI — https://aidancompton001.github.io/edmi-landing/variant-d.html
6. Provenly Homes — https://aidancompton001.github.io/provenly-homes/
7. Studio of Glamour — https://glamour.ais152.com/
8. YY-DGUV Prüfservice — https://aidancompton001.github.io/yy-dguv/

## Open issues / TODO
- **FORM-1** Web3Forms access key — placeholder. Primary FormSubmit ✅ активирован (PX-008). Web3Forms fallback всё ещё неактивен. Триггер: первый 429/500 от FormSubmit.
- **LH-1** Lighthouse baseline mobile — не снят (PX-002a Open Q #1). Отдельная PX-004.
- **LEGAL-1** impressum.html — содержит `[TODO CEO]` плейсхолдеры (полное имя, адрес, USt/Kleinunternehmer). До широкой публикации.
- **I18N-1** impressum/datenschutz — DE only. EN-перевод желателен для иностранных лидов (отдельная PX по решению CEO).
- **OG-1** `assets/og-image.jpg` — auto-generated через `scripts/generate-brand-images.py`. CEO может заменить на кастомный.

## Что в продакшене
- 4 страницы: index, impressum (DE), datenschutz (DE), 404 (EN)
- 8 проектов в Selected Work из `data/projects.json`
- Mona Sans variable + JetBrains Mono self-hosted (DSGVO)
- WhatsApp FAB → `wa.me/4915563675772` (DSGVO 2-click)
- Form: FormSubmit.co primary → `ebaias.muc@gmail.com`
- Languages: EN/DE toggle на index

## Документы
- `BUILD.md` — deploy guide
- `CLAUDE.md` — правила для Claude-агентов
- `TEAM.md` — состав команды
- `DEVLOG.md` — журнал разработки (S001..S005)
- `docs/tasks/PX_REGISTRY.md` — реестр PX-задач
- `docs/tasks/PX-002a_audit_and_roadmap.md` — аудит и roadmap
