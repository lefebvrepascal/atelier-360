import json, os, time, urllib.parse, urllib.request, io
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "Atelier360-medias/1.0 (cours de géographie; https://github.com/lefebvrepascal/atelier-360)"}
def get(url, tries=5):
    for k in range(tries):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300).read()
        except Exception as e: print("retry", url[:90], e); time.sleep(5 * (k + 1))
    raise RuntimeError(url)
for d in ("arts", "panos", "cand"): os.makedirs("medias/" + d, exist_ok=True)
def search(q, n=30, w=1600):
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "format": "json", "generator": "search", "gsrsearch": q, "gsrnamespace": 6, "gsrlimit": n, "prop": "imageinfo", "iiprop": "url|size|extmetadata|mime", "iiextmetadatafilter": "Artist|LicenseShortName", "iiurlwidth": w})
    return sorted(json.loads(get(u)).get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
cr = {}; seen = set()
ARTQ = json.load(open("outils_tmp/g6_q.json"))
for tag, qs in ARTQ["arts"].items():
    for i, q in enumerate(qs):
        try: pages = search(q)
        except Exception as e: print("err", q, e); continue
        for p in pages:
            ii = p.get("imageinfo", [{}])[0]
            if p["title"] in seen or not ii.get("mime", "").startswith(("image/jpeg", "image/png")) or min(ii.get("width", 0), ii.get("height", 0)) < 600: continue
            seen.add(p["title"]); k = f"{tag}{i:02d}"
            try:
                im = Image.open(io.BytesIO(get(ii["thumburl"]))).convert("RGB"); im.save(f"medias/arts/{k}.jpg", quality=88)
                m = ii.get("extmetadata", {}); cr[k] = {"q": q, "file": p["title"][5:], "license": m.get("LicenseShortName", {}).get("value", ""), "artist": m.get("Artist", {}).get("value", "")[:200]}
                print(k, p["title"][:60]); break
            except Exception as e: print(e)
        time.sleep(0.2)
n = 0
for q in ARTQ["panos"]:
    try: pages = search(q, 40, 4096)
    except Exception as e: print("err", q, e); continue
    k2 = 0
    for p in pages:
        ii = p.get("imageinfo", [{}])[0]; w, h = ii.get("width", 0), ii.get("height", 1)
        if p["title"] in seen or w < 4000 or not (1.95 < w / h < 2.05): continue
        seen.add(p["title"]); k = f"gp{n:03d}"; n += 1
        try: im = Image.open(io.BytesIO(get(ii["thumburl"]))).convert("RGB")
        except Exception as e: print(e); continue
        im.save(f"medias/panos/{k}.jpg", quality=88); im.resize((512, 256)).save(f"medias/cand/{k}.jpg", quality=75)
        m = ii.get("extmetadata", {}); cr[k] = {"q": q, "file": p["title"][5:], "license": m.get("LicenseShortName", {}).get("value", ""), "artist": m.get("Artist", {}).get("value", "")[:200]}
        print(k, q, p["title"][:60]); k2 += 1
        if k2 >= 2: break
    time.sleep(0.3)
for hname in ARTQ["ph"]:
    try:
        f = json.loads(get("https://api.polyhaven.com/files/" + hname)); url = f.get("tonemapped", {}).get("url")
        im = Image.open(io.BytesIO(get(url))).convert("RGB"); im = im.resize((4096, 2048), Image.LANCZOS)
        im.save(f"medias/panos/{hname}.jpg", quality=90); im.resize((512, 256)).save(f"medias/cand/{hname}.jpg", quality=75); cr[hname] = {"file": hname, "license": "CC0", "artist": "Poly Haven"}; print(hname)
    except Exception as e: print("ph fail", hname, e)
json.dump(cr, open("medias/credits.json", "w"), ensure_ascii=False, indent=1)
