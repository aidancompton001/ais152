# STATUS — AiS152

**Live:** https://ais152.com
**Production версия:** v2 (Editorial Ink, multi-asset)
**Last deploy:** 2026-04-28 (PX-006 — `c7c9496`)
**Откат-теги:** `v2-pre-px006` (`aa5b0dd`), `v2-pre-px005` (`576cc14`), `v2-pre-px004` (`22691c3`), `v1-pre-redesign` (`7568a39`)

## Текущая активная задача
— нет (последняя завершена: PX-006 «Speed is the moat» — реальные сроки 1h/24h/3d)

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
- **FORM-1** Web3Forms access key — placeholder в `assets/js/form.js`. Primary FormSubmit работает; fallback неактивен. Открывать PX по триггеру первого 429/500 от FormSubmit.
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
