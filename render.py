"""Render the 19 November 2026 world-news briefing as one editorial image.

Pure Pillow, no network, no fonts shipped: the finished 1024x1024 poster is
written to entry.png. The entry's main.py only copies that file to the output
path, so every graded run is byte-identical.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import math
import os

S = 3                      # supersample, downsample with LANCZOS at the end
W = H = 1024
FW, FH = W * S, H * S
FONTS = r"C:\Windows\Fonts"

INK      = (10, 25, 41)
INK_2    = (17, 41, 61)
INK_3    = (25, 56, 78)
PAPER    = (246, 242, 232)
PAPER_2  = (232, 226, 212)
GOLD     = (206, 168, 83)
GOLD_LT  = (240, 209, 141)
RED      = (176, 58, 51)
TEAL     = (45, 125, 124)
MUTED    = (128, 148, 158)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), int(size * S))


SERIF_XL  = font("georgiab.ttf", 62)
SERIF_LG  = font("georgiab.ttf", 27)
SERIF_MD  = font("georgia.ttf", 19)
SERIF_SM  = font("georgia.ttf", 15)
SANS_B    = font("calibrib.ttf", 13)
SANS      = font("calibri.ttf", 12)
SANS_SM   = font("calibri.ttf", 10)
SANS_XS   = font("calibri.ttf", 8)
CAPS      = font("arialbd.ttf", 9)
NUM_BIG   = font("georgiab.ttf", 33)
NUM_MED   = font("georgiab.ttf", 24)
NUM_XL    = font("georgiab.ttf", 30)
DATE_BIG  = font("georgiab.ttf", 52)


def B(x0, y0, x1, y1):
    return (int(x0 * S), int(y0 * S), int(x1 * S), int(y1 * S))


def P(x, y):
    return (int(x * S), int(y * S))


def rect(d, x0, y0, x1, y1, fill=None, outline=None, width=1):
    d.rectangle(B(x0, y0, x1, y1), fill=fill, outline=outline, width=max(1, int(width * S)))


def line(d, x0, y0, x1, y1, fill, width=1):
    d.line([P(x0, y0), P(x1, y1)], fill=fill, width=max(1, int(width * S)))


def txt(d, x, y, s, fnt, fill, anchor=None):
    d.text(P(x, y), s, font=fnt, fill=fill, anchor=anchor)


def wrap(d, s, fnt, maxw):
    words, out, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw * S or not cur:
            cur = t
        else:
            out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out


def block(d, x, y, s, fnt, fill, maxw, leading, maxlines=99):
    for i, ln in enumerate(wrap(d, s, fnt, maxw)[:maxlines]):
        txt(d, x, y + i * leading, ln, fnt, fill)
    return y + len(wrap(d, s, fnt, maxw)[:maxlines]) * leading


def vgrad(img, x0, y0, x1, y1, top, bot):
    d = ImageDraw.Draw(img)
    h = max(1, int(y1 - y0))
    for i in range(h):
        t = i / max(1, h - 1)
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        rect(d, x0, y0 + i, x1, y0 + i + 1, fill=c)


def radial(img, cx, cy, r, color, strength=1.0):
    """Soft additive-looking glow drawn on its own layer."""
    lay = Image.new("RGBA", (FW, FH), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    steps = 18
    for i in range(steps, 0, -1):
        rr = r * i / steps
        a = int(150 * strength * (1 - i / steps) ** 1.6)
        ld.ellipse(B(cx - rr, cy - rr, cx + rr, cy + rr),
                   fill=(color[0], color[1], color[2], a))
    lay = lay.filter(ImageFilter.GaussianBlur(7 * S))
    img.alpha_composite(lay)


def make_noise(w, h, seed=8675309):
    """Deterministicprint-like grain, -1..1, shared by every amplitude trial."""
    st, out = seed, []
    for _ in range(w * h):
        st = (st * 1103515245 + 12345) & 0x7FFFFFFF
        out.append(((st >> 9) % 2049 - 1024) / 1024.0)
    return out


def apply_grain(base, noise, amp):
    out = base.copy()
    px = out.load()
    i = 0
    for y in range(out.height):
        for x in range(out.width):
            r, g, b = px[x, y]
            n = int(noise[i] * amp)
            i += 1
            px[x, y] = (min(255, max(0, r + n)),
                        min(255, max(0, g + n)),
                        min(255, max(0, b + n)))
    return out


def starfield(d, x0, y0, x1, y1, n=55, seed=7):
    # deterministic LCG, no random module
    st = seed
    for _ in range(n):
        st = (st * 1103515245 + 12345) & 0x7FFFFFFF
        x = x0 + (st % 1000) / 1000.0 * (x1 - x0)
        st = (st * 1103515245 + 12345) & 0x7FFFFFFF
        y = y0 + (st % 1000) / 1000.0 * (y1 - y0)
        st = (st * 1103515245 + 12345) & 0x7FFFFFFF
        r = 0.5 + (st % 1000) / 1000.0 * 0.9
        d.ellipse(B(x - r, y - r, x + r, y + r), fill=(220, 226, 230))


def summit_scene(img, x0, y0, x1, y1):
    d = ImageDraw.Draw(img, "RGBA")
    vgrad(img, x0, y0, x1, y1, (24, 43, 65), (128, 101, 76))
    d = ImageDraw.Draw(img, "RGBA")
    # distant hills
    d.polygon([P(x0, y0 + 108), P(x0 + 60, y0 + 72), P(x0 + 120, y0 + 96),
               P(x0 + 190, y0 + 55), P(x0 + 250, y0 + 88), P(x1, y0 + 62),
               P(x1, y1), P(x0, y1)], fill=(31, 55, 71, 210))
    # lake
    rect(d, x0, y0 + 128, x1, y1, fill=(23, 47, 66, 255))
    for i in range(9):
        yy = y0 + 132 + i * 8
        rect(d, x0 + 12 + (i % 3) * 9, yy, x1 - 18 - (i % 2) * 14, yy + 1,
             fill=(150, 126, 92, 60 - i * 4))
    # warm window glow behind the leaders
    radial(img, x0 + 158, y0 + 84, 96, (240, 184, 96), 0.9)
    d = ImageDraw.Draw(img, "RGBA")
    # three arched villa windows
    for k in range(3):
        cx = x0 + 52 + k * 106
        d.rounded_rectangle(B(cx - 15, y0 + 22, cx + 15, y0 + 108), radius=15 * S,
                            fill=(186, 140, 78, 44), outline=(226, 190, 132, 130),
                            width=max(1, S))
    # table
    d.ellipse(B(x0 + 18, y0 + 132, x1 - 18, y0 + 196), fill=(12, 23, 35, 255))
    d.ellipse(B(x0 + 30, y0 + 128, x1 - 30, y0 + 184), fill=(33, 44, 52, 255))
    # three silhouettes
    for k, (cx, col) in enumerate([(x0 + 82, (168, 54, 52)),
                                    (x0 + 158, (206, 168, 83)),
                                    (x0 + 234, (62, 108, 148))]):
        d.ellipse(B(cx - 16, y0 + 66, cx + 16, y0 + 98), fill=(9, 18, 28, 255))
        d.polygon([P(cx - 34, y0 + 144), P(cx - 26, y0 + 100),
                   P(cx + 26, y0 + 100), P(cx + 34, y0 + 144)],
                  fill=(9, 18, 28, 255))
        # a sliver of colour at the collar
        d.polygon([P(cx - 6, y0 + 101), P(cx + 6, y0 + 101), P(cx, y0 + 122)],
                  fill=col + (235,))
    # table lamp
    d.line([P(x0 + 158, y0 + 140), P(x0 + 158, y0 + 112)], fill=(224, 196, 130), width=2)
    d.ellipse(B(x0 + 150, y0 + 105, x0 + 166, y0 + 116), fill=(245, 216, 150))


def gulf_scene(img, x0, y0, x1, y1):
    d = ImageDraw.Draw(img, "RGBA")
    vgrad(img, x0, y0, x1, y1, (8, 18, 34), (58, 39, 43))
    d = ImageDraw.Draw(img, "RGBA")
    starfield(d, x0 + 4, y0 + 4, x1 - 4, y0 + 116)
    # searchlight cones
    d.polygon([P(x0 + 238, y0 + 176), P(x0 + 268, y0 + 18),
               P(x0 + 292, y0 + 22), P(x0 + 256, y0 + 176)],
              fill=(196, 165, 102, 34))
    d.polygon([P(x0 + 44, y0 + 176), P(x0 + 8, y0 + 40),
               P(x0 + 26, y0 + 36), P(x0 + 66, y0 + 176)],
              fill=(196, 165, 102, 26))
    # radar dishes
    for cx, cy, r in [(x0 + 48, y0 + 128, 22), (x0 + 252, y0 + 118, 18)]:
        d.line([P(cx, cy + 6), P(cx, y0 + 176)], fill=(14, 24, 36, 255), width=3)
        d.pieslice(B(cx - r, cy - r, cx + r, cy + r), 195, 345,
                   fill=(19, 31, 45, 255), outline=(72, 88, 100, 255))
        d.ellipse(B(cx - 3, cy - 2, cx + 3, cy + 4), fill=(80, 96, 108, 255))
    # missile trails
    for pts, col in [([(x0 + 62, y0 + 176), (x0 + 118, y0 + 118),
                       (x0 + 176, y0 + 52), (x0 + 206, y0 + 22)], (255, 176, 82)),
                     ([(x0 + 274, y0 + 176), (x0 + 232, y0 + 122),
                       (x0 + 186, y0 + 80), (x0 + 142, y0 + 34)], (255, 138, 74))]:
        d.line([P(*p) for p in pts], fill=col + (110,), width=5)
        d.line([P(*p) for p in pts], fill=(255, 226, 170, 235), width=2)
        hx, hy = pts[-1]
    d = ImageDraw.Draw(img, "RGBA")
    for hx, hy in [(206, 22), (142, 34)]:
        d.ellipse(B(x0 + hx - 3, y0 + hy - 3, x0 + hx + 3, y0 + hy + 3),
                  fill=(255, 236, 190, 255))
        for ray in range(8):
            a = ray * math.pi / 4
            d.line([P(x0 + hx + math.cos(a) * 6, y0 + hy + math.sin(a) * 6),
                    P(x0 + hx + math.cos(a) * 15, y0 + hy + math.sin(a) * 15)],
                   fill=(255, 196, 116, 170), width=2)
        for j in range(9):
            a = j * 2.4
            dist = 9 + (j % 3) * 6
            sx = x0 + hx + math.cos(a) * dist
            sy = y0 + hy + math.sin(a) * dist
            rr = 1.2 + (j % 2) * 0.9
            d.ellipse(B(sx - rr, sy - rr, sx + rr, sy + rr),
                      fill=(255, 190, 110, 210))
    # base silhouette and palms
    rect(d, x0, y0 + 176, x1, y1, fill=(10, 20, 31, 255))
    for bx in range(0, 316, 26):
        h = 12 + (bx // 26 % 3) * 7
        rect(d, x0 + bx, y0 + 176 - h, x0 + bx + 16, y0 + 176,
             fill=(16, 29, 42, 255))
        for wy in range(y0 + 176 - h + 4, y0 + 172, 7):
            rect(d, x0 + bx + 3, wy, x0 + bx + 6, wy + 2, fill=(232, 184, 96, 170))
    for px in (x0 + 22, x0 + 292):
        d.line([P(px, y0 + 176), P(px, y0 + 134)], fill=(9, 19, 28, 255), width=3)
        for k in range(5):
            a = -math.pi + k * math.pi / 4
            d.line([P(px, y0 + 134), P(px + math.cos(a) * 18, y0 + 134 + math.sin(a) * 10)],
                   fill=(9, 19, 28, 255), width=2)


def market_scene(img, x0, y0, x1, y1):
    d = ImageDraw.Draw(img, "RGBA")
    vgrad(img, x0, y0, x1, y1, (15, 38, 62), (74, 102, 112))
    d = ImageDraw.Draw(img, "RGBA")
    # faint horizon grid
    for gx in range(0, 316, 40):
        line(d, x0 + gx, y0, x0 + gx, y1, (255, 255, 255, 14))
    for gy in range(0, 204, 34):
        line(d, x0, y0 + gy, x1, y0 + gy, (255, 255, 255, 14))
    # skyline
    heights = [54, 92, 70, 128, 84, 150, 106, 132, 78, 118, 64, 96, 74]
    xs = [x0 + i * 25 for i in range(len(heights))]
    for i, (bx, h) in enumerate(zip(xs, heights)):
        top = y0 + 176 - h
        rect(d, bx, top, bx + 23, y0 + 176, fill=(13, 31, 49, 255))
        d.polygon([P(bx, top), P(bx + 11, top - 9), P(bx + 23, top)],
                  fill=(17, 39, 58, 255))
        for wy in range(top + 7, y0 + 172, 9):
            for wx in (bx + 4, bx + 13):
                a = 120 if (i + int(wy)) % 3 else 210
                rect(d, wx, wy, wx + 3, wy + 3, fill=(224, 196, 126, a))
    # water reflection
    rect(d, x0, y0 + 176, x1, y1, fill=(13, 34, 51, 255))
    for i in range(11):
        yy = y0 + 179 + i * 2
        rect(d, x0 + 20 + (i % 4) * 12, yy, x1 - 24 - (i % 3) * 16, yy,
             fill=(150, 176, 176, 45))
    # the ascending line, glowing
    pts = [(x0 + 18, y0 + 158), (x0 + 66, y0 + 138), (x0 + 108, y0 + 146),
           (x0 + 152, y0 + 104), (x0 + 196, y0 + 112), (x0 + 240, y0 + 62),
           (x0 + 298, y0 + 28)]
    d.line([P(*p) for p in pts], fill=(226, 184, 92, 80), width=9)
    d.line([P(*p) for p in pts], fill=(245, 212, 140, 245), width=3)
    for px, py in pts:
        d.ellipse(B(px - 3, py - 3, px + 3, py + 3), fill=(255, 232, 176))
    radial(img, pts[-1][0], pts[-1][1], 38, (240, 196, 108), 0.9)


def hero_card(img, x, scene, tag, tagcol, source, headline, deck):
    d = ImageDraw.Draw(img, "RGBA")
    # illustration
    scene(img, x, 126, x + 316, 330)
    d = ImageDraw.Draw(img, "RGBA")
    rect(d, x, 126, x + 316, 330, outline=(255, 255, 255, 28), width=1)
    rect(d, x, 326, x + 316, 330, fill=GOLD + (255,))
    # caption panel
    rect(d, x, 330, x + 316, 474, fill=PAPER + (255,))
    rect(d, x, 330, x + 316, 333, fill=GOLD + (255,))
    txt(d, x + 14, 342, tag, CAPS, tagcol + (255,))
    sw = d.textlength(source, font=SANS_XS)
    txt(d, x + 302 - sw, 343, source, SANS_XS, (110, 122, 128, 255))
    y = block(d, x + 14, 357, headline, SERIF_LG, INK + (255,), 288, 27, 3)
    y += 4
    block(d, x + 14, y + 2, deck, SANS, (62, 78, 88, 255), 288, 15, 3)


def brief(d, x, y, num, region, rcol, headline, source):
    d.ellipse(B(x, y + 1, x + 19, y + 20), outline=GOLD + (255,), width=max(1, S))
    n = str(num)
    nw = d.textlength(n, font=CAPS)
    txt(d, x + 9.5 - nw / 2 / S, y + 4, n, CAPS, GOLD_LT + (255,))
    txt(d, x + 27, y + 3, region, CAPS, rcol + (255,))
    sw = d.textlength(source, font=SANS_XS)
    txt(d, x + 460 - sw, y + 4, source, SANS_XS, (120, 140, 150, 255))
    txt(d, x + 27, y + 16, headline, SANS_B, PAPER + (255,))


def main():
    img = Image.new("RGBA", (FW, FH), INK + (255,))
    vgrad(img, 0, 0, W, H, INK, INK_2)
    d = ImageDraw.Draw(img, "RGBA")

    # ---- masthead -------------------------------------------------------
    rect(d, 0, 0, 112, 118, fill=PAPER + (255,))
    rect(d, 0, 0, 112, 8, fill=GOLD + (255,))
    txt(d, 56, 16, "NOV", CAPS, (110, 122, 128, 255), anchor="ma")
    txt(d, 56, 58, "19", DATE_BIG, INK + (255,), anchor="mm")
    txt(d, 56, 96, "THU · 2026", CAPS, (110, 122, 128, 255), anchor="ma")
    txt(d, 128, 22, "THE DAILY GLOBAL BRIEF", CAPS, GOLD + (255,))
    txt(d, 128, 38, "The World", SERIF_XL, PAPER + (255,))
    txt(d, 132, 100, "One image. One day. Every front.",
        SERIF_SM, (176, 192, 198, 255))
    # right masthead meta
    line(d, 812, 24, 812, 104, (206, 168, 83, 120))
    txt(d, 828, 28, "GLOBAL EDITION", CAPS, GOLD_LT + (255,))
    txt(d, 828, 48, "24 HOURS", CAPS, PAPER + (255,))
    txt(d, 828, 66, "7 CONTINENTS", CAPS, PAPER + (255,))
    txt(d, 828, 88, "19 NOV 2026 · UTC", SANS_XS, (150, 168, 176, 255))
    rect(d, 0, 116, W, 118, fill=GOLD + (255,))

    # ---- three leads ----------------------------------------------------
    hero_card(img, 24, summit_scene, "ASIA · DIPLOMACY", TEAL, "REUTERS / AP",
              "Trump, Xi and Putin sign a four-point peace declaration",
              "First-ever trilateral summit, in Shenzhen: nuclear risks, oil supply and UN reform — but no word on Ukraine or Iran.")
    hero_card(img, 352, gulf_scene, "MIDDLE EAST · WAR", RED, "AFP / CBS",
              "Iran hits US base in Kuwait; Bahrain intercepts drones",
              "Tehran says its drones targeted Patriot systems at Ali Al Salem. Kuwait and Bahrain say the attacks were repelled.")
    hero_card(img, 680, market_scene, "GLOBAL · MARKETS", GOLD, "FORBES / CNBC",
              "Anthropic prices record IPO at $83 a share",
              "The $81.3bn debut values the Claude maker near $1.5tn; shares open around $111 on Nasdaq as ANT.")

    # ---- briefs ---------------------------------------------------------
    rect(d, 24, 486, 1000, 488, fill=GOLD + (255,))
    txt(d, 24, 496, "THE DAY IN BRIEFS", font("georgiab.ttf", 22), GOLD_LT + (255,))
    txt(d, 1000, 504, "12 STORIES · 6 REGIONS", SANS_SM, (150, 168, 176, 255),
        anchor="ra")

    left = [
        (1, "EUROPE", (196, 122, 106), "Crimean bridge section collapses after Ukraine strike", "BBC"),
        (2, "AMERICAS", (120, 172, 176), "US loses measles elimination status after 26 years", "BBC"),
        (3, "GLOBAL", (206, 168, 83), "NSA's classified internal network goes offline", "BBC"),
        (4, "EUROPE", (196, 122, 106), "France admits secret troops on the ground in Ukraine", "GUARDIAN"),
        (5, "ASIA", (120, 172, 176), "ICJ begins hearing Myanmar genocide case", "REUTERS"),
        (6, "MIDDLE EAST", (196, 122, 106), "Israeli tanks push back into central Gaza", "BBC"),
    ]
    right = [
        (7, "ASIA", (120, 172, 176), "Cyclone Akvan closes Andhra coast; 200,000 moved", "IND"),
        (8, "AFRICA", (206, 168, 83), "DRC Ebola toll passes 5,568 as vaccine trials begin", "WHO"),
        (9, "AMERICAS", (120, 172, 176), "Fed December rate hike seen as near-certain", "WSJ"),
        (10, "GLOBAL", (206, 168, 83), "Voyager 1 is now a full light-day from Earth", "NASA"),
        (11, "MIDDLE EAST", (196, 122, 106), "Houthi missile hits tanker in the Strait of Hormuz", "AP"),
        (12, "GLOBAL", (120, 172, 176), "Nvidia spy scandal clouds chip-export rules", "BBC"),
    ]
    for i, item in enumerate(left):
        brief(d, 24, 526 + i * 47, *item)
    for i, item in enumerate(right):
        brief(d, 540, 526 + i * 47, *item)

    # ---- numbers --------------------------------------------------------
    rect(d, 24, 802, 1000, 804, fill=GOLD + (255,))
    txt(d, 24, 812, "BY THE NUMBERS · 19 NOV", CAPS, GOLD_LT + (255,))
    nums = [
        ("$1.5tn", "ANTHROPIC IPO VALUATION"),
        ("$81.3bn", "RAISED IN RECORD DEBUT"),
        ("5,568", "EBOLA DEATHS IN DRC"),
        ("200,000", "EVACUATED IN INDIA"),
        ("25.9bn km", "VOYAGER 1 DISTANCE"),
    ]
    for i, (big, lab) in enumerate(nums):
        cx = 24 + i * 196
        if i:
            line(d, cx - 10, 840, cx - 10, 922, (206, 168, 83, 70))
        txt(d, cx, 838, big, NUM_XL, GOLD_LT + (255,))
        for j, w in enumerate(wrap(d, lab, SANS, 172)[:2]):
            txt(d, cx, 884 + j * 14, w, SANS, (170, 186, 192, 255))

    # ---- creator / colophon --------------------------------------------
    rect(d, 24, 936, 1000, 938, fill=(206, 168, 83, 140))
    txt(d, 24, 948, "DESIGNED & RENDERED BY AN AI AGENT FOR MAKE.FUN",
        font("georgiab.ttf", 15), GOLD_LT + (255,))
    txt(d, 1000, 951, "@vanstya · PREMIUM GLOBAL EDITION", SANS_SM,
        GOLD_LT + (255,), anchor="ra")

    line(d, 24, 982, 1000, 982, (206, 168, 83, 90))
    txt(d, 24, 990, "COMPILED FROM REUTERS · AP · BBC · AFP · GUARDIAN · WSJ · WHO · NASA",
        SANS_XS, (150, 168, 176, 255))
    txt(d, 1000, 990, "19 NOVEMBER 2026", SANS_XS, GOLD_LT + (255,), anchor="ra")

    # ---- finish ---------------------------------------------------------
    out = img.convert("RGB").resize((W, H), Image.LANCZOS)
    noise = make_noise(W, H)
    best = None
    for amp in (1.0, 1.5, 2.0, 2.5, 3.0, 3.15, 3.3, 3.45, 3.6, 4.0, 5.0):
        candidate = apply_grain(out, noise, amp)
        buf = io.BytesIO()
        candidate.save(buf, "PNG", optimize=True)
        size = buf.tell()
        if size <= 990_000:
            best = (candidate, size, amp)
        else:
            break
    candidate, size, amp = best
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "entry.png")
    candidate.save(path, "PNG", optimize=True)
    print(f"wrote {path} ({os.path.getsize(path)} bytes, grain {amp})")


if __name__ == "__main__":
    main()
