"""Histoire 3e « La Seconde Guerre mondiale, une guerre d'anéantissement » — format Atelier 360."""
import json, sys, base64
sys.path.insert(0, "/home/claude/ww1")
from helpers import uid, durl, pano, info, quiz, vf, order, match, find, scene, errors
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
D = "/home/claude/ww2"; M = "/home/claude/wmed/medias"; ARTS = f"{M}/arts"; PN = f"{M}/panos"

def img(path, box=None, q=85):
    im = Image.open(path).convert("RGB")
    if box: im = im.crop(box)
    s = min(1, 1280 / im.width, 1280 / im.height)
    if s < 1: im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    return durl(im, q)
def snd(n): return "data:audio/mpeg;base64," + base64.b64encode(open(f"{D}/audio/{n}.mp3", "rb").read()).decode()
def i(title, text, az, el, key=None, audio=None, image=None, **kw):
    h = info(title, text, az, el, **kw)
    if key: h["image"] = img(f"{ARTS}/{key}.jpg")
    if image: h["image"] = image
    if audio: h["audio"] = snd(audio)
    return h
pos = lambda g: json.load(open(f"{D}/gal/{g}.jpg.pos.json"))
G1, G2, G3, G4 = pos("g1"), pos("g2"), pos("g3"), pos("g4")
at = lambda p, k: (p[k]["az"], p[k]["el_cartel"])
def thumb(p): return durl(Image.open(p).convert("RGB").resize((256, 128)), 70)
AR = json.load(open(f"{D}/vid/arch.json"))
S = []

# 1 ------------------------------------------------------------------ une guerre mondiale
S.append(scene("Une guerre mondiale", pano(f"{D}/gal/g1.jpg"),
 "Bienvenue au musée de la Seconde Guerre mondiale. De 1939 à 1945, la guerre touche tous les continents et fait environ 60 millions de morts, en majorité des civils. Commence par la frise devant toi, puis fais le tour de la salle.",
 [
  i("Six années de guerre", "La guerre commence le 1er septembre 1939 et se termine le 2 septembre 1945. Elle oppose l'Axe (Allemagne, Italie, Japon) aux Alliés (Royaume-Uni, France, puis URSS et États-Unis à partir de 1941). On distingue deux phases : les victoires de l'Axe (1939-1942), puis la contre-offensive alliée (1942-1945).", *at(G1, "w_frise"), "w_frise"),
  i("L'Europe dominée par l'Axe", "En 1942, l'Allemagne nazie et ses alliés contrôlent presque toute l'Europe, de la France à l'URSS. Seuls le Royaume-Uni et quelques pays neutres (Suisse, Suède, Espagne, Portugal) y échappent.", *at(G1, "w_map"), "w_map"),
  i("Le régime nazi", "Arrivé au pouvoir en 1933, Hitler impose une dictature totalitaire. Son idéologie est raciste et antisémite : il veut conquérir un « espace vital » à l'Est et soumettre les peuples qu'il juge « inférieurs ». Les grands rassemblements de Nuremberg servent sa propagande.", *at(G1, "w_nuremberg_rally"), "w_nuremberg_rally"),
  i("L'invasion de la Pologne", "Le 1er septembre 1939, l'armée allemande envahit la Pologne. Le 3 septembre, le Royaume-Uni et la France déclarent la guerre à l'Allemagne. Sur cette photo, des soldats allemands arrachent une barrière de la frontière polonaise.", *at(G1, "w_poland"), "w_poland"),
  i("Dunkerque, juin 1940", "En mai-juin 1940, l'Allemagne envahit les Pays-Bas, la Belgique et la France : c'est la « guerre éclair ». Encerclés, plus de 300 000 soldats britanniques et français sont évacués par la mer depuis Dunkerque. Écoute Winston Churchill, Premier ministre britannique, en mai 1940.", *at(G1, "w_dunkirk"), "w_dunkirk", "s_churchill"),
  i("Le Blitz", "De septembre 1940 à mai 1941, l'aviation allemande bombarde Londres et les villes anglaises. Plus de 40 000 civils sont tués. Mais le Royaume-Uni résiste seul face à Hitler. Écoute une sirène d'alerte aérienne.", *at(G1, "w_blitz"), "w_blitz", "s_siren"),
  i("Pearl Harbor", "Le 7 décembre 1941, l'aviation japonaise attaque par surprise la flotte américaine à Pearl Harbor (Hawaï). Les États-Unis entrent en guerre : le conflit devient vraiment mondial. Écoute le président Roosevelt devant le Congrès, le lendemain.", *at(G1, "w_arizona"), "w_arizona", "s_infamy"),
  i("Stalingrad", "En juin 1941, Hitler envahit l'URSS. D'août 1942 à février 1943, Allemands et Soviétiques se battent rue par rue à Stalingrad. La ville est détruite. La capitulation allemande, le 2 février 1943, est un tournant de la guerre.", *at(G1, "w_stalingrad"), "w_stalingrad"),
  i("Une victoire soviétique", "Le général Tchouïkov (à droite) et ses officiers défendent Stalingrad. Après cette victoire, l'Armée rouge reprend l'offensive et avance jusqu'à Berlin en 1945. L'URSS est le pays qui a perdu le plus d'habitants : environ 26 millions de morts.", *at(G1, "w_stalingrad2"), "w_stalingrad2"),
  quiz("L'Axe", "Quels pays forment l'Axe ?", ["Royaume-Uni, France, URSS", "Allemagne, Italie, Japon", "États-Unis, Chine, URSS", "Allemagne, Royaume-Uni, Italie"], 1, "L'Axe réunit l'Allemagne nazie, l'Italie fasciste et le Japon.", -150, -24),
  order("Chronologie", "Range ces événements dans l'ordre.", ["Invasion de la Pologne", "Défaite de la France", "Attaque de Pearl Harbor", "Victoire soviétique à Stalingrad"], "Septembre 1939, juin 1940, décembre 1941, février 1943.", 150, -24),
  vf("La Seconde Guerre mondiale a tué surtout des soldats.", False, "La majorité des victimes sont des civils : bombardements, massacres, famines et génocides.", 180, -24),
 ]))

# 2 ------------------------------------------------------------------ bunker Valentin
S.append(scene("Une guerre totale : le bunker Valentin", pano(f"{PN}/valentin.jpg"),
 "Tu es dans le bunker Valentin, près de Brême, en Allemagne. Les nazis voulaient y construire des sous-marins à la chaîne. Ce lieu montre ce qu'est une guerre totale : toute l'économie et toute la population sont mobilisées, et des hommes sont forcés de travailler pour l'ennemi.",
 [
  i("Un bunker géant", "Le bunker Valentin mesure 426 mètres de long. Ses murs et son toit de béton font jusqu'à 7 mètres d'épaisseur pour résister aux bombes. Il est construit de 1943 à 1945 mais n'a jamais servi.", 0, 6),
  i("Le travail forcé", "Plus de 10 000 personnes ont été forcées de le construire : prisonniers de guerre, déportés des camps de concentration, travailleurs étrangers. Plus d'un millier sont morts d'épuisement, de faim ou de mauvais traitements.", -55, 0),
  i("Une guerre totale", "Dans une guerre totale, les États mobilisent toutes leurs forces : les usines fabriquent des armes, les femmes remplacent les hommes partis au front, la propagande encadre les esprits. Les civils deviennent aussi des cibles.", 55, 0),
  i("Le STO", "En France, à partir de 1943, le Service du travail obligatoire (STO) envoie environ 600 000 jeunes Français travailler en Allemagne. Beaucoup refusent et rejoignent les maquis de la Résistance.", 125, 3),
  i("Un lieu de mémoire", "Aujourd'hui, le bunker est un lieu de mémoire (Denkort Bunker Valentin). Les vitrines et les panneaux racontent l'histoire des travailleurs forcés.", -125, 3),
  find("Les bombes alliées ont percé le toit du bunker en 1945. Trouve le trou dans le plafond !", -7, 40, "Bravo ! En mars 1945, des bombes spéciales britanniques ont percé le toit de béton.", 0, -25, tol=18),
  quiz("Le travail forcé", "Qui a construit le bunker Valentin ?", ["Des ouvriers volontaires bien payés", "Des prisonniers et des travailleurs forcés", "Des soldats américains", "Des machines automatiques"], 1, "Les nazis ont exploité plus de 10 000 prisonniers, déportés et travailleurs forcés.", 90, -24),
  vf("Dans une guerre totale, seuls les soldats participent à l'effort de guerre.", False, "Toute la société est mobilisée : économie, ouvriers, femmes, scientifiques, propagande.", -90, -24),
 ]))

# 3 ------------------------------------------------------------------ la France
S.append(scene("La France dans la guerre", pano(f"{D}/gal/g2.jpg"),
 "En juin 1940, la France est vaincue. Le maréchal Pétain signe l'armistice et met en place le régime de Vichy, qui collabore avec l'Allemagne nazie. Mais certains Français refusent la défaite : c'est la Résistance. Fais le tour de la salle.",
 [
  i("L'appel du 18 juin", "Le 18 juin 1940, depuis Londres, le général de Gaulle appelle à la radio BBC à continuer le combat. Cette affiche, collée à Londres en août 1940, reprend son message : « La France a perdu une bataille ! Mais la France n'a pas perdu la guerre ! »", *at(G2, "w_appel"), "w_appel"),
  i("La France libre", "De Gaulle crée la France libre et les Forces françaises libres (FFL). Il parle régulièrement aux Français à la radio de Londres, que beaucoup écoutent en cachette.", *at(G2, "w_degaulle_bbc"), "w_degaulle_bbc"),
  i("Jean Moulin", "Envoyé par de Gaulle, Jean Moulin unifie les mouvements de résistance de l'intérieur et crée le Conseil national de la Résistance (CNR) en mai 1943. Arrêté par la Gestapo en juin 1943, il meurt sous la torture sans avoir parlé.", *at(G2, "w_moulin"), "w_moulin"),
  i("L'Affiche rouge", "En 1944, les nazis placardent cette affiche contre le groupe Manouchian, des résistants communistes, souvent étrangers et juifs. Elle veut faire croire que la Résistance est faite de « terroristes » étrangers. 22 d'entre eux sont fusillés au Mont-Valérien.", *at(G2, "w_affiche_rouge"), "w_affiche_rouge"),
  i("L'étoile jaune", "À partir de juin 1942, les Juifs de plus de 6 ans doivent porter une étoile jaune en zone occupée. Jenny Plocki montre la sienne : son père a été arrêté et déporté. En juillet 1942, la police française arrête environ 13 000 Juifs à Paris : c'est la rafle du Vel d'Hiv.", *at(G2, "w_etoile"), "w_etoile"),
  i("Une vie difficile", "Pendant l'Occupation, la nourriture, les vêtements et le charbon sont rationnés. Il faut des tickets pour acheter du pain ou de la viande. Le marché noir se développe.", *at(G2, "w_tickets"), "w_tickets"),
  i("La collaboration", "Le 24 octobre 1940, à Montoire, Pétain rencontre Hitler et annonce qu'il entre « dans la voie de la collaboration ». Le régime de Vichy supprime la République, persécute les Juifs et aide l'occupant à traquer les résistants.", *at(G2, "w_montoire"), "w_montoire"),
  i("La ligne de démarcation", "Après l'armistice, la France est coupée en deux : la zone occupée par l'Allemagne au nord et à l'ouest, la zone « libre » gouvernée par Vichy au sud. Il faut un laissez-passer pour franchir la ligne. En novembre 1942, les Allemands occupent toute la France.", *at(G2, "w_demarcation"), "w_demarcation"),
  i("La Libération de Paris", "Le 25 août 1944, après une insurrection des résistants parisiens, la 2e division blindée du général Leclerc entre dans Paris. Le lendemain, de Gaulle descend les Champs-Élysées, acclamé par la foule.", *at(G2, "w_paris44"), "w_paris44"),
  match("Collaboration ou Résistance ?", "Associe chaque personnage ou document à son camp.", [["Pétain à Montoire", "Collaboration"], ["L'appel du 18 juin", "France libre"], ["Jean Moulin", "Résistance intérieure"], ["L'Affiche rouge", "Propagande nazie"]], "Bravo ! Tu sais distinguer collaboration et Résistance.", 180, -24),
  quiz("Vichy", "Qui dirige le régime de Vichy ?", ["Le général de Gaulle", "Le maréchal Pétain", "Jean Moulin", "Le général Leclerc"], 1, "Le maréchal Pétain reçoit les pleins pouvoirs le 10 juillet 1940 et dirige l'État français jusqu'en 1944.", -150, -24),
  vf("La rafle du Vel d'Hiv a été organisée par la police française.", True, "Les 16 et 17 juillet 1942, la police française arrête environ 13 000 Juifs, dont plus de 4 000 enfants, à la demande des nazis.", 150, -24),
 ]))

# 4 ------------------------------------------------------------------ Oradour
O2 = img(f"{PN}/oradour2.jpg", (1200, 200, 3760, 1200)); O3 = img(f"{PN}/oradour3.jpg", (1500, 200, 4500, 1865))
S.append(scene("Oradour-sur-Glane, 10 juin 1944", pano(f"{D}/pw/oradour_w.jpg"),
 "Voici une photo panoramique du village martyr d'Oradour-sur-Glane, en Haute-Vienne. Le 10 juin 1944, quatre jours après le Débarquement, des soldats SS y massacrent 643 habitants. Le village a été laissé en ruines pour que l'on n'oublie pas. Regarde-le en silence.",
 [
  i("Le massacre", "Le 10 juin 1944, la division SS Das Reich, qui remonte vers la Normandie, encercle le village. Les hommes sont fusillés dans des granges ; les femmes et les enfants sont enfermés dans l'église, qui est incendiée. 643 personnes sont tuées, dont plus de 200 enfants.", -35, 8),
  i("Un village martyr", "Après la guerre, l'État décide de conserver les ruines telles quelles. Un nouveau village a été reconstruit à côté. On visite les rues, les maisons brûlées, les rails du tramway.", 25, 8),
  i("Les traces du drame", "Partout dans les ruines, on voit des objets du quotidien : machines à coudre, vélos, voitures rouillées comme celle du médecin du village.", 70, -5, image=O2),
  i("Le mémorial", "Le cimetière et le mémorial gardent les noms des victimes. Un centre de la mémoire, à l'entrée, explique le massacre aux visiteurs.", -75, -5, image=O3),
  i("Une guerre d'anéantissement", "Les nazis mènent aussi une guerre contre les civils : massacres, représailles contre la population pour terroriser et punir les soutiens de la Résistance. À l'Est, des milliers de villages ont subi le même sort.", 0, -20),
  quiz("Oradour", "Combien de personnes ont été massacrées à Oradour-sur-Glane ?", ["43", "143", "643", "6 400"], 2, "643 habitants et personnes de passage, dont plus de 200 enfants, ont été tués le 10 juin 1944.", -130, -15),
  vf("Les victimes d'Oradour étaient des soldats.", False, "Ce sont des civils : hommes, femmes et enfants du village.", 130, -15),
 ]))

# 5 ------------------------------------------------------------------ la Shoah
S.append(scene("La Shoah", pano(f"{D}/gal/g3.jpg"),
 "Cette salle est consacrée à la Shoah, le génocide des Juifs d'Europe. Un génocide est l'extermination d'un peuple parce qu'il est ce qu'il est. Environ 6 millions de Juifs ont été assassinés par les nazis. Les Tsiganes ont aussi été victimes d'un génocide. Prends le temps de lire.",
 [
  i("Deux sortes de camps", "Les camps de concentration (Dachau, Buchenwald, Mauthausen…) enferment opposants, résistants, Juifs, Tsiganes, homosexuels… qui y meurent de faim, d'épuisement et de violences. Les centres de mise à mort (Treblinka, Sobibor, Auschwitz-Birkenau…) sont construits pour tuer les Juifs dès leur arrivée, dans des chambres à gaz.", *at(G3, "w_camps"), "w_camps"),
  i("La Shoah par balles", "À partir de 1941, en URSS occupée, des unités mobiles allemandes, les Einsatzgruppen, fusillent les Juifs au bord de fosses communes. Plus d'un million et demi de personnes sont tuées ainsi.", 0, -22),
  i("Auschwitz I", "Auschwitz, en Pologne, est le plus grand complexe concentrationnaire nazi. Au-dessus de l'entrée du camp principal, l'inscription mensongère « Arbeit macht frei » : « le travail rend libre ».", *at(G3, "w_auschwitz_gate"), "w_auschwitz_gate"),
  i("Auschwitz-Birkenau", "Les trains de déportés entrent par ce porche. Sur le quai, les SS « sélectionnent » : la plupart des déportés sont envoyés immédiatement dans les chambres à gaz. Environ 1,1 million de personnes sont assassinées à Auschwitz-Birkenau, dont un million de Juifs.", *at(G3, "w_birkenau_gate"), "w_birkenau_gate"),
  i("Les traces du camp", "Aujourd'hui, il reste les rails, les ruines des chambres à gaz dynamitées par les SS et les fondations des baraques. Le camp est libéré par l'Armée rouge le 27 janvier 1945, devenu la Journée internationale de la mémoire de l'Holocauste.", *at(G3, "w_birkenau_ramp"), "w_birkenau_ramp"),
  i("Les enfants d'Izieu", "Dans cette maison de l'Ain, 44 enfants juifs étaient cachés. Le 6 avril 1944, sur ordre de Klaus Barbie, chef de la Gestapo de Lyon, ils sont arrêtés avec leurs éducateurs et déportés à Auschwitz. Aucun enfant n'est revenu.", *at(G3, "w_izieu"), "w_izieu"),
  i("Le Mur des Noms", "Au Mémorial de la Shoah, à Paris, sont gravés les noms des quelque 76 000 Juifs déportés de France, dont 11 000 enfants. Seuls environ 2 500 sont revenus.", *at(G3, "w_murnoms"), "w_murnoms"),
  i("Anne Frank", "Anne Frank, jeune Juive allemande, se cache avec sa famille à Amsterdam pendant deux ans. Elle y écrit son Journal. Dénoncés, ils sont arrêtés en août 1944. Anne meurt du typhus au camp de Bergen-Belsen en 1945, à 15 ans.", *at(G3, "w_annefrank"), "w_annefrank"),
  quiz("Le génocide", "Combien de Juifs ont été assassinés pendant la Shoah ?", ["Environ 600 000", "Environ 1 million", "Environ 6 millions", "Environ 60 millions"], 2, "Environ 6 millions de Juifs, soit les deux tiers des Juifs d'Europe, ont été assassinés.", -150, -24),
  match("Les mots de la Shoah", "Associe chaque mot à sa définition.", [["Génocide", "Extermination d'un peuple"], ["Déportation", "Transfert forcé vers les camps"], ["Camp de concentration", "Lieu d'enfermement et de travail forcé"], ["Centre de mise à mort", "Lieu construit pour tuer"]], "Bravo, ces mots sont essentiels pour comprendre la Shoah.", 150, -24),
  vf("Les centres de mise à mort se trouvaient surtout en Pologne.", True, "Treblinka, Sobibor, Belzec, Chelmno, Majdanek et Auschwitz-Birkenau étaient en Pologne occupée.", 180, -24),
 ]))

# 6 ------------------------------------------------------------------ Dachau
S.append(scene("Le mémorial de Dachau", pano(f"{PN}/dachau.jpg"),
 "Tu es au mémorial du camp de concentration de Dachau, près de Munich. C'est le premier camp ouvert par les nazis, dès mars 1933. Il a servi de modèle aux autres camps. Ce lieu invite au recueillement.",
 [
  i("Le monument international", "Cette sculpture de Nandor Glid, elle-même rescapée de la guerre, représente des corps de déportés pris dans les barbelés. Elle a été inaugurée en 1968.", 0, 30),
  i("1933-1945", "Pendant douze ans, plus de 200 000 personnes de toute l'Europe sont enfermées à Dachau : opposants politiques, résistants, Juifs, Tsiganes, prêtres, homosexuels… Plus de 41 000 y meurent.", 0, 2),
  i("La vie au camp", "À gauche, on voit l'emplacement des baraques. Les déportés y dorment entassés. Ils portent un uniforme rayé et un numéro, subissent l'appel interminable, la faim, le froid, les coups et le travail forcé.", -100, 0),
  i("La libération", "Le 29 avril 1945, l'armée américaine libère le camp. Les soldats découvrent des milliers de déportés affamés et malades. Ces images ont révélé au monde l'horreur des camps.", 100, 0),
  i("« Plus jamais »", "Les visiteurs déposent des couronnes de fleurs. Sur le monument, une inscription en cinq langues dit « Plus jamais ». Témoigner et transmettre la mémoire est un devoir.", 150, 5),
  find("Trouve les couronnes de fleurs déposées en hommage aux victimes.", 152, -3, "Bravo ! Chaque année, des délégations de toute l'Europe rendent hommage aux victimes.", 60, -25, tol=15),
  quiz("Dachau", "Quand le camp de Dachau a-t-il été ouvert ?", ["En 1933", "En 1939", "En 1942", "En 1945"], 0, "Dès mars 1933, quelques semaines après l'arrivée d'Hitler au pouvoir, pour enfermer ses opposants.", -60, -25),
 ]))

# 7 ------------------------------------------------------------------ Arromanches
S.append(scene("Arromanches, le port du Débarquement", pano(f"{D}/pw/arromanches_w.jpg"),
 "Voici une vue panoramique de la plage d'Arromanches, en Normandie. Le 6 juin 1944, les Alliés débarquent sur les côtes normandes : c'est le Jour J. Au large, on voit encore les restes d'un port artificiel construit pour ravitailler les armées.",
 [
  i("Le Jour J", "Le 6 juin 1944, environ 156 000 soldats américains, britanniques et canadiens débarquent sur cinq plages : Utah, Omaha, Gold, Juno et Sword. 177 Français du commando Kieffer sont aussi présents. C'est l'opération Overlord, commandée par le général Eisenhower.", -40, 12, "w_jaws"),
  i("Le port artificiel", "Faute de grand port, les Britanniques ont fabriqué en Angleterre d'énormes caissons de béton, remorqués à travers la Manche puis coulés au large d'Arromanches. Des millions de tonnes de matériel y ont débarqué.", 15, 12),
  i("Le mur de l'Atlantique", "Pour empêcher un débarquement, les Allemands ont construit des bunkers et des batteries de canons tout le long de la côte, comme ici à Longues-sur-Mer.", 60, 12, "w_longues"),
  i("Omaha Beach", "Sur la plage d'Omaha, les soldats américains subissent de très lourdes pertes face aux mitrailleuses allemandes. Le cimetière américain de Colleville-sur-Mer compte plus de 9 000 tombes.", -75, -14, image=img(f"{PN}/omaha.jpg")),
  find("Trouve les caissons du port artificiel, au large.", 10, 0, "Bravo ! Ces blocs de béton sont là depuis 1944.", 0, -20, tol=35),
  quiz("Le Débarquement", "Combien de plages ont été utilisées le 6 juin 1944 ?", ["2", "3", "5", "10"], 2, "Cinq plages : Utah et Omaha (Américains), Gold et Sword (Britanniques), Juno (Canadiens).", 120, -15),
 ]))

# 8 ------------------------------------------------------------------ archives vidéo
T = round(AR["duration"]); cards = AR["cards"]
S.append(scene("Images d'archives (vidéo 360°)",
 {"type": "video", "name": "ww2_archives_360.mp4", "ext": "mp4", "layout": "mono", "loop": False, "mute": False, "duration": T, "thumb": thumb(f"{PN}/reichstag.jpg")},
 "Regarde ces films d'époque, projetés sur un grand écran devant le Reichstag, à Berlin : le Débarquement, la Libération de Paris, la victoire du 8 mai 1945, Berlin et Hiroshima en ruines, le procès de Nuremberg.",
 [info(c["title"], c["text"], 0, -30, t0=c["t0"], t1=c["t1"]) for c in cards] + [
  order("De 1944 à 1946", "Remets ces événements dans l'ordre.", ["Débarquement en Normandie", "Libération de Paris", "Capitulation de l'Allemagne", "Bombe atomique sur Hiroshima", "Procès de Nuremberg"], "6 juin 1944, 25 août 1944, 8 mai 1945, 6 août 1945, 1945-1946.", 120, -20),
 ]))

# 9 ------------------------------------------------------------------ Hiroshima
S.append(scene("Hiroshima, 6 août 1945", pano(f"{D}/pw/hiroshima_w.jpg"),
 "Voici Hiroshima aujourd'hui, au Japon. Au centre, le Dôme de la bombe atomique, un des rares bâtiments restés debout. Le 6 août 1945, les États-Unis larguent pour la première fois une bombe atomique sur une ville.",
 [
  i("La bombe atomique", "La bombe explose à 600 mètres au-dessus de la ville. Environ 70 000 personnes meurent sur le coup ; à la fin de 1945, on compte environ 140 000 morts, à cause des brûlures et des radiations. Écoute le président Truman annoncer la nouvelle.", -45, 8, "w_hiroshima_ruins", "s_truman"),
  i("Le Dôme de Genbaku", "Ce bâtiment était le palais de l'industrie. Il se trouvait presque sous l'explosion. Il a été conservé en ruine et classé au patrimoine mondial de l'UNESCO en 1996, comme symbole de paix.", -10, 15, "w_dome"),
  i("Nagasaki et la capitulation", "Le 9 août 1945, une seconde bombe détruit Nagasaki. Le Japon capitule le 2 septembre 1945 : c'est la fin de la Seconde Guerre mondiale.", 45, 8, "w_nagasaki"),
  i("L'âge nucléaire", "Avec la bombe atomique, l'humanité est capable de s'autodétruire. La peur de l'arme nucléaire marquera toute la guerre froide.", 75, -12),
  find("Trouve le Dôme de la bombe atomique, au centre du panorama.", -10, 3, "Bravo ! Le dôme est le Mémorial de la paix d'Hiroshima.", 0, -18, tol=10),
  vf("Le Japon a capitulé avant l'Allemagne.", False, "L'Allemagne capitule le 8 mai 1945, le Japon le 2 septembre 1945.", -80, -12),
 ]))

# 10 ------------------------------------------------------------------ victoire et bilan
S.append(scene("Victoire et bilan", pano(f"{D}/gal/g4.jpg"),
 "Dernière salle : la victoire des Alliés et le bilan de la guerre. Observe le graphique devant toi, puis fais le tour de la salle et réponds aux questions finales.",
 [
  i("Un bilan effroyable", "Environ 60 millions de morts, dont plus de la moitié de civils. L'URSS compte 26 millions de morts, la Chine environ 15 millions, l'Allemagne 7 millions, la Pologne 6 millions, la France environ 600 000. Des villes entières sont détruites et des millions de personnes sont déplacées.", *at(G4, "w_bilan"), "w_bilan"),
  i("Le Débarquement", "Sur cette célèbre photo de Robert Sargent, des soldats américains quittent leur barge pour Omaha Beach, le 6 juin 1944.", *at(G4, "w_jaws"), "w_jaws"),
  i("Le général Leclerc", "Leclerc commande la 2e division blindée, qui libère Paris en août 1944 puis Strasbourg en novembre 1944, tenant ainsi le serment de Koufra.", *at(G4, "w_leclerc"), "w_leclerc"),
  i("La chute de Berlin", "Le 30 avril 1945, Hitler se suicide. Le 2 mai, Berlin tombe aux mains de l'Armée rouge. Cette photo célèbre montre un soldat soviétique hissant le drapeau rouge sur le Reichstag.", *at(G4, "w_reichstag_flag"), "w_reichstag_flag"),
  i("Le 8 mai 1945", "L'Allemagne capitule sans condition. À Londres, Winston Churchill salue la foule depuis un balcon. En France, le 8 mai est un jour férié.", *at(G4, "w_ve_day"), "w_ve_day"),
  i("La conférence de Yalta", "En février 1945, Churchill, Roosevelt et Staline se réunissent à Yalta pour préparer l'après-guerre : le partage de l'Allemagne et la création de l'ONU.", *at(G4, "w_yalta"), "w_yalta"),
  i("Hiroshima", "Le 6 août 1945, la première bombe atomique est lancée sur Hiroshima. Le nuage de l'explosion monte à des kilomètres de hauteur.", *at(G4, "w_hiroshima_cloud"), "w_hiroshima_cloud"),
  i("Nagasaki", "Trois jours plus tard, une seconde bombe détruit Nagasaki. Le Japon capitule le 2 septembre 1945.", *at(G4, "w_nagasaki"), "w_nagasaki"),
  i("Juger les crimes", "Au procès de Nuremberg (1945-1946), un tribunal international juge 22 dirigeants nazis. Douze sont condamnés à mort. On y définit le crime contre l'humanité. Pour garantir la paix, 51 pays fondent l'ONU en octobre 1945.", *at(G4, "w_nuremberg"), "w_nuremberg"),
  quiz("Le bilan", "Combien de morts la Seconde Guerre mondiale a-t-elle causés ?", ["Environ 6 millions", "Environ 20 millions", "Environ 60 millions", "Environ 200 millions"], 2, "Environ 60 millions de morts, en majorité des civils.", -150, -24),
  match("Les dates de la fin de la guerre", "Associe chaque date à l'événement.", [["6 juin 1944", "Débarquement en Normandie"], ["25 août 1944", "Libération de Paris"], ["8 mai 1945", "Capitulation de l'Allemagne"], ["6 août 1945", "Bombe sur Hiroshima"], ["2 septembre 1945", "Capitulation du Japon"]], "Bravo, tu connais les grandes dates !", 150, -24),
  quiz("L'ONU", "Pourquoi l'ONU est-elle créée en 1945 ?", ["Pour punir l'Allemagne", "Pour maintenir la paix dans le monde", "Pour organiser les Jeux olympiques", "Pour diriger l'Europe"], 1, "L'Organisation des Nations unies veut préserver la paix et faire respecter les droits humains.", 180, -24),
  i("Crédits", "Photos 360° : Wikimedia Commons (CC BY-SA) et Poly Haven (CC0). Photos et films d'archives : domaine public (US National Archives, Office of War Information, Truman Library, Imperial War Museum…), sauf mentions CC BY-SA sur Commons. Discours de Roosevelt, Churchill et Truman : domaine public. Salles de musée, frise, schémas et musique : créés pour ce cours.", 0, -45),
 ]))

# 11 ------------------------------------------------------------------ vidéo récapitulative
S.append(scene("Se souvenir (vidéo 360°)",
 {"type": "video", "name": "ww2_memoire_360.mp4", "ext": "mp4", "layout": "mono", "loop": False, "mute": False, "duration": 130, "thumb": thumb(f"{PN}/dachau.jpg")},
 "Pour terminer, écoute ce résumé de la guerre en visitant des lieux de mémoire : le bunker Valentin, Dachau, Mauthausen, Buchenwald et Berlin.",
 [
  info("Le bunker Valentin", "Guerre totale et travail forcé.", 0, -35, t0=0, t1=25.5),
  info("Dachau", "Le premier camp de concentration, 1933.", 0, -35, t0=25.5, t1=51),
  info("Mauthausen", "Un camp de concentration en Autriche, avec sa carrière de pierre.", 0, -35, t0=51, t1=76.5),
  info("Buchenwald", "Le mémorial du camp de Buchenwald, près de Weimar.", 0, -35, t0=76.5, t1=102),
  info("Berlin", "Le Reichstag, symbole de la défaite nazie en 1945.", 0, -35, t0=102),
  vf("Les lieux de mémoire servent à transmettre l'histoire aux nouvelles générations.", True, "Mémoriaux, musées et cérémonies permettent de ne pas oublier les victimes.", 120, -20),
 ]))

course = {"id": uid(), "title": "La Seconde Guerre mondiale, une guerre d'anéantissement", "matiere": "Histoire", "niveau": "3e", "voix": "fr-FR",
 "objectif": "Connaître les grandes phases de la Seconde Guerre mondiale (1939-1945) ; comprendre la guerre totale et la guerre d'anéantissement ; distinguer collaboration et Résistance en France ; connaître la Shoah et distinguer camps de concentration et centres de mise à mort ; dresser le bilan de la guerre.",
 "updated": 0, "scenes": S}
if errors: print("\n".join(errors)); sys.exit(1)
json.dump(course, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False)
print("scènes", len(S), "points", sum(len(s["hotspots"]) for s in S))
