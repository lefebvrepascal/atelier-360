"""Fabrique les images emboîtées (carrées) du zoom continu, de l'Univers au proton, et leur placement."""
import json, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
Image.MAX_IMAGE_PIXELS = None
N = 1536; OUT = "/home/claude/zoom/quilt"; os.makedirs(OUT, exist_ok=True)
A1 = "/home/claude/zmed/medias/arts"; A2 = "/home/claude/qmed/medias/arts"; IGN = "/home/claude/qmed2/medias/ign"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
rng = np.random.default_rng(11)
LV = []
def font(s): return ImageFont.truetype(FB, s)
def label(d, xy, t, s=34, col=(255, 255, 255), anchor="la"):
    d.text(xy, t, font=font(s), fill=col, anchor=anchor, stroke_width=max(2, s // 10), stroke_fill=(0, 0, 0))
def save(name, im, e, cx=0.5, cy=0.5):
    im = im.convert("RGB").resize((N, N), Image.LANCZOS); im.save(f"{OUT}/{name}.jpg", quality=86)
    a = np.asarray(im).astype(float); edge = np.concatenate([a[:8].reshape(-1, 3), a[-8:].reshape(-1, 3), a[:, :8].reshape(-1, 3), a[:, -8:].reshape(-1, 3)])
    LV.append(dict(name=name, e=round(e, 3), cx=round(cx, 4), cy=round(cy, 4), fill=[int(v) for v in edge.mean(0)]))
def stars(im, n, smax=1.6, cmin=60, cmax=255):
    d = ImageDraw.Draw(im)
    for _ in range(n):
        x, y = rng.uniform(0, im.width, 2); s = rng.uniform(0.4, smax); c = int(rng.uniform(cmin, cmax)); t = rng.choice([(1, 1, 1), (1, .9, .75), (.8, .9, 1)])
        d.ellipse([x - s, y - s, x + s, y + s], fill=tuple(int(c * v) for v in t))
def glow(im, x, y, r, col):
    a = np.asarray(im).astype(float); H, W = a.shape[:2]; yy, xx = np.mgrid[0:H, 0:W]; d2 = ((xx - x) ** 2 + (yy - y) ** 2) / (r * r)
    g = np.exp(-d2)[..., None] * np.array(col)[None, None, :]; return Image.fromarray(np.clip(a + g, 0, 255).astype(np.uint8))
def ortho_globe(tex, lat0, lon0, D, size, shade=True):
    """globe orthographique de diamètre D px centré dans une image size×size, texture équirectangulaire"""
    T = np.asarray(tex.convert("RGB")).astype(float); th, tw = T.shape[:2]
    yy, xx = np.mgrid[0:size, 0:size]; X = (xx - size / 2 + 0.5) / (D / 2); Y = -(yy - size / 2 + 0.5) / (D / 2); r2 = X * X + Y * Y; m = r2 <= 1
    Zc = np.sqrt(np.clip(1 - r2, 0, 1)); la0, lo0 = math.radians(lat0), math.radians(lon0)
    lat = np.arcsin(np.clip(Zc * math.sin(la0) + Y * math.cos(la0), -1, 1)); lon = lo0 + np.arctan2(X, Zc * math.cos(la0) - Y * math.sin(la0))
    u = ((lon / (2 * math.pi) + 0.5) % 1) * (tw - 1); v = (0.5 - lat / math.pi) * (th - 1)
    c = T[v.astype(int).clip(0, th - 1), u.astype(int).clip(0, tw - 1)]
    if shade: c = c * (0.55 + 0.45 * Zc)[..., None]
    out = np.zeros((size, size, 3)); out[m] = c[m]; a = np.zeros((size, size)); a[m] = 1
    return Image.fromarray(out.astype(np.uint8)), Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1))
def paste_globe(im, gl, x, y):
    g, a = gl; im.paste(g, (int(x - g.width / 2), int(y - g.height / 2)), a)
LAT, LON = 50.782043, 3.122895
earth = Image.open(f"{A1}/earth_tex.jpg")

# 1. Univers observable : boule du fond diffus cosmologique
import base64, io
cmbq = json.load(open("/home/claude/zoom/zoom_360.json"))["scenes"][1]["env"]["levels"][0]["obj"]["img"]
cmb = Image.open(io.BytesIO(base64.b64decode(cmbq.split(",")[1])))
im = Image.new("RGB", (N, N), (0, 0, 0)); paste_globe(im, ortho_globe(cmb, 20, 0, N * 0.9, N, shade=False), N / 2, N / 2); save("univers", im, math.log10(8.8e26 / 0.9))
# 2. toile cosmique (simulation) puis 3. champ de galaxies (Hubble)
cw = Image.open(f"{A1}/cosmicweb.jpg"); s = min(cw.size); cw = cw.crop(((cw.width - s) // 2, (cw.height - s) // 2, (cw.width + s) // 2, (cw.height + s) // 2)); save("toile", cw, 25.3)
hu = Image.open(f"{A1}/hudf.jpg"); save("galaxies", hu.crop((300, 300, 2100, 2100)), 24.0)
# 4. Groupe local (P. C. Budassi, CC BY 4.0) : image complétée en carré
lg = Image.open(f"{A2}/localgroup.jpg"); im = Image.new("RGB", (2400, 2400), (0, 0, 0)); im.paste(lg, (0, 640)); save("groupe_local", im, math.log10(2400 / 0.498 * 9.461e18), 588 / 2400, (526 + 640) / 2400)
# 5. Voie lactée (vue d'artiste NASA/JPL-Caltech) : le Soleil est en (0,5 ; 0,69)
save("voie_lactee", Image.open(f"{A1}/mw_art.jpg"), 21.08, 0.5, 0.69)
# 6. région du Soleil dans la Voie lactée (≈ 3 000 années-lumière)
im = Image.new("RGB", (N, N), (6, 7, 14)); a = np.asarray(im).astype(float)
yy, xx = np.mgrid[0:N, 0:N]; band = np.exp(-((yy - N * 0.5 - 0.25 * (xx - N / 2)) / (N * 0.33)) ** 2)
for k, col in enumerate([(70, 80, 120), (110, 70, 90)]):
    noise = np.asarray(Image.fromarray((rng.random((48, 48)) * 255).astype(np.uint8)).resize((N, N), Image.BICUBIC).filter(ImageFilter.GaussianBlur(30))).astype(float) / 255
    a += (band * noise * 0.9)[..., None] * np.array(col)[None, None, :]
im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); stars(im, 9000, 1.3, 40, 230); im = glow(im, N / 2, N / 2, 10, (255, 230, 150))
d = ImageDraw.Draw(im); d.ellipse([N / 2 - 30, N / 2 - 30, N / 2 + 30, N / 2 + 30], outline=(245, 183, 0), width=4); label(d, (N / 2 + 40, N / 2 - 70), "Soleil", 46, (245, 183, 0))
save("region_soleil", im, math.log10(3e19))
# 7. étoiles voisines (≈ 32 années-lumière)
S7 = 3e17; im = Image.new("RGB", (N, N), (2, 3, 8)); stars(im, 700, 1.1, 30, 140); d = ImageDraw.Draw(im)
AL = 9.461e15
for nm, dist, ang, col, sz in [("Proxima du Centaure", 4.24, -35, (255, 140, 110), 6), ("Alpha du Centaure", 4.37, -28, (255, 236, 200), 9), ("Étoile de Barnard", 5.96, 150, (255, 150, 120), 6),
                               ("Wolf 359", 7.9, 95, (255, 130, 110), 5), ("Sirius", 8.6, 210, (210, 225, 255), 13), ("Epsilon Eridani", 10.5, 260, (255, 210, 160), 8), ("Procyon", 11.5, 40, (240, 240, 255), 10)]:
    r = dist * AL / S7 * N; x = N / 2 + r * math.cos(math.radians(ang)); y = N / 2 + r * math.sin(math.radians(ang)); im = glow(im, x, y, sz * 1.6, col); d = ImageDraw.Draw(im); label(d, (x + 16, y - 16), nm, 30)
im = glow(im, N / 2, N / 2, 14, (255, 225, 140)); d = ImageDraw.Draw(im); label(d, (N / 2 + 18, N / 2 + 10), "Soleil", 38, (245, 183, 0))
save("etoiles_voisines", im, math.log10(S7))
# 8. le Soleil vu de très loin (≈ 0,3 année-lumière)
im = Image.new("RGB", (N, N), (2, 3, 8)); stars(im, 350, 1.0, 20, 110); im = glow(im, N / 2, N / 2, 9, (255, 230, 160)); d = ImageDraw.Draw(im); label(d, (N / 2 + 18, N / 2 + 8), "Soleil", 34, (245, 183, 0))
save("soleil_lointain", im, math.log10(3e15))
# 9. système solaire  10. planètes intérieures
UA = 1.496e11
def orbits(S, pl, earth_ang=-30, labels=True, sun_r=10):
    im = Image.new("RGB", (N, N), (2, 3, 8)); stars(im, 300, 1.0, 20, 100); im = glow(im, N / 2, N / 2, sun_r, (255, 220, 120)); d = ImageDraw.Draw(im); ex = ey = None
    for nm, au, col, ang in pl:
        r = au * UA / S * N
        if r > 2: d.ellipse([N / 2 - r, N / 2 - r, N / 2 + r, N / 2 + r], outline=(80, 95, 140), width=2)
        a = math.radians(earth_ang if nm == "Terre" else ang); x = N / 2 + r * math.cos(a); y = N / 2 + r * math.sin(a)
        if r > 2: d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=col)
        if nm == "Terre": ex, ey = x, y
        if labels and r > 30: label(d, (x + 10, y + 6), nm, 30)
    return im, d, ex, ey
PL = [("Mercure", 0.387, (180, 170, 150), 200), ("Vénus", 0.723, (230, 200, 120), 120), ("Terre", 1.0, (80, 150, 255), 0), ("Mars", 1.524, (220, 100, 60), 60),
      ("Jupiter", 5.2, (220, 180, 140), 150), ("Saturne", 9.58, (230, 210, 150), 250), ("Uranus", 19.2, (150, 220, 230), 20), ("Neptune", 30.1, (90, 120, 240), 300)]
S9 = 1.2e13; im, d, ex, ey = orbits(S9, PL); label(d, (N / 2 + 16, N / 2 - 40), "Soleil", 34, (245, 183, 0)); save("systeme_solaire", im, math.log10(S9))
S10 = 5e11; im, d, ex, ey = orbits(S10, PL[:4], sun_r=14); label(d, (N / 2 + 20, N / 2 - 44), "Soleil", 36, (245, 183, 0)); save("planetes_interieures", im, math.log10(S10), ex / N, ey / N)
# 11. la Terre et l'orbite de la Lune (petite échelle)  12. la Terre et la Lune
S11 = 2.5e10; im = Image.new("RGB", (N, N), (2, 3, 8)); stars(im, 250, 1.0, 20, 100); d = ImageDraw.Draw(im); r = 3.844e8 / S11 * N
d.ellipse([N / 2 - r, N / 2 - r, N / 2 + r, N / 2 + r], outline=(110, 120, 150), width=2); d.ellipse([N / 2 - 3, N / 2 - 3, N / 2 + 3, N / 2 + 3], fill=(90, 150, 255)); label(d, (N / 2 + 30, N / 2 + 10), "Terre", 34)
save("terre_lointaine", im, math.log10(S11))
S12 = 1.2e9; im = Image.new("RGB", (N, N), (2, 3, 8)); stars(im, 250, 1.0, 20, 100); d = ImageDraw.Draw(im); r = 3.844e8 / S12 * N
d.ellipse([N / 2 - r, N / 2 - r, N / 2 + r, N / 2 + r], outline=(110, 120, 150), width=2)
paste_globe(im, ortho_globe(earth, LAT, LON, 1.2742e7 / S12 * N, 40), N / 2, N / 2)
mx, my = N / 2 + r * math.cos(math.radians(-40)), N / 2 + r * math.sin(math.radians(-40)); rm = max(3, 3.47e6 / S12 * N / 2); d.ellipse([mx - rm, my - rm, mx + rm, my + rm], fill=(190, 190, 185))
label(d, (N / 2 + 26, N / 2 + 10), "Terre", 34); label(d, (mx + 12, my - 10), "Lune", 34); save("terre_lune", im, math.log10(S12))
# 13. la Terre vue de l'espace, centrée sur Halluin
D13 = 0.8; im = Image.new("RGB", (N, N), (2, 3, 8)); stars(im, 300, 1.0, 20, 110); paste_globe(im, ortho_globe(earth, LAT, LON, N * D13, N), N / 2, N / 2)
save("terre", im, math.log10(1.2742e7 / D13))
# 14+ : images satellites (Sentinel-2 cloudless EOX, CC BY 4.0) puis orthophotos IGN (Licence Ouverte)
import math as m_
def res(z): return 156543.03392 * m_.cos(m_.radians(LAT)) / 2 ** z
def eox(z): return Image.open(f"{IGN}/eox{z}.jpg").convert("RGB")
for z in (7, 9, 11, 13): save(f"sat{z}", eox(z), math.log10(res(z) * 2048))
def ign_fill(z):
    a = np.asarray(Image.open(f"{IGN}/z{z}.jpg").convert("RGB")).astype(int)
    # sous-couche Sentinel-2 agrandie (Belgique hors couverture IGN, dalles manquantes)
    f = 2 ** (z - 14); b = eox(14); c = 1024; w = 2048 / f; base = np.asarray(b.crop((c - w / 2, c - w / 2, c + w / 2, c + w / 2)).resize((2048, 2048), Image.BICUBIC)).astype(int)
    hole = ((a[..., 0] > 245) & (a[..., 1] > 245) & (a[..., 2] > 245)) | ((a[..., 0] > 240) & (a[..., 1] < 20) & (a[..., 2] > 240))
    hm = Image.fromarray((hole * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(4)); k = np.asarray(hm).astype(float)[..., None] / 255
    return Image.fromarray((a * (1 - k) + base * k).astype(np.uint8))
for z in (15, 17, 19): save(f"ign{z}", ign_fill(z), math.log10(res(z) * 2048))
cour = ign_fill(19); c = 1024; w = 512; court = cour.crop((c - w // 2, c - w // 2, c + w // 2, c + w // 2)); save("cour", court, math.log10(res(19) * w))
# toi (élève allongé dans la cour, vu de dessus) : 4 m
S = 4.0; g = cour.crop((c - 11, c - 11, c + 11, c + 11)).resize((N, N), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6)); a = np.asarray(g).astype(float)
a = a * 0.9 + (rng.random((N, N, 1)) * 18 - 9); im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(im)
px = N / S  # pixels par mètre ; la joue est au centre
hx, hy = N / 2 - 0.06 * px, N / 2 + 0.03 * px
body = (hx + 0.12 * px, hy); d.ellipse([hx - 0.11 * px, hy - 0.13 * px, hx + 0.11 * px, hy + 0.13 * px], fill=(232, 190, 160))
d.ellipse([hx - 0.12 * px, hy - 0.15 * px, hx + 0.02 * px, hy + 0.15 * px], fill=(70, 45, 30))
d.rounded_rectangle([hx + 0.1 * px, hy - 0.24 * px, hx + 0.72 * px, hy + 0.24 * px], radius=int(0.1 * px), fill=(30, 90, 170))
d.rounded_rectangle([hx + 0.7 * px, hy - 0.2 * px, hx + 1.55 * px, hy - 0.02 * px], radius=int(0.08 * px), fill=(40, 45, 60)); d.rounded_rectangle([hx + 0.7 * px, hy + 0.02 * px, hx + 1.55 * px, hy + 0.2 * px], radius=int(0.08 * px), fill=(40, 45, 60))
d.rounded_rectangle([hx + 0.15 * px, hy - 0.42 * px, hx + 0.7 * px, hy - 0.3 * px], radius=int(0.05 * px), fill=(30, 90, 170)); d.rounded_rectangle([hx + 0.15 * px, hy + 0.3 * px, hx + 0.7 * px, hy + 0.42 * px], radius=int(0.05 * px), fill=(30, 90, 170))
d.ellipse([hx + 0.62 * px, hy - 0.44 * px, hx + 0.74 * px, hy - 0.3 * px], fill=(232, 190, 160)); d.ellipse([hx + 0.62 * px, hy + 0.3 * px, hx + 0.74 * px, hy + 0.44 * px], fill=(232, 190, 160))
im = im.filter(ImageFilter.GaussianBlur(1.2)); save("toi", im, math.log10(S))
# peau (3 cm puis 3 mm) : texture procédurale
def skin(scale, ridge):
    yy, xx = np.mgrid[0:N, 0:N] / N; base = np.array([226, 182, 152], float)
    n1 = np.asarray(Image.fromarray((rng.random((64, 64)) * 255).astype(np.uint8)).resize((N, N), Image.BICUBIC)).astype(float) / 255
    n2 = np.asarray(Image.fromarray((rng.random((256, 256)) * 255).astype(np.uint8)).resize((N, N), Image.BICUBIC)).astype(float) / 255
    a = base[None, None, :] * (0.92 + 0.1 * n1[..., None]) * (0.95 + 0.06 * n2[..., None])
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(im, "RGBA")
    for _ in range(ridge):
        x0, y0 = rng.uniform(0, N, 2); ang = rng.uniform(0, 6.28); L = rng.uniform(80, 400); pts = [(x0, y0)]
        for k in range(12): ang += rng.normal(0, 0.15); x0 += math.cos(ang) * L / 12; y0 += math.sin(ang) * L / 12; pts.append((x0, y0))
        d.line(pts, fill=(170, 120, 100, 90), width=int(rng.uniform(2, 5)))
    for _ in range(scale):
        x, y = rng.uniform(0, N, 2); r = rng.uniform(3, 9); d.ellipse([x - r, y - r, x + r, y + r], fill=(160, 110, 95, 110))
    return im.filter(ImageFilter.GaussianBlur(1.5))
save("peau_3cm", skin(140, 160), math.log10(0.03))
im = skin(30, 40); d = ImageDraw.Draw(im, "RGBA")
for _ in range(900):
    x, y = rng.uniform(0, N, 2); r = rng.uniform(14, 30); pts = [(x + r * math.cos(t) * rng.uniform(0.8, 1.2), y + r * math.sin(t) * rng.uniform(0.8, 1.2)) for t in np.linspace(0, 6.28, 7)[:-1]]
    d.polygon(pts, outline=(180, 130, 110, 120))
save("peau_3mm", im.filter(ImageFilter.GaussianBlur(1)), math.log10(0.003))
# cellules de la joue (microscope, CC0) centrées sur le noyau de la cellule
ck = Image.open(f"{A2}/cheek.jpg"); sx = ck.width / 900; cx0, cy0 = 450 * sx, 297 * sx; side = ck.height
im = Image.new("RGB", (side, side), (0, 0, 0)); im.paste(ck.crop((int(cx0 - side / 2), 0, int(cx0 + side / 2), side)), (0, 0))
save("cellules_joue", im, math.log10(225e-6), 0.5, cy0 / side)
# une cellule (HeLa, CC BY-SA 4.0) centrée sur son noyau : 10 µm = 72 px sur 900
he = Image.open(f"{A2}/hela.jpg"); k = he.width / 900; c0 = (450 * k, 440 * k); w = 400 * k
save("cellule", he.crop((int(c0[0] - w / 2), int(c0[1] - w / 2), int(c0[0] + w / 2), int(c0[1] + w / 2))), math.log10(400 / 72 * 10e-6))
# noyau de la cellule (procédural, bleu comme en fluorescence)
im = Image.new("RGB", (N, N), (0, 0, 0)); a = np.zeros((N, N, 3)); yy, xx = np.mgrid[0:N, 0:N]; X = (xx - N / 2) / (N * 0.42); Y = (yy - N / 2) / (N * 0.3); r = X * X + Y * Y
n = np.asarray(Image.fromarray((rng.random((90, 90)) * 255).astype(np.uint8)).resize((N, N), Image.BICUBIC)).astype(float) / 255
m = np.clip((1 - r) * 6, 0, 1); a[..., 2] = (120 + 120 * n) * m; a[..., 0] = 20 * n * m; a[..., 1] = 30 * n * m
save("noyau_cellule", Image.fromarray(a.astype(np.uint8)).filter(ImageFilter.GaussianBlur(2)), math.log10(2.2e-5))
# ADN enroulé (perles sur un fil)
im = Image.new("RGB", (N, N), (4, 6, 22)); d = ImageDraw.Draw(im); t = np.linspace(0, 1, 2000)
for k in range(5):
    phase = rng.uniform(0, 6.28); yc = N * (0.15 + 0.17 * k); pts = [(N * u, yc + 120 * math.sin(6 * math.pi * u + phase) + 40 * math.sin(23 * u + k)) for u in t]
    d.line(pts, fill=(120, 150, 230), width=8)
    for u in np.linspace(0.03, 0.97, 9):
        x, y = N * u, yc + 120 * math.sin(6 * math.pi * u + phase) + 40 * math.sin(23 * u + k); d.ellipse([x - 38, y - 38, x + 38, y + 38], fill=(180, 120, 200), outline=(230, 190, 240), width=4)
label(d, (40, 40), "ADN enroulé autour de protéines", 44)
save("adn_enroule", im.filter(ImageFilter.GaussianBlur(1)), math.log10(3e-7))
# double hélice d'ADN (rendu 2D), puis atomes de l'ADN
im = Image.new("RGB", (N, N), (4, 6, 22)); d = ImageDraw.Draw(im); cols = [(230, 70, 60), (60, 140, 230), (240, 190, 40), (60, 180, 100)]
for i in range(140):
    u = i / 139; x = N * u; ph = u * 2 * math.pi * 3.3
    y1, y2 = N / 2 + 300 * math.sin(ph), N / 2 - 300 * math.sin(ph); z1 = math.cos(ph)
    if i % 4 == 0: c = cols[(i // 4) % 4]; d.line([(x, y1), (x, (y1 + y2) / 2)], fill=c, width=14); d.line([(x, (y1 + y2) / 2), (x, y2)], fill=cols[((i // 4) % 4) ^ 1], width=14)
for i in range(400):
    u = i / 399; x = N * u; ph = u * 2 * math.pi * 3.3
    for s in (1, -1):
        y = N / 2 + s * 300 * math.sin(ph); sh = 0.65 + 0.35 * s * math.cos(ph); d.ellipse([x - 22, y - 22, x + 22, y + 22], fill=tuple(int(c * sh) for c in (215, 220, 235)))
save("adn_helice", im, math.log10(6e-9))
im = Image.new("RGB", (N, N), (4, 6, 22)); a = np.asarray(im).astype(float); yy, xx = np.mgrid[0:N, 0:N]
AT = [((40, 40, 40), 150), ((225, 40, 30), 140), ((40, 80, 220), 145), ((240, 240, 240), 105), ((235, 150, 30), 170)]
pts = []
for _ in range(170):
    pts.append((rng.uniform(-100, N + 100), rng.uniform(-100, N + 100), AT[rng.choice([0, 0, 0, 1, 1, 2, 3, 3, 3, 4], p=None)], rng.uniform(0, 1)))
pts.append((N / 2, N / 2, AT[0], 2.0))
for x, y, (col, r), zd in sorted(pts, key=lambda p: p[3]):
    d2 = ((xx - x) ** 2 + (yy - y) ** 2) / (r * r); m = d2 < 1; sh = np.sqrt(np.clip(1 - d2, 0, 1)) * (0.6 + 0.4 * np.clip(1 - ((xx - x + r * 0.35) ** 2 + (yy - y + r * 0.35) ** 2) / (r * r), 0, 1))
    a[m] = (np.array(col)[None, :] * (0.35 + 0.75 * sh[m][:, None])).clip(0, 255)
save("atomes", Image.fromarray(a.astype(np.uint8)), math.log10(1.5e-9))
# atome de carbone : nuage d'électrons
im = np.zeros((N, N, 3)); X = (xx - N / 2) / N; Y = (yy - N / 2) / N; r = np.sqrt(X * X + Y * Y)
cl = np.exp(-r / 0.09) * 0.9 + np.exp(-((r - 0.25) / 0.07) ** 2) * 0.55; n = np.asarray(Image.fromarray((rng.random((200, 200)) * 255).astype(np.uint8)).resize((N, N), Image.BICUBIC)).astype(float) / 255
im[..., 0] = 40 * cl * (0.7 + 0.6 * n); im[..., 1] = 120 * cl * (0.7 + 0.6 * n); im[..., 2] = 255 * cl * (0.7 + 0.6 * n)
im = Image.fromarray(np.clip(im, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(im); label(d, (N / 2, N * 0.12), "Atome de carbone : nuage de 6 électrons", 44, anchor="ma")
save("atome", im, math.log10(4e-10))
# le vide de l'atome, puis le noyau qui apparaît
for nm, S, rg, lab in [("vide", 6e-12, 2.5, "… du vide …"), ("vers_noyau", 1.6e-13, 9, "noyau")]:
    im = np.zeros((N, N, 3)); haze = 0.18 * np.exp(-r / 0.6); im[..., 0] = 25 * haze; im[..., 1] = 60 * haze; im[..., 2] = 140 * haze
    im = Image.fromarray(np.clip(im * 1.0, 0, 255).astype(np.uint8)); im = glow(im, N / 2, N / 2, rg, (255, 90, 60)); d = ImageDraw.Draw(im)
    label(d, (N / 2, N / 2 + 60 if lab == "noyau" else N * 0.3), lab, 48 if lab != "noyau" else 36, (230, 230, 255), anchor="ma"); save(nm, im, math.log10(S))
# noyau de carbone : 6 protons, 6 neutrons ; un proton au centre exact
S = 9e-15; R = 0.85e-15 / S * N; P = [np.array([0.0, 0.0, 1.0])]
while len(P) < 12:
    v = rng.normal(0, 1, 3); v = v / np.linalg.norm(v) * rng.uniform(1.4, 2.1) * R
    if all(np.linalg.norm(v - q) > 1.6 * R for q in P): P.append(v)
a = np.zeros((N, N, 3)); a[..., 2] = 18; a[..., 0] = 10; zbuf = np.full((N, N), -1e9)
for k, p in enumerate(P):
    col = np.array((225, 70, 60) if k % 2 == 0 else (150, 160, 180)); x, y, zz = N / 2 + p[0], N / 2 + p[1], p[2]
    d2 = ((xx - x) ** 2 + (yy - y) ** 2) / (R * R); m = d2 < 1; h = zz + R * np.sqrt(np.clip(1 - d2, 0, 1)); m &= h > zbuf; zbuf[m] = h[m]
    sh = 0.45 + 0.6 * np.sqrt(np.clip(1 - d2, 0, 1)); a[m] = (col[None, :] * sh[m][:, None]).clip(0, 255)
im = Image.fromarray(a.astype(np.uint8)); d = ImageDraw.Draw(im); label(d, (N / 2, N * 0.08), "Noyau de carbone : 6 protons (rouges) et 6 neutrons (gris)", 40, anchor="ma")
save("noyau_atome", im, math.log10(S))
# le proton : 3 quarks (u, u, d) liés par les gluons
S = 2.3e-15; im = np.zeros((N, N, 3)); r2 = np.sqrt(((xx - N / 2) ** 2 + (yy - N / 2) ** 2)) / (N * 0.37)
glw = np.clip(1 - r2, 0, 1) ** 0.7; im[..., 0] = 200 * glw; im[..., 1] = 70 * glw; im[..., 2] = 80 * glw
im = Image.fromarray(np.clip(im, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(im)
Q = [(N / 2 + 180 * math.cos(a_), N / 2 + 180 * math.sin(a_)) for a_ in (math.radians(-90), math.radians(30), math.radians(150))]
for i in range(3):
    (x1, y1), (x2, y2) = Q[i], Q[(i + 1) % 3]; pts = []
    for s_ in np.linspace(0, 1, 60):
        x, y = x1 + (x2 - x1) * s_, y1 + (y2 - y1) * s_; nx, ny = -(y2 - y1), (x2 - x1); L = math.hypot(nx, ny); w = 18 * math.sin(s_ * math.pi * 14); pts.append((x + nx / L * w, y + ny / L * w))
    d.line(pts, fill=(245, 210, 70), width=6)
for (x, y), q in zip(Q, ["u", "u", "d"]):
    col = (235, 70, 60) if q == "u" else (60, 110, 230); d.ellipse([x - 70, y - 70, x + 70, y + 70], fill=col, outline=(255, 255, 255), width=5); d.text((x, y), q, font=font(80), fill=(255, 255, 255), anchor="mm")
label(d, (N / 2, N * 0.07), "Le proton : 2 quarks u et 1 quark d", 48, anchor="ma"); label(d, (N / 2, N * 0.9), "Le neutron, lui, contient 1 quark u et 2 quarks d", 38, (220, 220, 240), anchor="ma")
save("proton", im, math.log10(S))
json.dump(LV, open(f"{OUT}/quilt.json", "w"), ensure_ascii=False, indent=1)
for l in LV: print(f"{l['name']:22s} e={l['e']:7.2f} c=({l['cx']:.3f},{l['cy']:.3f})")
