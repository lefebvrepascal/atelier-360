"""Ajoute les voix (fichiers MP3) à un site exporté par Atelier 360.

Usage : python3 voix360.py <dossier du site> <modele.onnx> <modele.onnx.json>
Pour chaque cours (cours/<nom>/index.html), le script ouvre la page dans Chromium,
demande au lecteur la liste de toutes les phrases qu'il peut prononcer, les synthétise
avec une voix Piper, puis écrit cours/<nom>/audio/<empreinte>.mp3 et audio/voix.js.
"""
import sys, os, json, wave, subprocess, threading, functools, http.server, socketserver, tempfile
from playwright.sync_api import sync_playwright
from piper import PiperVoice

site = sys.argv[1]
VOICES = {"fr": "/home/claude/voix/vrepo/medias/voix/fr_FR-siwis-medium.onnx", "en": "/home/claude/voix/en/en_US-lessac-medium.onnx"}
_cache = {}
def get_voice(lang):
    k = lang[:2]
    if k not in VOICES: return None
    if k not in _cache: _cache[k] = PiperVoice.load(VOICES[k], config_path=VOICES[k] + ".json")
    return _cache[k]

Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=site)
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Q, directory=site))
port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()

courses = sorted(d for d in os.listdir(os.path.join(site, "cours")) if os.path.isfile(os.path.join(site, "cours", d, "index.html")))
if len(sys.argv) > 2: courses = [c for c in courses if c in sys.argv[2:]]
total = 0
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"])
    for c in courses:
        pg = b.new_page()
        pg.goto(f"http://127.0.0.1:{port}/cours/{c}/")
        pg.wait_for_function("window.P && P.speechUnits", timeout=30000)
        info = pg.evaluate("({units:P.speechUnits(), voix:(COURSE.voix||'fr-FR')})")
        pg.close()
        voice = get_voice(info["voix"])
        if voice is None:
            print(f"{c} : langue {info['voix']} sans voix, ignoré")
            continue
        out = os.path.join(site, "cours", c, "audio")
        os.makedirs(out, exist_ok=True)
        manifest = {}
        for u in info["units"]:
            mp3 = os.path.join(out, u["h"] + ".mp3")
            if not os.path.exists(mp3):
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
                    wav = tf.name
                with wave.open(wav, "wb") as wf:
                    voice.synthesize_wav(u["t"], wf)
                subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-af", "apad=pad_dur=0.15", "-ac", "1", "-b:a", "48k", mp3], check=True)
                os.unlink(wav)
            manifest[u["h"]] = "audio/" + u["h"] + ".mp3"
        with open(os.path.join(out, "voix.js"), "w", encoding="utf-8") as f:
            f.write("window.ATL_TTS=" + json.dumps(manifest) + ";\n")
        size = sum(os.path.getsize(os.path.join(out, x)) for x in os.listdir(out))
        total += len(manifest)
        print(f"{c} : {len(manifest)} phrases, {size/1048576:.1f} Mo")
    b.close()
srv.shutdown()
print("Total :", total, "phrases")
