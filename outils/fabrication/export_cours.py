"""Exporte UN cours (.json) avec l'éditeur Atelier 360 (index.html du dépôt), en site zip prêt à fusionner.
Usage : python3 export_cours.py <cours.json> <sortie.zip> [scene:video.mp4 ...]
Prérequis : pip install playwright ; Chrome/Chromium ; jszip.min.js (npm i jszip) — voir LISEZMOI.md"""
import sys, threading, functools, http.server, socketserver, os
from playwright.sync_api import sync_playwright
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
JZ = os.environ.get("JSZIP", "node_modules/jszip/dist/jszip.min.js")
CHROME = os.environ.get("CHROME", "/usr/bin/google-chrome")
src, out, vids = sys.argv[1], sys.argv[2], [a.split(":", 1) for a in sys.argv[3:]]
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Q, directory=REPO)); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
AF = open(REPO + "/aframe.min.js", "rb").read(); JS = open(JZ, "rb").read()
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--js-flags=--max-old-space-size=6000"])
    pg = b.new_context(accept_downloads=True, viewport={"width": 1500, "height": 900}).new_page()
    pg.route("**/aframe-v1.6.0.min.js", lambda r: r.fulfill(body=AF, content_type="application/javascript"))
    pg.route("**/jszip.min.js", lambda r: r.fulfill(body=JS, content_type="application/javascript"))
    pg.on("pageerror", lambda e: print("ERREUR PAGE", str(e)[:300], flush=True))
    pg.goto(f"http://127.0.0.1:{port}/index.html"); pg.wait_for_timeout(8000)
    pg.set_input_files("#impJson", src); pg.wait_for_timeout(15000)
    for si, v in vids:
        pg.click(f"#sceneList .scene-item[data-i='{si}']"); pg.wait_for_timeout(2500); pg.set_input_files("#upVid", v); pg.wait_for_timeout(15000)
        if pg.is_checked("#vLoop"): pg.uncheck("#vLoop"); pg.wait_for_timeout(500)
    titre = pg.input_value("#cTitle"); print("importé :", titre)
    pg.click("#sceneList .scene-item[data-i='0']"); pg.wait_for_timeout(3000)
    pg.evaluate("document.querySelectorAll('video').forEach(v=>{try{v.pause()}catch(e){}});const s=document.querySelector('a-scene');if(s&&s.renderer)s.renderer.setAnimationLoop(null);")
    pg.click("#exportBtn"); pg.wait_for_timeout(1500); pg.click("[data-xm='site']"); pg.wait_for_timeout(800)
    for pid, txt in pg.evaluate("[...document.querySelectorAll('#xList li')].map(l=>[l.querySelector('input').dataset.pub,l.textContent.trim()])"):
        if not txt.startswith(titre) and pg.is_checked(f"[data-pub='{pid}']"): pg.uncheck(f"[data-pub='{pid}']")
    with pg.expect_download(timeout=1500000) as dl:
        pg.click("#dlHtml")
        for k in range(60):
            pg.wait_for_timeout(15000)
            if k > 1 and "Télécharger" in pg.evaluate("document.querySelector('#dlHtml').textContent"): break
    dl.value.save_as(out); print("zip :", out); b.close()
