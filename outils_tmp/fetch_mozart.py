import json, os, time, urllib.parse, urllib.request, io
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "Atelier360-medias/1.0 (cours de musique; https://github.com/lefebvrepascal/atelier-360)"}
def get(url):
    for k in range(5):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300).read()
        except Exception as e: print("retry", url[:90], e); time.sleep(5 * (k + 1))
    print("ECHEC", url); return None
def info(title):
    q = urllib.parse.urlencode({"action": "query", "format": "json", "titles": "File:" + title, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiextmetadatafilter": "Artist|LicenseShortName"})
    return list(json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))["query"]["pages"].values())[0]["imageinfo"][0]
PANOS = {"konzerthaus": "Konzerthaus Wien großer Saal Parterre Kugelpanorama 360° (2023).jpg",
 "mozartsaal": "Konzerthaus Wien Mozartsaal Bühne Kugelpanorama 360° (2023).jpg",
 "mozartsaal_p": "Konzerthaus Wien Mozartsaal Parterre Kugelpanorama 360° (2023).jpg",
 "dom": "Salzburger Dom 360 Grad Ansicht Mitte.jpg", "residenz": "Residenzplatz Panorama.jpg",
 "schoenbrunn": "Schloss Schönbrunn - Vorplatz 360 Grad Panorama.jpg", "stpeter": "St Peter Salzburg panoramic view of interior fullsize.jpg",
 "prague": "Staromestske namesti.jpg", "hellbrunn": "Hellbrunn banqueting hall 360 panoramic view.jpg"}
ARTS = {"m_krafft": "Barbara Krafft - Porträt Wolfgang Amadeus Mozart (1819).jpg", "m_child": "Wolfgang amadeus mozart 1756 j hi.jpg",
 "m_leopold": "Leopold Mozart.jpg", "m_nannerl": "Nannerl Mozart.jpg", "m_family": "Mozart Family Croce.jpg",
 "m_carmontelle": "Louis Carrogis dit Carmontelle - Portrait de Wolfgang Amadeus Mozart (Salzbourg, 1756-Vienne, 1791) jouant à Paris avec son père Jean... - Google Art Project.jpg",
 "m_paris": "Arolsen Klebeband 14 001.jpg", "m_birth": "Salzburg, Getreidegasse 9, Mozarts Geburtshaus.jpg",
 "m_violin_child": "AUT — Bundesland Salzburg — Salzburg (Stadt) — Getreidegasse 9 (Mozartmuseum — Kindergeige von Wolfgang Amadeus Mozart — Geigenbauer Andreas Ferdinand Mayr) Mattes 2021.jpg",
 "m_schoenbrunn": "Heinrich Lefler Mozart in Schönbrunn.jpg", "m_marie": "Marie Antoinette and Mozart.png", "m_colloredo": "Hieronymus von Colloredo by Francesco Pavona.jpg",
 "m_lange": "Mozart (unfinished) by Lange 1782.jpg", "m_constanze": "Constanze Mozart by Hanson 1802.jpg",
 "m_nacht_autograph": "Mozart - Eine kleine Nachtmusik K.525 autograph.png", "m_sym40": "Menuet from Mozart Symphony 40 k 550.jpg",
 "m_fortepiano": "FortepianoAntonWalter.JPG", "m_violin": "Violin VL100.png", "m_clarinet": "Clarinet.jpg", "m_flute": "Flute.jpg", "m_horn": "Natural Horn (instrument).JPG",
 "m_schinkel": "Karl Friedrich Schinkel - Die Sternenhalle der Königin der Nacht (ca. 1815).jpg", "m_zettel": "Zauberflöte-Theaterzettel1791.jpg",
 "m_magicflute": "Mozart magic flute.jpg", "m_estates": "Estates Theatre, Prague.jpg", "m_requiem": "Mozart K626 Arbeitspartitur last page.jpg",
 "m_grave": "Mozart grave newly renovated, St. Marx Cemetery, autumn 2016 (I).jpg", "m_denkmal": "Mozart-Denkmal Wien.JPG",
 "m_kugeln": "Box of Original Mozart Kugeln Fürst.jpg", "m_statue": "Mozart Statue in Mozartplatz, Salzburg.jpg"}
AUDIO = {"a_nacht": "Mozart - Eine kleine Nachtmusik - 1. Allegro.ogg", "a_turca": "Rondo Alla Turka.ogg",
 "a_sym40": "Mozart - Symphony No. 40 in G minor, K550 - I. Molto allegro (Musopen Symphony).flac",
 "a_lacrimosa": "Mozart - Requiem (Krips) - VIII. Lacrimosa.flac",
 "a_reine": "W. A. Mozart - Die Zauberflöte - 18. Der Hölle Rache kocht in meinem Herzen (Ferenc Fricsay, 1953).ogg",
 "a_papageno": "W. A. Mozart - Die Zauberflöte - 03. Der Vogelfänger bin ich ja (Ferenc Fricsay, 1953).ogg",
 "a_clarinet": "Wolfgang Amadeus Mozart - Clarinet Concerto - 2. Adagio.ogg",
 "a_twinkle": "KV.265 12 Variations on Ah vous dirai-je, Maman Mozart JMC, Han.ogg",
 "a_figaro": "Mozart - Le nozze di Figaro, K492 - Overture (Musopen Symphony).flac",
 "a_flute_ov": "Mozart - Die Zauberflöte, K620 - Overture (Musopen Symphony).flac",
 "a_giovanni": "W. A. Mozart - Don Giovanni - 01. Ouverture (Josef Krips, Wiener Staatsoper, 1955).ogg",
 "a_facile": "Wolfgang Amadeus Mozart - sonata no. 16 in c major, k.545 'sonata facile' - i. allegro.ogg",
 "a_k467": "W. A. Mozart - Andante from Piano Concerto K 467 b. 1-23 fading.ogg",
 "a_flute_conc": "Wolfgang Amadeus Mozart - flute concerto in g major, k. 313 - i. allegro maestoso.ogg"}
for d in ("arts", "panos", "audio"): os.makedirs("medias/" + d, exist_ok=True)
credits = {}
def cred(key, title, ii):
    m = ii.get("extmetadata", {}); credits[key] = {"file": title, "artist": m.get("Artist", {}).get("value", ""), "license": m.get("LicenseShortName", {}).get("value", "")}
for key, title in PANOS.items():
    try:
        ii = info(title); im = Image.open(io.BytesIO(get(ii["url"]))).convert("RGB")
    except Exception as e: print("ECHEC", key, e); continue
    s = min(1, 8192 / im.width); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS); im.save(f"medias/panos/{key}.jpg", quality=92); cred(key, title, ii); print(key, im.size)
for key, title in ARTS.items():
    try:
        ii = info(title); im = Image.open(io.BytesIO(get(ii["url"])))
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA"); bg = Image.new("RGB", im.size, (255, 255, 255)); bg.paste(im, mask=im.split()[-1]); im = bg
        im = im.convert("RGB")
    except Exception as e: print("ECHEC", key, e); continue
    s = min(1, 2400 / max(im.size)); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS); im.save(f"medias/arts/{key}.jpg", quality=92); cred(key, title, ii); print(key, im.size)
for key, title in AUDIO.items():
    try:
        ii = info(title); b = get(ii["url"]); ext = title.rsplit(".", 1)[1]
        open(f"medias/audio/{key}.{ext}", "wb").write(b); cred(key, title, ii); print(key, len(b))
    except Exception as e: print("ECHEC", key, e)
json.dump(credits, open("medias/credits.json", "w"), ensure_ascii=False, indent=1)
