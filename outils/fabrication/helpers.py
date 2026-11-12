"""Assemble le cours « La Révolution française » au format Atelier 360 (.json)."""
import json, base64, io, uuid, sys
from PIL import Image

M = "/home/claude/ww1/med/medias"
LIM = {"intro": 400, "text": 400, "question": 240, "option": 90, "explanation": 300}
errors = []

def uid(): return uuid.uuid4().hex[:12]

def durl(im, q):
    b = io.BytesIO(); im.save(b, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

def pano(path):
    im = Image.open(path).convert("RGB").resize((4096, 2048), Image.LANCZOS)
    return {"type": "image", "data": durl(im, 86), "thumb": durl(im.resize((256, 128), Image.LANCZOS), 70), "name": path.split("/")[-1]}

def art(key):
    im = Image.open(f"{M}/arts/{key}.jpg").convert("RGB")
    s = min(1, 1280 / im.width, 1280 / im.height)
    if s < 1: im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    return durl(im, 85)

def check(h, where):
    for k in ("text", "question", "explanation"):
        if k in h and len(h[k]) > LIM[k]: errors.append(f"{where} {k} {len(h[k])} > {LIM[k]} : {h[k][:50]}")
    for o in h.get("options", []):
        if len(o) > LIM["option"]: errors.append(f"{where} option trop longue : {o}")
    return h

def info(title, text, az, el, img=None, **kw):
    h = {"id": uid(), "type": "info", "title": title, "text": text, "az": az, "el": el}
    if img: h["image"] = art(img)
    h.update(kw); return check(h, title)

def quiz(title, q, opts, ans, ex, az, el, **kw):
    h = {"id": uid(), "type": "quiz", "title": title, "question": q, "options": opts, "answer": ans, "explanation": ex, "az": az, "el": el}
    h.update(kw); return check(h, title)

def vf(q, ans_true, ex, az, el, **kw):
    h = {"id": uid(), "type": "quiz", "vf": True, "title": "Vrai ou faux", "question": q, "options": ["Vrai", "Faux"], "answer": 0 if ans_true else 1, "explanation": ex, "az": az, "el": el}
    h.update(kw); return check(h, q[:30])

def order(title, q, items, ex, az, el):
    return check({"id": uid(), "type": "order", "title": title, "question": q, "items": items, "explanation": ex, "az": az, "el": el}, title)

def match(title, q, pairs, ex, az, el):
    for a, b in pairs:
        if len(a) > 90 or len(b) > 90: errors.append("paire longue " + a)
    return check({"id": uid(), "type": "match", "title": title, "question": q, "pairs": pairs, "explanation": ex, "az": az, "el": el}, title)

def find(q, taz, tel, ex, az, el, tol=14):
    return check({"id": uid(), "type": "find", "title": "Défi", "question": q, "tAz": taz, "tEl": tel, "tol": tol, "explanation": ex, "az": az, "el": el}, q[:30])

def scene(name, env, intro, hots):
    if len(intro) > LIM["intro"]: errors.append(f"intro {name} {len(intro)}")
    return {"id": uid(), "name": name, "env": env, "intro": intro, "hotspots": hots}

