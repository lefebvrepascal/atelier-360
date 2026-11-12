import json, sys, math
c = json.load(open(sys.argv[1])); lim = float(sys.argv[2]) if len(sys.argv) > 2 else 7
for s in c["scenes"]:
    hs = s["hotspots"]
    for i in range(len(hs)):
        for j in range(i + 1, len(hs)):
            a, b = hs[i], hs[j]
            if a.get("t0") is not None or b.get("t0") is not None: continue
            daz = (a["az"] - b["az"] + 180) % 360 - 180; d = math.hypot(daz * math.cos(math.radians((a["el"] + b["el"]) / 2)), a["el"] - b["el"])
            if d < lim: print(s["name"][:20], "|", a.get("title"), a["az"], a["el"], "<->", b.get("title"), b["az"], b["el"], round(d, 1))
