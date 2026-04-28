# Fonts — DSGVO-safe self-hosting

> Loading fonts from `fonts.googleapis.com` is a [DSGVO violation in Germany](https://www.lg-muenchen-i.de/) (BGH 2022, LG München I, 20.01.2022, 3 O 17493/20). All font files must live in this folder and be served from the same origin as the site.

## Current state

The site ships with the **system font stack** as a fallback so it works immediately without any downloads. To get the real designed type, follow steps below.

## Step 1 — Download Mona Sans (primary, variable)

- Source: <https://github.com/github/mona-sans/releases> → latest release.
- License: SIL Open Font License 1.1 (free for commercial use).
- File needed:
  - `Mona-Sans.woff2` (variable font, weight 200-900, width 75-125, ~100 KB)
- Why Mona Sans: variable axes for **wght** and **wdth** lets us animate type weight and condensation on hover. Inter is fine but doesn't have variable width.

## Step 2 — Download JetBrains Mono (mono, code/labels)

- Source: <https://www.jetbrains.com/lp/mono/> → "Download JetBrains Mono" → unzip.
- License: SIL Open Font License 1.1.
- File needed:
  - `JetBrainsMono-Regular.woff2` (~30 KB)

## Step 3 — Drop the .woff2 files into this folder

Final tree:

```
assets/fonts/
├── README.md  (this file)
├── LICENSE-Mona-Sans.txt           ← copy from GitHub release
├── LICENSE-JetBrainsMono.txt       ← copy from JetBrains zip
├── Mona-Sans.woff2
└── JetBrainsMono-Regular.woff2
```

## Step 4 — Uncomment @font-face in `assets/css/tokens.css`

Open `assets/css/tokens.css`, find the block at the bottom labeled **"Mona Sans (variable, OFL — by GitHub)"**, and remove the `/* */` markers around the two `@font-face` rules.

## Step 5 — Verify

Open the site in a browser. DevTools → Network tab → filter "Font". You should see:
- `Mona-Sans.woff2` loaded from `ais152.com/assets/fonts/`
- `JetBrainsMono-Regular.woff2` loaded from same origin
- **Zero** requests to `fonts.googleapis.com` or `fonts.gstatic.com`

To confirm Mona Sans is actually rendering: hover over any heading. The weight should visibly thicken and the letters should slightly condense (this is the wght/wdth axis animation in `assets/css/components.css`).

---

## Optional — fallback to Inter

If you don't want Mona Sans, drop these instead:

- `Inter-Regular.woff2` (weight 400)
- `Inter-Medium.woff2` (weight 500)
- `Inter-SemiBold.woff2` (weight 600)
- `Inter-Bold.woff2` (weight 700)

Source: <https://rsms.me/inter/>. The variable font animation in components.css will simply be a no-op (Inter still looks great, just no on-hover thickening).

---

**Owner:** #14 Hans Landa signs off on this folder before any merge to `master`.
