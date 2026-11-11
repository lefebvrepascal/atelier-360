import json, os, time, urllib.parse, urllib.request, io
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "Atelier360-medias/1.0 (cours de musique; https://github.com/lefebvrepascal/atelier-360)"}
def get(url):
    for k in range(5):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300).read()
        except Exception as e: print("retry", e); time.sleep(5 * (k + 1))
t = "B.F. Keith Memorial Theater, Boston Opera House panorama.jpg"
q = urllib.parse.urlencode({"action": "query", "format": "json", "titles": "File:" + t, "prop": "imageinfo", "iiprop": "url|extmetadata"})
ii = list(json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))["query"]["pages"].values())[0]["imageinfo"][0]
os.makedirs("medias/panos", exist_ok=True)
im = Image.open(io.BytesIO(get(ii["url"]))).convert("RGB"); im.resize((8192, 4096), Image.LANCZOS).save("medias/panos/opera_boston.jpg", quality=92)
m = ii["extmetadata"]; json.dump({"opera_boston": {"file": t, "artist": m.get("Artist", {}).get("value", ""), "license": m.get("LicenseShortName", {}).get("value", "")}}, open("medias/credits.json", "w"), ensure_ascii=False)
print("ok")
