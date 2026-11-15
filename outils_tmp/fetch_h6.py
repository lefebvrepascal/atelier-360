import json, os, time, urllib.parse, urllib.request, io
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "Atelier360-medias/1.0 (cours de SVT; https://github.com/lefebvrepascal/atelier-360)"}
def get(url, tries=4):
    for k in range(tries):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300).read()
        except Exception as e: print("retry", url[:90], e); time.sleep(4 * (k + 1))
def api(**q):
    q.update(format="json"); r = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(q)); return json.loads(r) if r else {}
os.makedirs("medias/cand", exist_ok=True)
def thumb(url, path, w=None):
    b = get(url)
    if not b: return False
    try: Image.open(io.BytesIO(b)).convert("RGB").save(path, quality=78); return True
    except Exception as e: print("img", e); return False
def commons(qs, pano, n, tag):
    seen, out = set(), []
    for q in qs:
        d = api(action="query", generator="search", gsrsearch=q, gsrnamespace=6, gsrlimit=25, prop="imageinfo", iiprop="url|size|extmetadata|mime", iiurlwidth=500,
                iiextmetadatafilter="Artist|LicenseShortName|ImageDescription")
        pages = sorted(d.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
        k = 0
        for p in pages:
            t = p["title"]
            if t in seen or "imageinfo" not in p: continue
            ii = p["imageinfo"][0]; w, h = ii.get("width", 0), ii.get("height", 1)
            if not ii.get("mime", "").startswith(("image/jpeg", "image/png")): continue
            if pano and (w < 4000 or not (1.95 < w / h < 2.05)): continue
            if not pano and min(w, h) < 500: continue
            seen.add(t); m = ii.get("extmetadata", {})
            key = "%s%03d" % (tag, len(out))
            rec = {"k": key, "q": q, "title": t[5:], "w": w, "h": h, "lic": m.get("LicenseShortName", {}).get("value", ""), "artist": m.get("Artist", {}).get("value", "")[:200]}
            if thumb(ii.get("thumburl", ii["url"]), f"medias/cand/{key}.jpg"): out.append(rec); k += 1
            if k >= n: break
        time.sleep(0.2)
    return out
ARTQ = {
 "pre": ["Lucy skeleton Australopithecus cast", "Tautavel man skull", "Chauvet cave horses painting", "Lascaux painting bull", "hand stencil cave painting", "Homo sapiens migration map", "biface acheulean", "Neanderthal reconstruction"],
 "neo": ["Stonehenge", "Carnac alignements Ménec", "Catalhoyuk reconstruction", "Neolithic polished axe", "Neolithic pottery", "Skara Brae house", "einkorn wheat", "dolmen France"],
 "meso": ["Code of Hammurabi stele Louvre", "cuneiform tablet", "Ziggurat of Ur", "Uruk Warka vase", "Standard of Ur", "Ishtar gate Pergamon", "Gilgamesh tablet flood", "Mesopotamia map"],
 "gre": ["Parthenon Athens", "Acropolis Athens", "Athenian ostracon", "Pnyx Athens", "Olympia stadium", "Delphi theatre", "Greek amphora Achilles", "trireme Olympias"],
 "rom": ["Capitoline Wolf", "Roman Forum", "Romulus and Remus Rubens", "Etruscan sarcophagus spouses", "Palatine hill", "Curia Julia", "SPQR inscription", "Roman senate Maccari"],
 "jud": ["Dead Sea Scrolls Isaiah", "Israel Museum Shrine of the Book", "Mesha stele Louvre", "Arch of Titus menorah relief", "Torah scroll", "Synagogue Dura Europos", "Lachish relief British Museum", "Western Wall"],
 "emp": ["Colosseum Rome", "Pont du Gard", "Maison carrée Nîmes", "Bavay forum Bagacum", "Augustus of Prima Porta", "Roman legionary reenactment", "Roman road Via Appia", "Hadrian's Wall"],
 "chr": ["catacomb of Priscilla fresco", "Chi Rho symbol", "Constantine colossal head", "Old St Peter's basilica drawing", "Silk Road map", "Han dynasty pottery", "Terracotta army", "Great Wall Mutianyu"],
}
PANOQ = ["Lascaux replica 360", "cave equirectangular", "Font-de-Gaume", "Tautavel panorama", "Stonehenge equirectangular", "Stonehenge 360 panorama", "Carnac panorama 360", "megalith panosphere",
 "Ziggurat panorama 360", "Louvre Mesopotamian gallery 360", "Louvre panosphere", "Acropolis 360 panorama", "Parthenon equirectangular", "Ancient Agora Athens panorama 360", "Olympia panorama 360", "Delphi 360 panorama",
 "Roman Forum 360 panorama", "Forum Romanum equirectangular", "Palatine 360", "Colosseum 360 panorama", "Pont du Gard 360 panorama", "Nîmes arènes 360", "Arles amphitheatre 360", "Bavay panorama",
 "catacomb 360 panorama", "basilica Rome 360 panorama", "Jerusalem Old City 360 panorama", "Western Wall equirectangular", "Great Wall of China 360 panorama", "terracotta army 360 panorama", "Xi'an panorama 360", "Pompeii 360 panorama"]
res = {}
for tag, qs in ARTQ.items(): res[tag] = commons(qs, False, 1, tag); print(tag, len(res[tag]))
res["pano"] = commons(PANOQ, True, 2, "pano"); print("pano", len(res["pano"]))
res["polyhaven"] = []
json.dump(res, open("medias/cand/cand.json", "w"), ensure_ascii=False, indent=1)
