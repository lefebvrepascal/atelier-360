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
P = json.load(open("outils_tmp/bruno_pick.json"))
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
json.dump(cr, open("medias/credits.json", "w"), ensure_ascii=False, indent=1)
