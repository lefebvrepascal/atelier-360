import json, os, time, urllib.parse, urllib.request, io
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "Atelier360-medias/1.0 (cours de SVT; https://github.com/lefebvrepascal/atelier-360)"}
def get(url, tries=5):
    for k in range(tries):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=600).read()
        except Exception as e: print("retry", url[:90], e); time.sleep(5 * (k + 1))
    raise RuntimeError(url)
def info(t):
    q = urllib.parse.urlencode({"action": "query", "format": "json", "titles": "File:" + t, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiextmetadatafilter": "Artist|LicenseShortName"})
    return list(json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))["query"]["pages"].values())[0]["imageinfo"][0]
P = json.load(open("outils_tmp/en_pick.json"))
for d in ("arts", "panos"): os.makedirs("medias/" + d, exist_ok=True)
cr = {}
for kind, mx in (("arts", 1800), ("panos", 8192)):
    for k, t in P[kind].items():
        try:
            ii = info(t); im = Image.open(io.BytesIO(get(ii["url"]))).convert("RGB")
            if kind == "panos": im = im.resize((min(8192, im.width // 2 * 2), min(8192, im.width // 2 * 2) // 2), Image.LANCZOS)
            else:
                s = min(1, mx / max(im.size)); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
            im.save(f"medias/{kind}/{k}.jpg", quality=90)
            m = ii.get("extmetadata", {}); cr[k] = {"file": t, "artist": m.get("Artist", {}).get("value", ""), "license": m.get("LicenseShortName", {}).get("value", "")}
            print(k, im.size)
        except Exception as e: print("ECHEC", k, e)
        time.sleep(0.4)
for h in P["ph"]:
    f = json.loads(get("https://api.polyhaven.com/files/" + h)); url = f.get("tonemapped", {}).get("url")
    im = Image.open(io.BytesIO(get(url))).convert("RGB"); im = im.resize((8192, 4096), Image.LANCZOS) if im.width > 8192 else im
    im.save(f"medias/panos/{h}.jpg", quality=90); cr[h] = {"file": h, "artist": "Poly Haven", "license": "CC0"}; print(h, im.size)
def catsearch(q):
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "format": "json", "list": "search", "srsearch": q, "srnamespace": 14, "srlimit": 5})
    return [x["title"] for x in json.loads(get(u))["query"]["search"]]
def members(cat):
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "format": "json", "generator": "categorymembers", "gcmtitle": cat, "gcmtype": "file", "gcmlimit": 100, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiextmetadatafilter": "Artist|LicenseShortName", "iiurlwidth": 600})
    return list(json.loads(get(u)).get("query", {}).get("pages", {}).values())
os.makedirs("medias/cand", exist_ok=True); found = {}
for tag, qs in P["cats"].items():
    n = 0; seen = set()
    for q in qs:
        try: cats = catsearch(q)
        except Exception as e: print("cat", e); continue
        for cat in cats:
            for p in members(cat):
                ii = p.get("imageinfo", [{}])[0]; w, h = ii.get("width", 0), ii.get("height", 1)
                if p["title"] in seen or w < 4000 or not (1.95 < w / h < 2.05): continue
                seen.add(p["title"]); k = f"{tag}{n:02d}"
                try: Image.open(io.BytesIO(get(ii["thumburl"]))).convert("RGB").save(f"medias/cand/{k}.jpg", quality=80)
                except Exception as e: print(e); continue
                m = ii.get("extmetadata", {}); found[k] = {"file": p["title"][5:], "cat": cat, "url": ii["url"], "w": w, "license": m.get("LicenseShortName", {}).get("value", ""), "artist": m.get("Artist", {}).get("value", "")[:200]}
                n += 1
                if n >= 6: break
            if n >= 6: break
        if n >= 6: break
    print(tag, n)
json.dump(found, open("medias/cand/cats.json", "w"), ensure_ascii=False, indent=1)
json.dump(cr, open("medias/credits.json", "w"), ensure_ascii=False, indent=1)
