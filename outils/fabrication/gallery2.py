"""Rend une salle de musée 360° (équirectangulaire) avec les tableaux de 1789.
Usage : python3 gallery.py <dossier arts> <sortie.jpg>
Convention Atelier 360 : az 0 = centre de l'image = mur du fond (-Z) ; az 90 = mur de droite (+X).
"""
import sys, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ARTS, OUT, CFG = sys.argv[1], sys.argv[2], json.load(open(sys.argv[3]))
HALF = 4.2          # demi-largeur de la salle (m)
H = 5.2             # hauteur sous plafond
EYE = 1.6
PPM = 260           # pixels par mètre des textures murales
FS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FSB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FSI = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"

rng = np.random.default_rng(7)

WALL = CFG.get("wall", [128, 26, 34])
def wall_base(width_m):
    W, Hh = int(width_m * PPM), int(H * PPM)
    # tenture rouge damassée (motif léger), lambris bas, corniche dorée
    y = np.linspace(0, 1, Hh)[:, None]; x = np.linspace(0, width_m, W)[None, :]
    patt = 0.5 + 0.5 * np.sin(x * 9.0) * np.sin((1 - y) * H * 9.0)
    lum = 0.92 + 0.06 * patt + rng.normal(0, 0.012, (Hh, W))
    base = np.stack([WALL[0] * lum, WALL[1] * lum, WALL[2] * lum], -1)
    img = base.astype(np.float32)
    def band(y0, y1, col):
        a, b = int((H - y1) * PPM), int((H - y0) * PPM)
        img[a:b] = col
    band(0, 0.95, (226, 218, 198))          # lambris crème
    band(0.93, 1.0, (190, 150, 70))         # cimaise dorée
    band(0, 0.15, (120, 92, 60))            # plinthe
    band(H - 0.35, H, (238, 232, 216))      # corniche
    band(H - 0.42, H - 0.35, (196, 158, 76))
    # panneaux du lambris
    pw = 1.2
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for i in range(int(width_m / pw) + 1):
        x0 = int((i * pw + 0.12) * PPM); x1 = int(((i + 1) * pw - 0.12) * PPM)
        y0 = int((H - 0.82) * PPM); y1 = int((H - 0.25) * PPM)
        d.rectangle([x0, y0, x1, y1], outline=(200, 186, 156), width=6)
    return im

def frame_and_hang(wall, img_path, cx, cy_m, w_m, title, sub):
    """cx : position horizontale (m depuis la gauche du mur), cy_m : hauteur du centre."""
    art = Image.open(img_path).convert("RGB")
    h_m = w_m * art.height / art.width
    fw = 0.16
    W, Hh = int((w_m + 2 * fw) * PPM), int((h_m + 2 * fw) * PPM)
    fr = Image.new("RGB", (W, Hh))
    # cadre doré en dégradé
    a = np.zeros((Hh, W, 3), np.float32)
    yy, xx = np.mgrid[0:Hh, 0:W]
    dist = np.minimum.reduce([xx, yy, W - 1 - xx, Hh - 1 - yy]).astype(np.float32) / (fw * PPM)
    shade = 0.75 + 0.35 * np.cos(dist * math.pi * 2.2)
    gold = np.array([212, 170, 80], np.float32)
    a[:] = gold * shade[..., None]
    fr = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    fr.paste(art.resize((int(w_m * PPM), int(h_m * PPM)), Image.LANCZOS), (int(fw * PPM), int(fw * PPM)))
    x0 = int((cx - w_m / 2 - fw) * PPM); y0 = int((H - cy_m - h_m / 2 - fw) * PPM)
    # ombre portée
    sh = Image.new("L", (W + 80, Hh + 80), 0); ImageDraw.Draw(sh).rectangle([40, 40, W + 40, Hh + 40], fill=150)
    sh = sh.filter(ImageFilter.GaussianBlur(22))
    wall.paste((40, 6, 10), (x0 - 20, y0 - 10), sh)
    wall.paste(fr, (x0, y0))
    # cartel
    d = ImageDraw.Draw(wall)
    ty = y0 + Hh + int(0.12 * PPM)
    f1 = ImageFont.truetype(FSB, int(0.105 * PPM)); f2 = ImageFont.truetype(FSI, int(0.075 * PPM))
    cw = int(max(d.textlength(title, font=f1), d.textlength(sub, font=f2)) + 0.24 * PPM); ch = int(0.42 * PPM)
    cx0 = int(cx * PPM) - cw // 2
    d.rectangle([cx0, ty, cx0 + cw, ty + ch], fill=(244, 238, 224), outline=(150, 120, 60), width=4)
    d.text((cx0 + cw // 2, ty + int(0.14 * PPM)), title, font=f1, fill=(40, 30, 20), anchor="mm")
    d.text((cx0 + cw // 2, ty + int(0.30 * PPM)), sub, font=f2, fill=(80, 60, 40), anchor="mm")
    return h_m

def text_wall(wall, cx, cy_m, lines):
    d = ImageDraw.Draw(wall)
    y = int((H - cy_m) * PPM)
    for txt, size, bold in lines:
        f = ImageFont.truetype(FSB if bold else FS, int(size * PPM))
        d.text((int(cx * PPM), y), txt, font=f, fill=(246, 226, 170), anchor="mm")
        y += int(size * PPM * 1.5)

L = 2 * HALF
walls = {k: wall_base(L) for k in ("front", "right", "back", "left")}
P = lambda n: f"{ARTS}/{n}.jpg"
POS = {}
for it in CFG["items"]:
    wall, off, cy, w = it["wall"], it.get("off", 0.0), it.get("cy", 2.75), it["w"]
    frame_and_hang(walls[wall], P(it["key"]), HALF + off, cy, w, it["title"], it["sub"])
    s_m = HALF + off
    if wall == "front": px, pz = s_m - HALF, -HALF
    elif wall == "right": px, pz = HALF, s_m - HALF
    elif wall == "back": px, pz = HALF - s_m, HALF
    else: px, pz = -HALF, HALF - s_m
    az = math.degrees(math.atan2(px, -pz)); dist = math.hypot(px, pz)
    POS[it["key"]] = {"az": round(az, 1), "el": round(math.degrees(math.atan2(cy - EYE, dist)), 1), "el_cartel": round(math.degrees(math.atan2(cy - EYE - 1.2, dist)), 1)}
if CFG.get("title"):
    text_wall(walls[CFG.get("title_wall", "back")], HALF, CFG.get("title_cy", 4.4), [(CFG["title"], 0.30, True), (CFG.get("subtitle", ""), 0.17, False)])
json.dump(POS, open(OUT + ".pos.json", "w"), indent=1)

# Sol : parquet de Versailles (carrés à entrelacs en diagonale)
FP = 220
n = int(L * FP)
yy, xx = np.mgrid[0:n, 0:n].astype(np.float32) / FP
u, v = (xx + yy) / math.sqrt(2), (xx - yy) / math.sqrt(2)
cell = 1.0
fu, fv = (u / cell) % 1, (v / cell) % 1
grain = 0.5 + 0.5 * np.sin((u * 40 + np.sin(v * 3) * 2))
lines = (np.minimum.reduce([fu, 1 - fu, fv, 1 - fv]) < 0.015) | (np.abs(fu - 0.5) < 0.008) | (np.abs(fv - 0.5) < 0.008)
diag = np.abs(fu - fv) < 0.01
base = np.where((np.floor(u * 2) + np.floor(v * 2)) % 2 == 0, 1.0, 0.86)
lum = base * (0.86 + 0.14 * grain)
floor = np.stack([150 * lum, 98 * lum, 56 * lum], -1)
floor[lines | diag] *= 0.55
cx = cz = n / 2
r = np.hypot(xx - L / 2, yy - L / 2)
floor *= (1.05 - 0.25 * (r / (L / 1.4)))[..., None]
floor = np.clip(floor, 0, 255)
# tapis central
rug = (np.abs(xx - L / 2) < 1.5) & (np.abs(yy - L / 2) < 1.0)
rugb = rug & ((np.abs(np.abs(xx - L / 2) - 1.4) < 0.05) | (np.abs(np.abs(yy - L / 2) - 0.9) < 0.05))
floor[rug] = [44, 58, 104]; floor[rugb] = [196, 160, 74]
fleur = rug & (((xx * 2.5) % 1 - 0.5) ** 2 + ((yy * 2.5) % 1 - 0.5) ** 2 < 0.006)
floor[fleur] = [196, 160, 74]

# Plafond : caissons clairs et rosace
cn = int(L * 120)
yy2, xx2 = np.mgrid[0:cn, 0:cn].astype(np.float32) / 120
cu, cv = (xx2 / 1.25) % 1, (yy2 / 1.25) % 1
edge = np.minimum.reduce([cu, 1 - cu, cv, 1 - cv])
ceil = np.full((cn, cn, 3), 236, np.float32) * (0.85 + 0.15 * np.clip(edge * 8, 0, 1))[..., None]
ceil[edge < 0.04] = [200, 166, 90]
rr = np.hypot(xx2 - L / 2, yy2 - L / 2)
ceil[(rr > 1.0) & (rr < 1.12)] = [200, 166, 90]
ceil[rr < 0.25] = [214, 178, 96]
ceil = np.clip(ceil, 0, 255)

walls = {k: np.asarray(v, np.float32) for k, v in walls.items()}
floor_t, ceil_t = floor.astype(np.float32), ceil.astype(np.float32)

def sample(tex, s, t):
    """s,t dans [0,1] ; échantillonnage bilinéaire."""
    h, w = tex.shape[:2]
    x = np.clip(s * (w - 1), 0, w - 1); y = np.clip(t * (h - 1), 0, h - 1)
    x0 = np.floor(x).astype(int); y0 = np.floor(y).astype(int)
    x1 = np.minimum(x0 + 1, w - 1); y1 = np.minimum(y0 + 1, h - 1)
    fx = (x - x0)[:, None]; fy = (y - y0)[:, None]
    return (tex[y0, x0] * (1 - fx) * (1 - fy) + tex[y0, x1] * fx * (1 - fy) + tex[y1, x0] * (1 - fx) * fy + tex[y1, x1] * fx * fy)

OW, OH = 8192, 4096
out = np.zeros((OH, OW, 3), np.uint8)
az = (np.arange(OW) + 0.5) / OW * 2 * math.pi - math.pi
for r0 in range(0, OH, 256):
    el = math.pi / 2 - (np.arange(r0, min(OH, r0 + 256)) + 0.5) / OH * math.pi
    A, E = np.meshgrid(az, el)
    dx = (np.sin(A) * np.cos(E)).ravel(); dy = np.sin(E).ravel(); dz = (-np.cos(A) * np.cos(E)).ravel()
    col = np.zeros((dx.size, 3), np.float32)
    best = np.full(dx.size, np.inf)
    def hit(t, mask):
        global best
        m = mask & (t > 0) & (t < best); best = np.where(m, t, best); return m
    with np.errstate(divide="ignore", invalid="ignore"):
        # murs : front z=-HALF, back z=+HALF, right x=+HALF, left x=-HALF
        for name, axis, sign in (("front", 2, -1), ("back", 2, 1), ("right", 0, 1), ("left", 0, -1)):
            d = dz if axis == 2 else dx
            t = sign * HALF / d
            px, py, pz = dx * t, EYE + dy * t, dz * t
            ok = (py >= 0) & (py <= H) & (np.abs(px) <= HALF + 1e-6) & (np.abs(pz) <= HALF + 1e-6)
            m = hit(t, ok)
            # coordonnée horizontale vue depuis l'intérieur, de gauche à droite
            if name == "front": s = (px + HALF) / L
            elif name == "back": s = (HALF - px) / L
            elif name == "right": s = (pz + HALF) / L
            else: s = (HALF - pz) / L
            tt = 1 - py / H
            idx = np.where(m)[0]
            col[idx] = sample(walls[name], s[idx], tt[idx])
        t = -EYE / dy; m = hit(t, dy < 0)
        idx = np.where(m)[0]; px, pz = dx[idx] * t[idx], dz[idx] * t[idx]
        col[idx] = sample(floor_t, (px + HALF) / L, (pz + HALF) / L)
        t = (H - EYE) / dy; m = hit(t, dy > 0)
        idx = np.where(m)[0]; px, pz = dx[idx] * t[idx], dz[idx] * t[idx]
        col[idx] = sample(ceil_t, (px + HALF) / L, (pz + HALF) / L)
    # éclairage doux : un peu plus sombre loin et vers le haut des murs
    dist = np.clip(best, 0, 20)
    col *= (1.08 - 0.035 * dist)[:, None]
    out[r0:r0 + 256] = np.clip(col, 0, 255).astype(np.uint8).reshape(-1, OW, 3)
    print(r0, end=" ", flush=True)
Image.fromarray(out).resize((4096, 2048), Image.LANCZOS).save(OUT, quality=90)
print("ok", OUT)
