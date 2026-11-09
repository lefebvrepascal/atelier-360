import urllib.request, os
os.makedirs("medias/voix", exist_ok=True)
base = "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/"
for f in ("fr_FR-siwis-medium.onnx", "fr_FR-siwis-medium.onnx.json", "MODEL_CARD"):
    urllib.request.urlretrieve(base + f, "medias/voix/" + f); print(f, os.path.getsize("medias/voix/" + f))
