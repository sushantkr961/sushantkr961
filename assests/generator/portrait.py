"""Convert the supplied photo into a character grid (ASCII portrait).

Usage:  python3 portrait.py /path/to/photo.png
Writes portrait.json (luminance grid) + portrait_preview.png beside this script.
NOTE: POLY below is a hand-traced silhouette for the current photo (896x1191).
A different photo needs a new outline.

Pipeline (PIL only):
  1. crop head + shoulders
  2. build a subject mask from local sharpness (subject sharp, background bokeh)
     + row/column span fill to close the silhouette
  3. luminance -> character ramp, sampled on a grid with 0.6 cell aspect
Outputs: rows (list of str) and a bucket grid (0..N) for opacity classes.
"""
from PIL import Image, ImageFilter, ImageOps, ImageChops, ImageDraw, ImageFont
import json, sys, os

S = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(S, "photo.png")  # pass the photo path; the photo is not committed

COLS, ROWS = 56, 44          # character grid
CELL_ASPECT = 0.6            # monospace glyph width / line height
RAMP = " .·:-=+*#%@"         # dark -> bright (dark theme: bright = dense)

POLY = [(300,170),(360,110),(430,95),(520,100),(590,130),(650,175),(690,230),(705,300),(700,370),
        (690,440),(670,500),(650,560),(620,600),(600,640),(600,700),(700,690),(800,730),(870,790),(896,850),
        (896,1191),(0,1191),(0,880),(60,800),(150,730),(250,680),(300,660),(240,620),(200,560),(195,480),
        (200,400),(195,330),(210,270),(240,210)]

def subject_mask(im, crop):
    """Hand-traced silhouette (photo coordinates) shifted into crop space, feathered."""
    ox, oy = crop[0], crop[1]
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).polygon([(x - ox, y - oy) for x, y in POLY], fill=255)
    return m.filter(ImageFilter.GaussianBlur(4))

def build(cols=COLS, rows=ROWS, crop=(110, 60, 790, 950)):
    im = Image.open(SRC).convert("RGB").crop(crop)
    mask = subject_mask(im, crop)
    g = ImageOps.grayscale(im)
    g = ImageOps.autocontrast(g, cutoff=1).point(lambda v: int(255*((v/255)**0.85)))
    # darken background using mask
    bg = Image.new("L", g.size, 0)
    lifted = g.point(lambda v: max(v, 46))   # shadow floor inside the subject so the silhouette always reads
    g = Image.composite(lifted, bg, mask)
    # sample: target aspect = cols*CELL_ASPECT : rows
    tw, th = cols, rows
    # fit crop into grid keeping aspect (cell aspect corrected)
    src_w, src_h = g.size
    src_ratio = src_w / src_h
    grid_ratio = (cols * CELL_ASPECT) / rows
    if src_ratio > grid_ratio:   # source wider -> crop sides
        nw = int(src_h * grid_ratio); off = (src_w - nw) // 2
        g = g.crop((off, 0, off + nw, src_h))
    else:                        # source taller -> crop top/bottom
        nh = int(src_w / grid_ratio); off = (src_h - nh) // 4
        g = g.crop((0, off, src_w, off + nh))
    small = g.resize((tw, th), Image.LANCZOS)
    small = ImageOps.autocontrast(small, cutoff=2)
    px = small.load()
    n = len(RAMP)
    lines, buckets = [], []
    for y in range(th):
        line, brow = "", []
        for x in range(tw):
            v = px[x, y]
            idx = min(n - 1, int(v / 256 * n))
            line += RAMP[idx]
            brow.append(min(3, int(v / 64)))
        lines.append(line); buckets.append([px[x, y] for x in range(tw)])
    return lines, buckets, small

def preview(lines, path):
    font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 12)
    cw, ch = 7.2, 12
    img = Image.new("RGB", (int(len(lines[0]) * cw) + 20, len(lines) * ch + 20), (8, 12, 24))
    d = ImageDraw.Draw(img)
    for i, l in enumerate(lines):
        d.text((10, 10 + i * ch), l, font=font, fill=(120, 220, 240))
    img.save(path)

if __name__ == "__main__":
    lines, buckets, small = build()
    print("\n".join(lines))
    preview(lines, os.path.join(S, "portrait_preview.png"))
    small.resize((small.width * 6, small.height * 6), Image.NEAREST).save(os.path.join(S, "portrait_small.png"))
    json.dump({"lines": lines, "lum": buckets}, open(os.path.join(S, "portrait.json"), "w"))
