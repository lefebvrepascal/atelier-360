"""Exemples musicaux originaux pour le cours sur le blues (SoundFont GeneralUser GS).
Chaque exemple est composé ici, note par note : aucun enregistrement existant n'est réutilisé.
"""
import math, subprocess, sys, wave, random
import numpy as np
import tinysoundfont

SR = 44100
SF = "/home/claude/blues/gu/GeneralUser-GS.sf2"
random.seed(12)

class Song:
    def __init__(self, bpm, swing=True):
        self.bpm, self.swing, self.ev = bpm, swing, []
    def t(self, beat):
        """temps en secondes ; croches swinguées (2/3 - 1/3)"""
        b = math.floor(beat); f = beat - b
        if self.swing and abs(f - 0.5) < 1e-6: f = 2 / 3
        return (b + f) * 60 / self.bpm
    def note(self, ch, key, beat, dur, vel=90):
        s, e = self.t(beat), self.t(beat + dur) - 0.01
        self.ev.append((s, 1, ch, key, vel)); self.ev.append((max(s + 0.02, e), 0, ch, key, 0))
    def bend(self, ch, beat, value):
        self.ev.append((self.t(beat), 2, ch, value, 0))

def render(song, programs, out, tail=2.0, gain=1.0):
    syn = tinysoundfont.Synth(samplerate=SR, gain=-3)
    sf = syn.sfload(SF)
    for ch, (bank, preset) in programs.items():
        syn.program_select(ch, sf, bank, preset, True) if ch == 9 else syn.program_select(ch, sf, bank, preset)
        syn.pitchbend_range(ch, 2)
    ev = sorted(song.ev, key=lambda e: (e[0], e[1]))
    chunks = []; cur = 0
    for tm, kind, ch, key, vel in ev:
        n = int(tm * SR) - cur
        if n > 0: chunks.append(np.frombuffer(syn.generate(n), dtype=np.float32).copy()); cur += n
        if kind == 1: syn.noteon(ch, key, vel)
        elif kind == 0: syn.noteoff(ch, key)
        else: syn.pitchbend(ch, key)
    chunks.append(np.frombuffer(syn.generate(int(tail * SR)), dtype=np.float32).copy())
    a = np.concatenate(chunks).reshape(-1, 2)
    a = a / max(1e-6, np.abs(a).max()) * 0.89 * gain
    fade = int(0.8 * SR); a[-fade:] *= np.linspace(1, 0, fade)[:, None]
    wav = out.replace(".mp3", ".wav")
    with wave.open(wav, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((a * 32767).astype(np.int16).tobytes())
    if out.endswith(".mp3"):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-b:a", "128k", out], check=True)
    print(out, round(len(a) / SR, 1), "s")
    return len(a) / SR

# ------------------------------------------------------------------ outils harmoniques
# grille de 12 mesures en LA : I I I I / IV IV I I / V IV I V(turnaround)
GRID = ["I", "I", "I", "I", "IV", "IV", "I", "I", "V", "IV", "I", "V"]
ROOT = {"I": 45, "IV": 50, "V": 52}            # La2, Ré3, Mi3 (basses)
GM = dict(PIANO=(0, 0), EPIANO=(0, 4), ORGAN=(0, 16), NYLON=(0, 24), STEEL=(0, 25), JAZZG=(0, 26), CLEANG=(0, 27),
          OVERDRIVE=(0, 29), HARMO=(0, 22), ABASS=(0, 32), EBASS=(0, 33), DRUMS=(128, 0))
KICK, SNARE, HAT, RIDE, CRASH = 36, 38, 42, 51, 49

def shuffle_comp(s, ch, bar0, nbars, grid=GRID, vel=72, octave=0):
    """accompagnement « boogie » à la guitare : quinte puis sixte, croches swinguées"""
    for i in range(nbars):
        r = ROOT[grid[i % 12]] + 12 * octave; b = (bar0 + i) * 4
        for k in range(4):
            top = r + (7 if k % 2 == 0 else 9)
            for off in (0, 0.5):
                s.note(ch, r, b + k + off, 0.45, vel); s.note(ch, top, b + k + off, 0.45, vel - 6)

def walking_bass(s, ch, bar0, nbars, grid=GRID, vel=95):
    for i in range(nbars):
        r = ROOT[grid[i % 12]] - 12; b = (bar0 + i) * 4
        for k, iv in enumerate((0, 4, 7, 9) if i % 2 == 0 else (10, 9, 7, 4)):
            s.note(ch, r + iv, b + k, 0.9, vel)

def drums(s, bar0, nbars, vel=80, ride=False):
    for i in range(nbars):
        b = (bar0 + i) * 4
        for k in range(4):
            s.note(9, RIDE if ride else HAT, b + k, 0.2, vel - 10); s.note(9, RIDE if ride else HAT, b + k + 0.5, 0.2, vel - 30)
            if k in (0, 2): s.note(9, KICK, b + k, 0.3, vel)
            if k in (1, 3): s.note(9, SNARE, b + k, 0.3, vel - 5)

def piano_chords(s, ch, bar0, nbars, grid=GRID, vel=60):
    voic = {"I": (55, 61, 64, 67), "IV": (57, 60, 62, 66), "V": (56, 59, 62, 64)}   # 7es de dominante (A7, D7, E7)
    for i in range(nbars):
        b = (bar0 + i) * 4
        for k in (0.5, 1.5, 2.5, 3.5):
            for n in voic[grid[i % 12]]: s.note(ch, n, b + k, 0.35, vel)

A_BLUES = [57, 60, 62, 63, 64, 67, 69, 72, 74, 75, 76, 79, 81]   # La Do Ré Mib Mi Sol La…

def lick(s, ch, bar0, phrase, vel=96):
    """phrase = liste (temps_dans_la_mesure, note, durée[, bend])"""
    for p in phrase:
        bt, n, d = p[0], p[1], p[2]
        s.note(ch, n, bar0 * 4 + bt, d, vel)
        if len(p) > 3:
            s.bend(ch, bar0 * 4 + bt, 8192); s.bend(ch, bar0 * 4 + bt + 0.15, 8192 + int(4096 * p[3])); s.bend(ch, bar0 * 4 + bt + d, 8192)

# ------------------------------------------------------------------ 1. la grille de 12 mesures (avec un clic de mesure)
def ex_grille(out):
    s = Song(96)
    for k in range(4): s.note(9, 37, k, 0.2, 90)                       # décompte
    shuffle_comp(s, 0, 1, 12); walking_bass(s, 1, 1, 12); drums(s, 1, 12, 70)
    for i in range(12): s.note(9, CRASH if i in (0, 4, 8) else 37, (1 + i) * 4, 0.3, 70 if i in (0, 4, 8) else 50)
    s.note(0, 45, 13 * 4, 2, 80); s.note(0, 52, 13 * 4, 2, 70); s.note(1, 33, 13 * 4, 2, 90); s.note(9, CRASH, 13 * 4, 1, 80)
    return render(s, {0: GM["CLEANG"], 1: GM["ABASS"], 9: GM["DRUMS"]}, out)

# ------------------------------------------------------------------ 2. la gamme blues (avec les « blue notes » mises en valeur)
def ex_gamme(out):
    s = Song(80, swing=False)
    seq = [57, 60, 62, 63, 64, 67, 69, 67, 64, 63, 62, 60, 57]
    for i, n in enumerate(seq):
        s.note(0, n, i, 0.95 if n not in (63,) else 1.6, 100 if n == 63 else 85)
    b0 = len(seq) + 1
    # petite phrase qui utilise la gamme, avec une note « tirée » (bend)
    lick(s, 0, 0, [(b0 + 0, 69, 0.5), (b0 + 0.5, 67, 0.5), (b0 + 1, 64, 0.5), (b0 + 1.5, 62, 0.5, 0.5), (b0 + 2, 60, 1, 0.5), (b0 + 3, 57, 2)])
    s.note(1, 45, b0 * 1, 6, 70)
    return render(s, {0: GM["CLEANG"], 1: GM["ABASS"]}, out)

# ------------------------------------------------------------------ 3. appel et réponse (harmonica / guitare), forme AAB
def ex_appel(out):
    s = Song(88)
    call = [(0, 69, 0.5), (0.5, 72, 0.5), (1, 72, 1, 0.5), (2, 69, 0.5), (2.5, 67, 1)]
    resp = [(0, 76, 0.5), (0.5, 75, 0.5), (1, 72, 0.5), (1.5, 69, 1.5)]
    shuffle_comp(s, 2, 0, 12, vel=55); walking_bass(s, 1, 0, 12, vel=80); drums(s, 0, 12, 55)
    for phrase_bar in (0, 4):                       # A … A (même phrase répétée)
        lick(s, 0, phrase_bar, call); lick(s, 3, phrase_bar + 2, resp)
    lick(s, 0, 8, [(0, 76, 0.5), (0.5, 74, 0.5), (1, 72, 1, 0.5), (2, 69, 1)])   # B (phrase différente)
    lick(s, 3, 10, [(0, 72, 0.5), (0.5, 69, 0.5), (1, 67, 0.5), (1.5, 64, 0.5), (2, 69, 2)])
    s.note(2, 45, 48, 2, 70); s.note(1, 33, 48, 2, 90)
    return render(s, {0: GM["HARMO"], 1: GM["ABASS"], 2: GM["STEEL"], 3: GM["JAZZG"], 9: GM["DRUMS"]}, out)

# ------------------------------------------------------------------ 4. blues rural du Delta : guitare seule, basse alternée, notes glissées
def ex_delta(out):
    s = Song(84)
    for i in range(12):
        r = ROOT[GRID[i]] - 12 + (0 if GRID[i] != "I" else 12) - 12
        r = {"I": 40, "IV": 45, "V": 47}[GRID[i]]
        b = i * 4
        for k in range(4): s.note(0, r, b + k, 0.6, 80)                  # basse au pouce
        if i % 4 == 0 or i in (8, 9):
            top = {"I": 64, "IV": 69, "V": 71}[GRID[i]]
            lick(s, 0, i, [(1, top + 3, 0.5, 1.0), (1.5, top + 3, 0.5), (2, top, 1), (3, top - 2, 0.5, 0.5)], vel=88)
        else:
            for k in (0.5, 1.5, 2.5, 3.5): s.note(0, {"I": 59, "IV": 62, "V": 64}[GRID[i]], b + k, 0.3, 60)
    s.note(0, 40, 48, 3, 80); s.note(0, 64, 48, 3, 70); s.note(0, 59, 48, 3, 60)
    return render(s, {0: GM["STEEL"]}, out)

# ------------------------------------------------------------------ 5. blues électrique de Chicago : groupe complet
def ex_chicago(out, choruses=2):
    s = Song(100)
    n = 12 * choruses
    drums(s, 0, n, 85); walking_bass(s, 1, 0, n, vel=100); piano_chords(s, 2, 0, n, vel=50)
    shuffle_comp(s, 4, 0, n, vel=45, octave=0)
    riffs = [[(0, 69, 0.5), (0.5, 72, 0.5, 0.5), (1, 72, 1), (2.5, 69, 0.5), (3, 67, 1)],
             [(0, 76, 1.5, 1.0), (1.5, 72, 0.5), (2, 74, 0.5), (2.5, 72, 0.5), (3, 69, 1)],
             [(0, 81, 0.5), (0.5, 79, 0.5), (1, 76, 0.5), (1.5, 75, 0.5), (2, 72, 0.5), (2.5, 69, 1.5)]]
    for c in range(choruses):
        for bar in (0, 4, 8):
            lick(s, 3 if c == 1 else 0, c * 12 + bar, riffs[(bar // 4 + c) % 3], vel=100)
    s.note(1, 33, n * 4, 2, 100); s.note(9, CRASH, n * 4, 1, 90); s.note(3, 69, n * 4, 2, 100)
    return render(s, {0: GM["HARMO"], 1: GM["EBASS"], 2: GM["PIANO"], 3: GM["OVERDRIVE"], 4: GM["CLEANG"], 9: GM["DRUMS"]}, out)

# ------------------------------------------------------------------ 6. du blues au rock'n'roll : riff de boogie rapide
def ex_rock(out):
    s = Song(168, swing=False)
    for i in range(12):
        r = ROOT[GRID[i]]; b = i * 4
        for k in range(4):
            for off in (0, 0.5):
                top = r + (7 if k % 2 == 0 else 9)
                s.note(0, r, b + k + off, 0.4, 95); s.note(0, top, b + k + off, 0.4, 90)
            s.note(1, r - 12 + (0, 4, 7, 9)[k], b + k, 0.9, 100)
            s.note(9, HAT, b + k, 0.2, 70); s.note(9, HAT, b + k + 0.5, 0.2, 55)
            s.note(9, SNARE if k % 2 else KICK, b + k, 0.3, 100)
    lick(s, 2, 0, [(0, 76, 0.25), (0.25, 76, 0.25), (0.5, 79, 0.25, 0.5), (1, 76, 0.5)], vel=105)
    lick(s, 2, 8, [(0, 81, 0.5, 1.0), (1, 79, 0.25), (1.25, 76, 0.25), (1.5, 72, 0.5), (2, 69, 2)], vel=105)
    s.note(0, 45, 48, 3, 100); s.note(1, 33, 48, 3, 100); s.note(9, CRASH, 48, 1, 100)
    return render(s, {0: GM["OVERDRIVE"], 1: GM["EBASS"], 2: GM["OVERDRIVE"], 9: GM["DRUMS"]}, out)

if __name__ == "__main__":
    import os; os.makedirs("audio", exist_ok=True)
    for name, f in (("grille", ex_grille), ("gamme", ex_gamme), ("appel", ex_appel), ("delta", ex_delta), ("chicago", ex_chicago), ("rock", ex_rock)):
        f(f"audio/{name}.mp3")
