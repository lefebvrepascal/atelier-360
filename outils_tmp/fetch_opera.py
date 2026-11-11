import json, os, time, urllib.parse, urllib.request
UA = {"User-Agent": "Atelier360-medias/1.0 (cours de musique; https://github.com/lefebvrepascal/atelier-360)"}
def get(url):
    for k in range(5):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=600).read()
        except Exception as e: print("retry", url[:90], e); time.sleep(5 * (k + 1))
    print("ECHEC", url); return None
def info(title):
    q = urllib.parse.urlencode({"action": "query", "format": "json", "titles": "File:" + title, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiextmetadatafilter": "Artist|LicenseShortName"})
    return list(json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))["query"]["pages"].values())[0]["imageinfo"][0]
V = {"o_reine": "Queen of the Night 2.webm", "o_pamina": "Моцарт. Сцена (Паміна і хлопці) з опери \"Чарівна флейта\".ogv",
 "o_popper1": "Spotlight on Opera with Jan Popper - Mozart (Part 1).webm", "o_popper2": "Spotlight on Opera with Jan Popper - Mozart (Part 2).webm",
 "o_leporello": "В. А. Моцарт. Арія Лепорелло.ogv", "o_figaro": "Моарт. Каватина Фігаро - Олег Кабачій.ogv",
 "o_duet": "В. А. Моцарт. Дует Дон Жуана і Церліни.ogv", "o_reine_ua": "Mozart. The queen of the night aria in Ukrainian.ogv",
 "o_cherubino": "Моцарт Арія Керубіно - Анастасія Бєлєвцова.ogv"}
os.makedirs("medias/videos", exist_ok=True); cr = {}
for k, t in V.items():
    try:
        ii = info(t); b = get(ii["url"]); ext = t.rsplit(".", 1)[1]
        open(f"medias/videos/{k}.{ext}", "wb").write(b); m = ii.get("extmetadata", {})
        cr[k] = {"file": t, "artist": m.get("Artist", {}).get("value", ""), "license": m.get("LicenseShortName", {}).get("value", "")}; print(k, len(b))
    except Exception as e: print("ECHEC", k, e)
json.dump(cr, open("medias/credits.json", "w"), ensure_ascii=False, indent=1)
