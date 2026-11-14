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
 "mito": ["mitosis onion root tip micrograph", "mitosis stages fluorescence", "metaphase chromosomes micrograph", "anaphase micrograph", "human karyotype", "cell division micrograph"],
 "nutri": ["iodine test starch", "Fehling's test result", "biuret test protein", "anhydrous copper sulfate water", "food groups balanced diet", "digestive system diagram French", "intestinal villi micrograph", "nutrition facts label"],
 "molec": ["hemoglobin structure", "insulin structure ribbon", "starch granules micrograph", "cellulose structure", "DNA structure diagram", "triglyceride"],
 "phylo": ["lamprey", "Carcharodon carcharias", "rainbow trout", "Rana temporaria", "Lacerta bilineata", "Nile crocodile", "Columba livia", "house mouse", "chimpanzee", "Homo sapiens skull", "chimpanzee skull", "Australopithecus afarensis skull cast", "Homo erectus skull", "Neanderthal skull La Chapelle", "Archaeopteryx fossil", "Tiktaalik"],
 "geno": ["sickle cell anemia blood smear", "normal red blood cells micrograph", "DNA double helix", "chromosome X-shape micrograph", "EcoRI restriction enzyme", "Mendel"],
 "eche": ["epidermis histology", "human skin cross section diagram", "cheek cells microscope", "cell nucleus electron micrograph", "carbon atom model"],
}
PANOQ = ["Grande Galerie de l'Évolution panorama", "natural history museum panorama 360", "museum hall equirectangular", "market hall panorama 360", "marché couvert panosphère",
         "laboratory equirectangular", "biology laboratory 360 panorama", "greenhouse 360 panorama", "forest equirectangular", "hospital 360 panorama", "canteen 360 panorama", "supermarket equirectangular"]
res = {}
for tag, qs in ARTQ.items(): res[tag] = commons(qs, False, 3, tag); print(tag, len(res[tag]))
res["pano"] = commons(PANOQ, True, 4, "pano"); print("pano", len(res["pano"]))
ph = get("https://api.polyhaven.com/assets?t=hdris")
d = json.loads(ph) if ph else {}
phs = []
for k, v in d.items():
    txt = " ".join([k, v.get("name", "")] + v.get("tags", []) + v.get("categories", [])).lower()
    if any(w in txt for w in ("hospital", "lab", "museum", "kitchen", "market", "forest", "cafe", "restaurant", "school", "garden", "greenhouse", "studio", "workshop", "library", "hall", "shop", "store")):
        if thumb(f"https://cdn.polyhaven.com/asset_img/thumbs/{k}.png?width=512&height=256", f"medias/cand/ph_{k}.jpg"): phs.append(k)
res["polyhaven"] = phs; print("ph", len(phs))
json.dump(res, open("medias/cand/cand.json", "w"), ensure_ascii=False, indent=1)
