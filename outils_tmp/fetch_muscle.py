import json, os, time, urllib.parse, urllib.request, io
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "Atelier360-medias/1.0 (cours de SVT; https://github.com/lefebvrepascal/atelier-360)"}
def get(url):
    for k in range(5):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300).read()
        except Exception as e: print("retry", url[:90], e); time.sleep(5 * (k + 1))
    raise SystemExit("échec " + url)
def info(title):
    q = urllib.parse.urlencode({"action": "query", "format": "json", "titles": "File:" + title, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiextmetadatafilter": "Artist|LicenseShortName"})
    return list(json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))["query"]["pages"].values())[0]["imageinfo"][0]
ARTS = {"vesale": "Muscle man, by Vesalius. Wellcome L0001644.jpg", "bras_gray": "Arm muscles front superficial.png",
 "coureuses": "Girls compete in a 7 lap race during high school first term games in Machakos, Kenya.jpg",
 "fibres": "Muscle Tissue Skeletal Muscle Fibers (41241952644).jpg", "capillaire": "Muscle Tissue Capilary in Skeletal Muscle (28089112678).jpg",
 "tem": "Human skeletal muscle tissue 1 - TEM.jpg", "achille": "Achilles tendon 01.jpg", "radio_coude": "X-ray of normal elbow by lateral projection.jpg",
 "genou": "Coupe sagittale du genou (Gray 350).png", "spiro": "NASA Pilot Nils Larson Does a Spirometry Test.jpg",
 "stetho": "Woman listening to hear heart with a stethoscope.jpg", "jonction": "Electron micrograph of neuromuscular junction (cross-section).jpg",
 "histo": "Skeletal muscle - longitudinal section.jpg"}
AUDIO = {}
HDRI = []
_all = json.loads(get("https://api.polyhaven.com/assets?t=hdris"))
import re
cand = [i for i, a in _all.items() if re.search(r"stadium|gym|sport|track|court|pitch|football|basket|tennis|athlet|running|field_", i + " " + a.get("name", "") + " " + " ".join(a.get("tags", [])), re.I)]
print("CANDIDATS", cand)
HDRI = ["stadium_01", "orlando_stadium", "gym_01", "suburban_football_field", "netball_court", "squash_court", "gym_entrance"]
for d in ("arts", "audio", "panos"): os.makedirs("medias/" + d, exist_ok=True)
credits = {}
for key, title in ([] if os.environ.get("NOARTS") else ARTS.items()):
    ii = info(title); im = Image.open(io.BytesIO(get(ii["url"]))).convert("RGB")
    s = min(1, 2400 / max(im.size)); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS); im.save(f"medias/arts/{key}.jpg", quality=92)
    m = ii.get("extmetadata", {}); credits[key] = {"file": title, "artist": m.get("Artist", {}).get("value", ""), "license": m.get("LicenseShortName", {}).get("value", "")}
    print(key, im.size); time.sleep(0.4)
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
