import json, os, time, urllib.parse, urllib.request, io
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "Atelier360-medias/1.0 (cours d'anglais; https://github.com/lefebvrepascal/atelier-360)"}
def get(url):
    for k in range(4):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300).read()
        except Exception as e: print("retry", url[:90], e); time.sleep(5 * (k + 1))
def api(**q):
    q.update(format="json"); r = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(q)); return json.loads(r) if r else {}
ITEMS = {"pencil": "pencil white background", "pen": "ballpoint pen white background", "ruler": "ruler school plastic white background", "rubber": "eraser rubber white background",
 "scissors": "scissors white background", "pencilcase": "pencil case school", "exercisebook": "exercise book notebook school", "schoolbag": "school bag backpack white background",
 "apple": "red apple white background", "banana": "banana white background", "bread": "bread loaf white background", "water": "glass of water", "juice": "glass of orange juice", "milk": "glass of milk"}
os.makedirs("medias/obj", exist_ok=True); out = []
OK = ("CC0", "Public domain", "CC BY", "CC BY-SA", "PD")
for k, q in ITEMS.items():
    d = api(action="query", generator="search", gsrsearch=q + " filetype:bitmap", gsrnamespace=6, gsrlimit=12, prop="imageinfo", iiprop="url|size|extmetadata", iiurlwidth=1024, iiextmetadatafilter="Artist|LicenseShortName")
    pages = sorted(d.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99)); n = 0
    for p in pages:
        if "imageinfo" not in p: continue
        ii = p["imageinfo"][0]; m = ii.get("extmetadata", {}); lic = m.get("LicenseShortName", {}).get("value", "")
        if not lic.startswith(OK) or ii.get("width", 0) < 500: continue
        b = get(ii.get("thumburl", ii["url"]))
        if not b: continue
        try:
            im = Image.open(io.BytesIO(b))
            if im.mode in ("RGBA", "LA", "P"):
                im = im.convert("RGBA"); bg = Image.new("RGB", im.size, (255, 255, 255)); bg.paste(im, mask=im.split()[-1]); im = bg
            im.convert("RGB").save(f"medias/obj/{k}_{n}.jpg", quality=88)
        except Exception as e: print("img", e); continue
        out.append({"k": f"{k}_{n}", "title": p["title"], "url": ii.get("descriptionurl", ""), "lic": lic, "artist": m.get("Artist", {}).get("value", "")[:300]}); print(k, n, p["title"], lic); n += 1
        if n >= 4: break
json.dump(out, open("medias/obj/obj.json", "w"), ensure_ascii=False, indent=1)
