import json, os, time, urllib.parse, urllib.request, io
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "Atelier360-medias/1.0 (cours d'anglais; https://github.com/lefebvrepascal/atelier-360)"}
def get(url):
    for k in range(5):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=900).read()
        except Exception as e: print("retry", url[:90], e); time.sleep(8 * (k + 1))
def info(title):
    q = urllib.parse.urlencode({"action": "query", "format": "json", "titles": title, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiextmetadatafilter": "Artist|LicenseShortName|Credit"})
    p = list(json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))["query"]["pages"].values())[0]
    return p["imageinfo"][0] if "imageinfo" in p else None
PANOS = {"yard": "File:Kugelpanorama des Schiller-Gymnasiums Hof 20240520.jpg", "class1": "File:北大高中教室全景.jpg",
         "class2": "File:Kugelpanorama eines Klassenzimmers 20240903.jpg", "canteen": "File:Tallinna Ehituskool 013-sookla pano.jpg"}
os.makedirs("medias/panos", exist_ok=True); credits = {}
for k, t in PANOS.items():
    ii = info(t)
    if not ii: print("ABSENT", k); continue
    im = Image.open(io.BytesIO(get(ii["url"]))).convert("RGB"); s = min(1, 8192 / im.width)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS); im.save(f"medias/panos/{k}.jpg", quality=90)
    m = ii.get("extmetadata", {}); credits[k] = {"file": t, "url": ii.get("descriptionurl", ""), "artist": m.get("Artist", {}).get("value", ""), "license": m.get("LicenseShortName", {}).get("value", "")}
    print(k, im.size)
json.dump(credits, open("medias/credits.json", "w"), ensure_ascii=False, indent=1)
