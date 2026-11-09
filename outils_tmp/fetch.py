import json, os, sys, time, urllib.parse, urllib.request, io
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "Atelier360-medias/1.0 (cours d'histoire; https://github.com/lefebvrepascal/atelier-360)"}
PANOS = {
 "champ_de_mars": "Eiffel Tower and Champ-de-Mars panorama, April 2008.jpg",
 "concorde": "Place de la Concorde, Paris March 2007.jpg",
 "hotel_de_ville": "Port de l'Hôtel de Ville, Paris 4 February 2007.jpg",
 "pantheon": "Saint-Étienne du Mont, Paris 11 March 2007.jpg",
 "louvre": "Louvre panosphere 20200303.jpg",
 "vert_galant": "Square du Vert-Galant panosphere.jpg",
 "notre_dame": "Panorama Notre-Dame de Paris.jpg",
}
ARTS = {
 "etats_generaux": "Ouverture des Etats Généraux, le 5 mai 1789, par Louis-Charles Auguste Couder. Paris Musées 20231031152637.jpg",
 "jeu_de_paume": "Jacques-Louis David - Serment du Jeu de paume, le 20 juin 1789 - P67 - Musée Carnavalet - 2.jpg",
 "louis16": "Antoine-François Callet - Louis XVI, roi de France et de Navarre (1754-1793), revêtu du grand costume royal en 1779 - Google Art Project.jpg",
 "marie_antoinette": "Louise Elisabeth Vigée-Lebrun - Marie-Antoinette dit « à la Rose » - Google Art Project.jpg",
 "trois_ordres": "Révolution française. Ancien Régime. Caricature sur les Trois-Ordres Le Tiers-Etat portant sur son dos le Clergé et la, G.23830.jpg",
 "cahier": "Cahier de doléances de la commune d'Andel (Côtes-d'Armor), 1788-1789 (page 1).jpg",
 "bastille": "Prise de la Bastille.jpg",
 "ddhc": "Jean-Jacques Le Barbier - Déclaration des droits de l'homme et du citoyen - P708 - Musée Carnavalet.jpg",
 "federation": "Charles Thévenin - La fête de la Fédération, le 14 juillet 1790, au Champ-de-Mars, actuel 7ème arrondissement - La Fête de la Fédération, le 14 juillet 1790, au Champ-de-Mars - Musée Carnavalet - 2.jpg",
 "varennes": "Arrestation de Louis XVI à Varennes, 21-22 juin 1791. D.9095.jpg",
 "dix_aout": "Jacques Bertaux - La Journée du 10 août (1792).jpg",
 "valmy": "Valmy Battle painting.jpg",
 "marseillaise": "Pils rouget lisle chantant marseillaise mb (Musée).jpg",
 "execution_louis16": "N°78 Supplice de Louis XVI, place de la révolution. Le 21 Janvier 1793 ou Ier Pluviôse An Ier de la République. G.28718.jpg",
 "sans_culotte": "Louis Léopold Boilly - Portrait du chanteur Simon Chenard (1758-1832), en costume de sans-culotte, portant un drapeau à la - P8 - Musée Carnavalet.jpg",
 "robespierre": "Robespierre.jpg",
 "ma_supplice": "Portrait de Marie Antoinette reine de France conduite au supplice, déssiné à la plume par David... - dessin - copié sur l'original éxistant dans la collection Soulavie - btv1b84119831.jpg",
 "conciergerie": "Conciergerie and Cour de Cassation, Paris 2 April 2014.jpg",
 "thermidor": "Révolution française Nuit du 9 au 10 Thermidor An II ou 27-28 juillet 1794. Attentat par la Convention contre Robespie, G.31916.jpg",
 "calendrier": "Calendrier Républicain, G.4140.jpg",
 "brumaire": "Bouchot - Le general Bonaparte au Conseil des Cinq-Cents.jpg",
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
        time.sleep(1)
json.dump(credits, open("medias/credits.json", "w"), ensure_ascii=False, indent=1)
