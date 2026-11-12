import urllib.request, re, os
os.makedirs("medias", exist_ok=True); out = []
def head(u, extra=None):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Atelier360-check", "Origin": "https://atelier360-sacre-coeur.netlify.app"}), timeout=120)
        b = r.read(); return r.status, len(b), r.headers.get("Access-Control-Allow-Origin"), b
    except Exception as e: return str(e), 0, None, b""
A = "https://atelier360-sacre-coeur.netlify.app"; M = "https://atelier360-medias.netlify.app/asr/"
s, n, c, b = head(A + "/"); h = b.decode("utf-8", "ignore"); i = h.find("cours/hello-words-for-school-and-home/")
sec = [m.group(1) for m in re.finditer(r"<h2[^>]*>(.*?)</h2>", h) if m.start() < i][-1:] if i > 0 else None
out.append(f"accueil {s} carte={i>0} section={sec}")
for u in [A + "/cours/hello-words-for-school-and-home/", A + "/cours/hello-words-for-school-and-home/audio/voix.js", M + "vosk.js", M + "vosk-model-small-en-us-0.15.tar.gz", M + "LISEZMOI.txt"]:
    s, n, c, _ = head(u); out.append(f"{u} {s} {n} CORS={c}")
print("\n".join(out)); open("medias/check.txt", "w").write("\n".join(out))
