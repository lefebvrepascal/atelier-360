"""SVT 5e « Le muscle à l'effort : énergie et circulation » — recherche et téléchargement de candidats (Commons, Poly Haven)."""
import json, os, time, urllib.parse, urllib.request, io, re
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "Atelier360-medias/1.0 (cours de SVT; https://github.com/lefebvrepascal/atelier-360)"}
def get(url, t=300):
    for k in range(5):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=t).read()
        except Exception as e: print("retry", url[:90], e); time.sleep(5 * (k + 1))
    print("ECHEC", url[:120]); return None
FREE = re.compile(r"public domain|^pd|cc0|cc by|cc-by|attribution", re.I)
def search(q, n, w=1600):
    p = urllib.parse.urlencode({"action": "query", "format": "json", "generator": "search", "gsrnamespace": 6, "gsrsearch": q, "gsrlimit": n,
        "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata", "iiurlwidth": w, "iiextmetadatafilter": "Artist|LicenseShortName|ImageDescription"})
    r = get("https://commons.wikimedia.org/w/api.php?" + p)
    if not r: return []
    pages = json.loads(r).get("query", {}).get("pages", {})
    return sorted(pages.values(), key=lambda p: p.get("index", 0))
IMG = {"coeur": ["heart diagram fr svg", "schéma coeur humain", "Heart diagram-fr"], "circ": ["appareil circulatoire schéma", "Circulatory System fr", "circulation sanguine schéma français", "double circulation sanguine"],
 "capil": ["capillary network blood vessels", "capillaries red blood cells micrograph", "artery vein capillary diagram"],
 "gr": ["red blood cells scanning electron micrograph", "erythrocytes SEM"], "debit": ["blood flow distribution rest exercise", "cardiac output exercise"],
 "therm": ["thermography human body exercise", "thermal image runner", "infrared thermography athlete"], "sueur": ["sweating athlete", "runner sweat"],
 "echo": ["echocardiogram heart", "stethoscope heart auscultation"], "harvey": ["William Harvey portrait", "Harvey De motu cordis veins"],
 "course": ["school cross country race children", "students running athletics track"], "poumon": ["alveoli capillaries diagram", "lungs diagram fr"],
 "mito": ["mitochondria muscle electron micrograph"], "veine": ["vein valves diagram", "artery cross section histology"]}
PANO = ["equirectangular stadium", "equirectangular athletics track", "360 panorama running track", "equirectangular gymnasium", "equirectangular sports hall", "Kugelpanorama Sporthalle", "equirectangular hospital", "equirectangular biology laboratory", "equirectangular school classroom science"]
VID = ["filetype:video heart beating animation", "filetype:video heart anatomy 3D", "filetype:video echocardiogram", "filetype:video blood flow capillary", "filetype:video red blood cells flowing", "filetype:video runner running slow motion", "filetype:video athletics race", "filetype:video blood circulation animation"]
for d in ("cand", "panos", "videos"): os.makedirs("medias/" + d, exist_ok=True)
idx = []; seen = set()
def meta(p):
    ii = p["imageinfo"][0]; m = ii.get("extmetadata", {})
    return ii, {"file": p["title"][5:], "artist": re.sub("<[^>]+>", "", m.get("Artist", {}).get("value", ""))[:150], "license": m.get("LicenseShortName", {}).get("value", ""),
        "desc": re.sub("<[^>]+>", "", m.get("ImageDescription", {}).get("value", ""))[:300], "w": ii.get("width"), "h": ii.get("height"), "mime": ii.get("mime"), "size": ii.get("size")}
k = 0
for grp, qs in IMG.items():
    for q in qs:
        for p in search(q, 10):
            if "imageinfo" not in p or p["title"] in seen: continue
            ii, md = meta(p)
            if not FREE.search(md["license"]) or not md["mime"].startswith("image"): continue
            seen.add(p["title"]); k += 1; key = f"{grp}_{k:03d}"
            b = get(ii.get("thumburl") or ii["url"])
            if not b: continue
            try: im = Image.open(io.BytesIO(b)).convert("RGB")
            except Exception as e: print("img", e); continue
            s = min(1, 1600 / max(im.size)); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS); im.save(f"medias/cand/{key}.jpg", quality=88)
            md.update(key=key, q=q); idx.append(md); time.sleep(0.2)
for q in PANO:
    for p in search(q, 12, 1024):
        if "imageinfo" not in p or p["title"] in seen: continue
        ii, md = meta(p)
        if not FREE.search(md["license"]) or not md["w"] or abs(md["w"] / md["h"] - 2) > 0.05 or md["w"] < 4000: continue
        seen.add(p["title"]); k += 1; key = f"pano_{k:03d}"
        b = get(ii.get("thumburl"))
        if b: Image.open(io.BytesIO(b)).convert("RGB").save(f"medias/cand/{key}.jpg", quality=85); md.update(key=key, q=q, url=ii["url"]); idx.append(md)
for q in VID:
    for p in search(q, 10, 640):
        if "imageinfo" not in p or p["title"] in seen: continue
        ii, md = meta(p)
        if not FREE.search(md["license"]): continue
        seen.add(p["title"]); k += 1; key = f"vid_{k:03d}"
        b = get(ii.get("thumburl")) if ii.get("thumburl") else None
        if b:
            try: Image.open(io.BytesIO(b)).convert("RGB").save(f"medias/cand/{key}.jpg", quality=85)
            except Exception: pass
        md.update(key=key, q=q, url=ii["url"]); idx.append(md)
        if md["size"] and md["size"] < 60e6:
            v = get(ii["url"], 900)
            if v: open(f"medias/videos/{key}." + ii["url"].rsplit(".", 1)[1], "wb").write(v)
# Poly Haven : panoramas sportifs, hôpital, labo
_all = json.loads(get("https://api.polyhaven.com/assets?t=hdris") or b"{}")
ph = [i for i, a in _all.items() if re.search(r"stadium|gym|sport|track|court|pitch|football|athlet|hospital|lab|school|classroom|hall", i + " " + " ".join(a.get("tags", [])) + " " + " ".join(a.get("categories", [])), re.I)]
for h in ph:
    f = json.loads(get("https://api.polyhaven.com/files/" + h) or b"{}"); url = f.get("tonemapped", {}).get("url")
    if not url: continue
    b = get(url)
    if not b: continue
    im = Image.open(io.BytesIO(b)).convert("RGB"); im.resize((1024, 512)).save(f"medias/cand/ph_{h}.jpg", quality=80)
    im = im.resize((8192, 4096), Image.LANCZOS) if im.width > 8192 else im; im.save(f"medias/panos/{h}.jpg", quality=90)
    idx.append({"key": "ph_" + h, "file": h, "artist": "Poly Haven", "license": "CC0"})
json.dump(idx, open("medias/index.json", "w"), ensure_ascii=False, indent=1)
print("candidats", len(idx))
