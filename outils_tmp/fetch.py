import json, os, sys, time, urllib.parse, urllib.request, io
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "Atelier360-medias/1.0 (cours d'histoire; https://github.com/lefebvrepascal/atelier-360)"}
PANOS = {}
ARTS = {
 "sarajevo": "DC-1914-27-d-Sarajevo.jpg",
 "europe1914": "Europe 1914.jpg",
 "mobilisation": "Ordre de Mobilisation générale 2 août 1914.jpg",
 "marne_taxi": "Taxi de la Marne, Musée de l'Armée-IMG 0987.jpg",
 "marne_carte": "Bataille de la Marne, positions au 9 septembre.png",
 "poilus": "Poilus descendant aux tranchées - btv1b6933429g.jpg",
 "tranchee_photo": "En Champagne, poilus réorganisant une tranchée \"boche\" qui vient d'être prise - btv1b9044267h.jpg",
 "gaz": "Au cantonnement, avant le départ pour la première ligne ; les soldats essayent leur masque contre les gaz - btv1b9044571f.jpg",
 "vallotton": "Félix Valloton-Verdun. Tableau de guerre-1917.jpg",
 "voie_sacree": "At the Battle of Verdun - French reserves and ammunition are brought in by motorcades.png",
 "fort_douaumont": "Douaumontfort.jpg",
 "ossuaire": "Ossuaire de Douaumont, Verdun 1914-1918 P-FG-CP-01050-13.jpg",
 "cimetiere_douaumont": "Verdun - Cimetière de Douaumont (1).jpg",
 "on_les_aura": "On les aura 2 E EMPRUNT DE LA DEFENSE NATIONALE souscrivez, AFF4893.jpg",
 "munitions": "'The Munitions Girls' oil painting, England, 1918 Wellcome L0059548.jpg",
 "tirailleurs": "Ippécourt. 42e de tirailleurs Sénégalais - Fonds Berthelé - 49Fi699.jpg",
 "nevinson": "Christopher richard wynne nevinson, la mitrailleuse, 1915.jpg",
 "halluin_lys1": "The Hundred Days Offensive, August-november 1918 Q7130.jpg",
 "halluin_lys2": "The Hundred Days Offensive, August-november 1918 Q7132.jpg",
 "halluin_eglise": "Halluin.Église Saint-Hilaire d'Halluin.jpg",
 "halluin_monument": "Halluin.Monument aux morts.jpg",
 "halluin_monument_auj": "Halluin cimetiere mon aux morts.jpg",
 "halluin_tram": "Halluin Rue de Lille Arrêt du tramway.jpg",
 "front_1918": "Front line, 16 October 1918.jpg",
 "armistice_foule": "L'Opéra le 11 novembre 1918, D.7649.jpg",
 "foch": "Ferdinand Foch (1851-1929), maréchal de France, 1918, ND5545(1).jpg",
 "orpen": "William Orpen - The Signing of Peace in the Hall of Mirrors, Versailles.jpg",
 "renault_ft": "Char Renault FT servant de support à la collecte pour un emprunt de guerre en 1918.jpg",
 "lens_ruines": "Lens, la Grande place (ruines) - btv1b53018476c.jpg",
}
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
        time.sleep(0.5)
json.dump(credits, open("medias/credits.json", "w"), ensure_ascii=False, indent=1)
