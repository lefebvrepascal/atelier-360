import json, os, time, urllib.parse, urllib.request, io
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "Atelier360-medias/1.0 (cours de SVT; https://github.com/lefebvrepascal/atelier-360)"}
def get(url, tries=4):
    for k in range(tries):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300).read()
        except Exception as e: print("retry", url[:90], e); time.sleep(4 * (k + 1))
def api(**q):
    q.update(format="json"); r = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(q)); return json.loads(r) if r else {}
os.makedirs("medias/cand", exist_ok=True)
def thumb(url, path, w=None):
    b = get(url)
    if not b: return False
    try: Image.open(io.BytesIO(b)).convert("RGB").save(path, quality=78); return True
    except Exception as e: print("img", e); return False
def commons(qs, pano, n, tag):
    seen, out = set(), []
    for q in qs:
        d = api(action="query", generator="search", gsrsearch=q, gsrnamespace=6, gsrlimit=25, prop="imageinfo", iiprop="url|size|extmetadata|mime", iiurlwidth=500,
                iiextmetadatafilter="Artist|LicenseShortName|ImageDescription")
        pages = sorted(d.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
        k = 0
        for p in pages:
            t = p["title"]
            if t in seen or "imageinfo" not in p: continue
            ii = p["imageinfo"][0]; w, h = ii.get("width", 0), ii.get("height", 1)
            if not ii.get("mime", "").startswith(("image/jpeg", "image/png")): continue
            if pano and (w < 4000 or not (1.95 < w / h < 2.05)): continue
            if not pano and min(w, h) < 500: continue
            seen.add(t); m = ii.get("extmetadata", {})
            key = "%s%03d" % (tag, len(out))
            rec = {"k": key, "q": q, "title": t[5:], "w": w, "h": h, "lic": m.get("LicenseShortName", {}).get("value", ""), "artist": m.get("Artist", {}).get("value", "")[:200]}
            if thumb(ii.get("thumburl", ii["url"]), f"medias/cand/{key}.jpg"): out.append(rec); k += 1
            if k >= n: break
        time.sleep(0.2)
    return out
ARTQ = {}
PANOQ = ["Chicago panosphere", "Chicago 360°", "Navy Pier panorama equirectangular", "Millennium Park panosphere", "Chicago Riverwalk 360", "Mapillary Chicago",
 "Glacier National Park panosphere", "Yellowstone panosphere", "Rocky Mountain National Park 360", "Lemhi Pass", "Cape Disappointment panorama", "Great Falls Missouri River",
 "Uluru panosphere", "Sydney Harbour panosphere", "Circular Quay 360", "Sydney Opera House 360°", "Melbourne panosphere",
 "Waitangi Treaty Grounds", "Rotorua panosphere", "Auckland panosphere", "Tongariro 360", "New Zealand panosphere beach",
 "Selma Alabama panorama", "Montgomery Alabama panosphere", "diner panosphere", "Ellis Island 360"]
res = {}
for tag, qs in ARTQ.items(): res[tag] = commons(qs, False, 2, tag); print(tag, len(res[tag]))
res["pano"] = commons(PANOQ, True, 2, "pnb"); print("pano", len(res["pano"]))
ph = get("https://api.polyhaven.com/assets?t=hdris")
d = json.loads(ph) if ph else {}
phs = []
for k, v in d.items():
    txt = " ".join([k, v.get("name", "")] + v.get("tags", []) + v.get("categories", [])).lower()
    if any(w in txt for w in ("mountain", "desert", "coast", "beach", "canyon", "prairie", "river", "lake", "diner", "factory", "industrial", "cliff", "bay", "valley", "plain", "savanna", "road", "highway", "city", "urban", "skyscraper", "harbor", "port")):
        if thumb(f"https://cdn.polyhaven.com/asset_img/thumbs/{k}.png?width=512&height=256", f"medias/cand/ph_{k}.jpg"): phs.append(k)
res["polyhaven"] = phs; print("ph", len(phs))
json.dump(res, open("medias/cand/cand.json", "w"), ensure_ascii=False, indent=1)
