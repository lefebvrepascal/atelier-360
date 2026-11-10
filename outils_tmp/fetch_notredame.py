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
ARTS = {"facade": "Cathédrale Notre-Dame de Paris, 20 March 2014.jpg", "portails": "Façade et portails de Notre Dame de Paris.JPG",
 "jugement": "Tympan Portail Jugement Dernier Cathédrale Notre-Dame Paris 1.jpg", "rois": "Galerie des rois of Notre-Dame de Paris, May 2012.jpg",
 "gargouille": "Gargouilles gargoyles Notre Dame de Paris.jpg", "stryge": "PARIS 44 Notre-Dame Les Chimères, Le Stryge.jpg",
 "chevet": "Notre Dame chevet.jpg", "arcb": "Arcs boutants du chevet.jpg", "fleche": "Flèche Notre-Dame de Paris.jpg",
 "feu": "Flèche en feu - Spire on Fire.jpeg", "charpente": "La charpente de Notre-Dame de Paris, novembre 2025.jpg",
 "bourdon": "Bourdon de Notre-Dame de Paris.jpg", "rose_n": "North rose window of Notre-Dame de Paris, Aug 2010.jpg",
 "rose_s": "South rose window of Notre-Dame de Paris (interior), December 2024 (5).jpg", "orgue": "Great organ of Notre-Dame de Paris 2024 (1).jpg",
 "nef": "Nave of Notre-Dame de Paris towards the portal, 2024 (1).jpg", "nef2": "Cathédrale Notre-Dame de Paris - 15.jpg",
 "voute": "Paris Notre-Dame Vaults 01.JPG", "vierge": "Madonna and Child dit Notre-Dame de Paris 2024 (7).jpg",
 "stalles": "Choir stalls, Notre Dame, Paris, ZM.JPG", "vld": "Félix Nadar 1820-1910 portraits Eugène Viollet le Duc.jpg",
 "hugo": "Achille Devéria, Victor Hugo, 1829, NGA 208390.jpg", "sacre": "Jacques-Louis David - The Coronation of Napoleon (1805-1807).jpg",
 "fouquet": "Construction du Temple de Jérusalem.jpg", "sully": "Sceau-Maurice de Sully-A01.jpg", "plan": "Plan de la cathédrale Notre-Dame-de-Paris. D.14500-14.jpg",
 "bascote": "Cathédrale Notre-Dame de Paris - Gothic rib vaults and side aisle.jpg"}
CPANOS = {"parvis_nuit": "Panorama Notre-Dame de Paris.jpg", "cite": "Île de la Cité, Paris 18 November 2006.jpg", "seine_nuit": "The Seine in Paris, 25 February 2007.jpg"}
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
