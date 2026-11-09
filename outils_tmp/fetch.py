import json, os, sys, time, urllib.parse, urllib.request, io
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "Atelier360-medias/1.0 (cours d'histoire; https://github.com/lefebvrepascal/atelier-360)"}
PANOS = {}
ARTS = {"jeu_de_paume": "Jacques‑Louis David, Le Serment du Jeu de Paume, 1791, Versailles, Château de Versailles.jpg"}
def get(url):
    for k in range(5):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180).read()
        except Exception as e:
            print("retry", url[:80], e); time.sleep(5 * (k + 1))
    raise SystemExit("échec " + url)
def info(title):
    q = urllib.parse.urlencode({"action": "query", "format": "json", "titles": "File:" + title, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiextmetadatafilter": "Artist|LicenseShortName|ObjectName|DateTimeOriginal|Credit"})
    p = list(json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))["query"]["pages"].values())[0]
    return p["imageinfo"][0]
os.makedirs("medias/panos", exist_ok=True); os.makedirs("medias/arts", exist_ok=True)
credits = {}
for kind, d, maxw in (("panos", PANOS, 8192), ("arts", ARTS, 2400)):
    for key, title in d.items():
        ii = info(title)
        im = Image.open(io.BytesIO(get(ii["url"]))).convert("RGB")
        if kind == "panos":
            im = im.resize((maxw, maxw // 2), Image.LANCZOS)
        else:
            s = min(1, maxw / max(im.size)); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        im.save(f"medias/{kind}/{key}.jpg", quality=92, optimize=True)
        m = ii.get("extmetadata", {})
        credits[key] = {"file": title, "page": ii.get("descriptionurl"), "artist": m.get("Artist", {}).get("value", ""), "license": m.get("LicenseShortName", {}).get("value", ""), "size": [ii["width"], ii["height"]]}
        print(kind, key, im.size)
        time.sleep(1)
json.dump(credits, open("medias/credits.json", "w"), ensure_ascii=False, indent=1)
