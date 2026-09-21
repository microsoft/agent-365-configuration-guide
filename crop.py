# -*- coding: utf-8 -*-
import json, os
from PIL import Image
BASE = os.path.dirname(os.path.abspath(__file__))
deck = json.load(open(os.path.join(BASE,"deck.json"), encoding="utf-8"))
SLIDES = os.path.join(BASE, "slides")
IMG = os.path.join(BASE, "img"); os.makedirs(IMG, exist_ok=True)

INTRO = {3,18,26,31,38,48,65,81}
SW, SH = 12192000, 6858000
# slides whose side-by-side pictures should be split into vertically stacked crops.
# value = x-boundary(EMU); shapes with center-x below go to part "a", others to part "b".
SPLITS = {58: 6096000}

def is_title(sh):
    nm = sh["name"].lower()
    return ("title" in nm) or sh["name"].startswith("제목") or ("제목" in sh["name"])
def is_side(sh):
    return sh["name"] in ("Additional explanation",) or sh["name"].startswith("TextBox")

def content_shapes(shapes):
    out=[]
    for sh in shapes:
        if sh["kind"]=="text" and (is_title(sh) or is_side(sh)):
            continue
        if sh["w"] and sh["h"]:
            out.append(sh)
    return out

def crop_from(im, shs, W, H, name):
    sx, sy = W/SW, H/SH
    l = min(s["left"] for s in shs); t = min(s["top"] for s in shs)
    r = max(s["left"]+s["w"] for s in shs); b = max(s["top"]+s["h"] for s in shs)
    pad = int(SW*0.012)
    l-=pad; t-=pad; r+=pad; b+=pad
    x0=max(0,int(l*sx)); y0=max(0,int(t*sy)); x1=min(W,int(r*sx)); y1=min(H,int(b*sy))
    im.crop((x0,y0,x1,y1)).save(os.path.join(IMG, name))

for n in range(1, len(deck)+1):
    if n in INTRO or n==1 or n==2:
        continue
    src = os.path.join(SLIDES, f"slide-{n:02d}.png")
    if not os.path.exists(src): continue
    im = Image.open(src); W,H = im.size
    shs = content_shapes(deck[n-1]["shapes"])
    if not shs:
        continue
    if n in SPLITS:
        mid = SPLITS[n]
        left = [s for s in shs if s["left"]+s["w"]/2 < mid]
        right = [s for s in shs if s["left"]+s["w"]/2 >= mid]
        crop_from(im, left, W, H, f"slide-{n:02d}a.png")
        crop_from(im, right, W, H, f"slide-{n:02d}b.png")
        continue
    crop_from(im, shs, W, H, f"slide-{n:02d}.png")
print("cropped ->", len(os.listdir(IMG)))
