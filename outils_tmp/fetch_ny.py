import json, os, time, urllib.parse, urllib.request, io, subprocess
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "Atelier360-medias/1.0 (cours d'anglais; https://github.com/lefebvrepascal/atelier-360)"}
PANOS = {"ground_zero": "Ground-Zero-Memorial-Photo-Sphere.jpg",
 "flatiron": "Flatiron Building, Madison Square, Broadway - NYC Panorama - panoramio.jpg",
 "central_park": "Central Park - New York - USA - panoramio (3).jpg",
 "dumbo": "Mapillary (lNoUSbtyAsdX6uYPQDqejz) (mapboy) 2024-04-04 15H01M57S998.jpg"}
ARTS = {"liberty": "Statue of Liberty and Ellis Island in New York Harbor (7237132094).jpg",
 "liberty2": "Lady Liberty under a blue sky (cropped).jpg",
 "ellis_hine": "Albanian woman at Ellis Island 1905.jpg",
 "ellis_italians": "Group of Italian immigrants waiting at Ellis Island by Lewis Hine (1908, NYPL 460704) (front).jpg",
 "ellis_hall": "Ellis Island - Great Hall.JPG",
 "cab": "Yellow cab on Times Square Manhattan - New York City.jpg",
 "empire": "View of Empire State Building from Rockefeller Center New York City dllu.jpg",
 "brooklyn_bridge": "Brooklyn Bridge from 60 water.jpg",
 "subway": "Train stopping at a New York subway station (Unsplash).jpg",
 "eagle": "Bald Eagle Portrait.jpg",
 "thanksgiving": "Macy's parade balloon inflation (11678).jpg",
 "hotdog": "Sabrett Hot Dog Cart, New York City.jpg",
 "baseball": "View of a baseball game (Unsplash).jpg",
 "grand_central": "Grand Central Terminal Main Concourse 2019-10-03 20-02.jpg",
 "skyline": "Lower Manhattan skyline from New York Harbor, New York.jpg",
 "apollo": "Apollo Theater, Harlem (2011).jpg",
 "dancers": "Dancers at Times Square (40430022745).jpg"}
def get(url):
    for k in range(5):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300).read()
        except Exception as e: print("retry", e); time.sleep(5 * (k + 1))
    raise SystemExit("échec " + url)
def info(title):
    q = urllib.parse.urlencode({"action": "query", "format": "json", "titles": "File:" + title, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiextmetadatafilter": "Artist|LicenseShortName"})
    return list(json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))["query"]["pages"].values())[0]["imageinfo"][0]
os.makedirs("medias/panos", exist_ok=True); os.makedirs("medias/arts", exist_ok=True); os.makedirs("medias/video", exist_ok=True)
credits = {}
for kind, d, maxw in (("panos", PANOS, 8192), ("arts", ARTS, 2400)):
    for key, title in d.items():
        ii = info(title); im = Image.open(io.BytesIO(get(ii["url"]))).convert("RGB")
        if kind == "panos": im = im.resize((min(8192, im.width), min(8192, im.width) // 2), Image.LANCZOS)
        else:
            s = min(1, maxw / max(im.size)); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        im.save(f"medias/{kind}/{key}.jpg", quality=92)
        m = ii.get("extmetadata", {})
        credits[key] = {"file": title, "artist": m.get("Artist", {}).get("value", ""), "license": m.get("LicenseShortName", {}).get("value", "")}
        print(key, im.size); time.sleep(0.5)
json.dump(credits, open("medias/credits.json", "w"), ensure_ascii=False, indent=1)
# vidéo 360° : planche de vignettes toutes les 15 s
ii = info("NYC in 360 - Surviving COVID.webm")
open("/tmp/nyc.webm", "wb").write(get(ii["url"]))
subprocess.run(["ffmpeg", "-loglevel", "error", "-i", "/tmp/nyc.webm", "-vf", "fps=1/15,scale=640:320", "medias/video/f%03d.jpg"], check=True)
print(os.listdir("medias/video"))
