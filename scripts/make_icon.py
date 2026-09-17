#!/usr/bin/env python3
"""Bober Brain Camp icon — timber 3x3 camp slate, one cream answer-blank.

Paints every face at native size. 16px is a pixel map so the grid+hole
survives. Larger faces are a light pine tablet, dark wells, round ear
nubs, round gold nail. Not a chocolate-bar face, not logs, not a sword.
"""

from __future__ import annotations

import struct
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / "assets" / "icons"

# Brand (BRAND_MARK.md)
EMBER = (0x4A, 0x28, 0x18)
FUR = (0x8B, 0x5A, 0x2B)
CREAM = (0xF4, 0xE6, 0xC3)
GOLD = (0xF5, 0xC4, 0x00)
WOOD = (0x5C, 0x3A, 0x1A)
INK = (0x1A, 0x10, 0x28)

# Camp pine board — cream/fur mix so wells pit, not a dark chocolate bar.
PINE = (0xC4, 0x96, 0x58)
PINE_LIT = (0xD8, 0xB4, 0x78)
PINE_DIM = (0x9A, 0x6E, 0x3A)
WELL = WOOD
WELL_PIT = (0x3A, 0x22, 0x10)
CREAM_LIT = (0xFF, 0xF6, 0xE2)
GOLD_LIT = (0xFF, 0xE6, 0x66)

ICO_FACES = (16, 24, 32, 48, 64, 128, 256)
MISSING = (2, 2)

# 16x16 map. Keys: . ember  i ink  e fur  p pine  w well  c cream  g gold
PX16 = [
    "...ee....ee.....",
    "..eeee..eeee....",
    "..eeee..eeee....",
    ".iiiiiiiiiiiiii.",
    ".ippgpppppppppi.",
    ".ipwwpwwpwwpppi.",
    ".ipwwpwwpwwpppi.",
    ".ippppppppppppi.",
    ".ipwwpwwpwwpppi.",
    ".ipwwpwwpwwpppi.",
    ".ippppppppppppi.",
    ".ipwwpwwpccpppi.",
    ".ipwwpwwpccpppi.",
    ".ippppppppppppi.",
    ".iiiiiiiiiiiiii.",
    "................",
]

PX16_COLOR = {
    ".": EMBER,
    "i": INK,
    "e": FUR,
    "p": PINE,
    "w": WELL,
    "c": CREAM,
    "g": GOLD,
}


def _rgba(rgb: tuple[int, int, int], a: int = 255) -> tuple[int, int, int, int]:
    return (rgb[0], rgb[1], rgb[2], a)


def _paint_16() -> Image.Image:
    img = Image.new("RGBA", (16, 16), _rgba(EMBER))
    px = img.load()
    for y, row in enumerate(PX16):
        for x, ch in enumerate(row):
            px[x, y] = _rgba(PX16_COLOR[ch])
    return img


def _layout(size: int) -> dict:
    """Square 3x3 lattice. Cells stay larger than the pine rail."""
    side_pad = max(1, round(size * 0.05))
    bot_pad = max(1, round(size * 0.04))
    ear_band = max(6, round(size * 0.22))
    ink = max(1, round(size / 18))

    limit = min(size - 2 * side_pad, size - ear_band - bot_pad)
    cell, gut, rail = 2, 1, 1
    for c in range(max(2, (limit - 2 * ink) // 3), 1, -1):
        remain = limit - 3 * c - 2 * ink
        min_g = max(1, round(c * 0.18))
        min_r = max(2 if size >= 32 else 1, round(c * 0.50))
        if remain < 2 * min_g + 2 * min_r:
            continue
        g = min_g
        r = (remain // 2) - g
        if r < min_r:
            continue
        if r >= c:
            r = max(min_r, c - 1)
            g = max(1, (remain // 2) - r)
        cell, gut, rail = c, g, r
        break

    grid = 3 * cell + 2 * gut
    body = grid + 2 * rail
    outer = body + 2 * ink
    left = (size - outer) // 2
    top = size - outer - bot_pad
    if top < ink:
        top = max(0, (size - outer) // 5)

    ink_box = (left, top, left + outer - 1, top + outer - 1)
    pine_box = (ink_box[0] + ink, ink_box[1] + ink, ink_box[2] - ink, ink_box[3] - ink)
    gl = pine_box[0] + rail
    gt = pine_box[1] + rail
    wells = []
    for row in range(3):
        for col in range(3):
            x0 = gl + col * (cell + gut)
            y0 = gt + row * (cell + gut)
            wells.append((x0, y0, x0 + cell - 1, y0 + cell - 1))

    tack_r = max(1, round(size * 0.022))
    if size <= 32:
        tack_r = 1
    if rail >= 3:
        tack_r = min(tack_r, max(1, rail // 2))
    tack_cx = pine_box[0] + max(tack_r + 1, rail // 2)
    tack_cy = pine_box[1] + max(tack_r + 1, rail // 2)
    return {
        "cell": cell,
        "gut": gut,
        "rail": rail,
        "ink": ink,
        "ink_box": ink_box,
        "pine_box": pine_box,
        "wells": wells,
        "tack": (tack_cx, tack_cy, tack_r),
        "ear_band": ear_band,
    }


def _box(draw: ImageDraw.ImageDraw, b, fill) -> None:
    draw.rectangle([b[0], b[1], b[2], b[3]], fill=fill)


def _nub(draw: ImageDraw.ImageDraw, cx: float, cy: float, rx: float, ry: float, fill, ink, k: float) -> None:
    """Round ear-bump (ellipse). Ink ring first so 32px still has an outline."""
    draw.ellipse([cx - rx - k, cy - ry - k, cx + rx + k, cy + ry + k], fill=ink)
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=fill)


def _draw_ears(draw: ImageDraw.ImageDraw, size: int, lay: dict) -> None:
    """Small round nubs drawn BEHIND the slate. Far apart so they are not glasses."""
    ib = lay["ink_box"]
    k = max(1, round(size / 64))
    width = ib[2] - ib[0] + 1
    ry = max(3.2, size * 0.072)
    rx = ry * 0.70
    # Centers sit just under the top ink so the slate clips them into caps.
    cy = ib[1] + ry * 0.28
    lx = ib[0] + width * 0.22
    rx_c = ib[0] + width * 0.78
    _nub(draw, lx, cy, rx, ry, FUR, INK, k)
    _nub(draw, rx_c, cy, rx, ry, FUR, INK, k)


def _draw_slate(draw: ImageDraw.ImageDraw, size: int, lay: dict) -> None:
    _box(draw, lay["ink_box"], INK)
    _box(draw, lay["pine_box"], PINE)
    if size >= 48:
        pb = lay["pine_box"]
        lip = max(1, lay["rail"] // 3)
        _box(draw, (pb[0], pb[1], pb[2], pb[1] + lip), PINE_LIT)
        _box(draw, (pb[0], pb[3] - lip, pb[2], pb[3]), PINE_DIM)
        _box(draw, (pb[0], pb[1], pb[0] + lip, pb[3]), PINE_LIT)
        _box(draw, (pb[2] - lip, pb[1], pb[2], pb[3]), PINE_DIM)


def _draw_wells(draw: ImageDraw.ImageDraw, size: int, lay: dict) -> None:
    cell = lay["cell"]
    for row in range(3):
        for col in range(3):
            b = lay["wells"][row * 3 + col]
            if (row, col) == MISSING:
                _draw_punch(draw, size, b)
                continue
            _box(draw, b, WELL)
            if size >= 48 and cell >= 6:
                inset = max(1, cell // 7)
                _box(draw, (b[0], b[1], b[2], b[1] + inset), WELL_PIT)
                _box(draw, (b[0], b[1], b[0] + inset, b[3]), WELL_PIT)


def _draw_punch(draw: ImageDraw.ImageDraw, size: int, b) -> None:
    _box(draw, b, CREAM)
    w = b[2] - b[0] + 1
    if size >= 48 and w >= 6:
        rim = max(1, w // 9)
        _box(draw, (b[0], b[1], b[2], b[1] + rim), PINE_DIM)
        _box(draw, (b[0], b[1], b[0] + rim, b[3]), PINE_DIM)
        inner = (b[0] + rim, b[1] + rim, b[2] - max(0, rim - 1), b[3] - max(0, rim - 1))
        if inner[2] > inner[0] and inner[3] > inner[1]:
            _box(draw, inner, CREAM_LIT)


def _draw_tack(draw: ImageDraw.ImageDraw, size: int, lay: dict) -> None:
    cx, cy, r = lay["tack"]
    k = 1 if size < 96 else max(1, round(r * 0.30))
    # Round nail head — not a diamond, not a crown jewel, not a moon.
    draw.ellipse([cx - r - k, cy - r - k, cx + r + k, cy + r + k], fill=INK)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD)
    if size >= 48 and r >= 3:
        draw.ellipse(
            [cx - r * 0.45, cy - r * 0.55, cx + r * 0.10, cy - r * 0.05],
            fill=GOLD_LIT,
        )


def paint(size: int) -> Image.Image:
    if size == 16:
        return _paint_16()
    img = Image.new("RGBA", (size, size), _rgba(EMBER))
    draw = ImageDraw.Draw(img)
    lay = _layout(size)
    _draw_ears(draw, size, lay)
    _draw_slate(draw, size, lay)
    _draw_wells(draw, size, lay)
    _draw_tack(draw, size, lay)
    return img


def _png_bytes(img: Image.Image) -> bytes:
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def write_ico(path: Path, faces: dict[int, Image.Image]) -> None:
    order = sorted(faces)
    payloads = [_png_bytes(faces[s].convert("RGBA")) for s in order]
    count = len(order)
    offset = 6 + 16 * count
    blob = bytearray(struct.pack("<HHH", 0, 1, count))
    for s, payload in zip(order, payloads):
        w = 0 if s >= 256 else s
        h = 0 if s >= 256 else s
        blob += struct.pack("<BBBBHHII", w, h, 0, 0, 1, 32, len(payload), offset)
        offset += len(payload)
    path.write_bytes(bytes(blob) + b"".join(payloads))


def main() -> None:
    ICON_DIR.mkdir(parents=True, exist_ok=True)
    faces = {s: paint(s) for s in ICO_FACES}
    write_ico(ICON_DIR / "bober-brain-camp.ico", faces)
    paint(192).save(ICON_DIR / "icon-192.png")
    paint(512).save(ICON_DIR / "icon-512.png")
    print(f"wrote {ICON_DIR / 'bober-brain-camp.ico'}")
    print(f"wrote {ICON_DIR / 'icon-192.png'}")
    print(f"wrote {ICON_DIR / 'icon-512.png'}")


if __name__ == "__main__":
    main()
