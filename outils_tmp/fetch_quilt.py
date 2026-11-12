import json, os, time, urllib.parse, urllib.request, io
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "Atelier360-medias/1.0 (cours de physique; https://github.com/lefebvrepascal/atelier-360)"}
def get(url):
    for k in range(5):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300).read()
        except Exception as e: print("retry", url[:90], e); time.sleep(5 * (k + 1))
    raise SystemExit("échec " + url)
def info(title):
    q = urllib.parse.urlencode({"action": "query", "format": "json", "titles": "File:" + title, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiextmetadatafilter": "Artist|LicenseShortName"})
    return list(json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))["query"]["pages"].values())[0]["imageinfo"][0]
ARTS = {"localgroup": "The Local Group Top View.jpg", "mw_annot": "236084main MilkyWay-full-annotated.jpg", "europe": "Europe satellite orthographic.jpg",
 "cheek": "Human cheek cells from science class.jpg", "hela": "Multicolor fluorescence image of a living HeLa cell.jpg"}
CPANOS = {}
AUDIO = {}
HDRI = []
for d in ("arts", "audio", "panos"): os.makedirs("medias/" + d, exist_ok=True)
credits = {}
for key, title in ARTS.items():
    ii = info(title); im = Image.open(io.BytesIO(get(ii["url"]))).convert("RGB")
    s = min(1, 2400 / max(im.size)); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS); im.save(f"medias/arts/{key}.jpg", quality=92)
    m = ii.get("extmetadata", {}); credits[key] = {"file": title, "artist": m.get("Artist", {}).get("value", ""), "license": m.get("LicenseShortName", {}).get("value", "")}
    print(key, im.size); time.sleep(0.4)
for key, title in CPANOS.items():
    ii = info(title); im = Image.open(io.BytesIO(get(ii["url"]))).convert("RGB")
    s = min(1, 8192 / im.width); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS); im.save(f"medias/panos/{key}.jpg", quality=92)
    m = ii.get("extmetadata", {}); credits[key] = {"file": title, "artist": m.get("Artist", {}).get("value", ""), "license": m.get("LicenseShortName", {}).get("value", "")}
    print(key, im.size)
for key, title in AUDIO.items():
    ii = info(title); ext = title.rsplit(".", 1)[1]; open(f"medias/audio/{key}.{ext}", "wb").write(get(ii["url"]))
    m = ii.get("extmetadata", {}); credits[key] = {"file": title, "artist": m.get("Artist", {}).get("value", ""), "license": m.get("LicenseShortName", {}).get("value", "")}
for h in HDRI:
    f = json.loads(get("https://api.polyhaven.com/files/" + h))
    url = f.get("tonemapped", {}).get("url")
    print(h, url)
    im = Image.open(io.BytesIO(get(url))).convert("RGB"); im = im.resize((8192, 4096), Image.LANCZOS) if im.width > 8192 else im
    im.save(f"medias/panos/{h}.jpg", quality=90); im.resize((1024, 512)).save(f"medias/panos/{h}_p.jpg", quality=80); credits[h] = {"file": h, "artist": "Poly Haven", "license": "CC0"}
json.dump(credits, open("medias/credits.json", "w"), ensure_ascii=False, indent=1)
# --- Orthophotos IGN (Licence Ouverte Etalab 2.0) centrées sur le collège
import math
os.makedirs("medias/ign", exist_ok=True)
g = json.loads(get("https://data.geopf.fr/geocodage/search?q=" + urllib.parse.quote("26 rue Marthe Nollet 59250 Halluin") + "&limit=1"))
lon, lat = g["features"][0]["geometry"]["coordinates"]; print("géocodage", lat, lon, g["features"][0]["properties"].get("label"))
meta = {"lat": lat, "lon": lon, "levels": {}}
for z in (9, 11, 13, 15, 17, 19, 20):
    n = 2 ** z; X = (lon + 180) / 360 * 256 * n; Y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * 256 * n
    x0, y0 = int(X - 1024), int(Y - 1024); im = Image.new("RGB", (2048, 2048), (128, 128, 128)); miss = 0
    for tx in range(x0 // 256, (x0 + 2048) // 256 + 1):
        for ty in range(y0 // 256, (y0 + 2048) // 256 + 1):
            u = f"https://data.geopf.fr/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=ORTHOIMAGERY.ORTHOPHOTOS&STYLE=normal&TILEMATRIXSET=PM&TILEMATRIX={z}&TILEROW={ty}&TILECOL={tx}&FORMAT=image/jpeg"
            try: t = Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read())).convert("RGB"); im.paste(t, (tx * 256 - x0, ty * 256 - y0))
            except Exception as e: miss += 1
    res = 156543.03392 * math.cos(math.radians(lat)) / n
    im.save(f"medias/ign/z{z}.jpg", quality=90); meta["levels"][z] = {"res": res, "width_m": res * 2048, "missing": miss}; print("ign", z, round(res * 2048), "m", "manquantes", miss)
json.dump(meta, open("medias/ign/meta.json", "w"), indent=1)
