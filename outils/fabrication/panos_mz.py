import numpy as np, cv2
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
exec(open("/home/claude/versailles/panos.py").read().split("\ndef save(")[0])
def fill(path, center_el, sky=None):
    im = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    s = W / im.shape[1]; band = cv2.resize(im, (W, int(im.shape[0] * s)), interpolation=cv2.INTER_AREA); bh = band.shape[0]
    vdeg = bh / W * 360; top = max(int((0.5 - (center_el + vdeg / 2) / 180) * H), 0)
    out = stretch_fill(band, top, bh, W, H, 40, 120)
    nb = H - top - bh
    if nb > 0:
        med = np.median(band[-80:], axis=0)            # une ligne : médiane par colonne
        row = cv2.blur(med[None], (301, 1))[0]
        mean = band[-80:].reshape(-1, 3).mean(0)
        res = np.empty((nb, W, 3), np.float32)
        for i in range(nb):
            t = i / nb; kk = int(301 + t * 2500) | 1
            r = cv2.blur(row[None], (kk, 1))[0] if i % 8 == 0 else r
            res[i] = r * (1 - min(1, t * 1.4) * 0.8) + mean * (min(1, t * 1.4) * 0.8)
        f = 60; ramp = np.linspace(0, 1, f)[:, None, None]
        res[:f] = band[-f:] * (1 - ramp) + res[:f] * ramp
        res = cv2.GaussianBlur(res, (1, 31), 0); res[:f] = band[-f:] * (1 - ramp) + res[:f] * ramp
        out[top + bh:] = res
    if sky is not None:
        sk = cv2.resize(np.asarray(Image.open(sky).convert("RGB")).astype(np.float32), (W, H)); f = 320
        rp = np.clip((top + f - np.arange(H)) / (2 * f), 0, 1)[:, None, None]
        ref = band[:20].reshape(-1, 3).mean(0); sref = sk[max(0, top - 30):max(30, top)].reshape(-1, 3).mean(0)
        out = out * (1 - rp) + sk * (ref / np.maximum(sref, 1)) * rp
    return np.clip(out, 0, 255).astype(np.uint8)
def save(a, p): Image.fromarray(a).save(p, quality=92); print(p)
P = "/home/claude/mzmed/medias/panos"; SKY = "/home/claude/lgmed/medias/panos/kloofendal_48d_partly_cloudy_puresky.jpg"
save(fill(f"{P}/residenz.jpg", 12.0, SKY), "/home/claude/mozart/pano_residenz.jpg")
save(fill(f"{P}/schoenbrunn.jpg", 3.0, SKY), "/home/claude/mozart/pano_schoenbrunn.jpg")
save(fill(f"{P}/dom.jpg", 6.0), "/home/claude/mozart/pano_dom.jpg")
save(fill(f"{P}/stpeter.jpg", 8.0), "/home/claude/mozart/pano_stpeter.jpg")
