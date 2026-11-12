import json, os, time, urllib.parse, urllib.request, io
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "Atelier360-medias/1.0 (cours d'anglais; https://github.com/lefebvrepascal/atelier-360)"}
def get(url, tries=4):
    for k in range(tries):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=600).read()
        except Exception as e: print("retry", url[:90], e); time.sleep(5 * (k + 1))
def api(**q):
    q.update(format="json"); r = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(q)); return json.loads(r) if r else {}
os.makedirs("medias/cand", exist_ok=True); os.makedirs("medias/vosk", exist_ok=True)
Q = ["classroom equirectangular", "classroom 360 panorama", "classroom spherical panorama", "Klassenzimmer Kugelpanorama", "salle de classe panorama 360",
     "school equirectangular", "school 360 panorama interior", "Schule Kugelpanorama", "school library equirectangular", "lecture room equirectangular",
     "playground equirectangular", "schoolyard 360 panorama", "school canteen panorama 360", "school corridor equirectangular", "Klassenraum 360"]
seen, out = set(), []
for q in Q:
    d = api(action="query", list="search", srsearch=q, srnamespace=6, srlimit=40)
    for it in d.get("query", {}).get("search", []):
        t = it["title"]
        if t in seen: continue
        seen.add(t)
        p = api(action="query", titles=t, prop="imageinfo|categories", iiprop="url|size|extmetadata", iiurlwidth=900, cllimit=30,
                iiextmetadatafilter="Artist|LicenseShortName|ImageDescription")
        pg = list(p.get("query", {}).get("pages", {}).values())
        if not pg or "imageinfo" not in pg[0]: continue
        ii = pg[0]["imageinfo"][0]; w, h = ii.get("width", 0), ii.get("height", 1)
        if w < 3000 or not (1.85 < w / h < 2.15): continue
        m = ii.get("extmetadata", {})
        rec = {"q": q, "title": t, "w": w, "h": h, "url": ii["url"], "lic": m.get("LicenseShortName", {}).get("value", ""),
               "artist": m.get("Artist", {}).get("value", "")[:200], "desc": m.get("ImageDescription", {}).get("value", "")[:300],
               "cats": [c["title"] for c in pg[0].get("categories", [])]}
        k = "c%03d" % len(out); rec["k"] = k
        b = get(ii.get("thumburl", ii["url"]))
        if b:
            try: Image.open(io.BytesIO(b)).convert("RGB").save(f"medias/cand/{k}.jpg", quality=80)
            except Exception as e: print("img", e)
        out.append(rec); print(k, t, w, h, rec["lic"])
json.dump(out, open("medias/cand/commons.json", "w"), ensure_ascii=False, indent=1)
ph = get("https://api.polyhaven.com/assets?t=hdris&c=indoor")
if ph:
    d = json.loads(ph); json.dump({k: {"name": v.get("name"), "categories": v.get("categories"), "tags": v.get("tags"), "authors": v.get("authors")} for k, v in d.items()},
                                  open("medias/cand/polyhaven.json", "w"), ensure_ascii=False, indent=1)
    for k, v in d.items():
        txt = " ".join([k, v.get("name", "")] + v.get("tags", []) + v.get("categories", [])).lower()
        if any(w in txt for w in ("school", "class", "library", "office", "hall", "kitchen", "room", "gym", "corridor", "lecture")):
            b = get(f"https://cdn.polyhaven.com/asset_img/thumbs/{k}.png?width=640&height=320", 2)
            if b:
                try: Image.open(io.BytesIO(b)).convert("RGB").save(f"medias/cand/ph_{k}.jpg", quality=80)
                except Exception as e: print("ph", e)
for u in ["https://ccoreilly.github.io/vosk-browser/models/vosk-model-small-en-us-0.15.tar.gz"]:
    b = get(u)
    if b: open("medias/vosk/" + u.rsplit("/", 1)[1], "wb").write(b); print("vosk", len(b))
