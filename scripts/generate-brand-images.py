#!/usr/bin/env python3
"""Generate og-image.jpg + apple-touch-icon.png for AiS1.52.

Output:
  assets/og-image.jpg          1200 x 630   (Open Graph share preview)
  assets/apple-touch-icon.png  180 x 180    (iOS Home Screen icon)

Run:
  python3 scripts/generate-brand-images.py
"""
from PIL import Image, ImageDraw, ImageFont
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets')

# Editorial Ink palette (must match assets/css/tokens.css)
BG     = (11, 14, 18)        # #0B0E12
TX     = (244, 239, 229)     # #F4EFE5
TX_MU  = (244, 239, 229)     # 0.62 alpha applied separately
AC     = (255, 106, 60)      # #FF6A3C — coral
LINK   = (125, 196, 255)     # #7DC4FF — sky

# Font candidates (first one that exists wins)
FONT_PATHS = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf',
    '/System/Library/Fonts/Helvetica.ttc',
    'C:/Windows/Fonts/arialbd.ttf',
    '/Library/Fonts/Arial Bold.ttf',
]
MONO_PATHS = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',
    '/usr/share/fonts/dejavu/DejaVuSansMono-Bold.ttf',
    '/System/Library/Fonts/Menlo.ttc',
    'C:/Windows/Fonts/consolab.ttf',
]


def find_font(paths, size):
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    print(f'[warn] no font found in {paths}, using default', file=sys.stderr)
    return ImageFont.load_default()


def make_og():
    W, H = 1200, 630
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img, 'RGBA')

    # Dot grid background, fading from center
    cx, cy = W / 2, H / 2
    max_dist = (cx ** 2 + cy ** 2) ** 0.5
    for y in range(0, H, 28):
        for x in range(0, W, 28):
            dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            fade = 1 - min(1, dist / max_dist) * 0.65
            alpha = int(34 * fade)
            d.rectangle([x - 1, y - 1, x + 1, y + 1],
                        fill=(244, 239, 229, alpha))

    # Soft coral glow blob top-right
    for r in range(380, 60, -20):
        a = int(2 + (380 - r) / 380 * 6)
        d.ellipse([W - 200 - r, -180 - r // 2, W - 200 + r, -180 + r],
                  fill=(255, 106, 60, a))

    # Soft sky glow bottom-left (subtle)
    for r in range(280, 40, -16):
        a = int(1 + (280 - r) / 280 * 4)
        d.ellipse([-160 - r, H - 60 - r // 2, -160 + r, H - 60 + r],
                  fill=(125, 196, 255, a))

    # Fonts
    f_huge = find_font(FONT_PATHS, 168)
    f_big = find_font(FONT_PATHS, 56)
    f_mid = find_font(FONT_PATHS, 38)
    f_small = find_font(MONO_PATHS, 22)

    PAD = 88

    # Wordmark "AiS" + small "1.52" version mark
    d.text((PAD, 142), 'AiS', font=f_huge, fill=TX)
    bbox = d.textbbox((PAD, 142), 'AiS', font=f_huge)
    ais_right = bbox[2]
    d.text((ais_right + 22, 232), '1.52', font=f_big, fill=AC)

    # Tagline (two lines)
    d.text((PAD, 352), 'Engineering AI systems', font=f_mid, fill=TX)
    d.text((PAD, 408), 'for teams that ship.', font=f_mid, fill=(244, 239, 229, 158))

    # Mono footer label
    d.text((PAD, 520), 'MUNICH · DE   /   AIS152.COM',
           font=f_small, fill=AC)

    # Brand accent strokes
    d.rectangle([0, 0, 8, 96], fill=AC)              # coral top-left tick
    d.rectangle([W - 96, H - 8, W, H], fill=TX)      # bone bottom-right tick
    d.rectangle([W - 96 - 16, H - 8, W - 96 - 8, H], fill=AC)

    out = os.path.join(OUT, 'og-image.jpg')
    img.save(out, 'JPEG', quality=88, optimize=True, progressive=True)
    print(f'[ok]  {out}  ({os.path.getsize(out) // 1024} KB)')


def make_apple_icon():
    S = 180
    img = Image.new('RGB', (S, S), BG)
    d = ImageDraw.Draw(img, 'RGBA')

    # Subtle dot grid (denser, smaller)
    for y in range(0, S, 14):
        for x in range(0, S, 14):
            d.rectangle([x, y, x, y], fill=(244, 239, 229, 28))

    # Coral top stripe
    d.rectangle([0, 0, S, 4], fill=AC)

    # Fonts
    f_main = find_font(FONT_PATHS, 76)
    f_ver = find_font(FONT_PATHS, 18)

    # Centered "AiS"
    text = 'AiS'
    bbox = d.textbbox((0, 0), text, font=f_main)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    d.text(((S - w) / 2 - bbox[0], (S - h) / 2 - bbox[1] - 12),
           text, font=f_main, fill=TX)

    # "1.52" under
    text2 = '1.52'
    bbox2 = d.textbbox((0, 0), text2, font=f_ver)
    w2 = bbox2[2] - bbox2[0]
    d.text(((S - w2) / 2 - bbox2[0], 132), text2, font=f_ver, fill=AC)

    out = os.path.join(OUT, 'apple-touch-icon.png')
    img.save(out, 'PNG', optimize=True)
    print(f'[ok]  {out}  ({os.path.getsize(out) // 1024} KB)')


if __name__ == '__main__':
    make_og()
    make_apple_icon()
    print('\nDone. Re-run after changing text or palette in this script.')
