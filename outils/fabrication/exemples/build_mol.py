"""Physique-chimie 4e « Modéliser les molécules » — molécules 3D manipulables à la main (Atelier 360)."""
import json, sys
import numpy as np
sys.path.insert(0, "/home/claude/ww1"); sys.path.insert(0, "/home/claude/mol")
from helpers import uid, durl, quiz, vf, order, match, find, scene, errors, check
from molgen import single, reaction, chain_groups
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
M = "/home/claude/molmed/medias"

def pano(path, roll=0):
    im = Image.open(path).convert("RGB").resize((4096, 2048), Image.LANCZOS)
    if roll: im = Image.fromarray(np.roll(np.asarray(im), -int(roll / 360 * 4096), axis=1))
    return {"type": "image", "data": durl(im, 86), "thumb": durl(im.resize((256, 128), Image.LANCZOS), 70), "name": path.split("/")[-1]}
def art(key):
    im = Image.open(f"{M}/arts/{key}.jpg").convert("RGB"); s = min(1, 1280 / im.width, 1280 / im.height)
    if s < 1: im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    return durl(im, 85)
def i(title, text, az, el, img=None):
    h = {"id": uid(), "type": "info", "title": title, "text": text, "az": az, "el": el}
    if img: h["image"] = art(img)
    return check(h, title)
def mol(title, text, spec, az, el=-4):
    h = {"id": uid(), "type": "mol", "title": title, "text": text, "az": az, "el": el, "mol": spec}
    for n in spec.get("notes", []) + spec.get("steps", []):
        if n and len(n) > 300: errors.append(f"{title} note trop longue")
    return check(h, title)
CH = f"{M}/panos/chimie.jpg"
S = []

# 1 --------------------------------------------------------------------------
S.append(scene("Des atomes aux molécules", pano(CH),
 "Bienvenue dans une salle de chimie ! Toute la matière qui nous entoure est faite d'atomes, si petits qu'on ne peut pas les voir. Pour les étudier, les chimistes utilisent des modèles. Ouvre les points marqués d'une molécule : elle apparaît devant toi et tu peux l'attraper avec les mains.",
 [
  i("Les atomes", "Un atome est minuscule : environ un dix-millionième de millimètre. On connaît 118 sortes d'atomes, les éléments chimiques. Chacun a un nom et un symbole : H pour l'hydrogène, C pour le carbone, O pour l'oxygène, N pour l'azote.", -120, 4, "dalton"),
  i("Les modèles moléculaires", "En classe, on représente chaque atome par une boule. Le code des couleurs est le même partout : hydrogène en blanc, carbone en noir, oxygène en rouge, azote en bleu. Les bâtonnets représentent les liaisons entre les atomes.", -80, 2, "molymods"),
  mol("Le dihydrogène H₂", "Une molécule est un assemblage d'atomes liés entre eux. La molécule de dihydrogène est formée de 2 atomes d'hydrogène. Sa formule chimique est H₂ : le petit 2 indique le nombre d'atomes.",
      single("[H][H]", "H₂", notes=[None, "Les deux atomes d'hydrogène sont séparés : la molécule H₂ contient 2 atomes."]), 5),
  mol("Le dioxygène O₂", "Le dioxygène, que nous respirons, représente environ 21 % de l'air. Sa molécule est formée de 2 atomes d'oxygène reliés par une double liaison : regarde les deux bâtonnets.",
      single("O=O", "O₂", notes=[None, "La molécule de dioxygène contient 2 atomes d'oxygène."]), 40),
  mol("Le diazote N₂", "Le diazote représente environ 78 % de l'air. Ses 2 atomes d'azote sont reliés par une triple liaison, très solide.",
      single("N#N", "N₂", notes=[None, "La molécule de diazote contient 2 atomes d'azote."]), 75),
  find("Trouve le tableau périodique des éléments, affiché au mur.", -32, 9, "Bravo ! Le tableau périodique, inventé par Mendeleïev en 1869, range tous les éléments chimiques.", -160, -10, tol=16),
  quiz("Code couleur", "Dans les modèles moléculaires, de quelle couleur est l'atome d'oxygène ?", ["Blanc", "Noir", "Rouge", "Bleu"], 2, "Oxygène en rouge, hydrogène en blanc, carbone en noir, azote en bleu.", 150, -12),
  vf("Une molécule est un assemblage d'atomes liés entre eux.", True, "Oui ! Les atomes d'une molécule sont reliés par des liaisons.", 120, 8),
 ]))

# 2 --------------------------------------------------------------------------
S.append(scene("Les molécules de la vie courante", pano(CH, roll=115),
 "Voici quatre molécules très courantes. Ouvre chacune d'elles, fais-la tourner dans tes mains et éclate-la pour compter ses atomes. Retiens bien leur formule chimique.",
 [
  mol("L'eau H₂O", "La molécule d'eau est formée de 2 atomes d'hydrogène et d'1 atome d'oxygène : sa formule est H₂O. Elle a la forme d'un V. Observe l'angle entre les deux liaisons.",
      single("O", "H₂O", notes=[None, "La molécule d'eau est éclatée : 1 atome d'oxygène et 2 atomes d'hydrogène, soit 3 atomes."]), -45),
  mol("Le dioxyde de carbone CO₂", "Le dioxyde de carbone est rejeté quand on respire et quand on brûle du bois ou de l'essence. Sa molécule est droite : 1 atome de carbone entre 2 atomes d'oxygène, reliés par des doubles liaisons.",
      single("O=C=O", "CO₂", notes=[None, "1 atome de carbone et 2 atomes d'oxygène : 3 atomes en tout."]), -15),
  mol("Le méthane CH₄", "Le méthane est le gaz de ville utilisé pour cuisiner. Son atome de carbone est lié à 4 atomes d'hydrogène, disposés comme les sommets d'une pyramide : c'est un tétraèdre.",
      single("C", "CH₄", notes=[None, "1 atome de carbone et 4 atomes d'hydrogène : 5 atomes en tout."]), 15),
  mol("L'ammoniac NH₃", "L'ammoniac sert à fabriquer des engrais. Sa molécule est formée d'1 atome d'azote et de 3 atomes d'hydrogène : sa formule est NH₃.",
      single("N", "NH₃", notes=[None, "1 atome d'azote et 3 atomes d'hydrogène : 4 atomes en tout."]), 45),
  i("Combien de molécules ?", "Une simple goutte d'eau contient environ 1 700 milliards de milliards de molécules d'eau ! C'est pour cela qu'on ne peut pas les voir à l'œil nu.", 90, 4, "goutte"),
  quiz("Lire une formule", "Que signifie la formule CO₂ ?", ["1 atome de carbone et 2 atomes d'oxygène", "2 atomes de carbone et 1 atome d'oxygène", "1 atome de cobalt et 2 atomes d'oxygène", "2 molécules de monoxyde de carbone"], 0, "Le chiffre en indice indique le nombre d'atomes de l'élément placé juste avant. Sans chiffre, il y a 1 atome.", 130, -10),
  match("Formules et noms", "Associe chaque formule au nom de la molécule.", [["H₂O", "Eau"], ["CO₂", "Dioxyde de carbone"], ["CH₄", "Méthane"], ["NH₃", "Ammoniac"], ["O₂", "Dioxygène"]], "Bravo, tu sais lire les formules chimiques !", -130, -10),
  quiz("Compter", "Combien d'atomes en tout dans une molécule de méthane CH₄ ?", ["1", "4", "5", "6"], 2, "1 atome de carbone + 4 atomes d'hydrogène = 5 atomes.", 175, -10),
 ]))

# 3 --------------------------------------------------------------------------
S.append(scene("Des molécules plus grosses", pano(f"{M}/panos/vintage_measuring_lab.jpg"),
 "Certaines molécules contiennent beaucoup plus d'atomes. Ouvre-les, éclate-les en atomes et compte-les avant de répondre aux questions.",
 [
  mol("L'éthanol C₂H₆O", "L'éthanol est l'alcool des boissons alcoolisées et du gel hydroalcoolique. Sa molécule contient 2 atomes de carbone, 6 atomes d'hydrogène et 1 atome d'oxygène.",
      single("CCO", "C₂H₆O", notes=[None, "2 atomes de carbone, 6 d'hydrogène et 1 d'oxygène : 9 atomes."]), -40),
  mol("Le glucose C₆H₁₂O₆", "Le glucose est un sucre fabriqué par les plantes grâce à la photosynthèse. C'est le carburant de nos muscles et de notre cerveau. Ses atomes forment un cycle.",
      single("OC[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O", "C₆H₁₂O₆", notes=[None, "6 atomes de carbone, 12 d'hydrogène et 6 d'oxygène : 24 atomes en tout."]), 0),
  mol("La caféine C₈H₁₀N₄O₂", "La caféine se trouve dans le café, le thé et certains sodas. Sa molécule contient des atomes de carbone, d'hydrogène, d'azote et d'oxygène, organisés en deux cycles.",
      single("Cn1cnc2c1c(=O)n(C)c(=O)n2C", "C₈H₁₀N₄O₂", notes=[None, "8 atomes de carbone, 10 d'hydrogène, 4 d'azote et 2 d'oxygène : 24 atomes."]), 40),
  quiz("Le glucose", "Combien d'atomes de carbone contient une molécule de glucose C₆H₁₂O₆ ?", ["1", "6", "12", "24"], 1, "Le chiffre 6 après le C indique 6 atomes de carbone.", 120, -8),
  quiz("La caféine", "Quels éléments chimiques trouve-t-on dans la caféine C₈H₁₀N₄O₂ ?", ["Carbone et hydrogène seulement", "Carbone, hydrogène, azote et oxygène", "Calcium, hydrogène, néon et oxygène", "Cuivre, hélium et azote"], 1, "C = carbone, H = hydrogène, N = azote, O = oxygène.", -120, -8),
  vf("Toutes les molécules contiennent des atomes de carbone.", False, "Non : l'eau H₂O, le dioxygène O₂ ou l'ammoniac NH₃ n'en contiennent pas.", 180, -8),
 ]))

# 4 --------------------------------------------------------------------------
oct_ = single("CCCCCCCC", "C₈H₁₈", straight=True, groups=chain_groups, explodeLabel="Couper la chaîne",
  notes=["Voici un morceau de chaîne de 8 atomes de carbone.", "La chaîne est coupée en 4 morceaux de 2 atomes de carbone.", "Tout est éclaté en atomes : 8 atomes de carbone et 18 atomes d'hydrogène."])
S.append(scene("Éclater une chaîne : le polyéthylène", pano(f"{M}/panos/vintage_measuring_lab.jpg", roll=180),
 "Les matières plastiques sont faites de molécules géantes en forme de chaînes : les polymères. Ici, tu vas éclater une chaîne carbonée en deux étapes : d'abord en morceaux, puis en atomes. Tu peux aussi écarter les deux mains pour l'éclater.",
 [
  mol("Une chaîne de carbone", "Dans le polyéthylène, les atomes de carbone forment une longue chaîne en zigzag ; chacun porte des atomes d'hydrogène. Ce modèle n'en montre que 8 : une vraie chaîne en compte des milliers !", oct_, 0),
  i("Le polyéthylène", "Le polyéthylène est le plastique le plus fabriqué au monde : sacs, films, bouteilles de lait, bouchons… Il est fabriqué en accrochant les unes aux autres des milliers de petites molécules d'éthylène C₂H₄.", -50, 4, "polyethylene"),
  i("Des granulés de plastique", "Dans l'industrie, les polymères sont livrés sous forme de granulés. Chauffés, ils deviennent mous et sont moulés en objets.", 50, 4, "granules"),
  mol("L'éthylène C₂H₄", "L'éthylène est le « motif » de départ du polyéthylène. Ses 2 atomes de carbone sont reliés par une double liaison. Lors de la fabrication, cette double liaison s'ouvre pour accrocher les molécules entre elles.",
      single("C=C", "C₂H₄", notes=[None, "2 atomes de carbone et 4 atomes d'hydrogène."]), 95),
  quiz("Les polymères", "Qu'est-ce qu'un polymère ?", ["Un atome très lourd", "Une très longue molécule formée d'un motif répété", "Un mélange d'eau et de sel", "Un élément du tableau périodique"], 1, "« Poly » veut dire plusieurs : un polymère répète des milliers de fois le même motif.", -100, -8),
  vf("La formule C₈H₁₈ indique 8 atomes de carbone et 18 atomes d'hydrogène.", True, "Oui : 26 atomes en tout, comme tu as pu le compter en éclatant la chaîne.", 150, -8),
 ]))

# 5 --------------------------------------------------------------------------
comb = reaction(["C", "O=O", "O=O"], ["O=C=O", "O", "O"], "CH₄ + 2 O₂", "CO₂ + 2 H₂O",
  steps=["Les réactifs : 1 molécule de méthane et 2 molécules de dioxygène.", "Les liaisons se cassent : les molécules se séparent en atomes.",
         "Les atomes se réarrangent autrement. Aucun n'apparaît, aucun ne disparaît.", "De nouvelles liaisons se forment : 1 molécule de dioxyde de carbone et 2 molécules d'eau. Ce sont les mêmes atomes !"])
S.append(scene("Une transformation chimique : la combustion du méthane", pano(CH, roll=-120),
 "Quand le gaz brûle dans une cuisinière, une transformation chimique a lieu. Ouvre la réaction et fais-la avancer étape par étape : tu vas voir les atomes changer de partenaires.",
 [
  mol("La combustion du méthane", "Le méthane réagit avec le dioxygène de l'air : il se forme du dioxyde de carbone et de l'eau. Au cours d'une transformation chimique, les atomes des réactifs se réarrangent pour former de nouvelles molécules, les produits.", comb, 0),
  i("La flamme du gaz", "La flamme bleue d'une cuisinière est la combustion du méthane. Elle libère de l'énergie, sous forme de chaleur et de lumière.", -50, 6, "flamme"),
  i("Lavoisier", "Antoine Lavoisier, chimiste français (1743-1794), a montré en pesant soigneusement réactifs et produits que la masse totale se conserve. On résume souvent son idée ainsi : « Rien ne se perd, rien ne se crée, tout se transforme. »", 50, 6, "lavoisier"),
  i("L'équation de réaction", "On écrit la transformation sous forme d'équation : CH₄ + 2 O₂ → CO₂ + 2 H₂O. Les nombres devant les formules indiquent le nombre de molécules. Il y a autant d'atomes de chaque sorte à gauche qu'à droite.", 0, 26),
  quiz("Conservation", "Combien d'atomes d'oxygène y a-t-il dans les réactifs « CH₄ + 2 O₂ » ?", ["1", "2", "4", "6"], 2, "2 molécules O₂ × 2 atomes = 4 atomes d'oxygène. On en retrouve 4 dans les produits : 2 dans CO₂ et 1 dans chaque H₂O.", 110, -8),
  vf("Au cours d'une transformation chimique, des atomes disparaissent.", False, "Non ! Les atomes se conservent : ils se réarrangent seulement pour former d'autres molécules. La masse se conserve donc aussi.", -110, -8),
 ]))

# 6 --------------------------------------------------------------------------
eau = reaction(["[H][H]", "[H][H]", "O=O"], ["O", "O"], "2 H₂ + O₂", "2 H₂O",
  steps=["Les réactifs : 2 molécules de dihydrogène et 1 molécule de dioxygène.", "Les liaisons se cassent.", "Les atomes se réarrangent.", "Il se forme 2 molécules d'eau. On a toujours 4 atomes d'hydrogène et 2 atomes d'oxygène."])
carb = reaction(["[C]", "O=O"], ["O=C=O"], "C + O₂", "CO₂",
  steps=["Les réactifs : 1 atome de carbone et 1 molécule de dioxygène.", "La liaison du dioxygène se casse.", "Les atomes se réarrangent.", "Il se forme 1 molécule de dioxyde de carbone."])
S.append(scene("D'autres transformations chimiques", pano(f"{M}/panos/school_hall.jpg", roll=60),
 "Voici deux autres transformations chimiques. Fais-les avancer étape par étape et vérifie à chaque fois que les atomes se conservent.",
 [
  mol("La synthèse de l'eau", "Le dihydrogène brûle dans le dioxygène en formant de l'eau. Cette réaction alimente certaines fusées et les voitures à hydrogène : elle ne rejette que de l'eau.", eau, -30),
  mol("La combustion du carbone", "Le charbon de bois est presque du carbone pur. Quand il brûle dans un barbecue, ses atomes de carbone s'associent au dioxygène pour former du dioxyde de carbone.", carb, 30),
  quiz("Équation juste", "Quelle équation respecte la conservation des atomes ?", ["H₂ + O₂ → H₂O", "2 H₂ + O₂ → 2 H₂O", "H₂ + O₂ → 2 H₂O", "2 H₂ + 2 O₂ → H₂O"], 1, "À gauche : 4 H et 2 O. À droite : 2 × H₂O = 4 H et 2 O. C'est équilibré !", 100, -8),
  quiz("Réactifs et produits", "Dans la combustion du carbone, quel est le produit ?", ["Le carbone", "Le dioxygène", "Le dioxyde de carbone", "L'eau"], 2, "Les réactifs (carbone et dioxygène) disparaissent ; le produit formé est le dioxyde de carbone.", -100, -8),
 ]))

# 7 --------------------------------------------------------------------------
S.append(scene("Bilan", pano(CH, roll=-125),
 "Dernière étape : vérifie ce que tu as retenu sur les atomes, les molécules et les transformations chimiques.",
 [
  order("Du plus petit au plus grand", "Range du plus petit au plus grand.", ["Un atome d'hydrogène", "Une molécule d'eau", "Une molécule de glucose", "Une chaîne de polyéthylène", "Une goutte d'eau"], "L'atome est le plus petit ; les molécules sont faites d'atomes ; une goutte contient des milliards de milliards de molécules.", -40, -6),
  match("Vocabulaire", "Associe chaque mot à sa définition.", [["Atome", "Plus petite particule d'un élément"], ["Molécule", "Assemblage d'atomes liés"], ["Formule chimique", "Indique les atomes d'une molécule"], ["Réactif", "Espèce consommée lors d'une réaction"], ["Produit", "Espèce formée lors d'une réaction"]], "Bravo, tu maîtrises le vocabulaire de la chimie !", 0, -6),
  quiz("La conservation", "Au cours d'une transformation chimique…", ["les atomes disparaissent", "de nouveaux atomes sont créés", "les atomes se réarrangent et se conservent", "la masse augmente toujours"], 2, "Les atomes se conservent, donc la masse totale se conserve aussi.", 40, -6),
  quiz("Formule", "Une molécule contient 2 atomes de carbone, 4 atomes d'hydrogène et 2 atomes d'oxygène. Quelle est sa formule ?", ["C₂H₄O₂", "C₄H₂O₂", "CH₂O", "C₂H₂O₄"], 0, "C'est l'acide acétique du vinaigre : C₂H₄O₂.", 80, -6),
  i("Crédits", "Photos 360° : Wikimedia Commons (salle de chimie, CC BY 4.0) et Poly Haven (CC0). Images : Wikimedia Commons (domaine public, CC BY et CC BY-SA). Modèles 3D des molécules calculés avec RDKit pour ce cours.", 180, -20),
 ]))

course = {"id": uid(), "title": "Modéliser les molécules : atomes, molécules et transformations chimiques", "matiere": "Physique-chimie", "niveau": "4e", "voix": "fr-FR",
 "objectif": "Utiliser des modèles moléculaires ; lire et écrire une formule chimique ; compter les atomes d'une molécule ; comprendre qu'une transformation chimique est un réarrangement d'atomes qui se conservent.",
 "updated": 0, "scenes": S}
if errors: print("\n".join(errors)); sys.exit(1)
json.dump(course, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False)
print("scènes", len(S), "points", sum(len(s["hotspots"]) for s in S))
