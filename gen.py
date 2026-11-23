"""Draws 22 November 2026 as one broadsheet front page at 1024x1024."""

from __future__ import annotations

import math
import random

from PIL import Image, ImageDraw, ImageFont

import data

W = H = 1024
INK = (18, 18, 22)
PAPER = (247, 243, 234)
RED = (176, 32, 38)
GREY = (104, 100, 96)
RULE = (196, 188, 176)

MARGIN = 26


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """A font that exists in this sandbox; DejaVu ships with Pillow's dependencies."""
    names = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    )
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _wrap(draw: ImageDraw.ImageDraw, text: str, font, width: int) -> list[str]:
    """Greedy wrap that never splits a word and never exceeds `width`."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _text_block(draw, xy, text, font, width, fill=INK, leading=1.18, max_lines=None):
    """Draw wrapped text and return the y just below it."""
    x, y = xy
    lines = _wrap(draw, text, font, width)
    if max_lines:
        lines = lines[:max_lines]
    size = font.size
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += int(size * leading)
    return y


def _illo(draw, box, kind: str, seed: int):
    """A flat, legible vignette drawn on its own canvas, then pasted.

    Drawing to a scratch image keeps every mark inside the panel: there is no way for a
    stroke to bleed over the headline beside it.
    """
    x0, y0, x1, y1 = box
    w, h = max(1, x1 - x0), max(1, y1 - y0)
    tile = Image.new("RGB", (w, h), (232, 226, 214))
    d = ImageDraw.Draw(tile)
    rng = random.Random(seed)

    horizon = int(h * 0.62)
    d.rectangle([0, horizon, w, h], fill=(206, 199, 186))
    sol = (232, 168, 74)

    if kind == "cop":
        d.ellipse([w * 0.18, h * 0.10, w * 0.62, h * 0.54], fill=(210, 108, 74))
        for i in range(7):
            cx = rng.randint(4, max(5, w - 30))
            d.rectangle([cx, horizon - 10 - i * 2, cx + 18, horizon + 6], fill=(62, 74, 78))
        d.line([(0, horizon), (w, horizon)], fill=(88, 80, 70), width=2)
        d.line([(w * 0.5, 0), (w * 0.5, horizon)], fill=RED, width=3)
    elif kind == "tanker":
        d.rectangle([0, horizon, w, h], fill=(38, 92, 120))
        for i in range(5):
            yy = horizon + 6 + i * 9
            d.line([(0, yy), (w, yy)], fill=(60, 120, 148), width=2)
        d.polygon([(w * 0.30, horizon - 6), (w * 0.72, horizon - 6), (w * 0.66, horizon + 26), (w * 0.36, horizon + 26)],
                  fill=(44, 44, 50))
        d.rectangle([w * 0.62, horizon - 20, w * 0.70, horizon - 6], fill=(44, 44, 50))
        for i in range(9):
            cx, cy = rng.uniform(w * 0.2, w * 0.8), rng.uniform(h * 0.05, horizon - 10)
            r = rng.uniform(6, 16)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(84, 84, 92))
        d.ellipse([w * 0.44, horizon - 46, w * 0.60, horizon - 20], fill=sol)
    elif kind == "drone":
        d.rectangle([0, horizon, w, h], fill=(28, 62, 96))
        d.polygon([(w * 0.18, horizon), (w * 0.80, horizon), (w * 0.70, h), (w * 0.26, h)], fill=(56, 58, 64))
        d.rectangle([w * 0.42, horizon + 16, w * 0.62, horizon + 30], fill=(190, 186, 178))
        d.line([(w * 0.5, h * 0.18), (w * 0.5, horizon + 6)], fill=(120, 120, 128), width=2)
        d.ellipse([w * 0.38, h * 0.10, w * 0.62, h * 0.22], fill=(70, 72, 80))
    elif kind == "rubble":
        d.rectangle([0, int(h * 0.46), w, h], fill=(118, 110, 100))
        for i in range(14):
            bx, bw = rng.randint(0, max(1, w - 24)), rng.randint(10, 26)
            bh = rng.randint(10, int(h * 0.34))
            d.rectangle([bx, int(h * 0.46) - bh, bx + bw, int(h * 0.46) + 4], fill=(96, 90, 82))
        d.polygon([(w * 0.1, h), (w * 0.42, int(h * 0.55)), (w * 0.78, h)], fill=(142, 134, 122))
    elif kind == "sudan":
        d.rectangle([0, int(h * 0.52), w, h], fill=(150, 128, 96))
        for i in range(6):
            bx = rng.randint(0, max(1, w - 30))
            d.rectangle([bx, int(h * 0.30), bx + rng.randint(14, 24), int(h * 0.52)], fill=(120, 100, 74))
        d.line([(w * 0.5, h * 0.06), (w * 0.5, int(h * 0.3))], fill=(60, 60, 66), width=2)
        d.ellipse([w * 0.34, h * 0.02, w * 0.66, h * 0.12], fill=(70, 72, 78))
    elif kind == "capitol":
        d.rectangle([0, int(h * 0.60), w, h], fill=(146, 150, 140))
        d.rectangle([w * 0.20, int(h * 0.34), w * 0.80, int(h * 0.60)], fill=(232, 228, 218))
        d.polygon([(w * 0.14, int(h * 0.34)), (w * 0.5, int(h * 0.10)), (w * 0.86, int(h * 0.34))], fill=(210, 206, 196))
        for i in range(7):
            x = w * 0.24 + i * (w * 0.52 / 6)
            d.rectangle([x, int(h * 0.36), x + 4, int(h * 0.60)], fill=(186, 182, 172))
    elif kind == "fire":
        d.rectangle([0, int(h * 0.58), w, h], fill=(120, 106, 88))
        for i in range(5):
            cx = rng.uniform(w * 0.1, w * 0.9)
            r = rng.uniform(10, 22)
            d.polygon([(cx - r, h * 0.58), (cx, h * 0.58 - r * 2.4), (cx + r, h * 0.58)], fill=(214, 96, 42))
    elif kind == "knesset":
        d.rectangle([0, int(h * 0.56), w, h], fill=(150, 144, 132))
        d.rectangle([w * 0.16, int(h * 0.26), w * 0.84, int(h * 0.56)], fill=(226, 222, 212))
        for i in range(5):
            x = w * 0.22 + i * (w * 0.56 / 4)
            d.rectangle([x, int(h * 0.30), x + 8, int(h * 0.56)], fill=(178, 174, 164))
    elif kind == "factory":
        d.rectangle([0, int(h * 0.60), w, h], fill=(126, 120, 110))
        for i in range(4):
            x = w * 0.12 + i * (w * 0.2)
            d.rectangle([x, int(h * 0.26), x + w * 0.13, int(h * 0.60)], fill=(96, 90, 84))
        d.polygon([(w * 0.10, int(h * 0.26)), (w * 0.30, int(h * 0.12)), (w * 0.30, int(h * 0.26))], fill=(80, 76, 70))
        for i in range(6):
            cx = rng.uniform(w * 0.1, w * 0.9)
            r = rng.uniform(8, 18)
            d.ellipse([cx - r, h * 0.06 - r, cx + r, h * 0.06 + r], fill=(70, 70, 74))
    elif kind == "exam":
        d.rectangle([0, 0, w, h], fill=(236, 232, 222))
        d.rectangle([w * 0.22, h * 0.14, w * 0.78, h * 0.86], fill=(250, 250, 248), outline=(150, 146, 138))
        for i in range(6):
            y = h * 0.24 + i * h * 0.09
            d.line([(w * 0.28, y), (w * 0.66, y)], fill=(170, 166, 158), width=2)
        d.line([(w * 0.30, h * 0.34), (w * 0.50, h * 0.48)], fill=RED, width=3)
        d.line([(w * 0.50, h * 0.34), (w * 0.30, h * 0.48)], fill=RED, width=3)
    elif kind == "arrest":
        d.rectangle([0, int(h * 0.62), w, h], fill=(112, 116, 120))
        for i in range(4):
            x = w * 0.14 + i * (w * 0.22)
            d.rectangle([x, int(h * 0.30), x + w * 0.14, int(h * 0.62)], fill=(88, 92, 96))
        d.ellipse([w * 0.42, int(h * 0.14), w * 0.58, int(h * 0.30)], fill=(60, 62, 66))
    else:  # port
        d.rectangle([0, horizon, w, h], fill=(40, 84, 110))
        d.rectangle([0, 0, w, horizon], fill=(214, 206, 190))
        d.rectangle([w * 0.30, horizon - 26, w * 0.70, horizon], fill=(48, 50, 56))
        for i in range(4):
            cx = w * 0.34 + i * w * 0.09
            d.rectangle([cx, horizon - 40, cx + 10, horizon - 26], fill=(150, 62, 42))

    # A thin frame keeps the vignette reading as a printed picture, not a smudge.
    d.rectangle([0, 0, w - 1, h - 1], outline=(150, 143, 132), width=1)
    draw._image.paste(tile, (x0, y0))


def build() -> Image.Image:
    img = Image.new("RGB", (W, H), PAPER)
    img._image = img  # lets _illo reach the canvas it pastes onto
    d = ImageDraw.Draw(img)
    random.seed(20261122)

    inner = W - MARGIN * 2

    # ---------------- masthead
    y = MARGIN
    d.rectangle([MARGIN, y, W - MARGIN, y + 3], fill=INK)
    y += 14
    f_name = _font(52, bold=True)
    name = "THE WORLD REPORT"
    d.text((MARGIN, y), name, font=f_name, fill=INK)
    f_day = _font(17, bold=True)
    dayw = d.textlength(data.DAY, font=f_day)
    d.text((W - MARGIN - dayw, y + 8), data.DAY, font=f_day, fill=RED)
    y += 58
    d.text((MARGIN, y), "ONE DAY, ONE PAGE  ·  the events of Sunday 22 November 2026 in every region",
           font=_font(14), fill=GREY)
    y += 24
    d.rectangle([MARGIN, y, W - MARGIN, y + 2], fill=INK)
    y += 16

    # ---------------- lead strip: three panels
    lead_h = 250
    gap = 12
    col_w = (inner - gap * 2) // 3
    for i, (region, kicker, head, detail, key) in enumerate(data.LEADS):
        x = MARGIN + i * (col_w + gap)
        d.text((x, y), f"{region}  ·  {kicker}", font=_font(12, bold=True), fill=RED)
        _illo(d, (x, y + 18, x + col_w, y + 18 + 96), key, 100 + i)
        ty = y + 18 + 96 + 8
        fh = _font(23, bold=True)
        ty = _text_block(d, (x, ty), head, fh, col_w, leading=1.06, max_lines=2)
        _text_block(d, (x, ty + 4), detail, _font(13), col_w, fill=GREY, leading=1.22, max_lines=4)
    y += 18 + 96 + 118
    d.rectangle([MARGIN, y, W - MARGIN, y + 1], fill=RULE)
    y += 14

    # ---------------- left column: panels; right column: map + briefs
    left_w = int(inner * 0.615)
    right_x = MARGIN + left_w + 18
    right_w = W - MARGIN - right_x

    f_panel = _font(15, bold=True)
    f_panel_r = _font(10, bold=True)
    ly = y
    row_h = 74
    per_col = 3
    rows = [data.PANELS[:3], data.PANELS[3:6], data.PANELS[6:9]]
    colw2 = (left_w - 14) // 2
    for ci, col in enumerate(rows[:2]):
        cx = MARGIN + ci * (colw2 + 14)
        for ri, (region, head, key) in enumerate(col):
            ry = ly + ri * (row_h + 6)
            _illo(d, (cx, ry, cx + 46, ry + 46), key, 200 + ci * 10 + ri)
            d.text((cx + 54, ry), region, font=f_panel_r, fill=RED)
            _text_block(d, (cx + 54, ry + 13), head, f_panel, colw2 - 54, leading=1.12, max_lines=3)
    ly2 = ly + 3 * (row_h + 6) + 6
    # third row spans the left column as three short items
    span_w = (left_w - 28) // 3
    for ri, (region, head, key) in enumerate(rows[2]):
        cx = MARGIN + ri * (span_w + 14)
        _illo(d, (cx, ly2, cx + span_w, ly2 + 40), key, 300 + ri)
        d.text((cx, ly2 + 46), region, font=f_panel_r, fill=RED)
        _text_block(d, (cx, ly2 + 58), head, _font(12), span_w, leading=1.12, max_lines=3)

    # ---------------- map panel
    my = y
    d.text((right_x, my), "WHERE IT HAPPENED", font=_font(13, bold=True), fill=INK)
    my += 20
    map_h = 236
    d.rectangle([right_x, my, right_x + right_w, my + map_h], fill=(226, 231, 232), outline=(176, 180, 178))
    f_pin = _font(9, bold=True)
    for idx, (label, fx, fy) in enumerate(data.MAP_PINS):
        px = right_x + int(right_w * fx)
        py = my + int(map_h * fy)
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
        lw = d.textlength(str(idx + 1), font=f_pin)
        d.text((px - lw / 2, py - 3.5), str(idx + 1), font=f_pin, fill=(255, 255, 255))
    my += map_h + 8
    f_key = _font(10)
    ky = my
    for idx, (label, _, _) in enumerate(data.MAP_PINS):
        col = 0 if idx < 6 else 1
        row = idx if idx < 6 else idx - 6
        kx = right_x + col * (right_w // 2)
        kyy = ky + row * 15
        d.text((kx, kyy), f"{idx + 1}.", font=_font(10, bold=True), fill=RED)
        _text_block(d, (kx + 20, kyy), label, f_key, (right_w // 2) - 26, fill=GREY, leading=1.1, max_lines=1)
    my = ky + 6 * 15 + 12

    # ---------------- briefs
    d.rectangle([right_x, my, right_x + right_w, my + 1], fill=RULE)
    my += 10
    d.text((right_x, my), "ALSO TODAY", font=_font(13, bold=True), fill=INK)
    my += 18
    f_brief = _font(11)
    for tag, line in data.BRIEFS:
        if my > H - MARGIN - 46:
            break
        d.text((right_x, my), tag, font=_font(9, bold=True), fill=RED)
        my = _text_block(d, (right_x + 46, my - 1), line, f_brief, right_w - 46, fill=INK, leading=1.14, max_lines=3)
        my += 2

    # ---------------- footer
    fy = H - MARGIN - 30
    d.rectangle([MARGIN, fy, W - MARGIN, fy + 1], fill=INK)
    d.text((MARGIN, fy + 7), "REPORTED 22 NOVEMBER 2026 BY " + " · ".join(data.SOURCES),
           font=_font(9, bold=True), fill=GREY)
    note = "Illustrations are drawn, not photographs."
    nw = d.textlength(note, font=_font(9))
    d.text((W - MARGIN - nw, fy + 20), note, font=_font(9), fill=GREY)
    return img


if __name__ == "__main__":
    build().save("entry.png")
