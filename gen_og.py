#!/usr/bin/env python3
"""Generate 1200x630 OG share images for every Jev Hub page.

Run with the venv python (needs Pillow):
  /Users/alex/.workbuddy/binaries/python/envs/default/bin/python gen_og.py

Writes PNGs into og/<lang>-<slug>.png (+ og/default.png).
build.py copies og/ into site/og/ on every build.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE, "og")
W, H = 1200, 630

sys.path.insert(0, BASE)
from content_en import PAGES as PAGES_EN      # noqa: E402
from content_zh import PAGES as PAGES_ZH      # noqa: E402

# palette (matches assets/style.css)
PAPER = "#F5F4EF"
INK = "#14161A"
NAVY = "#0E1726"
ACCENT = "#E85D3D"
MUTED = "#6B6F76"
LINE = "#D9D6CC"

F_HELV = "/System/Library/Fonts/Helvetica.ttc"
F_HELV_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
F_MONO = "/System/Library/Fonts/Menlo.ttc"
F_CN = "/System/Library/Fonts/Hiragino Sans GB.ttc"


def font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def wrap(draw, text, fnt, max_w, by_word=False):
    lines, cur = [], ""
    units = text.split(" ") if by_word else list(text)
    sep = " " if by_word else ""
    for u in units:
        trial = (cur + sep + u) if cur else u
        if draw.textlength(trial, font=fnt) > max_w and cur:
            lines.append(cur)
            cur = u
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def make_card(path, title, subtitle, site_label, is_zh):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # top & bottom border rules
    d.rectangle([0, 0, W, 6], fill=NAVY)
    d.rectangle([0, H - 6, W, H], fill=NAVY)

    # brand row: dark "J" mark + wordmark + unofficial
    d.rounded_rectangle([72, 64, 128, 120], radius=12, fill=NAVY)
    fj = font(F_MONO, 38)
    d.text((100, 92), "J", font=fj, fill=ACCENT, anchor="mm")
    f_brand = font(F_HELV_BOLD, 34)
    d.text((148, 92), "jev.hub", font=f_brand, fill=INK, anchor="lm")
    f_unoff = font(F_MONO, 22)
    uw = d.textlength("unofficial", font=f_unoff)
    d.text((156 + d.textlength("jev.hub", font=f_brand), 92), "unofficial",
           font=f_unoff, fill=MUTED, anchor="lm")

    # subtitle kicker above title
    f_kick = font(F_CN if is_zh else F_MONO, 24)
    d.text((72, 208), subtitle, font=f_kick, fill=ACCENT, anchor="lm")

    # big wrapped title
    f_title = font(F_CN if is_zh else F_HELV_BOLD, 72)
    lines = wrap(d, title, f_title, W - 144, by_word=not is_zh)
    if len(lines) > 3:
        f_title = font(F_CN if is_zh else F_HELV_BOLD, 58)
        lines = wrap(d, title, f_title, W - 144, by_word=not is_zh)
    y = 296
    for ln in lines[:3]:
        d.text((72, y), ln, font=f_title, fill=NAVY, anchor="lm")
        y += 88

    # footer: site label + accent dot
    f_foot = font(F_MONO, 26)
    d.ellipse([72, H - 88, 88, H - 72], fill=ACCENT)
    d.text((104, H - 80), site_label, font=f_foot, fill=MUTED, anchor="lm")

    img.save(path, "PNG", optimize=True)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    n = 0
    for slug, page in PAGES_EN.items():
        make_card(os.path.join(OUT_DIR, f"en-{slug}.png"),
                  title=page["title"].split("—")[0].split("|")[0].strip(),
                  subtitle="THE UNOFFICIAL JEV TRACKER",
                  site_label="jev-ai.live", is_zh=False)
        n += 1
    for slug, page in PAGES_ZH.items():
        make_card(os.path.join(OUT_DIR, f"zh-{slug}.png"),
                  title=page["title"].split("—")[0].split("|")[0].split("：")[0].strip(),
                  subtitle="JEV 非官方追踪站 · 每日更新",
                  site_label="jev-ai.live", is_zh=True)
        n += 1
    # fallback for any page without a dedicated image
    make_card(os.path.join(OUT_DIR, "default.png"),
              title="Jev AI, decoded", subtitle="THE UNOFFICIAL JEV TRACKER",
              site_label="jev-ai.live", is_zh=False)
    print(f"generated {n + 1} OG images -> {OUT_DIR}")


if __name__ == "__main__":
    main()
