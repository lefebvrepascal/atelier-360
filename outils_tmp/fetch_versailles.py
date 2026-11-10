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
ARTS = {"rigaud": "Rigaud Louis XIV 1701.jpg", "patel": "Chateau de Versailles 1668 Pierre Patel.jpg", "lenotre": "Andre-Le-Nostre1.jpg",
 "lebrun": "Nicolas de Largillière - Portrait of Charles Le Brun - WGA12471.jpg", "mansart": "Francois de Troy - Porträtt av Jules Hardouin Mansart - NMH 2783-1863 - Nationalmuseum.jpg",
 "plan": "Plan de Versailles - Gesamtplan von Delagrife 1746.jpg", "conde": "Réception du Grand Condé par Louis XIV - Jean-Léon Gérôme - Musée d'Orsay RF 2004 15.jpg",
 "marly": "Machine de Marly.jpg", "lully": "Jean-Baptiste Lully 02.jpg", "ma": "Louise Elisabeth Vigée-Lebrun - Marie-Antoinette dit « à la Rose » - Google Art Project.jpg",
 "allegrain": "Promenade de Louis XIV en vue du Parterre du Nord vers 1688.jpg", "octobre": "Journée Mémorable du 6 Octobre 1789. Départ de Versailles pour Paris. De Messieurs les Gardes du Corps, et Gardes Nation, G.27982.jpg",
 "apollon": "Versailles Bassin d'Apollon 001.jpg", "chambre": "Lit de Louis XIV.jpg", "chapelle": "Intérieur de la chapelle royale de Versailles 2023 2.jpg",
 "galerie": "Galerie des Glaces (23934705229).jpg", "lustre": "Château de Versailles, galerie des glaces, lustre.jpg",
 "roi_gouverne": "Charles Le Brun - Le Roi gouverne par lui-même, 1661 - Google Art Project.jpg", "plaf_aix": "Paix conclue à Aix la Chapelle 1668 Ceiling Hall of mirrors Versailles.jpg",
 "plaf_foudre": "Foudre Hall of Mirrors Versailles.jpg", "plaf_gand": "Prise de la ville et de la citadelle de Gand en six jours - Hall of Mirrors (Palace of Versailles).jpg",
 "fenetre": "Château de Versailles, galerie des glaces, fenêtre et vue sur le jardin.jpg", "latone": "Parc de Versailles, parterre de Latone, bassin de Latone 02.jpg"}
CPANOS = {"bibliotheque": "Château de Versailles, petit appartement de la reine, 1er étage, bibliothèque, pano equirectangular.jpg",
 "orangerie": "Panorama de l'Orangerie - Château de Versailles - P1050169-P1050193.jpg", "salle_bal": "Salle de Bal - Versailles - P1180011-P1180022.jpg",
 "trianon": "Jardins du Grand Trianon - Versailles - P1180359-P1180372.jpg"}
AUDIO = {}
HDRI = ["kloofendal_48d_partly_cloudy_puresky", "kloppenheim_06_puresky"]
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
