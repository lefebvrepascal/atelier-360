"""Regroupe les cours par matière sur la page d'accueil d'un site exporté par l'éditeur Atelier 360.
Usage : python3 group_matieres.py <dossier cours-immersifs-360>"""
import re, sys, unicodedata, html

p = sys.argv[1].rstrip("/") + "/index.html"
s = open(p, encoding="utf-8").read()
if 'class="mat"' in s:
    sys.exit("déjà regroupé")
a = s.index("<ul>"); b = s.index("</ul>", a) + 5
cards = re.findall(r'<li class="card">.*?</li>', s[a:b], re.S)
NIV = {"6e": 6, "5e": 5, "4e": 4, "3e": 3}
groups = {}
for c in cards:
    eb = html.unescape(re.search(r'<span class="eb">(.*?)</span>', c).group(1))
    mat, _, niv = eb.partition(" · ")
    titre = html.unescape(re.search(r'<span class="h">(.*?)</span>', c).group(1))
    groups.setdefault(mat.strip() or "Autres", []).append((-NIV.get(niv.strip(), 0), titre, c))
slug = lambda t: re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFD", t.lower()).encode("ascii", "ignore").decode()).strip("-")
COUL = ["#f5b700", "#4fc3a1", "#6aa8ff", "#ff7a6b", "#c38bff", "#ffb066", "#7ad3f0", "#e3e36b"]
mats = sorted(groups, key=lambda m: unicodedata.normalize("NFD", m.lower()))
nav = '<nav class="matnav" aria-label="Matières">' + "".join(
    f'<a href="#{slug(m)}" style="--c:{COUL[k % len(COUL)]}">{html.escape(m)} <b>{len(groups[m])}</b></a>' for k, m in enumerate(mats)) + "</nav>"
secs = []
for k, m in enumerate(mats):
    items = "".join(c for _, _, c in sorted(groups[m]))
    n = len(groups[m])
    secs.append(f'<section class="mat" id="{slug(m)}" style="--c:{COUL[k % len(COUL)]}"><h2>{html.escape(m)}<span>{n} cours</span></h2><ul>{items}</ul></section>')
css = """.matnav{max-width:1100px;margin:0 auto 22px;display:flex;flex-wrap:wrap;gap:10px}
.matnav a{color:#eef0f8;text-decoration:none;font-weight:700;font-size:18px;padding:12px 18px;border-radius:999px;background:#1c2134;border:2px solid var(--c)}
.matnav a:hover,.matnav a:focus{background:var(--c);color:#0e111c}.matnav b{opacity:.75;margin-left:4px}
.mat{max-width:1100px;margin:0 auto 34px;scroll-margin-top:16px}
.mat h2{font-family:"Bricolage Grotesque","Segoe UI",sans-serif;font-weight:800;font-size:clamp(24px,3.5vw,34px);margin:0 0 14px;padding-left:14px;border-left:8px solid var(--c);display:flex;align-items:baseline;gap:14px}
.mat h2 span{font-family:"Atkinson Hyperlegible",sans-serif;font-size:17px;font-weight:700;color:#9aa1bb}
.mat .card .eb{color:var(--c)}"""
s = s[:a] + nav + "".join(secs) + s[b:]
s = s.replace("</style>", css + "</style>", 1)
open(p, "w", encoding="utf-8").write(s)
print({m: len(v) for m, v in groups.items()})
