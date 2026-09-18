#!/usr/bin/env python3
"""Unique camp stills for remaining Trivia IDs. Skips files that already exist."""
from pathlib import Path
from PIL import Image, ImageDraw
import math

OUT = Path(__file__).resolve().parents[1] / "assets" / "teach"
W, H = 960, 540
INK = (26, 16, 40)
CREAM = (244, 230, 195)
WOOD = (139, 90, 43)
DARK = (58, 42, 26)
GOLD = (245, 196, 0)
ICE = (168, 196, 232)
MOSS = (61, 107, 56)
SKY1 = (58, 42, 106)
SKY2 = (232, 150, 90)
FUR = (166, 106, 58)

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def sky(im, dusk=True):
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        c = lerp(SKY1, SKY2, t) if dusk else lerp((120, 180, 220), (200, 230, 180), t)
        d.line([(0, y), (W, y)], fill=c)

def ground(d, y=400, c=MOSS):
    d.rectangle([0, y, W, H], fill=c)

def outline_ellipse(d, box, fill, width=4):
    d.ellipse(box, fill=fill, outline=INK, width=width)

def outline_rect(d, box, fill, width=4, r=12):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=INK, width=width)

def beaver(d, x, y, s=1.0, rot=0):
    # simple square-head beaver facing right
    hs = int(46 * s)
    outline_ellipse(d, [x - int(38*s), y, x + int(42*s), y + int(52*s)], FUR)
    outline_rect(d, [x - hs, y - int(52*s), x + hs, y + int(8*s)], FUR, r=10)
    # ears
    outline_ellipse(d, [x - int(40*s), y - int(58*s), x - int(18*s), y - int(34*s)], FUR)
    outline_ellipse(d, [x + int(18*s), y - int(58*s), x + int(40*s), y - int(34*s)], FUR)
    # eyes
    d.ellipse([x - int(18*s), y - int(22*s), x - int(8*s), y - int(12*s)], fill=INK)
    d.ellipse([x + int(8*s), y - int(22*s), x + int(18*s), y - int(12*s)], fill=INK)
    # teeth
    d.rectangle([x - int(8*s), y - int(4*s), x + int(8*s), y + int(10*s)], fill=CREAM, outline=INK)
    # tail
    outline_ellipse(d, [x - int(78*s), y + int(18*s), x - int(28*s), y + int(42*s)], DARK)

def stick(d, x1, y1, x2, y2, w=8, c=WOOD):
    d.line([(x1, y1), (x2, y2)], fill=INK, width=w + 4)
    d.line([(x1, y1), (x2, y2)], fill=c, width=w)

SCENES = {}

def add(tid, fn):
    SCENES[tid] = fn

def s_square(im):
    d = ImageDraw.Draw(im); sky(im, False); ground(d, 430)
    # four equal stick walls
    pts = [(280, 180), (680, 180), (680, 380), (280, 380)]
    for i in range(4):
        a, b = pts[i], pts[(i + 1) % 4]
        stick(d, a[0], a[1], b[0], b[1], 14)
    beaver(d, 200, 300, 0.9)

def s_grid(im):
    d = ImageDraw.Draw(im); sky(im, False); ground(d)
    for r in range(3):
        for c in range(4):
            outline_rect(d, [220 + c*120, 140 + r*90, 320 + c*120, 220 + r*90], WOOD)
    beaver(d, 120, 380, 0.85)

def s_biscuits(im):
    d = ImageDraw.Draw(im); sky(im); ground(d, 420, WOOD)
    for i, x0 in enumerate((180, 560)):
        for j in range(5):
            outline_ellipse(d, [x0 + (j % 3)*50, 250 + (j // 3)*50, x0 + 40 + (j % 3)*50, 290 + (j // 3)*50], GOLD)
    beaver(d, 480, 380, 0.8)

def s_line180(im):
    d = ImageDraw.Draw(im); sky(im); ground(d, 360, WOOD)
    d.line([(80, 300), (880, 300)], fill=INK, width=10)
    d.line([(80, 300), (480, 300)], fill=GOLD, width=6)
    beaver(d, 200, 420, 0.8)

def s_right(im):
    d = ImageDraw.Draw(im); sky(im, False); ground(d)
    stick(d, 300, 400, 300, 160, 16)
    stick(d, 300, 400, 620, 400, 16)
    beaver(d, 720, 360, 0.9)

def s_platform(im):
    d = ImageDraw.Draw(im); sky(im, False); ground(d)
    for r in range(2):
        for c in range(5):
            outline_rect(d, [180 + c*110, 220 + r*80, 270 + c*110, 290 + r*80], WOOD)
    beaver(d, 100, 400, 0.8)

def s_tri(im):
    d = ImageDraw.Draw(im); sky(im); ground(d)
    d.polygon([(480, 120), (220, 400), (740, 400)], outline=INK)
    d.line([(220, 400), (740, 400)], fill=GOLD, width=8)
    beaver(d, 140, 360, 0.75)

def s_circle(im):
    d = ImageDraw.Draw(im); sky(im, False); ground(d, 430, ICE)
    outline_ellipse(d, [280, 120, 700, 440], ICE)
    beaver(d, 490, 280, 0.7)

def s_odd(im):
    d = ImageDraw.Draw(im); sky(im); ground(d)
    for i, x in enumerate((180, 340, 500, 660)):
        c = WOOD if i < 3 else ICE
        outline_rect(d, [x, 220, x + 120, 360], c)
    beaver(d, 120, 400, 0.8)

def s_power(im):
    d = ImageDraw.Draw(im); sky(im); ground(d)
    n = 1
    x = 120
    for k in range(3):
        n *= 2
        for i in range(n):
            stick(d, x + i * 18, 380, x + i * 18, 280 - k * 20, 8)
        x += n * 18 + 40
    beaver(d, 820, 360, 0.8)

def s_mean(im):
    d = ImageDraw.Draw(im); sky(im); ground(d, 420, WOOD)
    for n, x in ((2, 160), (4, 360), (6, 560)):
        for i in range(n):
            outline_ellipse(d, [x, 240 + i * 28, x + 40, 270 + i * 28], GOLD)
    outline_ellipse(d, [780, 280, 860, 360], GOLD)
    beaver(d, 100, 400, 0.75)

def s_pct(im):
    d = ImageDraw.Draw(im); sky(im, False); ground(d)
    for i in range(8):
        c = GOLD if i < 2 else WOOD
        stick(d, 200 + i * 70, 360, 200 + i * 70, 200, 12, c)
    beaver(d, 120, 400, 0.8)

def s_heatflow(im):
    d = ImageDraw.Draw(im); sky(im); ground(d, 400, WOOD)
    outline_rect(d, [160, 220, 340, 320], (200, 80, 40))
    outline_rect(d, [500, 240, 760, 340], ICE)
    d.polygon([(340, 260), (500, 270), (340, 290)], fill=GOLD, outline=INK)
    beaver(d, 820, 360, 0.8)

def s_abszero(im):
    d = ImageDraw.Draw(im)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp((20, 30, 80), (180, 210, 230), y / H))
    outline_rect(d, [420, 80, 520, 460], CREAM, r=20)
    d.rectangle([440, 400, 500, 440], fill=ICE, outline=INK)
    beaver(d, 200, 360, 0.85)

def s_embers(im):
    d = ImageDraw.Draw(im); sky(im); ground(d, 400, DARK)
    outline_ellipse(d, [300, 300, 420, 400], (180, 60, 20))
    d.ellipse([330, 320, 390, 370], fill=GOLD)
    beaver(d, 620, 340, 0.9)

def s_boil(im):
    d = ImageDraw.Draw(im); sky(im); ground(d, 400, WOOD)
    outline_ellipse(d, [360, 220, 560, 380], (80, 80, 90))
    d.polygon([(430, 160), (490, 160), (500, 230), (420, 230)], fill=CREAM, outline=INK)
    beaver(d, 700, 360, 0.85)

def s_melt(im):
    d = ImageDraw.Draw(im); sky(im, False); ground(d, 360, ICE)
    outline_ellipse(d, [200, 280, 760, 500], ICE)
    d.polygon([(300, 300), (400, 260), (500, 310)], fill=CREAM, outline=INK)
    beaver(d, 160, 300, 0.8)

def s_pan(im):
    d = ImageDraw.Draw(im); sky(im); ground(d, 400, WOOD)
    outline_ellipse(d, [280, 240, 520, 360], (90, 90, 100))
    outline_rect(d, [520, 280, 700, 310], WOOD)
    beaver(d, 180, 360, 0.85)

def s_plume(im):
    d = ImageDraw.Draw(im); sky(im); ground(d, 420, WOOD)
    outline_ellipse(d, [400, 80, 560, 280], (220, 120, 60))
    d.polygon([(420, 420), (480, 200), (540, 420)], fill=(200, 80, 40), outline=INK)
    beaver(d, 200, 360, 0.8)

def s_rad(im):
    d = ImageDraw.Draw(im); sky(im); ground(d, 400, DARK)
    outline_ellipse(d, [120, 260, 280, 400], (200, 70, 20))
    for i in range(5):
        d.arc([40 - i*10, 180 - i*10, 360 + i*10, 480 + i*10], 300, 60, fill=GOLD, width=3)
    beaver(d, 700, 340, 0.95)

def s_wet(im):
    d = ImageDraw.Draw(im); sky(im, False); ground(d, 400, ICE)
    beaver(d, 400, 300, 1.1)
    d.ellipse([360, 200, 500, 260], fill=ICE, outline=INK)

def s_expand(im):
    d = ImageDraw.Draw(im); sky(im); ground(d)
    outline_rect(d, [180, 240, 320, 360], WOOD)
    outline_rect(d, [480, 200, 720, 400], (180, 80, 40), r=8)
    beaver(d, 820, 360, 0.8)

def s_newton(im):
    d = ImageDraw.Draw(im); sky(im, False); ground(d, 380)
    outline_rect(d, [200, 300, 420, 360], WOOD)
    d.polygon([(420, 300), (560, 240), (560, 280), (420, 340)], fill=DARK, outline=INK)
    beaver(d, 700, 320, 0.9)

def s_curie(im):
    d = ImageDraw.Draw(im); sky(im); ground(d, 400, WOOD)
    outline_rect(d, [300, 200, 500, 360], (40, 40, 50))
    d.ellipse([360, 230, 440, 310], fill=(180, 255, 120), outline=INK)
    beaver(d, 700, 340, 0.9)

def s_faraday(im):
    d = ImageDraw.Draw(im); sky(im); ground(d, 400, WOOD)
    outline_ellipse(d, [280, 180, 420, 320], (80, 80, 90))
    for a in range(0, 360, 30):
        r = math.radians(a)
        d.line([(350, 250), (350 + 80*math.cos(r), 250 + 80*math.sin(r))], fill=GOLD, width=3)
    beaver(d, 700, 340, 0.85)

def s_darwin(im):
    d = ImageDraw.Draw(im); sky(im, False); ground(d)
    for i, x in enumerate((220, 400, 580, 760)):
        outline_ellipse(d, [x, 260, x + 70, 320], (80 + i*30, 90, 40))
        outline_ellipse(d, [x + 10, 220, x + 60, 270], FUR)
    beaver(d, 120, 380, 0.8)

def s_photo(im):
    d = ImageDraw.Draw(im); sky(im); ground(d, 400, WOOD)
    outline_rect(d, [200, 160, 280, 280], GOLD, r=8)
    d.ellipse([400, 240, 460, 300], fill=(40, 40, 50), outline=INK)
    d.line([(280, 200), (400, 260)], fill=GOLD, width=6)
    beaver(d, 700, 340, 0.85)

def s_maxwell(im):
    d = ImageDraw.Draw(im); sky(im); ground(d)
    outline_ellipse(d, [200, 200, 360, 280], ICE)
    d.ellipse([500, 180, 620, 300], fill=GOLD, outline=INK)
    stick(d, 360, 240, 500, 240, 6, GOLD)
    beaver(d, 780, 360, 0.8)

def s_watt(im):
    d = ImageDraw.Draw(im); sky(im); ground(d, 400, WOOD)
    outline_rect(d, [280, 160, 520, 380], (90, 90, 100), r=6)
    outline_ellipse(d, [330, 200, 470, 280], ICE)
    beaver(d, 720, 340, 0.85)

def s_kepler(im):
    d = ImageDraw.Draw(im)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp((20, 16, 50), (40, 30, 80), y / H))
    d.ellipse([300, 160, 700, 400], outline=GOLD, width=5)
    d.ellipse([470, 250, 530, 310], fill=GOLD)
    beaver(d, 160, 380, 0.8)

def s_lodge(im):
    d = ImageDraw.Draw(im); sky(im, False); ground(d, 360, ICE)
    outline_ellipse(d, [280, 180, 700, 420], WOOD)
    d.ellipse([400, 240, 560, 340], fill=DARK)
    beaver(d, 160, 360, 0.8)

def s_under(im):
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 260], fill=ICE)
    d.rectangle([0, 260, W, H], fill=(40, 80, 120))
    outline_ellipse(d, [300, 80, 680, 280], WOOD)
    d.ellipse([440, 250, 520, 330], fill=(20, 40, 80))
    beaver(d, 480, 400, 0.7)

def s_dry(im):
    d = ImageDraw.Draw(im); sky(im); ground(d, 400, WOOD)
    outline_rect(d, [260, 160, 700, 380], WOOD, r=20)
    beaver(d, 480, 300, 0.7)
    beaver(d, 380, 320, 0.45)

def s_pond(im):
    d = ImageDraw.Draw(im); sky(im, False); ground(d)
    stick(d, 200, 300, 760, 300, 18)
    stick(d, 200, 300, 200, 200, 14)
    stick(d, 760, 300, 760, 200, 14)
    outline_ellipse(d, [240, 310, 720, 500], ICE)
    beaver(d, 140, 240, 0.75)

def s_teeth(im):
    d = ImageDraw.Draw(im); sky(im, False); ground(d)
    beaver(d, 400, 280, 1.4)
    stick(d, 560, 200, 820, 260, 20)

def s_tail(im):
    d = ImageDraw.Draw(im); sky(im, False); ground(d, 360, ICE)
    beaver(d, 420, 260, 1.2)
    d.ellipse([200, 320, 360, 400], fill=DARK, outline=INK, width=4)

def s_kits(im):
    d = ImageDraw.Draw(im); sky(im); ground(d, 400, WOOD)
    beaver(d, 360, 280, 1.0)
    beaver(d, 520, 320, 0.55)
    beaver(d, 620, 330, 0.5)

def s_winter(im):
    d = ImageDraw.Draw(im); sky(im)
    ground(d, 380, ICE)
    outline_ellipse(d, [400, 280, 560, 400], (200, 80, 30))
    beaver(d, 200, 340, 0.9)

def s_snowhat(im):
    d = ImageDraw.Draw(im); sky(im)
    ground(d, 400, ICE)
    outline_ellipse(d, [280, 220, 700, 460], WOOD)
    outline_ellipse(d, [260, 140, 720, 260], CREAM)

def s_damdef(im):
    d = ImageDraw.Draw(im); sky(im, False); ground(d, 400)
    stick(d, 300, 120, 300, 400, 22)
    stick(d, 660, 120, 660, 400, 22)
    stick(d, 300, 260, 660, 260, 16)
    beaver(d, 480, 200, 0.8)

def s_slate(im):
    d = ImageDraw.Draw(im); sky(im); ground(d, 420, WOOD)
    for r in range(3):
        for c in range(3):
            box = [300 + c*110, 120 + r*110, 400 + c*110, 220 + r*110]
            if r == 2 and c == 2:
                d.rounded_rectangle(box, 8, outline=GOLD, width=4)
            else:
                outline_rect(d, box, CREAM)
    beaver(d, 160, 360, 0.8)

def s_count(im):
    d = ImageDraw.Draw(im); sky(im, False); ground(d)
    for n, x in ((1, 180), (2, 400), (3, 650)):
        for i in range(n):
            stick(d, x + i * 24, 340, x + i * 24, 200, 10)
    beaver(d, 100, 400, 0.75)

def s_iceodd(im):
    d = ImageDraw.Draw(im); sky(im); ground(d)
    for i, x in enumerate((160, 340, 520, 700)):
        fill = WOOD if i < 3 else ICE
        outline_rect(d, [x, 200, x + 140, 360], fill)
    beaver(d, 80, 400, 0.7)

def s_clock(im):
    d = ImageDraw.Draw(im); sky(im); ground(d)
    cx, cy = 480, 260
    outline_ellipse(d, [cx-140, cy-140, cx+140, cy+140], CREAM)
    stick(d, cx, cy, cx, cy - 110, 10, WOOD)
    beaver(d, 160, 400, 0.8)

def s_tint(im):
    d = ImageDraw.Draw(im); sky(im); ground(d)
    cols = [WOOD, CREAM, ICE]
    for i, c in enumerate(cols):
        outline_rect(d, [200 + i*180, 180, 350 + i*180, 380], c)
    beaver(d, 100, 400, 0.75)

def s_stack(im):
    d = ImageDraw.Draw(im); sky(im); ground(d)
    outline_rect(d, [360, 160, 560, 280], WOOD)
    outline_rect(d, [380, 240, 580, 360], ICE)
    beaver(d, 180, 380, 0.85)

def s_ring(im):
    d = ImageDraw.Draw(im); sky(im); ground(d)
    outline_rect(d, [360, 180, 560, 380], WOOD)
    d.ellipse([340, 160, 580, 400], outline=GOLD, width=10)
    beaver(d, 180, 380, 0.85)

def s_add(im):
    d = ImageDraw.Draw(im); sky(im, False); ground(d)
    stick(d, 180, 300, 180, 180, 12)
    stick(d, 280, 300, 280, 180, 12)
    d.line([(320, 240), (380, 240)], fill=INK, width=6)
    stick(d, 440, 300, 440, 180, 12)
    stick(d, 470, 300, 470, 180, 12)
    beaver(d, 700, 360, 0.85)

def s_grow(im):
    d = ImageDraw.Draw(im); sky(im)
    ground(d, 400, ICE)
    for i, s in enumerate((40, 70, 110)):
        x = 180 + i * 180
        outline_ellipse(d, [x, 300 - s, x + s * 2, 300 + s], CREAM)
    beaver(d, 800, 360, 0.8)

def s_latin(im):
    d = ImageDraw.Draw(im); sky(im); ground(d)
    fam = [WOOD, ICE, GOLD]
    for r in range(3):
        for c in range(3):
            outline_rect(d, [280 + c*140, 120 + r*120, 400 + c*140, 220 + r*120], fam[(r + c) % 3])
    beaver(d, 140, 400, 0.75)

def s_speed(im):
    d = ImageDraw.Draw(im); sky(im); ground(d)
    for r in range(2):
        for c in range(2):
            outline_rect(d, [300 + c*160, 140 + r*160, 440 + c*160, 280 + r*160], CREAM)
    beaver(d, 160, 380, 0.8)

def s_drywood(im):
    d = ImageDraw.Draw(im); sky(im); ground(d, 400, DARK)
    for i in range(6):
        stick(d, 200 + i * 40, 360, 230 + i * 40, 200, 10)
    outline_ellipse(d, [500, 260, 640, 400], (200, 80, 20))
    beaver(d, 780, 340, 0.85)

def s_boots(im):
    d = ImageDraw.Draw(im); sky(im); ground(d, 400, WOOD)
    outline_ellipse(d, [500, 240, 680, 400], (200, 80, 20))
    outline_rect(d, [220, 300, 300, 400], DARK)
    outline_rect(d, [320, 300, 400, 400], DARK)
    beaver(d, 160, 340, 0.8)

def s_holder(im):
    d = ImageDraw.Draw(im); sky(im); ground(d)
    beaver(d, 480, 280, 1.2)
    outline_rect(d, [400, 360, 560, 400], GOLD, r=8)

def s_badge(im):
    d = ImageDraw.Draw(im); sky(im); ground(d)
    outline_ellipse(d, [380, 160, 580, 360], GOLD)
    beaver(d, 200, 360, 0.9)

def s_pause(im):
    d = ImageDraw.Draw(im); sky(im); ground(d)
    outline_rect(d, [200, 180, 420, 360], CREAM)
    d.polygon([(280, 220), (280, 320), (360, 270)], fill=MOSS, outline=INK)
    outline_rect(d, [520, 180, 760, 360], WOOD)
    d.rectangle([580, 230, 620, 310], fill=INK)
    d.rectangle([660, 230, 700, 310], fill=INK)
    beaver(d, 120, 400, 0.7)

def s_short(im):
    d = ImageDraw.Draw(im); sky(im); ground(d)
    beaver(d, 360, 280, 1.0)
    outline_ellipse(d, [560, 280, 700, 400], (200, 90, 30))

def s_next(im):
    d = ImageDraw.Draw(im); sky(im); ground(d)
    outline_rect(d, [280, 200, 680, 340], CREAM, r=16)
    d.polygon([(620, 240), (620, 300), (680, 270)], fill=GOLD, outline=INK)
    beaver(d, 180, 360, 0.85)

def s_social(im):
    d = ImageDraw.Draw(im); sky(im); ground(d)
    beaver(d, 300, 300, 0.9)
    beaver(d, 520, 300, 0.9)
    beaver(d, 700, 320, 0.8)

def s_about(im):
    d = ImageDraw.Draw(im); sky(im); ground(d)
    outline_rect(d, [260, 120, 700, 400], CREAM, r=18)
    beaver(d, 160, 380, 0.8)

def s_firewood(im):
    d = ImageDraw.Draw(im); sky(im); ground(d, 400, DARK)
    for i in range(5):
        stick(d, 280 + i * 30, 360, 400 + i * 20, 240, 12)
    outline_ellipse(d, [420, 220, 560, 340], GOLD)
    beaver(d, 160, 360, 0.85)

def s_histnight(im):
    d = ImageDraw.Draw(im); sky(im)
    ground(d, 400, DARK)
    outline_ellipse(d, [400, 240, 560, 400], (220, 100, 30))
    beaver(d, 220, 320, 0.9)
    beaver(d, 700, 340, 0.85)

def s_qubit(im):
    d = ImageDraw.Draw(im); sky(im); ground(d)
    stick(d, 400, 360, 400, 160, 16)
    stick(d, 400, 360, 620, 360, 16)
    beaver(d, 220, 340, 0.9)

def s_coin(im):
    d = ImageDraw.Draw(im); sky(im); ground(d, 400, WOOD)
    outline_ellipse(d, [400, 180, 560, 340], GOLD)
    beaver(d, 220, 340, 0.9)

MAP = {
    "TQ09": s_qubit,
    "TQ10": s_short,
    "TQ11": s_rad,
    "TQ12": s_coin,
    "TQ13": s_square,
    "TQ14": s_grid,
    "TQ15": s_biscuits,
    "TQ16": s_line180,
    "TQ17": s_right,
    "TQ18": s_platform,
    "TQ19": s_tri,
    "TQ20": s_circle,
    "TQ21": s_odd,
    "TQ22": s_power,
    "TQ23": s_mean,
    "TQ24": s_pct,
    "TQ25": s_heatflow,
    "TQ27": s_abszero,
    "TQ29": s_embers,
    "TQ30": s_boil,
    "TQ31": s_melt,
    "TQ32": s_pan,
    "TQ33": s_plume,
    "TQ34": s_rad,
    "TQ35": s_wet,
    "TQ36": s_expand,
    "TQ38": s_newton,
    "TQ41": s_curie,
    "TQ42": s_faraday,
    "TQ43": s_darwin,
    "TQ44": s_photo,
    "TQ45": s_maxwell,
    "TQ46": s_watt,
    "TQ48": s_kepler,
    "TQ49": s_lodge,
    "TQ50": s_under,
    "TQ51": s_dry,
    "TQ52": s_pond,
    "TQ53": s_teeth,
    "TQ54": s_tail,
    "TQ55": s_lodge,
    "TQ56": s_kits,
    "TQ57": s_winter,
    "TQ58": s_snowhat,
    "TQ59": s_damdef,
    "TQ60": s_slate,
    "TQ61": s_count,
    "TQ62": s_iceodd,
    "TQ63": s_clock,
    "TQ64": s_odd,
    "TQ65": s_tint,
    "TQ66": s_stack,
    "TQ67": s_ring,
    "TQ68": s_add,
    "TQ69": s_grow,
    "TQ70": s_slate,
    "TQ71": s_latin,
    "TQ72": s_speed,
    "TQ73": s_drywood,
    "TQ74": s_boots,
    "TQ75": s_holder,
    "TQ76": s_badge,
    "TQ77": s_pause,
    "TQ78": s_holder,
    "TQ79": s_short,
    "TQ80": s_next,
    "TQ81": s_social,
    "TQ82": s_about,
    "TQ83": s_speed,
    "TQ84": s_histnight,
}

# unique seed offset so even shared drawers differ
UNIQUE_SHIFT = {
    "TQ09": (40, 0), "TQ10": (-30, 20), "TQ11": (20, -10), "TQ12": (-50, 10),
    "TQ34": (60, 0), "TQ55": (30, -20), "TQ64": (-40, 15), "TQ70": (25, 10),
    "TQ72": (-20, 25), "TQ75": (15, -15), "TQ78": (-25, 20), "TQ83": (35, -10),
}

def render(tid, fn):
    im = Image.new("RGB", (W, H), SKY1)
    fn(im)
    dx, dy = UNIQUE_SHIFT.get(tid, (hash(tid) % 40 - 20, hash(tid[::-1]) % 30 - 15))
    if dx or dy:
        im = im.transform(im.size, Image.AFFINE, (1, 0, -dx, 0, 1, -dy), fillcolor=SKY1)
    # unique color grade per id
    overlay = Image.new("RGB", im.size, ((abs(hash(tid)) % 40), 20, 40))
    im = Image.blend(im, overlay, 0.06)
    im.save(OUT / f"{tid}.jpg", quality=86)

def main():
    n = 0
    for i in range(1, 85):
        tid = f"TQ{i:02d}"
        dest = OUT / f"{tid}.jpg"
        if dest.exists() and dest.stat().st_size > 20000:
            continue
        fn = MAP.get(tid)
        if not fn:
            def fallback(im, k=i):
                d = ImageDraw.Draw(im); sky(im, k % 2 == 0); ground(d)
                beaver(d, 200 + (k * 37) % 500, 280, 0.8 + (k % 5) * 0.05)
                outline_rect(d, [600, 160, 820, 360], (WOOD, ICE, GOLD, CREAM)[k % 4])
            fn = fallback
        render(tid, fn)
        n += 1
        print("made", tid)
    print("created", n)

if __name__ == "__main__":
    main()
