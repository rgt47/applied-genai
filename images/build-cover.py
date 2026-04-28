#!/usr/bin/env python3
"""
Build a cover image for Applied Generative AI for Public
Health and Biostatistics, in the visual idiom of the
Springer Texts in Statistics series: two-zone composition
with a watercolour-painted top zone and a solid bottom zone,
clean sans-serif typography.

Differs from the SCAI, advanced, and practicum covers only
in palette: anchored on the applied-genai book's brand
ochre #a06a1f with warm bronze, amber, and cream accents.

Usage:
    python3 build-cover.py
Output:
    cover.png   (1200 x 1800, the book cover)
"""

import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# --- canvas ---------------------------------------------------------------

W, H        = 1200, 1800
SPLIT_Y     = int(H * 0.36)

# --- colours --------------------------------------------------------------

# brand ochre anchors the bottom zone
OCHRE       = (160, 106, 31)        # #a06a1f
OCHRE_DEEP  = (96, 60, 18)          # darker ochre / dark bronze
CREAM       = (248, 244, 233)
GOLD        = (220, 158, 70)
INK         = (45, 55, 72)
WHITE       = (255, 255, 255)

# top-zone watercolour palette: deep umber through bronze
# into warm ochre, amber, and pale cream. complementary to
# the brand ochre and visibly distinct from the practicum
# (teal-violet-coral), SCAI (navy-indigo-amber), and SCAI-
# advanced (burgundy-plum-rose-amber) covers.
WATERCOLOUR = [
    (60,  38,  18),    # deep umber
    (105, 65,  25),    # warm bronze
    (160, 106, 31),    # ochre (brand)
    (220, 158, 70),    # warm amber
    (240, 220, 180),   # pale cream
]

# --- helpers --------------------------------------------------------------

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def palette_at(t, palette=WATERCOLOUR):
    n = len(palette) - 1
    pos = t * n
    i   = int(pos)
    if i >= n:
        return palette[-1]
    return lerp(palette[i], palette[i + 1], pos - i)


def watercolour_zone(width, height, seed=37):
    """
    Build a soft watercolour-style gradient by drawing many
    overlapping radial blobs across the canvas.
    """
    rng  = random.Random(seed)
    base = Image.new('RGB', (width, height), (240, 240, 240))
    px   = base.load()

    for y in range(height):
        for x in range(width):
            t = (x / width * 0.55 + y / height * 0.45)
            t = max(0.0, min(1.0, t))
            px[x, y] = palette_at(t)

    overlay = Image.new('RGB', (width, height), (0, 0, 0))
    odraw   = ImageDraw.Draw(overlay)
    mask    = Image.new('L', (width, height), 0)
    mdraw   = ImageDraw.Draw(mask)

    for _ in range(28):
        cx = rng.randint(-100, width + 100)
        cy = rng.randint(-50, height + 50)
        r  = rng.randint(180, 480)
        col = palette_at(rng.uniform(0, 1))
        odraw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)
        mdraw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=70)

    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=120))
    mask    = mask.filter(ImageFilter.GaussianBlur(radius=80))
    base    = Image.composite(overlay, base, mask)

    base    = base.filter(ImageFilter.GaussianBlur(radius=2))
    return base


def add_paper_grain(img, strength=8, seed=11):
    rng    = random.Random(seed)
    grain  = Image.new('L', img.size, 128)
    gpx    = grain.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            gpx[x, y] = max(
                0, min(255, 128 + rng.randint(-strength, strength))
            )
    grain = grain.filter(ImageFilter.GaussianBlur(radius=0.5))
    img.paste(Image.blend(
        img.convert('RGB'),
        Image.merge('RGB', (grain, grain, grain)),
        0.05,
    ))
    return img


def font(name, size):
    candidates = {
        'avenir-medium':   ('/System/Library/Fonts/Avenir.ttc', 2),
        'avenir-heavy':    ('/System/Library/Fonts/Avenir.ttc', 6),
        'avenir-black':    ('/System/Library/Fonts/Avenir.ttc', 7),
        'avenir-book':     ('/System/Library/Fonts/Avenir.ttc', 1),
        'avenir-light':    ('/System/Library/Fonts/Avenir.ttc', 0),
        'helvetica-bold':  ('/System/Library/Fonts/Helvetica.ttc', 1),
        'helvetica':       ('/System/Library/Fonts/Helvetica.ttc', 0),
    }
    path, idx = candidates[name]
    return ImageFont.truetype(path, size, index=idx)


def draw_text(draw, xy, text, fnt, fill, anchor='lt'):
    draw.text(xy, text, font=fnt, fill=fill, anchor=anchor)


# --- build ---------------------------------------------------------------

def build():
    canvas = Image.new('RGB', (W, H), OCHRE)

    top = watercolour_zone(W, SPLIT_Y, seed=37)
    canvas.paste(top, (0, 0))

    draw = ImageDraw.Draw(canvas)

    # cream hairline divider
    draw.rectangle((0, SPLIT_Y, W, SPLIT_Y + 3), fill=CREAM)

    # left-edge spine accent
    draw.rectangle((0, 0, 14, SPLIT_Y), fill=OCHRE_DEEP)
    draw.rectangle((14, 0, 17, SPLIT_Y), fill=CREAM)

    # --- top-zone typography ---------------------------------------------
    series_fnt = font('avenir-heavy', 36)
    draw_text(draw, (60, 90),
              'GRADUATE BIOSTATISTICS SERIES',
              series_fnt, WHITE)

    author_fnt = font('avenir-medium', 64)
    authors = ['rgtlab Curriculum Project']
    y = 240
    for line in authors:
        draw_text(draw, (60, y), line, author_fnt, WHITE)
        y += 76

    # --- bottom-zone typography ------------------------------------------
    title_fnt   = font('avenir-black', 100)
    title_lines = ['Applied',
                   'Generative AI',
                   'for Health',
                   'Sciences Research']
    y = SPLIT_Y + 80
    for line in title_lines:
        draw_text(draw, (60, y), line, title_fnt, WHITE)
        y += 116

    sub_fnt = font('avenir-medium', 46)
    y += 20
    for line in ['A graduate textbook']:
        draw_text(draw, (62, y), line, sub_fnt, CREAM)
        y += 60

    edition_fnt  = font('avenir-light', 42)
    edition_text = 'First Edition  ·  2026'
    draw_text(draw, (60, H - 180), edition_text, edition_fnt,
              CREAM)

    mark_fnt = font('avenir-heavy', 44)
    draw_text(draw, (W - 60, H - 80), 'rgtlab', mark_fnt, WHITE,
              anchor='rs')
    draw.rectangle((W - 240, H - 64, W - 60, H - 60), fill=GOLD)

    canvas = add_paper_grain(canvas)
    return canvas


if __name__ == '__main__':
    img = build()
    out = 'cover.png'
    img.save(out, optimize=True)
    print(f'wrote {out} ({img.size[0]} x {img.size[1]})')
