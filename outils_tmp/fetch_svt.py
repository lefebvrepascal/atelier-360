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
ARTS = {"neutro_staph": "Scanning electron micrograph of Methicillin-resistant Staphylococcus aureus (MRSA) and a dead Human neutrophil - NIAID.jpg",
 "staph": "Methicillin-Resistant Staphylococcus Aureus (MRSA) Bacteria colorized scanning electron micrograph - 44.jpg", "ecoli": "E coli at 10000x, original.jpg",
 "grippe": "Colorized transmission electron micrograph of Avian influenza A H5N1 viruses.jpg", "lt": "T Lymphocyte (16760076824).jpg", "lt_vih": "HIV-infected T cell (6813384933).jpg",
 "lb": "Human B Lymphocyte - NIAID.jpg", "killer": "Killer T cells surround a cancer cell.png", "peau": "Skin- epidermis and dermis.jpg", "pasteur": "Louis Pasteur, foto av Paul Nadar, Crisco edit.jpg",
 "fleming": "Professor Alexander Fleming at work in his laboratory at St Mary's Hospital, London, during the Second World War. D17801.jpg", "mains": "Washing hands with soap (1).jpg",
 "echarde": "Splinter in fingertip.jpg", "vacc_ancien": "Vaccinating the poor (5039319130).jpg", "frottis": "Blood smear labelled.png", "vih": "HIV-budding.jpg",
 "neutro_anthrax": "Neutrophil with anthrax copy.jpg"}
AUDIO = {}
HDRI = []
for d in ("arts", "audio", "panos"): os.makedirs("medias/" + d, exist_ok=True)
credits = {}
for key, title in ARTS.items():
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
    im.save(f"medias/panos/{h}.jpg", quality=92); credits[h] = {"file": h, "artist": "Poly Haven", "license": "CC0"}
json.dump(credits, open("medias/credits.json", "w"), ensure_ascii=False, indent=1)
