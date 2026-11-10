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
ARTS = {
 "l_bus": "The Palace of Westminster, a Routemaster bus, and a red phone box, London, 8 December 2005.jpg", "l_cab": "2016 LTI TX4 London black cab.jpg",
 "l_phone": "Five classic red K6 telephone boxes on a pavement in London.jpg", "l_guard": "Guard of Buckingham Palace.JPG", "l_band": "Band of the Welsh Guards, Buckingham Palace, London - Diliff.jpg",
 "l_palace": "Buckingham Palace London Morning 2020 04.jpg", "l_towerbridge": "London, Tower Bridge -- 2016 -- 4676.jpg", "l_beefeater": "Yeoman Warder - Beefeater.JPG",
 "l_ravens": "Jubilee and Munin, Ravens, Tower of London 2016-04-30.jpg", "l_tube": "Mosaic Underground roundel, Maida Vale.jpg", "l_platform": "Platform 9 3-4 (King's Cross station, London, 2014).jpg",
 "l_globe": "Shakespeare's Globe Theatre, London - 2024-08-13.jpg", "l_king": "King Charles III (July 2023).jpg", "l_shakespeare": "Shakespeare.jpg",
 "l_fish": "Fish and Chips Bath, UK.jpg", "l_tea": "Classic cream tea - Nymans Garden Riding House.jpg", "l_eye": "London Eye by Day.jpg",
 "l_nelson": "Admiral Horatio Nelson, Nelson's Column, Trafalgar Square, London.JPG", "l_gallery": "The National Gallery south facade - geograph.org.uk - 3300034.jpg",
 "l_tower": "Tower of London viewed from the River Thames.jpg", "l_crown": "Imperial State Crown of Queen Victoria (2).jpg", "l_thames": "Aerial view of River Thames from Tower Bridge to Isle of Dogs.jpg",
 "g_kheops": "Giza Great Pyramid of Khufu (9793898043).jpg", "g_sphinx": "Great Sphinx of Giza and Pyramid of Cheops.jpg", "g_khufu": "Ivory statuette of Khufu from Abydos, 2551-2528 BCE; Egyptian Museum, Cairo (1).jpg",
 "g_gallery": "By ovedc - Interior of the Great Pyramid - 06.jpg", "g_kingch": "At the centre of the Great Pyramid (47315820161).jpg", "g_boat": "Grand Egyptian Museum - Khufu ship.jpg",
 "g_hiero": "Egyptian - Wall Fragment from the Tomb of Amenemhet and His Wife Hemet - Google Art Project.jpg", "g_bookdead": "El pesado del corazón en el Papiro de Hunefer.jpg",
 "g_mummy": "PXL 20231219 110740689 British Museum Egyptian Artefacts 35 ancient Egyptian mummy in a decorated coffin.jpg", "g_nile": "Agriculture Along the Nile River (50304448147).png",
 "g_rosetta": "Rosetta Stone.JPG", "g_champollion": "Leon Cogniet - Jean-Francois Champollion.jpg", "g_menkaure": "Menkaure (Mykerinos) Triad, 4th Dynasty (9797372503).jpg",
 "g_khafre_casing": "Khafre's Casing (31069966033).jpg", "g_aerial": "Cairo and the pyramids. Pyramids of Gizeh. Looking down on the three great pyramids of Egypt LOC matpc.12378.jpg",
 "g_scribe": "Le Scribe accroupi - Musée du Louvre Antiquités égyptiennes E 3023.jpg", "g_nebamun": "Tomb of Nebamun.jpg", "g_mastaba": "Giza EasternCemetery-view G7050-7060-7070.jpg"}
CPANOS = {"westminster": "Westminster Bridge panosphere 20250522.jpg", "stjames": "Spherical panorama Blue Bridge St James Park 20250522.jpg",
 "kingscross": "Kings Cross Railway Station Concourse 360x180, London, UK - Diliff.jpg", "trafalgar": "Trafalgar Square 360 Panorama, London - Jun 2009.jpg",
 "tower": "Panoramic view from Tower of London.jpg", "giza": "Giza pyramid complex - 360.jpg"}
HDRI = ["kloofendal_48d_partly_cloudy_puresky", "qwantani_puresky"]
AUDIO = {}
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
