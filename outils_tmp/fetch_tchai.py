import json, os, time, urllib.parse, urllib.request, io, subprocess
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
UA = {"User-Agent": "Atelier360-medias/1.0 (cours de musique; https://github.com/lefebvrepascal/atelier-360)"}
BUA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36", "Referer": "https://www.pexels.com/"}
def get(url, h=UA):
    for k in range(5):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=600).read()
        except Exception as e: print("retry", url[:80], e); time.sleep(5 * (k + 1))
    return None
def info(title):
    q = urllib.parse.urlencode({"action": "query", "format": "json", "titles": "File:" + title, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiextmetadatafilter": "Artist|LicenseShortName"})
    p = list(json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))["query"]["pages"].values())[0]
    return p["imageinfo"][0] if "imageinfo" in p else None
PANOS = {"kazan": "Санкт-Петербург, Казанский мост, сферопанорама.jpg", "palace": "Palace Square 2016-07 1469101716.jpg",
 "redsquare": "Panorama 360 Red Square.jpg", "nevsky": "Nevsky Prospekt 2016-03 1459001461.jpg", "neva": "Санкт-Петербург, Большая Нева между верфями сферопанорама.jpg"}
ARTS = {"t_portrait": ["Portrait of Pyotr Ilyich Tchaikovsky (1840-1893) by Nikolay Kuznetsov.jpg", "Kuznetsov Tchaikovsky.jpg", "Tchaikovsky by Reutlinger.jpg"],
 "t_reutlinger": ["Tchaikovsky by Reutlinger.jpg"], "t_1863": ["Tchaikovsky in 1863.JPG"], "t_family": ["Семья Чайковских 1848.jpg"],
 "t_votkinsk": ["Усадьба в Воткинске.jpg", "Chaykovsky Birth Place - 2.jpg"], "t_klin": ["Klin. Tchaikovsky State House-Museum. Main house P8120380 2800.jpg"],
 "t_salon": ["Tchaikovsky House-Museum Salon.JPG"], "t_vonmeck": ["Nadezhda von Meck.jpeg"], "t_rubinstein": ["Nikolai Rubinstein 1872.jpg"],
 "t_conservatory": ["Московская Государственная консерватория.JPG"], "t_greathall": ["Great Hall Moscow Conservatory 2024 03.jpg"],
 "t_bolshoi": ["Mihaly Zichy-Auditorium Bolshoi Theatre 1856.jpg"], "t_mariinsky": ["Mariinsky Theatre (exterior).jpg"],
 "t_legnani": ["Swanlakelegnani.jpg"], "t_swan_photo": ["\"Swan lake\", Ballets Russes.jpg"], "t_swan_sodre": ["Swan lake ballet at SODRE.jpg"],
 "t_nut1892": ["Nutcracker -Scene from Act I -Sergei Legat as Nutcracker, Stanislava Stanislavovna Belinskaya as Clara, & Unidentified as a Gingerbread Soldier -1892.jpg"],
 "t_nut_costume": ["Vzevolozhsky's costume sketch for Nutcracker.jpg"], "t_nut_sets": ["Nutcracker set designs.jpg"],
 "t_nut_boston": ["Boston Ballet The Nutcracker 2007.jpg"], "t_trepak": ["Stas Kmiec, The Nutcracker Ballet, Russian Trepak.jpg"],
 "t_hoffmann": ["Artuš Scheiner - Louskáček a Myší král 1.jpg"], "t_brianza": ["Carlotta Brianza 1890 Mariinsky Theater.jpg"], "t_petipa": ["Marius Petipa -1870.JPG"],
 "t_celesta": ["Celesta.jpg", "Celesta Schiedmayer Studio.jpg"], "t_grave": ["Tchaikovsky Grave.jpg"], "t_carnegie": ["Carnegie Hall August 2021.jpg"],
 "t_concerto_score": ["Piano Concerto No. 1 (Tchaikovsky).png"], "t_monument": ["Klin. Tchaikovsky State House-Museum. Monument to Pyotr Ilyich Tchaikovsky P8120385 3150.jpg"]}
AUDIO = {"a_sugar": "Tchaikovsky - Dance of the Sugar Plum Fairy - The Nutcracker.ogg",
 "a_sugar_trepak": "PDP-CH - National Symphony Orchestra of London - Stanford Robinson, conductor - The Nutcracker Suite, Op. 71 - Dance of the Sugar Plum Fairy - Russian Dance - Tchaikovsky - Decca-k1142-ar9057.flac",
 "a_flowers": "P.I. Tchaikovsky's Waltz of the Flowers Performed by The U.S. Army Band, c. 2019.mp3",
 "a_chinese": "PDP-CH - Philadelphia Orchestra - Leopold Stokowski - Nutcracker Suite, Opus 71A - Tchaikovsky - Chinese Dance - Dance of the Flutes - Hmv-db2541-2a87003.flac",
 "a_arab": "PDP-CH - Philadelphia Orchestra - Leopold Stokowski - Nutcracker Suite, Opus 71A - Tchaikovsky - Arab Dance - Hmv-db2541-2a87002.flac",
 "a_swan": "Tchaikovsky Swan Lake Op.20 No.10. Scène.ogg", "a_swan_waltz": "Tchaikovsky Swan Lake Op.20 No.2.Waltz.ogg",
 "a_czardas": "Tchaikovsky Swan Lake Op.20 No.20. Hungarian Dance-Czardas.ogg",
 "a_concerto": "Tchaikovsky, Concerto No.1 in B-flat minor Op.23, I. Allegro.ogg", "a_1812": "1812 Overture, Op. 48 - Pyotr Ilyich Tchaikovsky.ogg",
 "a_1812b": "1812 Overture - United States Marine Band.opus",
 "a_pathetique": "Tchaikovsky - Symphony No. 6 in B minor, Op. 74 'Pathétique' - IV. Finale – Adagio lamentoso (Musopen Symphony).flac",
 "a_pathetique1": "Tchaikovsky - Symphony No. 6 in B minor, Op. 74 'Pathétique' - I. Adagio - Allegro non troppo (Musopen Symphony).flac",
 "a_romeo": "Pyotr Ilyich Tchaikovsky - romeo and juliet- overture-fantasy.ogg", "a_june": "Tchaikovsky the Seasons June.ogg",
 "a_sleeping": "PDP-CH - Marek Weber, piano - The Sleeping Beauty Waltz - Tchaikovsky - Hmv-fkx110-2b4657.flac",
 "a_sym4": "Finale Tchaikovsky Symphony No 4.ogg", "a_violin": "Violin Concerto in D Major, Op. 35 - Pyotr Ilyich Tchaikovsky.ogg"}
CVIDS = {"v_sugar_orch": ("Чайковский Танец Феи Драже из балета Щелкунчик.webm", 0, 999), "v_trepak_orch": ("Чайковский Трепак из балета Щелкунчик.webm", 0, 999),
 "v_flowers_band": ("Waltz of the Flowers Performed by The U.S. Army Band (c. 2019).webm", 0, 150), "v_swan_salut": ("Royal Opera House - Salut.ogv", 0, 999),
 "v_alarusse": ("1 minute trailer for 'a la russe' ballet program.webm", 0, 999), "v_klin": ("Комната Давыдова.webm", 0, 999),
 "v_andante": ("Tchaikovsky - Andante Cantabile - performed by Nina Kotova and Russian String Orchestra, conducted by Misha Rachlevsky - October 27, 2019 - San Fernando Cathedral, San Antonio, Texas.webm", 0, 150),
 "v_concerto": ("Joven pianista interpretando el Concierto para piano No. 1 de Tchaikovsky en el Teatro Llave, Orizaba.webm", 0, 999),
 "v_oldfrench": ("Tchaikovsky Old French Song.webm", 0, 999), "v_1812": ("2005 1812 Overture.ogv", 830, 160),
 "v_klemperer": ("Tchaikovsky - Otto Klemperer conducts Symphony No. 5.webm", 0, 120)}
PVIDS = {"p_tutu_stage": "https://videos.pexels.com/video-files/26607116/11972144_1920_1080_30fps.mp4", "p_tutu_stage2": "https://videos.pexels.com/video-files/26607115/11972153_1920_1080_30fps.mp4",
 "p_group_stage": "https://videos.pexels.com/video-files/26726857/11993645_1920_1080_30fps.mp4", "p_white_tutu": "https://videos.pexels.com/video-files/5051378/5051378-hd_1920_1080_25fps.mp4",
 "p_pointe": "https://videos.pexels.com/video-files/5147635/5147635-hd_1920_1080_25fps.mp4", "p_couple": "https://videos.pexels.com/video-files/8462229/8462229-uhd_2732_1440_25fps.mp4",
 "p_swans": "https://videos.pexels.com/video-files/40439579/17279995_1920_1080_30fps.mp4", "p_girl_stage": "https://videos.pexels.com/video-files/26491560/11954288_1920_1080_24fps.mp4",
 "p_white_dress": "https://videos.pexels.com/video-files/8462219/8462219-uhd_2732_1440_25fps.mp4"}
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
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"/tmp/{k}.{ext}", "-ac", "2", "-b:a", "192k", f"medias/audio/{k}.mp3"], check=False); cred(k, t, ii); print(k)
for k, (t, ss, du) in CVIDS.items():
    ii = info(t)
    if not ii: print("ABSENT", k); continue
    ext = t.rsplit(".", 1)[1]; open(f"/tmp/{k}.{ext}", "wb").write(get(ii["url"]))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(ss), "-t", str(du), "-i", f"/tmp/{k}.{ext}", "-vf", "scale=-2:'min(1080,ih)'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", f"medias/videos/{k}.mp4"], check=False); cred(k, t, ii); print(k)
for k, u in PVIDS.items():
    b = get(u, BUA)
    if not b: continue
    open(f"/tmp/{k}.mp4", "wb").write(b)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"/tmp/{k}.mp4", "-t", "40", "-vf", "scale=1920:-2", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", f"medias/videos/{k}.mp4"], check=False)
    credits[k] = {"file": u, "artist": "Pexels", "license": "Pexels License"}; print(k)
json.dump(credits, open("medias/credits.json", "w"), ensure_ascii=False, indent=1)
