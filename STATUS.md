# STATUS — AiS152

**Live:** https://ais152.com
**Production версия:** v2 (Editorial Ink, multi-asset)
**Last deploy:** 2026-04-28 (PX-003)
**Откат-тег:** `v1-pre-redesign` (`7568a39`) — `git checkout v1-pre-redesign && git push -f origin v1-pre-redesign:master` для роллбэка

## Текущая активная задача
— нет (последняя завершена: PX-003 deploy v2)

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
