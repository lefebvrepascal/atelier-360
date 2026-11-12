"""Fusionne un cours exporté (zip d'export_cours.py) dans le dossier du site, range les vidéos à part et regroupe par matière.
Usage : python3 publier.py <dossier du site> <export.zip> [<dossier des médias> <url des médias>]
- le dossier du site contient index.html (page d'accueil), lib/, cours/<slug>/ ...
- si un dossier et une URL de médias sont donnés, les vidéos du cours y sont déplacées et le cours y renvoie
  (hébergement séparé des vidéos, en-têtes CORS : voir LISEZMOI.md).
Ensuite : python3 voix360_multi.py <dossier du site> <slug>  puis mise en ligne."""
import sys, os, re, zipfile, shutil, tempfile, subprocess
site, zp = sys.argv[1].rstrip("/"), sys.argv[2]; med = sys.argv[3] if len(sys.argv) > 4 else None; murl = sys.argv[4].rstrip("/") if med else None
tmp = tempfile.mkdtemp(); zipfile.ZipFile(zp).extractall(tmp); root = os.path.join(tmp, os.listdir(tmp)[0])
new_index = open(root + "/index.html", encoding="utf-8").read(); slug = os.listdir(root + "/cours")[0]
dst = f"{site}/cours/{slug}"
if os.path.isdir(dst): shutil.rmtree(dst)
shutil.copytree(f"{root}/cours/{slug}", dst)
if med and os.path.isdir(dst + "/videos"):
    os.makedirs(f"{med}/{slug}", exist_ok=True)
    for f in os.listdir(dst + "/videos"): shutil.move(f"{dst}/videos/{f}", f"{med}/{slug}/{f}")
    os.rmdir(dst + "/videos"); p = dst + "/index.html"; s = open(p, encoding="utf-8").read()
    open(p, "w", encoding="utf-8").write(s.replace('"src":"videos/', f'"src":"{murl}/{slug}/'))
card = re.findall(r'<li class="card">.*?</li>', new_index, re.S)[0]
old = open(site + "/index.html", encoding="utf-8").read()
cards = [c for c in re.findall(r'<li class="card">.*?</li>', old, re.S) if f'href="cours/{slug}/"' not in c] + [card]
# page d'accueil non regroupée : gabarit de l'export + toutes les cartes, puis regroupement par matière
a = new_index.index("<ul>"); b = new_index.index("</ul>", a)
page = new_index[:a + 4] + "".join(cards) + new_index[b:]
j = page.index("</style>"); page = page[:j] + ".card a:hover,.card a:focus-visible{outline:4px solid #f5b700;outline-offset:2px;border-radius:16px}.card a{min-height:72px}" + page[j:]
open(site + "/index.html", "w", encoding="utf-8").write(page)
subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "group_matieres.py"), site], check=True)
print("publié dans le site :", slug); shutil.rmtree(tmp)
