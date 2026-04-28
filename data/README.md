# Projects — how to add a new one in 30 seconds

This folder is the **source of truth** for the Selected Work section. Adding a new project = 1 JSON entry + 2 screenshots. **No HTML/CSS/JS edits required.**

## 1. Take screenshots

Open the live site in a desktop browser and take two screenshots of the homepage / hero:

| File | Size | Format | Max weight |
|------|------|--------|-----------|
| `assets/projects/{slug}.jpg`     | 1280 × 800  | JPG quality 85 | ≤ 200 KB |
| `assets/projects/{slug}@2x.jpg`  | 2560 × 1600 | JPG quality 85 | ≤ 600 KB |

If you don't have time to make a 2x screenshot, just reuse the 1x path for both fields. Retina screens will look softer but the layout still works.

> Tip: there's a `scripts/screenshots.mjs` Puppeteer script in the repo if you have many to do at once.

## 2. Add the JSON entry

Open `projects.json` and append an object to the array. Schema is in `projects.schema.json`. Validate at <https://www.jsonschemavalidator.net/> if unsure.

Minimal required fields:

```json
{
  "slug": "new-project",
  "title": "New Project",
  "tagline_en": "One line in English",
  "tagline_de": "Eine Zeile auf Deutsch",
  "year": 2026,
  "url": "https://example.com",
  "status": "live",
  "tags": ["Landing", "Static"],
  "summary_en": "Short description (≤ 200 chars).",
  "summary_de": "Kurze Beschreibung (≤ 200 Zeichen).",
  "screenshot": "assets/projects/new-project.jpg",
  "screenshot_2x": "assets/projects/new-project@2x.jpg",
  "featured": false,
  "order": 9
}
```

### Field reference

| Field | Type | Notes |
|-------|------|-------|
| `slug` | string | kebab-case, 2-40 chars, URL-safe |
| `title` | string | ≤ 60 chars |
| `tagline_en` / `tagline_de` | string | ≤ 80 chars each, shown under title |
| `year` | int | 2020-2030 |
| `url` | string | live URL, or `"#"` if no public URL |
| `status` | enum | `live` · `in-development` · `archived` |
| `tags` | string[] | 1-6 items, each ≤ 24 chars |
| `summary_en` / `summary_de` | string | ≤ 280 chars each |
| `screenshot` | string | path to 1x JPG |
| `screenshot_2x` | string | path to 2x JPG (optional) |
| `featured` | bool | reserved for future "highlights" filter |
| `order` | int | sort key, lowest = first in section |

## 3. Commit + push

```bash
git add data/projects.json assets/projects/
git commit -m "feat(projects): add {slug}"
git push
```

GitHub Pages rebuilds in ~2 minutes. **No HTML or CSS to touch.** The card renders automatically via `assets/js/projects.js`.

## 4. Removing a project

Two options:
- **Hide it:** set `"status": "archived"`. It stays in JSON for history but is not rendered.
- **Delete it:** remove the JSON entry and the matching screenshots from `assets/projects/`.

## 5. Reordering

Change `order` values. Lowest number = first card. Re-numbering doesn't have to be contiguous (1, 2, 5, 7 works just fine).

---

## Troubleshooting

**"Could not load projects" message in the section.**
JSON is invalid. Open <https://jsonlint.com>, paste your file, fix the syntax error, push again.

**Card shows but image is broken.**
Check the `screenshot` path is relative to the repo root and the file exists in `assets/projects/`.

**Card status pill shows wrong color.**
`status` must be exactly one of: `live`, `in-development`, `archived`. Anything else falls through to default.

**Site cache shows old data.**
GitHub Pages caches up to 10 minutes. Wait, or hard-refresh (`Ctrl+Shift+R`).
