import json, os, urllib.parse, urllib.request, subprocess
UA = {"User-Agent": "Atelier360-medias/1.0 (cours d'anglais; https://github.com/lefebvrepascal/atelier-360)"}
def get(url): return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=600).read()
os.makedirs("medias/video", exist_ok=True); os.makedirs("medias/voix", exist_ok=True)
q = urllib.parse.urlencode({"action": "query", "format": "json", "titles": "File:NYC in 360 - Surviving COVID.webm", "prop": "imageinfo", "iiprop": "url"})
url = list(json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))["query"]["pages"].values())[0]["imageinfo"][0]["url"]
open("/tmp/nyc.webm", "wb").write(get(url))
subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", "283", "-i", "/tmp/nyc.webm", "-t", "64", "-vf", "scale=3840:1920,fade=t=in:st=0:d=1.5,fade=t=out:st=62.5:d=1.5",
  "-af", "afade=t=in:st=0:d=1.5,afade=t=out:st=62:d=2", "-c:v", "libx264", "-preset", "slow", "-crf", "24", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
  "-movflags", "+faststart", "medias/video/manhattan_360.mp4"], check=True)
base = "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/"
for f in ("en_US-lessac-medium.onnx", "en_US-lessac-medium.onnx.json", "MODEL_CARD"):
    open("medias/voix/" + f, "wb").write(get(base + f))
print(os.listdir("medias/video"), os.path.getsize("medias/video/manhattan_360.mp4"))
