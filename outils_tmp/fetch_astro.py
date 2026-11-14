import json, os, time, urllib.parse, urllib.request, io
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "Atelier360-medias/1.0 (cours SVT; https://github.com/lefebvrepascal/atelier-360)"}
def get(url):
    for k in range(5):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180).read()
        except Exception as e: print("retry", url[:90], e); time.sleep(5*(k+1))
    raise RuntimeError("échec "+url)
def api(**p):
    p.update(action="query", format="json"); return json.loads(get("https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(p)))
IIP = dict(prop="imageinfo", iiprop="url|size|extmetadata|mime", iiextmetadatafilter="Artist|LicenseShortName")
def info(title):
    p = list(api(titles="File:"+title, **IIP)["query"]["pages"].values())[0]
    return p.get("imageinfo", [None])[0]
def search(q, n=30):
    r = api(generator="search", gsrsearch=q, gsrnamespace=6, gsrlimit=n, **IIP)
    out = []
    for p in r.get("query", {}).get("pages", {}).values():
        ii = p.get("imageinfo", [None])[0]
        if ii: out.append((p["title"][5:], ii, p.get("index", 99)))
    return [(t, ii) for t, ii, _ in sorted(out, key=lambda x: x[2])]
os.makedirs("medias/tex", exist_ok=True); os.makedirs("medias/panos", exist_ok=True); os.makedirs("medias/cand", exist_ok=True)
credits = {}
def meta(t, ii):
    m = ii.get("extmetadata", {}); return {"file": t, "page": ii.get("descriptionurl"), "artist": m.get("Artist", {}).get("value", ""), "license": m.get("LicenseShortName", {}).get("value", ""), "size": [ii["width"], ii["height"]]}
QUERIES = {
 "lune": ["Apollo 360 panorama", "lunar surface 360 panorama", "Chang'e 360 panorama Moon", "Apollo equirectangular", "Moon 360 VR panorama Apollo 17", "Yutu panorama 360", "Apollo 16 panorama 360", "Apollo 12 panorama 360"],
 "planetarium": ["planetarium 360 panorama equirectangular", "Cité de l'espace panorama 360", "observatory 360 equirectangular telescope dome"],
}
seen = set(); cand = {}
for grp, qs in QUERIES.items():
    n = 0
    for q in qs:
        try: res = search(q)
        except Exception as e: print("search fail", q, e); continue
        for t, ii in res:
            if t in seen: continue
            w, h = ii["width"], ii["height"]
            if not ii.get("mime", "").startswith("image/jpeg") and not ii.get("mime", "").startswith("image/png"): continue
            if h == 0 or not (1.95 <= w/h <= 2.05) or w < 4000: continue
            seen.add(t); n += 1
            key = f"{grp}_{n}"
            try:
                im = Image.open(io.BytesIO(get(ii["url"]))).convert("RGB")
            except Exception as e: print("dl fail", t, e); continue
            im.resize((8192, 4096) if im.width >= 6000 else (4096, 2048), Image.LANCZOS).save(f"medias/panos/{key}.jpg", quality=90)
            im.resize((1024, 512), Image.LANCZOS).save(f"medias/cand/{key}.jpg", quality=80)
            cand[key] = meta(t, ii); print("pano", key, t, w, h); time.sleep(0.3)
            if n >= 5: break
        if n >= 5: break
json.dump(credits, open("medias/credits.json", "w"), ensure_ascii=False, indent=1)
json.dump(cand, open("medias/candidats.json", "w"), ensure_ascii=False, indent=1)
