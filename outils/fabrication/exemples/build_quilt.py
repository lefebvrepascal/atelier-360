"""Physique-chimie 3e « De l'infiniment grand à l'infiniment petit » — voyage dans les échelles (Atelier 360)."""
import json, sys, io, base64
import numpy as np
sys.path.insert(0, "/home/claude/ww1"); sys.path.insert(0, "/home/claude/mol")
from helpers import uid, durl, quiz, vf, order, match, scene, errors, check
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
M = "/home/claude/zmed/medias"; BG = "/home/claude/zoom/bg"

def pano(path):
    im = Image.open(path).convert("RGB").resize((4096, 2048), Image.LANCZOS)
    return {"type": "image", "data": durl(im, 86), "thumb": durl(im.resize((256, 128), Image.LANCZOS), 70), "name": path.split("/")[-1]}
def img(path, mx=1600, q=84):
    im = Image.open(path).convert("RGB"); s = min(1, mx / max(im.size))
    if s < 1: im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    return durl(im, q)
def bgimg(path):
    return durl(Image.open(path).convert("RGB").resize((4096, 2048), Image.LANCZOS), 82)
def mollweide_to_equirect(path, W=2048, H=1024):
    src = np.asarray(Image.open(path).convert("RGB")); g = src.mean(2) > 25; ys, xs = np.where(g); src = src[ys.min():ys.max() + 1, xs.min() + 2:xs.max() - 1]; h, w = src.shape[:2]
    lon = np.linspace(-np.pi, np.pi, W); lat = np.linspace(np.pi / 2, -np.pi / 2, H); LON, LAT = np.meshgrid(lon, lat)
    th = LAT.copy()
    for _ in range(12):
        f = 2 * th + np.sin(2 * th) - np.pi * np.sin(LAT); th -= f / (2 + 2 * np.cos(2 * th) + 1e-9)
    x = 0.97 * 2 * np.sqrt(2) / np.pi * LON * np.cos(th); y = 0.97 * np.sqrt(2) * np.sin(th)
    px = ((x / (2 * np.sqrt(2)) + 1) / 2 * (w - 1)).astype(int).clip(0, w - 1); py = ((1 - (y / np.sqrt(2) + 1) / 2) * (h - 1)).astype(int).clip(0, h - 1)
    return durl(Image.fromarray(src[py, px]), 86)
def i(title, text, az, el, path=None):
    h = {"id": uid(), "type": "info", "title": title, "text": text, "az": az, "el": el}
    if path: h["image"] = img(path, 1280, 85)
    return check(h, title)
A = f"{M}/arts"

Q = json.load(open("/home/claude/zoom/quilt/quilt.json"))
QE = {l["name"]: l["e"] for l in Q}
def qimg(n):
    return "data:image/jpeg;base64," + base64.b64encode(open(f"/home/claude/zoom/quilt/{n}.jpg", "rb").read()).decode()
STOPS = [
 ("univers", "L'Univers observable", "Univers observable", "Diamètre ≈ 93 milliards d'années-lumière (≈ 10²⁷ m)", "C'est toute la partie de l'Univers dont la lumière a eu le temps de nous parvenir depuis le Big Bang, il y a 13,8 milliards d'années. Les couleurs montrent la plus ancienne lumière de l'Univers : le fond diffus cosmologique."),
 ("toile", "La toile cosmique", "Toile cosmique", "≈ 1 milliard d'années-lumière (≈ 10²⁵ m)", "Les galaxies forment d'immenses filaments séparés par de grands vides. Cette image est une simulation numérique."),
 ("galaxies", "Des milliers de galaxies", "Galaxies", "≈ 100 millions d'années-lumière (≈ 10²⁴ m)", "Sur cette photo du télescope spatial Hubble, presque chaque point lumineux est une galaxie. On estime qu'il en existe plus de 100 milliards."),
 ("groupe_local", "Le Groupe local", "Groupe local", "≈ 5 millions d'années-lumière (≈ 5 × 10²² m)", "Notre galaxie, la Voie lactée (« Milky Way »), fait partie d'un petit groupe d'une cinquantaine de galaxies, avec sa grande voisine Andromède, à 2,5 millions d'années-lumière."),
 ("voie_lactee", "La Voie lactée", "Voie lactée", "Diamètre ≈ 100 000 années-lumière (≈ 10²¹ m)", "Notre galaxie compte de 100 à 400 milliards d'étoiles. Nous visons le Soleil, situé dans un bras, à 26 000 années-lumière du centre. C'est une vue d'artiste : personne n'a photographié notre galaxie de l'extérieur."),
 ("etoiles_voisines", "Les étoiles voisines", "Étoiles voisines", "≈ 30 années-lumière (≈ 3 × 10¹⁷ m)", "L'étoile la plus proche du Soleil, Proxima du Centaure, est à 4,2 années-lumière. Une année-lumière, c'est la distance parcourue par la lumière en un an : environ 9 500 milliards de km."),
 ("systeme_solaire", "Le système solaire", "Système solaire", "≈ 10 milliards de km (≈ 10¹³ m)", "Le Soleil et ses planètes. Neptune, la plus lointaine, tourne à 4,5 milliards de km du Soleil. Les quatre planètes proches du Soleil sont encore toutes petites au centre."),
 ("planetes_interieures", "Les planètes proches du Soleil", "Planètes intérieures", "≈ 500 millions de km (≈ 5 × 10¹¹ m)", "Mercure, Vénus, la Terre et Mars. La Terre est à 150 millions de km du Soleil : c'est l'unité astronomique. Nous plongeons maintenant vers la Terre."),
 ("terre_lune", "La Terre et la Lune", "Terre et Lune", "≈ 1 million de km (≈ 10⁹ m)", "La Lune tourne autour de la Terre à environ 384 000 km. Sa lumière, qui est celle du Soleil réfléchie, met un peu plus d'une seconde pour nous parvenir."),
 ("terre", "La Terre", "Terre", "Diamètre ≈ 12 700 km (≈ 10⁷ m)", "Notre planète vue de l'espace, centrée sur… Halluin ! On reconnaît l'Europe, l'Afrique et l'océan Atlantique."),
 ("sat7", "L'Europe de l'Ouest", "Europe de l'Ouest", "≈ 1 500 km (≈ 10⁶ m)", "Image du satellite européen Sentinel-2. On voit la France, la Grande-Bretagne, la Belgique et les Pays-Bas."),
 ("sat9", "Le nord de la France et la Belgique", "Nord et Belgique", "≈ 400 km (≈ 4 × 10⁵ m)", "La Manche, la mer du Nord, la côte belge. Halluin se trouve au centre, juste à la frontière belge."),
 ("sat11", "La métropole lilloise", "Métropole lilloise", "≈ 100 km (10⁵ m)", "Lille, Roubaix, Tourcoing et la vallée de la Lys, qui marque la frontière avec la Belgique."),
 ("ign15", "Halluin", "Halluin", "≈ 6 km (≈ 6 × 10³ m)", "Notre ville, au bord de la Lys. De l'autre côté de la rivière, c'est la Belgique (la ville de Menin). Photo aérienne de l'IGN."),
 ("ign19", "Le quartier du collège", "Le collège", "≈ 400 m (≈ 4 × 10² m)", "Les rues autour du collège du Sacré-Cœur, rue Marthe Nollet. À cette échelle, on distingue les toits, les cours et les voitures."),
 ("toi", "Toi !", "Toi", "≈ 1,6 m (≈ 10⁰ m)", "Un élève allongé dans la cour. Tu te trouves entre l'infiniment grand et l'infiniment petit. Continuons vers ta joue…"),
 ("peau_3cm", "La peau", "La peau", "≈ 3 cm (≈ 10⁻² m)", "De très près, la peau montre des plis et des pores. Pour aller plus loin, il faut un microscope."),
 ("cellules_joue", "Des cellules de la joue", "Cellules de la joue", "≈ 0,2 mm (≈ 10⁻⁴ m)", "Au microscope, on voit les cellules qui tapissent l'intérieur de la joue. Chacune mesure environ 60 micromètres, avec un noyau au centre."),
 ("cellule", "Une cellule", "Une cellule", "≈ 50 µm (≈ 5 × 10⁻⁵ m)", "Une cellule humaine vue au microscope à fluorescence : le noyau en bleu, le squelette de la cellule en vert, les mitochondries en rouge."),
 ("noyau_cellule", "Le noyau de la cellule", "Noyau de la cellule", "≈ 20 µm (≈ 2 × 10⁻⁵ m)", "Le noyau contient l'ADN, la molécule qui porte l'information génétique."),
 ("adn_enroule", "L'ADN enroulé", "ADN enroulé", "≈ 300 nm (≈ 3 × 10⁻⁷ m)", "Dans le noyau, l'ADN est une très longue molécule enroulée autour de protéines, comme un fil autour de bobines."),
 ("adn_helice", "La double hélice d'ADN", "Double hélice", "Largeur ≈ 2 nm (≈ 10⁻⁹ m)", "L'ADN a la forme d'une échelle tordue : la double hélice. Les barreaux de couleur sont les bases qui forment le code génétique."),
 ("atomes", "Les atomes de l'ADN", "Atomes", "≈ 1 nm (≈ 10⁻⁹ m)", "L'ADN, comme toute la matière, est fait d'atomes : carbone en noir, oxygène en rouge, azote en bleu, hydrogène en blanc, phosphore en orange."),
 ("atome", "L'atome de carbone", "Atome", "≈ 0,2 nm (≈ 10⁻¹⁰ m)", "Autour d'un noyau minuscule, 6 électrons, chargés négativement, forment un nuage. L'électron est si petit qu'on ne lui connaît aucune taille."),
 ("vide", "Le vide de l'atome", "Le vide", "≈ 6 pm (≈ 10⁻¹¹ m)", "Entre les électrons et le noyau, il n'y a presque rien. Si l'atome avait la taille d'un stade de football, son noyau serait une tête d'épingle au centre !"),
 ("noyau_atome", "Le noyau de l'atome", "Noyau", "≈ 5 fm (≈ 10⁻¹⁴ m)", "Le noyau d'un atome de carbone : 6 protons (rouges, chargés positivement) et 6 neutrons (gris, sans charge). Il est 100 000 fois plus petit que l'atome."),
 ("proton", "Le proton", "Proton", "≈ 1,7 fm (≈ 10⁻¹⁵ m)", "Le proton est formé de 3 quarks, deux quarks u et un quark d, liés par les gluons. Le neutron, lui, contient un quark u et deux quarks d. Fin du voyage !"),
]
LEVELS = [dict(e=QE[k], name=n, short=sh, size=sz, text=tx) for k, n, sh, sz, tx in STOPS]
ADD = {"toile", "galaxies", "groupe_local", "voie_lactee", "region_soleil", "etoiles_voisines", "soleil_lointain", "systeme_solaire", "planetes_interieures", "terre_lointaine", "terre_lune", "terre"}
QUILT = [dict(e=l["e"], cx=l["cx"], cy=l["cy"], fill=l["fill"], add=l["name"] in ADD, img=qimg(l["name"])) for l in Q]
thumb = durl(Image.open("/home/claude/zoom/quilt/voie_lactee.jpg").convert("RGB").resize((256, 128), Image.LANCZOS), 70)

S = []
S.append(scene("Les puissances de dix", pano(f"{M}/panos/eso_mw.jpg"),
 "Voici le ciel étoilé tout autour de toi. Pour décrire des objets aussi différents qu'une galaxie ou un atome, les scientifiques utilisent les puissances de dix. Découvre-les avant de partir en voyage.",
 [
  i("Les puissances de dix", "10³ = 10 × 10 × 10 = 1 000 : c'est un 1 suivi de 3 zéros. 10⁶ = 1 000 000 (un million). À l'inverse, 10⁻³ = 0,001 (un millième) et 10⁻⁶ = 0,000 001 (un millionième). Chaque puissance de dix est 10 fois plus grande que la précédente.", -40, 5),
  i("Les ordres de grandeur", "L'ordre de grandeur d'une longueur est la puissance de dix la plus proche. Un collégien mesure 1,6 m : l'ordre de grandeur est 10⁰ m, soit 1 m. La Terre mesure 12 700 km, soit environ 10⁷ m.", 0, 5),
  i("Des unités adaptées", "1 km = 10³ m ; 1 mm = 10⁻³ m ; 1 micromètre (µm) = 10⁻⁶ m ; 1 nanomètre (nm) = 10⁻⁹ m. Pour les très grandes distances, on utilise l'année-lumière : environ 9 500 milliards de km, soit environ 10¹⁶ m.", 40, 5),
  quiz("10⁶", "Que vaut 10⁶ ?", ["60", "1 000", "1 000 000", "0,000 001"], 2, "10⁶ = un 1 suivi de 6 zéros = un million.", 100, -8),
  quiz("10⁻³", "Que vaut 10⁻³ mètre ?", ["1 kilomètre", "1 millimètre", "1 micromètre", "1 nanomètre"], 1, "10⁻³ m = 0,001 m = 1 millimètre.", -100, -8),
  vf("Une année-lumière est une durée.", False, "Non ! C'est une distance : celle parcourue par la lumière en une année, environ 9 500 milliards de kilomètres.", 180, -8),
 ]))
zs = scene("Voyage de l'infiniment grand à l'infiniment petit",
 {"type": "zoom", "mode": "quilt", "thumb": thumb, "quilt": QUILT, "levels": LEVELS},
 "Tu pars de l'Univers tout entier pour plonger, sans interruption, jusqu'au collège, puis jusqu'au proton. Écarte les deux mains en pinçant les doigts pour plonger vers l'infiniment petit, rapproche-les pour remonter. Ou lance la visite guidée. L'échelle des distances est sur ta gauche.",
 [])
S.append(zs)
S.append(scene("Au cœur de l'atome", pano(f"{BG}/sub.jpg"),
 "Tu es au cœur de la matière. Toute la matière qui t'entoure, l'air, l'eau, ton corps, est faite d'atomes. Découvre ce qui se cache à l'intérieur.",
 [
  i("La structure de l'atome", "Un atome est formé d'un noyau central, chargé positivement, et d'électrons, chargés négativement, qui se déplacent autour. Un atome contient autant d'électrons que de protons : il est électriquement neutre.", -40, 5),
  i("Le noyau", "Le noyau est formé de protons (chargés +) et de neutrons (sans charge). On les appelle les nucléons. Le noyau est environ 100 000 fois plus petit que l'atome, mais il contient presque toute sa masse.", 0, 5),
  i("L'électron", "L'électron est environ 1 800 fois plus léger qu'un proton. Ses charges négatives équilibrent les charges positives du noyau. Les électrons jouent un rôle essentiel dans les réactions chimiques et dans le courant électrique.", 40, 5),
  quiz("Les charges", "Quelle particule ne porte pas de charge électrique ?", ["Le proton", "Le neutron", "L'électron", "Le noyau"], 1, "Le neutron est neutre ; le proton est positif et l'électron négatif.", 100, -8),
  quiz("Neutralité", "Un atome de carbone a 6 protons. Combien a-t-il d'électrons ?", ["3", "6", "12", "0"], 1, "Un atome est électriquement neutre : il a autant d'électrons que de protons.", -100, -8),
  vf("L'atome est presque entièrement fait de vide.", True, "Oui : le noyau est minuscule et les électrons sont très légers et très petits. L'essentiel de l'atome est vide.", 180, -8),
 ]))
S.append(scene("Bilan : les ordres de grandeur", pano(f"{M}/panos/school_quad.jpg"),
 "De retour à l'échelle humaine ! Vérifie que tu sais classer les objets de l'Univers du plus grand au plus petit.",
 [
  order("Du plus grand au plus petit", "Range du plus grand au plus petit.", ["La Voie lactée", "Le système solaire", "La Terre", "Un être humain", "Une cellule", "Un atome", "Le noyau d'un atome"], "De 10²¹ m pour la Voie lactée à 10⁻¹⁴ m pour le noyau : 35 puissances de dix !", -50, -4),
  match("Ordres de grandeur", "Associe chaque objet à son ordre de grandeur.", [["La Terre", "10⁷ m"], ["Un être humain", "10⁰ m"], ["Une bactérie", "10⁻⁶ m"], ["Un atome", "10⁻¹⁰ m"], ["Le Soleil", "10⁹ m"]], "Bravo, tu maîtrises les ordres de grandeur !", 0, -4),
  quiz("Atome et noyau", "Combien de fois le noyau est-il plus petit que l'atome ?", ["10 fois", "100 fois", "100 000 fois", "Ils ont la même taille"], 2, "Le noyau mesure environ 10⁻¹⁵ m et l'atome 10⁻¹⁰ m : 10⁵, soit 100 000 fois plus petit.", 50, -4),
  quiz("L'année-lumière", "Pourquoi utilise-t-on l'année-lumière en astronomie ?", ["Pour mesurer le temps des voyages spatiaux", "Parce que les distances entre les étoiles sont immenses", "Parce que la lumière est lente", "Pour mesurer la taille des atomes"], 1, "Exprimées en kilomètres, les distances entre les étoiles seraient des nombres gigantesques.", 100, -4),
  i("Crédits", "Images : NASA, ESA, Hubble, Planck (ESA), Gemini Observatory, P. C. Budassi, Solar System Scope, Sentinel-2 cloudless 2016 par EOX (CC BY 4.0), orthophotos IGN (Licence Ouverte), Wikimedia Commons (domaine public, CC0, CC BY, CC BY-SA). Photos 360° : ESO, Poly Haven. Autres images créées pour ce cours.", 180, -18),
 ]))
course = {"id": uid(), "title": "De l'infiniment grand à l'infiniment petit", "matiere": "Physique-chimie", "niveau": "3e", "voix": "fr-FR",
 "objectif": "Voyager de l'Univers observable jusqu'à l'électron ; utiliser les puissances de dix et les ordres de grandeur ; connaître la structure de l'atome : noyau (protons et neutrons) et électrons.",
 "updated": 0, "scenes": S}
if errors: print("\n".join(errors)); sys.exit(1)
json.dump(course, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False)
print("scènes", len(S), "niveaux", len(LEVELS))
