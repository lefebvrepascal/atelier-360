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
 "chi": ["Chicago skyline 1900s photograph", "Cloud Gate Chicago", "Chicago L train elevated", "Great Chicago Fire 1871 illustration", "Chicago deep dish pizza", "Willis Tower"],
 "lc": ["Lewis and Clark map 1814", "Meriwether Lewis portrait Peale", "William Clark portrait Peale", "Sacagawea statue", "Lewis and Clark journal page", "Louisiana Purchase map"],
 "us45": ["Apollo 11 Aldrin footprint", "Berlin airlift C-54", "March on Washington 1963 crowd", "Fall of Berlin Wall 1989", "Neil Armstrong Apollo 11 portrait", "Barack Obama inauguration 2009 crowd"],
 "sp": ["Abraham Lincoln portrait 1863", "Gettysburg Address Bliss copy", "John F. Kennedy inaugural address 1961", "Martin Luther King March on Washington podium", "Emmeline Pankhurst speaking", "Lincoln Memorial statue"],
 "work": ["Lewis Hine spinner girl", "Lewis Hine breaker boys", "Ford assembly line 1913", "Rosie the Riveter poster", "soda fountain teenager 1950s", "lifeguard tower beach"],
 "mig": ["Dorothea Lange Migrant Mother", "Dust Bowl Texas 1935", "Route 66 shield sign", "Great Migration Chicago 1940s", "Sydney Opera House", "Uluru"],
 "cook": ["James Cook portrait Dance", "HMS Endeavour replica", "Maori hongi greeting", "Treaty of Waitangi document", "Maori waka canoe", "Wharenui meeting house"],
 "rights": ["suffragette parade 1913 Washington", "Emmeline Pankhurst arrest", "Rosa Parks 1955", "Selma to Montgomery march 1965", "Edmund Pettus Bridge", "Women's suffrage 19th amendment"],
}
PANOQ = ["Chicago equirectangular", "Chicago 360 panorama Millennium Park", "Cloud Gate 360 panorama", "Chicago river 360",
 "Missouri River panorama 360", "Rocky Mountains equirectangular", "Columbia River Gorge 360 panorama", "Montana 360 panorama prairie",
 "Lincoln Memorial 360 panorama", "National Mall equirectangular", "World War II Memorial Washington 360", "Washington DC 360 panorama",
 "diner interior 360 panorama", "factory equirectangular", "textile mill interior 360",
 "Route 66 360 panorama", "Arizona desert equirectangular", "Sydney 360 panorama", "Uluru 360 panorama", "Australian outback equirectangular",
 "New Zealand 360 panorama", "Bay of Islands panorama 360", "Waitangi 360", "Milford Sound 360 panorama",
 "Edmund Pettus Bridge 360", "Montgomery Alabama 360 panorama", "Parliament Square London 360 panorama", "Westminster equirectangular"]
res = {}
for tag, qs in ARTQ.items(): res[tag] = commons(qs, False, 2, tag); print(tag, len(res[tag]))
res["pano"] = commons(PANOQ, True, 2, "pano"); print("pano", len(res["pano"]))
res["polyhaven"] = []
json.dump(res, open("medias/cand/cand.json", "w"), ensure_ascii=False, indent=1)
