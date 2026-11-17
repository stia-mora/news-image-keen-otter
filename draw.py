#!/usr/bin/env python3
"""Draw the news-image-20261117 entry: a one-page newspaper front page.

All artwork is flat PIL geometry + real rendered text. No AI-generated imagery.
Output: entry.png, 1024x1024, <= 1 MiB.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 243, 232)
CARD = (255, 254, 249)
NAVY = (20, 33, 61)
RED = (192, 57, 43)
GREY = (90, 92, 96)
LIGHT_LINE = (20, 33, 61)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by measured pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def draw_bridge(d, x, y, w, h, c):
    # deck + two towers + sagging suspension cables between tower tops
    deck_y = y + h - 10
    t1, t2 = x + w * 0.28, x + w * 0.72
    d.line([(x, deck_y), (x + w, deck_y)], fill=c, width=5)
    d.rectangle([t1 - 3, y + 4, t1 + 3, deck_y], fill=c)
    d.rectangle([t2 - 3, y + 4, t2 + 3, deck_y], fill=c)
    # cable sags from tower top to tower top, bottom just above deck
    d.arc([t1, y + 4, t2, deck_y + 14], start=0, end=180, fill=c, width=3)
    d.arc([x, y + 4, t1, deck_y], start=0, end=180, fill=c, width=3)
    d.arc([t2, y + 4, x + w, deck_y], start=0, end=180, fill=c, width=3)
    d.line([(x, y + h - 2), (x + w, y + h - 2)], fill=c, width=3)

def draw_plane(d, x, y, w, h, c):
    # side view, nose to the right: fuselage, tail fin, swept wings
    d.ellipse([x + 4, y + h * 0.34, x + w - 2, y + h * 0.60], fill=c)
    # tail fin at the rear (left), rising up
    d.polygon([(x + 10, y + h * 0.42), (x + 22, y + 2),
               (x + 34, y + 4), (x + 30, y + h * 0.46)], fill=c)
    # main wing sweeping down-back from mid fuselage
    d.polygon([(x + w * 0.42, y + h * 0.52), (x + w * 0.62, y + h * 0.52),
               (x + w * 0.42, y + h - 4), (x + w * 0.30, y + h - 4)], fill=c)
    # rear stabiliser sweeping up-back
    d.polygon([(x + w * 0.16, y + h * 0.44), (x + w * 0.28, y + h * 0.44),
               (x + w * 0.14, y + h * 0.20), (x + w * 0.06, y + h * 0.20)], fill=c)
    for i in range(3):
        cx = x + w * (0.52 + i * 0.11)
        d.ellipse([cx, y + h * 0.42, cx + 6, y + h * 0.42 + 6], fill=CREAM)

def draw_tanker(d, x, y, w, h, c):
    # hull + superstructure + flame
    d.polygon([(x + 4, y + h * 0.55), (x + w - 4, y + h * 0.55),
               (x + w - 16, y + h - 6), (x + 16, y + h - 6)], fill=c)
    d.rectangle([x + w * 0.62, y + h * 0.28, x + w * 0.86, y + h * 0.55], fill=c)
    d.polygon([(x + w * 0.30, y + h * 0.52), (x + w * 0.38, y + h * 0.28),
               (x + w * 0.46, y + 6), (x + w * 0.52, y + h * 0.30),
               (x + w * 0.50, y + h * 0.52)], fill=RED)
    d.line([(x, y + h - 2), (x + w, y + h - 2)], fill=c, width=3)

def draw_bank(d, x, y, w, h, c):
    # pediment + columns + steps
    d.polygon([(x + 4, y + h * 0.30), (x + w / 2, y + 2),
               (x + w - 4, y + h * 0.30)], fill=c)
    for i in range(4):
        cx = x + w * (0.14 + i * 0.24)
        d.rectangle([cx, y + h * 0.36, cx + 10, y + h * 0.80], fill=c)
    d.rectangle([x + 4, y + h * 0.80, x + w - 4, y + h * 0.88], fill=c)
    d.rectangle([x, y + h * 0.90, x + w, y + h - 2], fill=c)

def draw_chip(d, x, y, w, h, c):
    s = min(w, h) - 24
    ox, oy = x + (w - s) / 2, y + (h - s) / 2 + 4
    for i in range(3):
        px = ox + s * (0.18 + i * 0.32)
        d.rectangle([px, oy - 8, px + 5, oy], fill=c)
        d.rectangle([px, oy + s, px + 5, oy + s + 8], fill=c)
        py = oy + s * (0.18 + i * 0.32)
        d.rectangle([ox - 8, py, ox, py + 5], fill=c)
        d.rectangle([ox + s, py, ox + s + 8, py + 5], fill=c)
    d.rectangle([ox, oy, ox + s, oy + s], fill=c)
    d.rectangle([ox + s * 0.28, oy + s * 0.28, ox + s * 0.72, oy + s * 0.72],
                fill=CREAM)
    d.rectangle([ox + s * 0.42, oy + s * 0.42, ox + s * 0.58, oy + s * 0.58],
                fill=RED)

def draw_rocket(d, x, y, w, h, c):
    cx = x + w / 2
    d.polygon([(cx - 12, y + h * 0.55), (cx - 12, y + h * 0.28),
               (cx, y + 2), (cx + 12, y + h * 0.28),
               (cx + 12, y + h * 0.55)], fill=c)
    d.polygon([(cx - 12, y + h * 0.45), (cx - 26, y + h * 0.72),
               (cx - 12, y + h * 0.62)], fill=c)
    d.polygon([(cx + 12, y + h * 0.45), (cx + 26, y + h * 0.72),
               (cx + 12, y + h * 0.62)], fill=c)
    d.ellipse([cx - 6, y + h * 0.22, cx + 6, y + h * 0.22 + 12], fill=CREAM)
    d.polygon([(cx - 7, y + h * 0.58), (cx + 7, y + h * 0.58),
               (cx, y + h - 2)], fill=RED)

ICONS = {
    "bridge": draw_bridge,
    "plane": draw_plane,
    "tanker": draw_tanker,
    "bank": draw_bank,
    "chip": draw_chip,
    "rocket": draw_rocket,
}

STORIES = [
    ("EUROPE", "Kerch Bridge span collapses after Ukrainian strike",
     "Ukraine hit the bridge to Crimea for a second straight night; "
     "Zelenskyy hailed an \"unprecedented operation\". Moscow vowed to rebuild.",
     "bridge"),
    ("ASIA", "Trump lands in Manila for ASEAN summit",
     "The US president signed a joint trade statement with Thailand; "
     "China confirmed a first Xi\u2013Trump\u2013Putin meeting in Shenzhen on Thursday.",
     "plane"),
    ("MIDDLE EAST", "Tankers hit mines near the Strait of Hormuz",
     "Iran's Revolutionary Guard said two tankers struck mines and caught fire; "
     "drones fired at a US radar site in Bahrain were intercepted.",
     "tanker"),
    ("BUSINESS", "JPMorgan blames software bug for outage",
     "The bank said a software bug slowed online banking, branches and Zelle "
     "on Monday \u2014 not a cyberattack.",
     "bank"),
    ("TECH", "Nvidia reports first earnings since Huang exit",
     "Results due after Tuesday's close, less than a week after co-founder "
     "Jensen Huang resigned as CEO.",
     "chip"),
    ("SPACE", "Vulcan rocket fails, 40 Amazon satellites lost",
     "A ULA Vulcan suffered an anomaly minutes into flight and failed to "
     "deliver its Amazon Leo payload.",
     "rocket"),
]

def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    mx = 36  # margin

    # --- masthead ---
    d.rectangle([mx, 24, W - mx, 30], fill=RED)
    f_title = font(BOLD, 58)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 40), title, font=f_title, fill=NAVY)
    f_date = font(BOLD, 31)
    date = "TUESDAY, 17 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 112), date, font=f_date, fill=RED)
    f_sub = font(REG, 23)
    sub = "Six stories that defined the day"
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, 150), sub, font=f_sub, fill=NAVY)
    d.line([(mx, 184), (W - mx, 184)], fill=NAVY, width=3)
    d.line([(mx, 190), (W - mx, 190)], fill=NAVY, width=1)

    # --- story grid: 2 cols x 3 rows ---
    gx, gy = mx, 204
    gap = 20
    cw = (W - 2 * mx - gap) // 2
    ch = 246
    f_tag = font(BOLD, 18)
    f_head = font(BOLD, 27)
    f_body = font(REG, 20)
    for i, (tag, head, body, icon) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = gx + col * (cw + gap)
        y0 = gy + row * (ch + 12)
        d.rectangle([x0, y0, x0 + cw, y0 + ch], fill=CARD, outline=NAVY, width=2)
        # red tag bar
        d.rectangle([x0, y0, x0 + cw, y0 + 4], fill=RED)
        px, py = x0 + 18, y0 + 16
        d.text((px, py), tag, font=f_tag, fill=RED)
        # flat icon in the top-right corner, clear of all text
        iw, ih = 92, 46
        ICONS[icon](d, x0 + cw - iw - 14, y0 + 8, iw, ih, NAVY)
        py += 34
        # headline, max 2 lines
        for line in wrap(d, head, f_head, cw - 36)[:2]:
            d.text((px, py), line, font=f_head, fill=NAVY)
            py += 33
        py += 4
        # summary, up to 4 lines at full cell width
        for line in wrap(d, body, f_body, cw - 36)[:4]:
            d.text((px, py), line, font=f_body, fill=NAVY)
            py += 25

    # --- footer ---
    fy = gy + 3 * ch + 2 * 12 + 10
    d.line([(mx, fy), (W - mx, fy)], fill=NAVY, width=2)
    f_foot = font(REG, 17)
    foot = ("As reported on 17 November 2026 \u00b7 Sources: BBC, AP, Reuters, "
            "Al Jazeera, CNN")
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, fy + 10), foot, font=f_foot, fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)

if __name__ == "__main__":
    main()
