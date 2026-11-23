"""Draws THE WORLD REPORT for 22 November 2026 and saves it as entry.png."""

import random

from PIL import Image, ImageDraw, ImageFont

from data import BRIEFS, DAY, LEADS, MAP_PINS, PANELS, SOURCES

W = H = 1024
PAPER = (247, 243, 234)
INK = (18, 18, 22)
RED = (176, 32, 38)
GREY = (104, 100, 96)
RULE = (196, 188, 176)
MARGIN = 26
OFF = {"mast_x": 0, "mast_y": -5, "strap_dy": -2, "lead_dy": 0, "small_dy": -9,
       "wide_dy": -6, "map_dx": 0, "map_dy": 0, "brief_dx": 0, "brief_dy": -6,
       "kicker_dy": -1, "head_dy": -1, "detail_dy": 0}
MAP_FILL = (226, 231, 232)
FRAME = (150, 143, 132)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


# --------------------------------------------------------------------------- fonts

def _font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return None


def _load(size):
    """Serif bold/regular with the DejaVuSans pair as fallback, then the bitmap font."""
    for bold_path, plain_path in ((SERIF_BOLD, SERIF), (SANS_BOLD, SANS)):
        bold = _font(bold_path, size)
        plain = _font(plain_path, size)
        if bold is not None and plain is not None:
            return bold, plain
    try:
        bitmap = ImageFont.load_default(size)
    except TypeError:  # older Pillow: fixed-size bitmap font
        bitmap = ImageFont.load_default()
    return bitmap, bitmap


# --------------------------------------------------------------------------- text

def _wrap(draw, text, font, width):
    """Greedy word wrap by draw.textlength; never splits a word."""
    words = text.split()
    if not words:
        return []
    lines = []
    line = words[0]
    for word in words[1:]:
        trial = line + " " + word
        if draw.textlength(trial, font=font) <= width:
            line = trial
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return lines


def _fit(draw, text, font, width, max_lines):
    """Wrap to at most max_lines; shortens (and marks) only if it would overflow."""
    lines = _wrap(draw, text, font, width)
    if len(lines) <= max_lines:
        return lines
    kept = lines[:max_lines]
    last = kept[-1]
    while last and draw.textlength(last + " ...", font=font) > width:
        last = last[:-1]
    kept[-1] = last.rstrip(" ,;:.") + " ..."
    return kept


def _para(draw, xy, lines, font, fill, step):
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += step
    return y


# --------------------------------------------------------------------------- illustrations

def _illo(img, box, kind, seed):
    """Flat vignette on its own scratch canvas of the box size, pasted at box origin."""
    x0, y0, x1, y1 = box
    bw, bh = max(1, x1 - x0), max(1, y1 - y0)
    tile = Image.new("RGB", (bw, bh), PAPER if kind in ("exam", "arrest", "port") else (232, 226, 214))
    d = ImageDraw.Draw(tile)
    rng = random.Random(seed)
    horizon = int(bh * 0.62)
    cx = bw // 2

    if kind == "cop":
        d.rectangle((3, 5, bw // 3 - 2, horizon), fill=(206, 199, 186))
        d.rectangle((bw // 3, 2, 2 * bw // 3 - 1, horizon), fill=(206, 199, 186))
        d.rectangle((2 * bw // 3, 7, bw - 6, horizon), fill=(206, 199, 186))
        d.ellipse((int(bw * 0.52), 6, int(bw * 0.78), int(bh * 0.42)), fill=(210, 108, 74))
        d.rectangle((3, horizon, bw - 4, bh - 2), fill=(206, 199, 186))
        d.rectangle((4, horizon - 34, bw // 2 - 6, horizon - 1), fill=(62, 74, 78))
        d.rectangle((int(bw * 0.55), horizon - 34, bw - 5, horizon - 1), fill=(62, 74, 78))
        d.rectangle((bw // 2 - 1, 0, bw // 2, bh - 1), fill=RED)

    elif kind == "tanker":
        d.rectangle((3, horizon, bw - 4, bh - 2), fill=(38, 92, 120))
        d.ellipse((int(bw * 0.55), 12, min(bw - 6, int(bw * 0.78)), int(bh * 0.5)), fill=(232, 168, 74))
        d.polygon([(bw // 3, horizon + 1), (bw - 6, horizon + 1), (bw // 3, horizon - 10)], fill=(44, 44, 50))
        d.rectangle((int(bw * 0.22), horizon - 30, int(bw * 0.28), horizon - 1), fill=(44, 44, 50))
        d.rectangle((int(bw * 0.30), horizon - 22, int(bw * 0.38), horizon - 1), fill=(44, 44, 50))
        for i in range(9):
            r = 4 + (i % 3) * 2
            ex = int(bw * 0.45) - i * 5 + rng.randint(-2, 2)
            ey = 14 + i * 4 + rng.randint(-2, 2)
            d.ellipse((ex - r, ey - r, ex + r, ey + r), fill=(84, 84, 92))

    elif kind == "drone":
        d.rectangle((3, 4, bw - 4, horizon), fill=(232, 226, 214))
        d.rectangle((3, horizon, bw - 4, bh - 2), fill=(28, 62, 96))
        d.polygon([(4, horizon + 1), (bw - 5, horizon + 1),
                   (bw - 12, bh - 3), (10, bh - 3)], fill=(56, 58, 64))
        d.rectangle((int(bw * 0.30), horizon - 8, bw - 26, bh - 12), fill=(56, 58, 64))
        d.ellipse((40, 18, 56, 30), fill=(70, 72, 80))
        d.rectangle((47, 24, 49, horizon - 2), fill=(120, 120, 128))
        d.rectangle((int(bw * 0.40), horizon + 6, int(bw * 0.55), horizon + 10), fill=(190, 186, 178))

    elif kind == "rubble":
        d.rectangle((3, 3, bw - 4, 12), fill=(232, 226, 214))
        d.rectangle((3, 13, bw - 4, horizon), fill=(96, 90, 82))
        d.polygon([(3, bh - 3), (3, horizon), (bw // 3, bh // 2),
                   (2 * bw // 3, horizon + 6), (bw - 4, bh - 20), (bw - 4, bh - 3)], fill=(118, 110, 100))
        for i in range(6):
            bx = 6 + i * 6 + rng.randint(0, 2)
            by = bh - 6 - (i % 3) * 3
            d.rectangle((bx, by, bx + 5, by + 4), fill=(142, 134, 122))

    elif kind == "sudan":
        d.rectangle((3, 3, bw - 20, horizon - 1), fill=(214, 96, 42))
        d.polygon([(bw - 21, 3), (bw - 4, 3), (bw - 4, 20)], fill=(232, 226, 214))
        d.rectangle((3, horizon, bw - 4, bh - 2), fill=(120, 106, 88))

    elif kind == "capitol":
        d.rectangle((3, 3, bw - 4, horizon), fill=(232, 226, 214))
        d.ellipse((cx - 12, 3, cx + 12, 16), fill=(70, 72, 78))
        d.rectangle((cx - 1, 10, cx, horizon - 1), fill=(60, 60, 66))
        d.rectangle((5, horizon - 16, bw - 6, horizon - 1), fill=(120, 100, 74))
        for i in range(5):
            x = 8 + i * 7
            d.rectangle((x, horizon - 13, x + 2, horizon - 4), fill=(232, 226, 214))
        d.rectangle((3, horizon, bw - 4, bh - 2), fill=(150, 128, 96))

    elif kind == "fire":
        d.rectangle((4, 10, bw - 5, 14), fill=(226, 222, 212))
        d.rectangle((4, 15, bw - 5, bh - 16), fill=(178, 174, 164))
        d.ellipse((8, bh - 22, 20, bh - 8), fill=(176, 32, 38))
        d.ellipse((22, bh - 26, 38, bh - 7), fill=(214, 96, 42))
        d.rectangle((4, bh - 15, bw - 5, bh - 4), fill=(150, 144, 132))

    elif kind == "knesset":
        d.rectangle((3, 3, bw - 4, 10), fill=(232, 226, 214))
        d.ellipse((cx - 14, 6, cx + 14, 17), fill=(210, 206, 196))
        d.rectangle((cx - 15, 16, cx + 15, 22), fill=(232, 228, 218))
        d.rectangle((cx - 14, 21, cx + 14, horizon - 1), fill=(186, 182, 172))
        d.rectangle((3, horizon, bw - 4, bh - 2), fill=(146, 150, 140))

    elif kind == "factory":
        d.rectangle((3, horizon, bw - 4, bh - 2), fill=(126, 120, 110))
        for i in range(3):
            x = 3 + i * 13
            d.rectangle((x, horizon - 18, x + 9, horizon - 1), fill=(70, 70, 74))
            d.polygon([(x, horizon - 18), (x + 5, horizon - 22), (x + 9, horizon - 18)], fill=(70, 70, 74))
        d.rectangle((bw - 20, horizon - 24, bw - 5, horizon - 1), fill=(96, 90, 84))
        d.rectangle((bw - 16, horizon - 20, bw - 14, horizon - 4), fill=(232, 226, 214))
        d.rectangle((bw - 11, horizon - 20, bw - 9, horizon - 4), fill=(232, 226, 214))

    elif kind == "exam":
        qw = bw - 8
        d.rectangle((3, 6, 3 + qw, 6 + 24), fill=(236, 232, 222))
        d.rectangle((5, 8, 5 + qw // 2, 8 + 20), fill=(250, 250, 248))
        d.rectangle((5 + qw // 2 + 2, 8, 3 + qw, 8 + 20), fill=(250, 250, 248))
        for i in range(3):
            y = 10 + i * 5
            d.rectangle((7, y, 5 + qw // 2 - 2, y), fill=(170, 166, 158))
        for i in range(3):
            y = 10 + i * 5
            w = qw // 2 - 8 - (4 if i == 2 else 0)
            d.rectangle((5 + qw // 2 + 4, y, 5 + qw // 2 + 4 + w, y), fill=(170, 166, 158))
        d.rectangle((3 + qw - 10, 22, 3 + qw - 4, 26), fill=RED)

    elif kind == "arrest":
        d.rectangle((3, 6, bw - 4, 14), fill=(232, 226, 214))
        d.rectangle((3, 14, bw - 4, 24), fill=(232, 226, 214))
        d.rectangle((3 + bw // 2 - 10, 14, 3 + bw // 2 + 10, 26), fill=(88, 92, 96))
        d.rectangle((3, 24, bw - 4, bh - 4), fill=(232, 226, 214))

    elif kind == "port":
        d.rectangle((3, 4, bw - 4, horizon), fill=(214, 206, 190))
        d.rectangle((3, horizon, bw - 18, bh - 3), fill=(214, 206, 190))
        d.rectangle((bw - 17, 4, bw - 4, bh - 3), fill=(48, 50, 56))
        d.rectangle((bw - 26, 14, bw - 16, 22), fill=(48, 50, 56))

    d.rectangle((0, 0, bw - 1, bh - 1), outline=FRAME)
    img.paste(tile, (x0, y0))


# --------------------------------------------------------------------------- sections

def _masthead(d, fonts):
    bold52 = fonts["52"][0]
    d.rectangle((MARGIN, 26, W - MARGIN, 28), fill=INK)
    d.text((MARGIN + OFF["mast_x"], 45 + OFF["mast_y"]), "THE WORLD REPORT", font=bold52, fill=INK)
    bold17 = fonts["17"][0]
    d.text((W - MARGIN - d.textlength(DAY, font=bold17), 52), DAY, font=bold17, fill=RED)
    d.text((MARGIN, 100 + OFF["strap_dy"]),
           "ONE DAY, ONE PAGE  \u00b7  the events of Sunday 22 November 2026 in every region",
           font=fonts["14"][1], fill=GREY)
    d.rectangle((MARGIN, 122, W - MARGIN, 124), fill=INK)


def _leads(img, d, fonts):
    bold12 = fonts["12"][0]
    bold23 = fonts["23"][0]
    plain13 = fonts["13"][1]
    inner = W - 2 * MARGIN
    gap = 12
    col = (inner - 2 * gap) // 3
    for i, (region, kicker, headline, detail, key) in enumerate(LEADS):
        x = MARGIN + i * (col + gap)
        d.text((x, 141 + OFF["kicker_dy"]), f"{region}  \u00b7  {kicker}", font=bold12, fill=RED)
        _illo(img, (x, 156 + OFF["lead_dy"], x + col, 252 + OFF["lead_dy"]), key, 100 + i)
        y = _para(d, (x, 261 + OFF["head_dy"]), _fit(d, headline, bold23, col, 2), bold23, INK, 24)
        _para(d, (x + 1, y + 3 + OFF["detail_dy"]), _fit(d, detail, plain13, col - 2, 4), plain13, GREY, 15)
    d.rectangle((MARGIN, 370, W - MARGIN, 371), fill=RULE)


def _panels(img, d, fonts):
    bold10 = fonts["10"][0]
    bold15 = fonts["15"][0]
    bold12 = fonts["12"][0]
    for r in range(2):
        for c in range(3):
            region, headline, key = PANELS[r * 3 + c]
            x = MARGIN + c * 305
            img_y = (384 if r == 0 else 464) + 10 + OFF["small_dy"]
            _illo(img, (x, img_y, x + 46, img_y + 46), key, 200 + r * 3 + c)
            d.text((x + 54, img_y - 1), region, font=bold10, fill=RED)
            _para(d, (x + 54, img_y + 12), _fit(d, headline, bold15, 250, 3), bold15, INK, 15)
    for c in range(3):
        region, headline, key = PANELS[6 + c]
        # 186px columns across the left area; the vignette and its two text lines sit
        # between the second panel row and the footer, clear of the map panel on the right.
        x = MARGIN + c * 203
        vy = 612 + OFF["wide_dy"]
        _illo(img, (x, vy, x + 188, vy + 58), key, 300 + c)
        d.text((x, vy + 64), region, font=bold10, fill=RED)
        _para(d, (x, vy + 78), _fit(d, headline, bold12, 185, 3), bold12, INK, 13)


def _map(d, fonts):
    bold13 = fonts["13"][0]
    bold10 = fonts["10"][0]
    plain10 = fonts["10"][1]
    mx0, my0, mx1, my1 = 642 + OFF["map_dx"], 404 + OFF["map_dy"], 996 + OFF["map_dx"], 640 + OFF["map_dy"]
    d.text((642 + OFF["map_dx"], 384 + OFF["map_dy"]), "WHERE IT HAPPENED", font=bold13, fill=INK)
    d.rectangle((mx0, my0, mx1, my1), fill=MAP_FILL, outline=(176, 180, 178))
    inset = 8
    for i, (_label, fx, fy) in enumerate(MAP_PINS):
        px = mx0 + inset + int(fx * (mx1 - mx0 - 2 * inset))
        py = my0 + inset + int(fy * (my1 - my0 - 2 * inset))
        d.ellipse((px - 4, py - 4, px + 4, py + 4), fill=RED)
        d.text((px + 6, py - 6), str(i + 1), font=bold10, fill=INK)
    col_w = (W - MARGIN - mx0) // 2
    for i, (label, _fx, _fy) in enumerate(MAP_PINS):
        c, r = divmod(i, 6)
        x = mx0 + c * col_w
        y = 652 + r * 15 + OFF["map_dy"]
        d.text((x, y), f"{i + 1}.", font=bold10, fill=RED)
        d.text((x + 17, y), label, font=plain10, fill=GREY)


def _briefs(d, fonts):
    bold13 = fonts["13"][0]
    bold9 = fonts["9"][0]
    plain11 = fonts["11"][1]
    d.rectangle((642, 750, W - MARGIN, 751), fill=RULE)
    d.text((642, 764), "ALSO TODAY", font=bold13, fill=INK)
    y = 784 + OFF["brief_dy"]
    limit = 958 + OFF["brief_dy"]
    for tag, line in BRIEFS:
        if y + 12 > limit:
            break
        d.text((642 + OFF["brief_dx"], y + OFF["brief_dy"]), tag, font=bold9, fill=RED)
        for ln in _fit(d, line, plain11, W - MARGIN - (642 + 46) - OFF["brief_dx"], 3):
            if y + 12 > limit:
                break
            d.text((642 + 46 + OFF["brief_dx"], y), ln, font=plain11, fill=INK)
            y += 13
        y += 1


def _footer(d, fonts):
    bold9 = fonts["9"][0]
    plain9 = fonts["9"][1]
    d.rectangle((MARGIN, 968, W - MARGIN, 969), fill=INK)
    d.text((MARGIN, 976), "REPORTED 22 NOVEMBER 2026 BY  " + " \u00b7 ".join(SOURCES),
           font=bold9, fill=GREY)
    note = "Illustrations are drawn, not photographs."
    d.text((W - MARGIN - d.textlength(note, font=plain9), 989), note, font=plain9, fill=GREY)


# --------------------------------------------------------------------------- page

def build():
    fonts = {str(s): _load(s) for s in (9, 10, 11, 12, 13, 14, 15, 17, 23, 52)}
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    _masthead(d, fonts)
    _leads(img, d, fonts)
    _panels(img, d, fonts)
    _map(d, fonts)
    _briefs(d, fonts)
    _footer(d, fonts)
    return img


if __name__ == "__main__":
    build().save("entry.png")