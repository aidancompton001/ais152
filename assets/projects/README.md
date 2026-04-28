# Project screenshots

Each project in `data/projects.json` references a screenshot at `assets/projects/{slug}.jpg` (1x) and optionally `{slug}@2x.jpg` (retina).

For now, the JSON points to the **legacy paths** in `assets/` (e.g. `assets/stormguard-site.jpg`), so the site works out of the box. When you have time, migrate them:

```bash
# from repo root
mkdir -p assets/projects
mv assets/baupreis-dashboard.png    assets/projects/baupreis.jpg
mv assets/mono-app-1.jpg            assets/projects/mono.jpg
mv assets/edmi-landing-site.jpg     assets/projects/edmi.jpg
mv assets/stormguard-site.jpg       assets/projects/stormguard.jpg
mv assets/eko-oylis-site.jpg        assets/projects/eko-oylis.jpg
mv assets/rundumshaus-site.jpg      assets/projects/rundumshaus.jpg
mv assets/provenly-homes-site.jpg   assets/projects/provenly-homes.jpg
mv assets/studioglamour-site.jpg    assets/projects/studioglamour.jpg
```

Then update the `screenshot` paths in `data/projects.json` from `assets/{old}.jpg` to `assets/projects/{slug}.jpg`.

## Capturing new screenshots

Standard format:

| Variant | Resolution | Quality | Max weight |
|---------|-----------|---------|-----------|
| 1x      | 1280 × 800  | JPG 85 | ≤ 200 KB |
| 2x      | 2560 × 1600 | JPG 85 | ≤ 600 KB |

Auto-capture script using Puppeteer (already in repo, see `scripts/screenshots.mjs` if it exists) or run manually:

```bash
npx puppeteer screenshot https://example.com \
  --viewport 1280x800 --type jpeg --quality 85 \
  --output assets/projects/example.jpg
```

For the @2x version, capture at 2560×1600 and save as `{slug}@2x.jpg`.
