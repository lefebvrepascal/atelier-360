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
TEX = ["sun", "mercury", "venus atmosphere", "venus surface", "earth daymap", "earth clouds", "moon", "mars", "jupiter", "saturn", "saturn ring alpha", "uranus", "neptune", "stars milky way"]
for k in TEX:
    t = "Solarsystemscope texture 2k %s.jpg" % k
    ii = info(t)
    if not ii and "ring" in k:
        t = t[:-4] + ".png"; ii = info(t)
    if not ii:
        c = search('Solarsystemscope texture %s' % k, 10)
        if not c: print("ABSENT", k); continue
        t, ii = c[0]
    raw = get(ii["url"]); im = Image.open(io.BytesIO(raw))
    key = k.replace(" ", "_")
    if "ring" in k: im.convert("RGBA").save(f"medias/tex/{key}.png", optimize=True)
    else:
        im = im.convert("RGB"); s = min(1, 2048/im.width); im = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS); im.save(f"medias/tex/{key}.jpg", quality=90)
    credits["tex_"+key] = meta(t, ii); print("tex", key, t, im.size); time.sleep(0.3)
QUERIES = {
 "mars": ["Curiosity rover 360 panorama equirectangular", "Mars panorama equirectangular", "Mars 360 panorama Perseverance", "Gale crater panorama 360"],
 "lune": ["Apollo panorama equirectangular", "Moon surface 360 panorama", "Apollo 17 panorama Taurus-Littrow", "Apollo 11 panorama Tranquility base 360"],
 "espace": ["Milky Way 360 panorama equirectangular", "night sky equirectangular panorama stars", "ESO 360 panorama Paranal night"],
 "observatoire": ["observatory dome interior panosphere", "planetarium interior 360 panorama", "Observatoire panosphere"],
 "terre": ["ISS 360 panorama equirectangular", "Earth from space 360 equirectangular"],
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
