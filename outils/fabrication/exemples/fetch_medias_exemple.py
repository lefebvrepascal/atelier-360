import json, os, time, urllib.parse, urllib.request, io, subprocess, glob
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "Atelier360-medias/1.0 (cours d'histoire; https://github.com/lefebvrepascal/atelier-360)"}
def get(url):
    for k in range(4):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=900).read()
        except Exception as e: print("retry", url[:80], e); time.sleep(5 * (k + 1))
def info(title):
    q = urllib.parse.urlencode({"action": "query", "format": "json", "titles": "File:" + title, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiextmetadatafilter": "Artist|LicenseShortName"})
    p = list(json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))["query"]["pages"].values())[0]
    return p["imageinfo"][0] if "imageinfo" in p else None
PANOS = {"buchenwald": "2019-02-15 145630 Gedenkstätte Buchenwald.jpg", "buchenwald2": "2019-02-15 132452 Gedenkstätte Buchenwald Mahnmalsanlage.jpg",
 "dachau": "2023-06-04 121443 Dachau KZ-Gedenkstätte.jpg", "dachau2": "2023-06-04 122046 Dachau KZ-Gedenkstätte.jpg",
 "mauthausen": "2023-10-01 113031 Mauthausen Memorial.jpg", "mauthausen2": "2023-10-01 114116 Mauthausen Memorial.jpg",
 "valentin": "2023-07-11 125840 Bremen Denkort Bunker Valentin.jpg", "arromanches": "Arromanches Mulberry Panorama.jpg",
 "oradour1": "Oradour Panorama 1.JPG", "oradour2": "Oradour Panorama 2.JPG", "oradour3": "Oradour-sur-Glane - Panorama.jpg",
 "hoc": "Pointe du hoc panorama.jpg", "hiroshima": "HiroshimaPeaceMemorialPanorama-2.jpg", "reichstag": "Reichstag 1 – Panorama (Greg Zaal via Poly Haven).jpg",
 "omaha": "Omaha Beach Panorama (41293612).jpeg", "arromanches2": "Arromanches-les-Bains Panorama.jpg"}
ARTS = {"w_jaws": ["Into the Jaws of Death 23-0455M edit.jpg"], "w_arizona": ["The USS Arizona (BB-39) burning after the Japanese attack on Pearl Harbor - NARA 195617 - Edit.jpg"],
 "w_hiroshima_cloud": ["Atomic cloud over Hiroshima - NARA 542192 - Edit.jpg", "Atomic cloud over Hiroshima.jpg"], "w_nagasaki": ["Nagasakibomb.jpg"],
 "w_hiroshima_ruins": ["Hiroshima aerial view after atomic bomb 8-1945.jpeg"], "w_dome": ["A-Bomb Dome.jpg"],
 "w_yalta": ["Yalta Conference (Churchill, Roosevelt, Stalin) (B&W).jpg"], "w_nuremberg": ["Defendants in the dock at the Nuremberg Trials.jpg", "Defendants in the dock at nuremberg trials.jpg"],
 "w_montoire": ["Bundesarchiv Bild 183-H25217, Henry Philippe Petain und Adolf Hitler.jpg"], "w_appel": ["A TOUS LES FRANCAIS La France a perdu une bataille Mais la France n'a pas perdu la guerre, 2022.0.252.jpg", "Appel du 18 juin.jpg"],
 "w_degaulle_bbc": ["Charles de Gaulle micro BBC Londres.jpg", "Charles de Gaulle micro BBC.jpg"], "w_affiche_rouge": ["Affiche rouge.jpg"], "w_moulin": ["Resistance.jpg", "Moulin Harcourt 1937.jpg"],
 "w_paris44": ["Crowds of French patriots line the Champs Elysees-edit2.jpg"], "w_leclerc": ["Liberation de paris - 26 aout 1944 - portrait du general jacques-philippe leclerc de hautecl 427563.jpg"],
 "w_poland": ["Danzig Police at Polish Border (1939-09-01).jpg"], "w_stalingrad": ["RIAN archive 2251 Destroyed Stalingrad does not give up.jpg"], "w_stalingrad2": ["RIAN archive 882837 The defenders of Stalingrad.jpg"],
 "w_blitz": ["The London Blitz 1940 HU54557.jpg"], "w_dunkirk": ["The British Evacuation From Dunkirk in 1940 HU2286.jpg"], "w_tickets": ["Tickets de rationnement-T.JPG"],
 "w_etoile": ["Jenny Plocki - Rafle Vel d'hiv étoile.jpg"], "w_birkenau_gate": ["Gate of Auschwitz II, 28 November 2007.jpg"], "w_birkenau_ramp": ["Auschwitz II-Birkenau. The unloading ramp.jpg"],
 "w_auschwitz_gate": ["The arbeit macht frei gate in Auschwitz I.jpg"], "w_izieu": ["Vue de la maison d'Izieu en 2019.jpg"], "w_murnoms": ["Wall of names, Memorial of the Shoah, Paris (cropped).jpg"],
 "w_annefrank": ["AnneFrankHouseAmsterdamtheNetherlands.jpg"], "w_nuremberg_rally": ["Bundesarchiv Bild 183-2008-1016-502, Nürnberg, Reichsparteitag der NSDAP.jpg"],
 "w_map": ["Second world war europe 1941-1942 map fr.png", "Second world war europe 1941-1942 map en.png", "Second world war europe 1941-1942 map de.png"], "w_demarcation": ["Ligne de démarcation 1940-1942 France Allier.png", "Carte de la ligne de démarcation.jpg"],
 "w_reichstag_flag": ["Raising a flag over the Reichstag - Restoration.jpg"], "w_ve_day": ["Winston Churchill waves to crowds in Whitehall in London as they celebrate VE Day, 8 May 1945. H41849.jpg"],
 "w_longues": ["Longues-sur-Mer Batterie de Longues-sur-Mer 07.jpg"], "w_lst": ["1944 NormandyLST clean.jpg"], "w_un": ["Signing of the United Nations Charter.jpg", "UN charter signing.jpg", "Signing the UN Charter.jpg"]}
AUDIO = {"s_infamy": "Roosevelt Infamy.ogg", "s_truman": "Truman on Hiroshima.oga", "s_siren": "Pneumatic Air Raid Siren.wav", "s_churchill": "Winston Churchill - Be Ye Men of Valour.ogg", "s_partisans": "Le Chant Des Partisans.ogg"}
CVIDS = {"v_dday": "D-Day 1944 Office of War Information.webm", "v_normandy": "Normandy Invasion.webm", "v_paris": "La Libération de Paris, 1944.ogv", "v_berlin": "Flug über das zerstörte Berlin 1945 (in Farbe), Teil 1.webm",
 "v_truman": "President Harry S. Truman on the Atomic Bombing of Hiroshima (1945).webm", "v_hiroshima": "342-usaf-11080 Hiroshima-Blast Effects.webm", "v_warends": "The War Ends in Europe.webm",
 "v_nuremberg": "Ouverture du procès de Nuremberg.webm", "v_truemmer": "SFP 186 - Truemmerfrauen.webm", "v_paris_parade": "US Forces Parade in Paris, France.webm"}
for d in ("arts", "panos", "audio", "videos"): os.makedirs("medias/" + d, exist_ok=True)
credits = {}
def cred(k, t, ii):
    m = ii.get("extmetadata", {}); credits[k] = {"file": t, "artist": m.get("Artist", {}).get("value", ""), "license": m.get("LicenseShortName", {}).get("value", "")}
for k, t in PANOS.items():
    ii = info(t)
    if not ii: print("ABSENT", k); continue
    im = Image.open(io.BytesIO(get(ii["url"]))).convert("RGB"); s = min(1, 8192 / im.width)
    im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS).save(f"medias/panos/{k}.jpg", quality=92); cred(k, t, ii); print(k, im.size)
for k, ts in ARTS.items():
    for t in ts:
        ii = info(t)
        if not ii: print("ABSENT", t); continue
        im = Image.open(io.BytesIO(get(ii["url"])))
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA"); bg = Image.new("RGB", im.size, (255, 255, 255)); bg.paste(im, mask=im.split()[-1]); im = bg
        im = im.convert("RGB"); s = min(1, 2400 / max(im.size))
        im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS).save(f"medias/arts/{k}.jpg", quality=92); cred(k, t, ii); print(k, t); break
for k, t in AUDIO.items():
    ii = info(t)
    if not ii: print("ABSENT", k); continue
    ext = t.rsplit(".", 1)[1]; open(f"/tmp/{k}.{ext}", "wb").write(get(ii["url"]))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"/tmp/{k}.{ext}", "-ac", "1", "-b:a", "128k", f"medias/audio/{k}.mp3"]); cred(k, t, ii); print(k)
for k, t in CVIDS.items():
    ii = info(t)
    if not ii: print("ABSENT", k); continue
    ext = t.rsplit(".", 1)[1]; b = get(ii["url"])
    if not b: continue
    open(f"/tmp/{k}.{ext}", "wb").write(b)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"/tmp/{k}.{ext}", "-vf", "scale=-2:'min(540,ih)'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "26",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k", f"/tmp/{k}.mp4"])
    sz = os.path.getsize(f"/tmp/{k}.mp4")
    if sz > 90_000_000: subprocess.run(["split", "-b", "90m", "-d", f"/tmp/{k}.mp4", f"medias/videos/{k}.mp4.part"])
    else: os.rename(f"/tmp/{k}.mp4", f"medias/videos/{k}.mp4")
    cred(k, t, ii); print(k, sz)
json.dump(credits, open("medias/credits.json", "w"), ensure_ascii=False, indent=1)
