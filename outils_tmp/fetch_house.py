import json, os, time, urllib.parse, urllib.request, io
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "Atelier360-medias/1.0 (cours d'anglais; https://github.com/lefebvrepascal/atelier-360)"}
BUA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36", "Referer": "https://www.pexels.com/"}
def get(url, h=UA):
    for k in range(5):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=300).read()
        except Exception as e: print("retry", url[:90], e); time.sleep(5 * (k + 1))
    print("ECHEC", url); return None
def info(title):
    q = urllib.parse.urlencode({"action": "query", "format": "json", "titles": "File:" + title, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiextmetadatafilter": "Artist|LicenseShortName"})
    return list(json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))["query"]["pages"].values())[0]["imageinfo"][0]
CPANOS = {"front": "Panoramic view from front of Sandburg Home (8011a8cd-22d4-49eb-9e1b-375cc7374aa3).jpg",
 "porch": "360 degree view from the Sandburg Home porch. (db7fe087-bc69-42c1-9cd3-02aea4c0f7d6).jpg",
 "living": "Sandburg Home Living Room (b7a0ca83-a5e6-41b5-bc4b-bd2f97ae97a2).jpg",
 "kitchen": "360 view of the Sandburg Home Kitchen (d0da8053-8da5-4c70-8e49-281c084900ec).jpg",
 "bedroom": "360 view of Mrs. Sandburg's Bedroom (2a47eada-2d4c-4c54-8bce-8fe81c56e617).jpg",
 "guest": "Sandburg Home Guest Room (7c0014e7-ccbc-40dc-be23-25236f546c2f).jpg",
 "bathroom": "Bathroom – Panorama (Greg Zaal via Poly Haven).jpg",
 "ensuite": "En suite – Panorama (Greg Zaal via Poly Haven).jpg",
 "garage": "Garage – Panorama (Greg Zaal via Poly Haven).jpg",
 "lythwood": "Lythwood room – Panorama (Greg Zaal via Poly Haven).jpg"}
ARTS = {"h_house": "Carl Sandurg House, Henderson County, NC, US.jpg", "h_side": "Side of the Carl Sandburg Home overlooking lake.jpg",
 "h_kitchen50": "The Sandburgs 1950s kitchen IMG 4857.JPG", "h_dining": "Sandburg dining room at Flat Rock, NC IMG 4856.JPG",
 "h_parlor": "Sandburg parlor with piano IMG 4861.JPG", "h_study": "Sandburg study IMG 4860.JPG"}
VIDS = {"v_house": "https://videos.pexels.com/video-files/5072388/5072388-hd_1920_1080_30fps.mp4",
 "v_house2": "https://videos.pexels.com/video-files/15857103/15857103-hd_1920_1080_60fps.mp4",
 "v_mailbox": "https://videos.pexels.com/video-files/6212408/6212408-hd_1920_1080_30fps.mp4",
 "v_alarm": "https://videos.pexels.com/video-files/7164570/7164570-hd_1920_1080_30fps.mp4",
 "v_teeth": "https://videos.pexels.com/video-files/10566590/10566590-hd_1920_1080_30fps.mp4",
 "v_breakfast": "https://videos.pexels.com/video-files/4297074/4297074-hd_1920_1080_25fps.mp4",
 "v_tv": "https://videos.pexels.com/video-files/6336762/6336762-hd_1920_1080_25fps.mp4",
 "v_remote": "https://videos.pexels.com/video-files/4297541/4297541-hd_1920_1080_25fps.mp4",
 "v_living": "https://videos.pexels.com/video-files/16641477/16641477-hd_1920_1080_30fps.mp4",
 "v_kitchen": "https://videos.pexels.com/video-files/17246203/17246203-hd_1920_1080_30fps.mp4",
 "v_familytv": "https://videos.pexels.com/video-files/7981370/7981370-hd_1920_1080_25fps.mp4",
 "v_basket": "https://videos.pexels.com/video-files/8337361/8337361-hd_1920_1080_30fps.mp4"}
for d in ("arts", "panos", "videos"): os.makedirs("medias/" + d, exist_ok=True)
credits = {}
for key, title in CPANOS.items():
    ii = info(title); b = get(ii["url"])
    if not b: continue
    im = Image.open(io.BytesIO(b)).convert("RGB")
    s = min(1, 8192 / im.width); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS); im.save(f"medias/panos/{key}.jpg", quality=92)
    m = ii.get("extmetadata", {}); credits[key] = {"file": title, "artist": m.get("Artist", {}).get("value", ""), "license": m.get("LicenseShortName", {}).get("value", "")}
    print(key, im.size)
for key, title in ARTS.items():
    try:
        ii = info(title); im = Image.open(io.BytesIO(get(ii["url"]))).convert("RGB")
    except Exception as e: print("ECHEC", key, e); continue
    s = min(1, 2400 / max(im.size)); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS); im.save(f"medias/arts/{key}.jpg", quality=92)
    m = ii.get("extmetadata", {}); credits[key] = {"file": title, "artist": m.get("Artist", {}).get("value", ""), "license": m.get("LicenseShortName", {}).get("value", "")}
    print(key, im.size)
for key, url in VIDS.items():
    b = get(url, BUA)
    if b: open(f"medias/videos/{key}.mp4", "wb").write(b); credits[key] = {"file": url, "artist": "Pexels", "license": "Pexels License"}; print(key, len(b))
json.dump(credits, open("medias/credits.json", "w"), ensure_ascii=False, indent=1)
