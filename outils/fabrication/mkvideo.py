"""Vidéo 360° : fondus enchaînés d'images équirectangulaires + narration Piper + musique (ducking)."""
import subprocess, wave
import numpy as np
from piper import PiperVoice
FR = "/home/claude/voix/vrepo/medias/voix/fr_FR-siwis-medium.onnx"; EN = "/home/claude/voix/en/en_US-lessac-medium.onnx"
def make(IM, NARR, music, voice, OUT, SEG=27.0, XF=2.5, mus_gain=0.5):
    n = len(IM); T = SEG * n - (n - 1) * XF
    V = PiperVoice.load(voice); SR = 44100; N = int(T * SR); vo = np.zeros(N, np.float32)
    for seg_i, txt in NARR:
        t0 = seg_i * (SEG - XF) + 1.5
        with wave.open("/tmp/vn.wav", "wb") as w: V.synthesize_wav(txt, w)
        with wave.open("/tmp/vn.wav") as w:
            sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        a = np.interp(np.linspace(0, len(a) - 1, int(len(a) * SR / sr)), np.arange(len(a)), a).astype(np.float32)
        i = int(t0 * SR); vo[i:i + len(a)] += a[: N - i]; d = len(a) / SR
        print(f"segment {seg_i}: {t0:.1f} -> {t0 + d:.1f}  (fin du segment {seg_i * (SEG - XF) + SEG:.1f})")
    raw = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-stream_loop", "-1", "-i", music, "-t", str(T + 1), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"])
    mus = np.frombuffer(raw, np.float32)[:N].copy()
    if len(mus) < N: mus = np.pad(mus, (0, N - len(mus)))
    env = np.convolve((np.abs(vo) > 0.01).astype(np.float32), np.ones(int(0.6 * SR)) / (0.6 * SR), "same")
    duck = 1 - 0.65 * np.clip(env * 3, 0, 1)
    fade = np.ones(N, np.float32); f = int(3 * SR); fade[-f:] = np.linspace(1, 0, f); fade[:SR] = np.linspace(0, 1, SR)
    mix = vo * 0.95 + mus * mus_gain * duck * fade; mix /= max(1.0, np.abs(mix).max() / 0.95)
    with wave.open("/tmp/vmix.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    inp = []
    for p in IM: inp += ["-loop", "1", "-framerate", "25", "-t", str(SEG), "-i", p]
    fc = ";".join(f"[{i}:v]scale=3840:1920:flags=lanczos,format=yuv420p,setsar=1[s{i}]" for i in range(n))
    prev = "s0"
    for i in range(1, n):
        lab = "v" if i == n - 1 else f"x{i}"
        fc += f";[{prev}][s{i}]xfade=transition=fade:duration={XF}:offset={i * (SEG - XF)}[{lab}]"; prev = lab
    if n == 1: fc += ";[s0]null[v]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + inp + ["-i", "/tmp/vmix.wav", "-filter_complex", fc, "-map", "[v]", "-map", f"{n}:a", "-t", str(T),
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", "-profile:v", "high", "-level", "5.1",
                    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", OUT], check=True)
    print("ok", OUT, T); return T
