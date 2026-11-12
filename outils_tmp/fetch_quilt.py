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
ARTS = {}
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
# --- Orthophotos IGN (Licence Ouverte Etalab 2.0) et Sentinel-2 cloudless 2016 (EOX, CC BY 4.0), centrées sur le collège
import math
os.makedirs("medias/ign", exist_ok=True)
lat, lon = 50.782043, 3.122895
def tile(u):
    for k in range(6):
        try: return Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read())).convert("RGB")
        except Exception as e:
            if "404" in str(e) or "400" in str(e): return None
            time.sleep(2 + 3 * k)
    return None
def mosaic(fmt, z, out):
    n = 2 ** z; X = (lon + 180) / 360 * 256 * n; Y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * 256 * n
    x0, y0 = int(X - 1024), int(Y - 1024); im = Image.new("RGB", (2048, 2048), (255, 0, 255)); miss = 0
    for tx in range(x0 // 256, (x0 + 2048) // 256 + 1):
        for ty in range(y0 // 256, (y0 + 2048) // 256 + 1):
            t = tile(fmt.format(z=z, x=tx, y=ty)); time.sleep(0.05)
            if t is None: miss += 1; continue
            im.paste(t, (tx * 256 - x0, ty * 256 - y0))
    im.save(out, quality=90); print(out, "manquantes", miss, flush=True)
IGN = "https://data.geopf.fr/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=ORTHOIMAGERY.ORTHOPHOTOS&STYLE=normal&TILEMATRIXSET=PM&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&FORMAT=image/jpeg"
EOX = "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless_3857/default/g/{z}/{y}/{x}.jpg"
for z in (7, 9, 11, 13, 14): mosaic(EOX, z, f"medias/ign/eox{z}.jpg")
for z in (15, 17, 19): mosaic(IGN, z, f"medias/ign/z{z}.jpg")
