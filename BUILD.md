# AiS152 — Build & Deploy guide

> Read this once. Then you're done.

This is a static site. Zero build step. Open `index.html` directly in a browser → it works. Push to `master` → GitHub Pages updates within ~2 minutes.

## File map

```
.
├── index.html              ← main page (start here when editing layout)
├── impressum.html          ← legal § 5 TMG
├── datenschutz.html        ← DSGVO Art. 13
├── 404.html                ← GitHub Pages 404 fallback
├── CNAME                   ← maps ais152.com (DO NOT TOUCH)
│
├── data/
│   ├── projects.json       ← source of truth for Selected Work
│   ├── projects.schema.json
│   └── README.md           ← "how to add a project in 30 seconds"
│
├── assets/
│   ├── css/
│   │   ├── tokens.css      ← design tokens (colors, type, spacing, motion)
│   │   ├── base.css        ← reset + typography + lang switching
│   │   ├── layout.css      ← header, sections, footer, responsive
│   │   ├── components.css  ← buttons, cards, forms, FAB, modal
│   │   └── motion.css      ← reveal classes + reduced-motion fallback
│   ├── js/
│   │   ├── lang.js         ← EN/DE switcher (loads first, no GSAP dep)
│   │   ├── projects.js     ← renders cards from projects.json
│   │   ├── form.js         ← FormSubmit + Web3Forms fallback
│   │   ├── whatsapp.js     ← DSGVO 2-click WhatsApp opener
│   │   └── main.js         ← Lenis + GSAP timelines + magnetic + counters
│   ├── fonts/
│   │   └── README.md       ← how to self-host Inter + JetBrains Mono
│   ├── projects/
│   │   └── README.md       ← screenshot specs
│   ├── favicon.svg
│   └── (legacy *-site.jpg screenshots — referenced by projects.json)
│
├── BUILD.md                ← this file
├── CLAUDE.md               ← project rules for Claude agents
├── TEAM.md                 ← team roster
└── docs/tasks/             ← roadmap files (PX-001, PX-002a)
```

## Open the site locally

```bash
# any static server works — pick one
npx serve .              # https://www.npmjs.com/package/serve
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

> Don't open `file://...` directly — `fetch('data/projects.json')` will fail with a CORS error on `file://` schemes. You need a real HTTP server.

## Deploy

Already configured: GitHub Pages on `master` branch with `CNAME` → `ais152.com`.

```bash
git add .
git commit -m "feat: redesign — engineering-grade portfolio"
git push origin master
```

Wait ~2 minutes. Visit <https://ais152.com>.

> GitHub Pages caches assets up to 10 minutes. After a deploy, all CSS/JS files are query-stringed with `?v=2026-04-27` to bust the cache. **When you change a CSS or JS file, bump the version string in `index.html`** (or generate a git short-hash, see "Cache busting" below).

## Cache busting (recommended)

After every deploy, swap the `?v=...` strings in `index.html` for the current git short-hash:

```bash
# automated way (one-liner)
HASH=$(git rev-parse --short HEAD)
sed -i.bak "s/?v=[a-zA-Z0-9-]*/?v=$HASH/g" index.html impressum.html datenschutz.html
rm index.html.bak impressum.html.bak datenschutz.html.bak
git add . && git commit -m "chore: cache-bust to $HASH" && git push
```

## Configuring the contact form

1. **FormSubmit (primary).** First time the form is submitted, FormSubmit will email `ebaias.muc@gmail.com` asking the CEO to confirm. Click the confirmation link once. After that, all future submissions arrive directly in the inbox.
2. **Web3Forms (fallback).** Optional but recommended — gives 2nd provider in case FormSubmit hits its 50-submissions/month free limit.
   - Sign up at <https://web3forms.com> (free, no credit card)
   - Copy the Access Key
   - Open `assets/js/form.js`
   - Replace `'YOUR_WEB3FORMS_ACCESS_KEY'` with the real key

## Configuring fonts (DSGVO requirement)

The site currently runs on the system font stack (works fine, but Inter is sharper). To upgrade:

→ See `assets/fonts/README.md` for the 5-step download + uncomment process.

## Adding a new project

→ See `data/README.md`. TL;DR: 1 JSON entry + 2 screenshots + push.

## Replacing legal placeholders

Open `impressum.html` and `datenschutz.html`. Search for `[TODO CEO]` and `[Vollständiger Name]` markers. Fill in real address + name + USt info before going live publicly.

## Quality gate before merging to master

Run through this checklist before each significant deploy:

- [ ] Open in Chrome at 1440px width — all sections render correctly
- [ ] Open in Chrome DevTools → toggle device → iPhone 14 — mobile layout works
- [ ] Click Lang toggle — all text switches EN ↔ DE
- [ ] Click WhatsApp FAB — DSGVO modal appears, then `wa.me/` link opens
- [ ] Submit a test form — receive email at `ebaias.muc@gmail.com`
- [ ] Run Lighthouse mobile — Performance ≥ 90, A11y ≥ 95, BP = 100, SEO ≥ 90
- [ ] Disable JS in DevTools — page still renders, links still work, no JS errors
- [ ] Enable `prefers-reduced-motion: reduce` — all animations skip, projects stack vertically
- [ ] Check Network tab — **zero** requests to `fonts.googleapis.com` or `fonts.gstatic.com`

## Rollback

```bash
git revert HEAD
git push
```

Or check old `index.html` version in git history — the previous single-file version is preserved as `archive/index_v1.html` if you saved it before the redesign.

## Architecture decisions

- **Static HTML, no build step.** Stack constraint from the project — GitHub Pages requires it, and zero build = zero things to break.
- **Multi-file, not single-file.** Override of the previous "one file rule" in CLAUDE.md, applies only to this redesign per CEO directive 2026-04-27. Rationale: 1056 lines of inline CSS+JS+HTML in one file is unmaintainable, multi-file lets the CEO edit one concern at a time.
- **Lenis + GSAP via CDN, not self-hosted.** Reduces page weight (CDN caching across sites), simplifies updates. Trade-off: tiny GDPR exposure for IP being sent to Cloudflare. Documented in `datenschutz.html` § 2.6.
- **System fonts as default.** DSGVO-safe out of the box. Optional upgrade to Inter+JetBrains Mono via `assets/fonts/README.md`.
- **No analytics.** Zero cookies, no banner needed. If you add analytics later, `datenschutz.html` § 4 must be updated and a cookie-consent banner added.
