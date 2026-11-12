"""Éducation musicale 4e « Tchaïkovski, le romantisme russe et le ballet » — format Atelier 360."""
import json, sys, base64
sys.path.insert(0, "/home/claude/ww1")
from helpers import uid, durl, pano, info, quiz, vf, order, match, find, scene, errors
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
D = "/home/claude/tchai"; ARTS = "/home/claude/tmed/medias/arts"; TP = "/home/claude/tmed/medias/panos"
def art(key):
    im = Image.open(f"{ARTS}/{key}.jpg").convert("RGB"); s = min(1, 1280 / im.width, 1280 / im.height)
    if s < 1: im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    return durl(im, 85)
def snd(n): return "data:audio/mpeg;base64," + base64.b64encode(open(f"{D}/audio/{n}.mp3", "rb").read()).decode()
def i(title, text, az, el, img=None, audio=None, **kw):
    h = info(title, text, az, el, **kw)
    if img: h["image"] = art(img)
    if audio: h["audio"] = snd(audio)
    return h
def P(path):
    im = Image.open(path).convert("RGB")
    if im.width != 4096: im = im.resize((4096, 2048), Image.LANCZOS)
    im.save("/tmp/p4k.jpg", quality=92); return pano("/tmp/p4k.jpg")
pos = lambda g: json.load(open(f"{D}/gal/{g}.jpg.pos.json"))
G1, G2, G3, G4 = pos("grusse"), pos("gballet"), pos("gnut"), pos("gfin")
at = lambda p, k: (p[k]["az"], p[k]["el_cartel"])
VJ = json.load(open(f"{D}/vid/vids.json"))
def thumb(p): return durl(Image.open(p).convert("RGB").resize((256, 128)), 70)
S = []

# 1 ------------------------------------------------------------------ un compositeur russe
S.append(scene("Un compositeur russe", pano(f"{D}/gal/grusse.jpg"),
 "Bienvenue au musée Tchaïkovski ! Piotr Ilitch Tchaïkovski est le plus célèbre des compositeurs russes. Il vit au XIXe siècle, à l'époque romantique. Ses ballets, Le Lac des cygnes et Casse-Noisette, sont joués dans le monde entier. Clique sur les tableaux et écoute les extraits.",
 [
  i("Une vie de musicien", "Tchaïkovski naît en 1840 et meurt en 1893. Il compose dans tous les genres : symphonies, concertos, opéras, pièces pour piano… mais ce sont surtout ses trois ballets qui l'ont rendu célèbre.", *at(G1, "t_frise"), "t_frise"),
  i("Une enfance dans l'Oural", "Tchaïkovski naît à Votkinsk, une petite ville industrielle de l'Oural, où son père dirige des usines. Enfant très sensible, il commence le piano à cinq ans.", *at(G1, "t_votkinsk"), "t_votkinsk"),
  i("La famille", "Sur cette photo de 1848, Piotr, 8 ans, pose avec ses parents, ses frères et sa sœur. Il adorait sa mère. Elle meurt du choléra quand il a 14 ans : un immense chagrin.", *at(G1, "t_family"), "t_family"),
  i("D'abord fonctionnaire", "Ses parents veulent qu'il ait un métier sérieux : il étudie le droit et devient fonctionnaire au ministère de la Justice. Mais à 22 ans, il choisit la musique et entre au nouveau conservatoire de Saint-Pétersbourg.", *at(G1, "t_1863"), "t_1863"),
  i("Écoute : Juin, Barcarolle", "Dans « Les Saisons », Tchaïkovski écrit douze pièces pour piano, une pour chaque mois. En juin, la barcarolle évoque une promenade en barque : une mélodie mélancolique, typique du romantisme.", at(G1, "t_1863")[0] + 14, at(G1, "t_1863")[1] - 12, None, "a_june"),
  i("Nikolaï Rubinstein", "Rubinstein fonde le conservatoire de Moscou et y engage Tchaïkovski comme professeur d'harmonie en 1866. Il devient son ami… même s'il critique durement son premier concerto pour piano !", *at(G1, "t_rubinstein"), "t_rubinstein"),
  i("Une amitié par lettres", "Nadejda von Meck, une riche veuve passionnée de musique, verse une pension à Tchaïkovski pendant treize ans. Ils s'écrivent plus de 1 200 lettres… mais ne se rencontrent presque jamais !", *at(G1, "t_vonmeck"), "t_vonmeck"),
  i("Le conservatoire de Moscou", "Aujourd'hui, le conservatoire de Moscou porte le nom de Tchaïkovski. Sa statue accueille les étudiants devant l'entrée.", *at(G1, "t_conservatory"), "t_conservatory"),
  i("La grande salle", "Dans cette salle, on joue encore ses œuvres. Le célèbre concours international Tchaïkovski, pour les jeunes musiciens, s'y déroule depuis 1958.", *at(G1, "t_greathall"), "t_greathall"),
  i("Le romantisme", "Le romantisme est un mouvement artistique du XIXe siècle. Les musiciens veulent exprimer leurs émotions : joie, tristesse, amour, nostalgie. Ils utilisent de grands orchestres et de belles mélodies. Tchaïkovski y ajoute des couleurs russes, inspirées des chants populaires.", *at(G1, "t_portrait"), "t_portrait"),
  quiz("Le métier", "Quel était le premier métier de Tchaïkovski ?", ["Danseur", "Fonctionnaire au ministère de la Justice", "Soldat", "Peintre"], 1, "Il a d'abord été fonctionnaire, avant d'entrer au conservatoire à 22 ans.", -150, -22),
  vf("Tchaïkovski vit à l'époque romantique, au XIXe siècle.", True, "Vrai : il vit de 1840 à 1893.", 150, -22),
  find("Trouve la photo de la famille de Tchaïkovski.", G1["t_family"]["az"], G1["t_family"]["el"], "Bravo ! Photo prise en 1848.", -90, -25, 14),
 ]))

# 2 ------------------------------------------------------------------ Saint-Pétersbourg
S.append(scene("Saint-Pétersbourg", P(f"{TP}/kazan.jpg"),
 "Te voici au-dessus de la perspective Nevski, la grande avenue de Saint-Pétersbourg (vraie photo 360°). Au XIXe siècle, c'est la capitale de l'Empire russe. Tchaïkovski y fait ses études et y crée ses grands ballets.",
 [
  i("La perspective Nevski", "La perspective Nevski est l'avenue la plus célèbre de Russie. Elle mesure plus de 4 km. Tchaïkovski s'y promenait souvent.", 0, -18),
  i("La cathédrale Notre-Dame-de-Kazan", "Avec sa grande colonnade en demi-cercle, cette cathédrale s'inspire de Saint-Pierre de Rome. Elle date du début du XIXe siècle.", 115, 8),
  i("La maison Singer", "Cet immeuble à la tour surmontée d'un globe abritait la société des machines à coudre Singer. C'est aujourd'hui une grande librairie.", -140, 6),
  i("Les canaux", "Saint-Pétersbourg est construite sur l'eau : on l'appelle la « Venise du Nord ». Voici le canal Griboïedov.", -105, -14),
  i("L'église du Sauveur-sur-le-Sang-Versé", "Au bout du canal, on aperçoit les bulbes colorés de cette église, construite à l'endroit où le tsar Alexandre II a été assassiné en 1881.", -100, 3),
  i("Le conservatoire", "Le conservatoire de Saint-Pétersbourg ouvre en 1862. Tchaïkovski est l'un de ses tout premiers élèves. Il en sort diplômé en 1865 avec une médaille d'argent.", 60, 6),
  i("Le théâtre Mariinsky", "Dans cette ville se trouve le théâtre Mariinsky, où sont créés La Belle au bois dormant (1890) et Casse-Noisette (1892).", -40, 4, "t_mariinsky"),
  i("Écoute : Concerto pour piano n° 1", "Le début de ce concerto est l'un des plus célèbres de la musique : de puissants accords de piano accompagnent une grande mélodie jouée par les cordes. C'est très romantique !", 30, 12, "t_concerto_score", "a_concerto"),
  quiz("La ville", "Comment surnomme-t-on Saint-Pétersbourg ?", ["La ville lumière", "La Venise du Nord", "La ville éternelle", "La grosse pomme"], 1, "Elle est construite sur des îles et traversée de canaux.", -60, -28),
  find("Trouve la cathédrale Notre-Dame-de-Kazan, avec sa colonnade.", 115, 8, "Bravo !", 160, -28, 16),
 ]))

# 3 ------------------------------------------------------------------ Moscou
S.append(scene("Moscou, la place Rouge", P(f"{D}/pano_redsquare.jpg"),
 "Te voici sur la place Rouge, au cœur de Moscou (vraie photo panoramique, sol complété). Tchaïkovski vit douze ans à Moscou, où il enseigne au conservatoire et compose de nombreuses œuvres.",
 [
  i("La cathédrale Basile-le-Bienheureux", "Avec ses bulbes colorés, cette cathédrale du XVIe siècle est le symbole de la Russie.", -160, 8),
  i("Le Kremlin", "Derrière ces hauts murs rouges se trouve le Kremlin, la forteresse des tsars. Ses cathédrales et ses cloches ont inspiré l'Ouverture 1812.", -100, 4),
  i("La tour Spasskaïa", "Sa grande horloge sonne les heures sur la place Rouge.", -137, 14),
  i("Écoute : l'Ouverture 1812", "Cette œuvre célèbre la victoire de la Russie contre l'armée de Napoléon en 1812. Écoute la fin : l'orchestre, les cloches des églises… et des coups de canon ! On entend aussi l'hymne russe de l'époque.", -60, 12, None, "a_1812"),
  i("Le musée d'Histoire", "Ce bâtiment de briques rouges abrite le musée historique d'État.", 25, 8),
  i("Les grands magasins GOUM", "Ce long bâtiment est une galerie commerciale de la fin du XIXe siècle.", 100, 12),
  i("Le Bolchoï", "Tout près d'ici, le théâtre Bolchoï accueille en 1877 la première du Lac des cygnes. Le ballet est d'abord un échec !", 0, 8, "t_bolshoi"),
  i("Le professeur", "De 1866 à 1878, Tchaïkovski enseigne l'harmonie au conservatoire de Moscou. Il écrit même un manuel d'harmonie pour ses élèves.", 60, 4, "t_rubinstein"),
  quiz("1812", "Que célèbre l'Ouverture 1812 ?", ["La naissance du tsar", "La victoire russe contre Napoléon", "La fondation de Moscou", "La fin de l'hiver"], 1, "La retraite de l'armée de Napoléon en 1812.", -100, -25),
  vf("On entend de vrais coups de canon dans l'Ouverture 1812.", True, "Vrai ! La partition prévoit des tirs de canon. En concert, on les remplace souvent par de grosses percussions.", 100, -25),
  find("Trouve la cathédrale aux bulbes colorés.", -160, 6, "Bravo, c'est Basile-le-Bienheureux !", 160, -25, 14),
 ]))

# 4 ------------------------------------------------------------------ le ballet
S.append(scene("Le ballet", pano(f"{D}/gal/gballet.jpg"),
 "Un ballet est un spectacle où une histoire est racontée par la danse et la musique, sans paroles. Tchaïkovski a transformé la musique de ballet : avant lui, elle servait surtout d'accompagnement. Avec lui, elle devient une grande œuvre symphonique.",
 [
  i("Écoute : le thème des cygnes", "Le Lac des cygnes (1877) : le prince Siegfried tombe amoureux d'Odette, une princesse transformée en cygne par un sorcier. Écoute le célèbre thème joué par le hautbois, accompagné par la harpe et les cordes en trémolo.", *at(G2, "t_swan_sodre"), "t_swan_sodre", "a_swan"),
  i("Odette, le cygne blanc", "La danseuse italienne Pierina Legnani danse Odette en 1895. Elle est aussi Odile, le cygne noir, et réalise 32 fouettés (tours sur une pointe) d'affilée !", *at(G2, "t_legnani"), "t_legnani"),
  i("Écoute : la valse", "Au premier acte du Lac des cygnes, les invités du prince dansent une grande valse. Compte : un-deux-trois, un-deux-trois… La valse est une danse à trois temps.", at(G2, "t_legnani")[0] - 14, at(G2, "t_legnani")[1] - 10, None, "a_swan_waltz"),
  i("Écoute : la czardas", "Au bal du troisième acte, Tchaïkovski écrit des danses de différents pays. La czardas est hongroise : elle commence lentement puis accélère !", at(G2, "t_swan_photo")[0] - 14, at(G2, "t_swan_photo")[1] - 10, None, "a_czardas"),
  i("La Belle au bois dormant", "Ce ballet (1890) raconte le conte de Charles Perrault. Carlotta Brianza crée le rôle de la princesse Aurore.", *at(G2, "t_brianza"), "t_brianza", "a_sleeping"),
  i("Marius Petipa", "Ce chorégraphe français, installé en Russie, invente les pas des ballets de Tchaïkovski. Un chorégraphe crée la danse, comme un compositeur crée la musique.", *at(G2, "t_petipa"), "t_petipa"),
  i("Le théâtre Mariinsky", "Le grand théâtre impérial de Saint-Pétersbourg, où sont créés La Belle au bois dormant et Casse-Noisette.", *at(G2, "t_mariinsky"), "t_mariinsky"),
  i("Le Bolchoï", "Le théâtre Bolchoï de Moscou, ici au XIXe siècle. Le Lac des cygnes y est créé en 1877.", *at(G2, "t_bolshoi"), "t_bolshoi"),
  i("Le tutu et les pointes", "Les ballerines portent un tutu, une jupe de tulle, et dansent sur la pointe des pieds grâce à des chaussons spéciaux : les pointes.", *at(G2, "t_swan_photo"), "t_swan_photo"),
  match("Le vocabulaire du ballet", "Associe chaque mot à sa définition.", [["Ballet", "Histoire racontée par la danse"], ["Chorégraphe", "Celui qui invente les pas"], ["Pointes", "Chaussons pour danser sur les orteils"], ["Valse", "Danse à trois temps"]], "Bravo !", -60, -25),
  quiz("Écoute", "Quel instrument joue le thème des cygnes ?", ["La trompette", "Le hautbois", "Le piano", "La guitare"], 1, "Le hautbois, un instrument à vent de la famille des bois, au son doux et un peu triste.", 60, -25),
  find("Trouve Pierina Legnani en Odette.", G2["t_legnani"]["az"], G2["t_legnani"]["el"], "Bravo !", 150, -25, 14),
 ]))

# 5 ------------------------------------------------------------------ vidéo ballet
B = VJ["ballet"]; tA = B["A"]
S.append(scene("Le ballet en vidéo",
 {"type": "video", "name": "tchai_ballet_360.mp4", "ext": "mp4", "layout": "mono", "loop": False, "mute": False, "duration": round(B["T"]), "thumb": thumb("/home/claude/op2/medias/panos/opera_boston.jpg")},
 "Installe-toi dans cette salle d'opéra (vraie photo 360°) et regarde la scène : d'abord des images de danseurs sur la musique du Lac des cygnes, puis le salut des « cygnes » au Royal Opera House de Londres et un extrait de spectacle du Ballet national des Pays-Bas.",
 [
  info("Le Lac des cygnes", "Écoute le thème des cygnes pendant que les danseurs travaillent : tutu, pointes, arabesques, pas de deux…", 0, -30, t0=0, t1=tA),
  info("Le salut des cygnes", "Royal Opera House de Londres : à la fin du Lac des cygnes, le corps de ballet, en tutus blancs, salue le public.", 0, -30, t0=tA, t1=tA + 21),
  info("Un spectacle de ballet", "Bande-annonce d'un programme « à la russe » du Ballet national des Pays-Bas, à Amsterdam : costumes, décors et pas de deux.", 0, -30, t0=tA + 21),
  quiz("Le ballet", "Dans un ballet, comment l'histoire est-elle racontée ?", ["Par des chanteurs", "Par la danse et la musique", "Par un narrateur", "Par des sous-titres"], 1, "Le ballet raconte une histoire sans paroles.", -110, -22),
  vf("Les danseuses du Lac des cygnes portent des tutus blancs.", True, "Vrai : elles représentent les cygnes.", 110, -22),
  info("Crédits vidéo", "Danseurs : Pexels (licence libre). Salut : Royal Opera House, Wikimedia Commons (CC BY-SA 4.0). Bande-annonce : Ballet national des Pays-Bas, Commons (CC BY-SA 3.0). Salle : Boston Opera House, Commons (CC BY-SA 4.0).", 180, -40),
 ]))

# 6 ------------------------------------------------------------------ Casse-Noisette
S.append(scene("Casse-Noisette", pano(f"{D}/gal/gnut.jpg"),
 "Casse-Noisette (1892) est le ballet de Noël par excellence. Le soir de Noël, la petite Clara reçoit un casse-noisette en bois. À minuit, il prend vie, combat le Roi des souris et emmène Clara au royaume des Confiseries, où l'on danse pour elle.",
 [
  i("Le conte", "Le ballet s'inspire d'un conte allemand d'E. T. A. Hoffmann, Casse-Noisette et le Roi des souris (1816).", *at(G3, "t_hoffmann"), "t_hoffmann"),
  i("La création", "Casse-Noisette est créé au théâtre Mariinsky le 18 décembre 1892. Sur cette photo, le Casse-Noisette, Clara et un soldat de pain d'épice.", *at(G3, "t_nut1892"), "t_nut1892"),
  i("Le célesta", "Tchaïkovski découvre à Paris un instrument nouveau : le célesta. C'est un clavier dont les marteaux frappent des lames de métal : on dirait des clochettes ou des gouttes d'eau ! Il l'utilise en secret pour la Fée Dragée.", *at(G3, "t_celesta"), "t_celesta"),
  i("Écoute : la Danse de la Fée Dragée", "Écoute le célesta, accompagné par les cordes en pizzicato (pincées) et la clarinette basse. Le son est léger, magique et mystérieux.", at(G3, "t_celesta")[0] - 13, at(G3, "t_celesta")[1] - 10, None, "a_sugar"),
  i("Écoute : la Danse russe (Trépak)", "Une danse très rapide et énergique, inspirée des danses populaires russes. Écoute l'accélération et le tambourin à la fin !", *at(G3, "t_trepak"), "t_trepak", "a_sugar_trepak"),
  i("Écoute : la Danse chinoise", "Les flûtes jouent des notes rapides et aiguës, au-dessus des bassons et des pizzicati. Au XIXe siècle, on imagine ainsi l'Orient, de façon très fantaisiste.", *at(G3, "t_nut_costume"), "t_nut_costume", "a_chinese"),
  i("Écoute : la Danse arabe", "Une danse lente et envoûtante, sur un rythme répété (un ostinato) des cordes graves et du tambourin.", at(G3, "t_nut_costume")[0] + 13, at(G3, "t_nut_costume")[1] - 12, None, "a_arab"),
  i("Écoute : la Valse des fleurs", "La grande valse finale commence par une longue introduction à la harpe, puis les cors chantent la mélodie, reprise par les cordes.", *at(G3, "t_nut_sets"), "t_nut_sets", "a_flowers"),
  i("Un ballet de Noël", "Aujourd'hui, Casse-Noisette est joué chaque hiver dans le monde entier. Pour beaucoup de compagnies de danse, c'est le spectacle le plus vu de l'année !", *at(G3, "t_nut_boston"), "t_nut_boston"),
  quiz("Le célesta", "Quel instrument nouveau Tchaïkovski utilise-t-il pour la Fée Dragée ?", ["L'orgue", "Le célesta", "Le xylophone", "Le clavecin"], 1, "Le célesta, inventé à Paris en 1886.", -60, -25),
  quiz("Écoute", "Quelle danse est très rapide et accélère à la fin ?", ["La Danse arabe", "La Danse russe (Trépak)", "La Danse de la Fée Dragée", "La Valse des fleurs"], 1, "Le Trépak, une danse populaire russe.", 60, -25),
  find("Trouve le célesta.", G3["t_celesta"]["az"], G3["t_celesta"]["el"], "Bravo !", 150, -25, 14),
 ]))

# 7 ------------------------------------------------------------------ vidéo orchestre
O = VJ["orch"]; pr = O["parts"]; s0 = [0, pr[0], pr[0] + pr[1], pr[0] + pr[1] + pr[2]]
S.append(scene("L'orchestre joue Tchaïkovski",
 {"type": "video", "name": "tchai_orchestre_360.mp4", "ext": "mp4", "layout": "mono", "loop": False, "mute": False, "duration": round(O["T"]), "thumb": thumb("/home/claude/mzmed/medias/panos/konzerthaus.jpg")},
 "Dans cette salle de concert (vraie photo 360°, Konzerthaus de Vienne), regarde sur la scène de vrais musiciens jouer Tchaïkovski : un orchestre symphonique dans la grande salle du conservatoire de Moscou, une harpiste, un jeune pianiste…",
 [
  info("La Danse de la Fée Dragée", "Orchestre symphonique, grande salle du conservatoire de Moscou. Repère le célesta et les violons qui jouent en pizzicato.", -35, -30, t0=s0[0], t1=s0[1]),
  info("Le Trépak", "Même orchestre : la danse russe, rapide et pleine d'énergie. Regarde le chef d'orchestre !", -35, -30, t0=s0[1], t1=s0[2]),
  info("La Valse des fleurs", "Interprétée par l'orchestre de l'US Army Band : regarde la harpe, puis les vents.", -35, -30, t0=s0[2], t1=s0[3]),
  info("Concerto pour piano n° 1", "Un jeune pianiste joue avec un orchestre, au théâtre Llave d'Orizaba (Mexique).", -35, -30, t0=s0[3]),
  quiz("L'orchestre", "Qui dirige l'orchestre ?", ["Le premier violon", "Le chef d'orchestre", "Le pianiste", "Le public"], 1, "Le chef d'orchestre donne le tempo et les nuances avec sa baguette.", 60, -22),
  quiz("Les familles", "La harpe appartient à la famille des…", ["Cuivres", "Cordes (pincées)", "Bois", "Percussions"], 1, "La harpe est un instrument à cordes pincées.", -130, -22),
  info("Crédits vidéo", "Orchestre (Moscou) : Wikimedia Commons, CC BY 3.0. US Army Band : domaine public. Pianiste : Commons, CC BY-SA 4.0. Salle : Konzerthaus Wien, Commons, CC BY-SA 4.0.", 145, -40),
 ]))

# 8 ------------------------------------------------------------------ la dernière symphonie
S.append(scene("La dernière symphonie", pano(f"{D}/gal/gfin.jpg"),
 "Dernière salle. À la fin de sa vie, Tchaïkovski est célèbre dans le monde entier. Il s'installe à Klin, près de Moscou, dans une maison calme où il compose ses dernières œuvres.",
 [
  i("La maison de Klin", "Tchaïkovski s'installe ici en 1892. La maison est devenue un musée en 1894, juste après sa mort : rien n'y a été changé.", *at(G4, "t_klin"), "t_klin"),
  i("Le salon et le piano", "Voici son salon, avec son piano à queue. Chaque année, le vainqueur du concours Tchaïkovski a l'honneur d'y jouer.", *at(G4, "t_salon"), "t_salon"),
  i("New York, 1891", "Tchaïkovski fait une tournée aux États-Unis et dirige le concert d'inauguration du Carnegie Hall, la plus célèbre salle de concert de New York.", *at(G4, "t_carnegie"), "t_carnegie"),
  i("Le concerto pour piano n° 1", "Voici le début de la partition : la main droite et la main gauche jouent de grands accords qui montent sur tout le clavier.", *at(G4, "t_concerto_score"), "t_concerto_score"),
  i("Écoute : la Symphonie Pathétique", "Sa 6e symphonie, la « Pathétique », se termine par un mouvement très lent et très triste (adagio lamentoso). Tchaïkovski la considère comme sa meilleure œuvre. Il meurt neuf jours après l'avoir dirigée, le 6 novembre 1893.", *at(G4, "t_reutlinger"), "t_reutlinger", "a_pathetique"),
  i("Sa tombe", "Tchaïkovski est enterré au cimetière Tikhvine de Saint-Pétersbourg, près d'autres grands compositeurs russes.", *at(G4, "t_grave"), "t_grave"),
  i("Un musicien toujours aimé", "Ses mélodies sont partout : au concert, au cinéma, dans les dessins animés et les publicités. Casse-Noisette est l'un des ballets les plus joués au monde.", *at(G4, "t_monument"), "t_monument"),
  quiz("Le romantisme", "Quelle est la principale caractéristique de la musique romantique ?", ["Elle est toujours rapide", "Elle exprime des émotions fortes", "Elle n'utilise que le piano", "Elle n'a pas de mélodie"], 1, "Les romantiques expriment leurs sentiments, avec de grands orchestres et de belles mélodies.", -60, -25),
  order("Les ballets de Tchaïkovski", "Range ses trois ballets dans l'ordre de création.", ["Le Lac des cygnes (1877)", "La Belle au bois dormant (1890)", "Casse-Noisette (1892)"], "Bravo !", 60, -25),
  match("Les œuvres", "Associe chaque œuvre à ce qu'on y entend.", [["Casse-Noisette", "Le célesta de la Fée Dragée"], ["Le Lac des cygnes", "Le thème au hautbois"], ["Ouverture 1812", "Des coups de canon"], ["Symphonie Pathétique", "Une fin lente et triste"]], "Bravo, tu connais bien Tchaïkovski !", 150, -25),
  i("Crédits", "Photos 360° : Wikimedia Commons (CC BY, CC BY-SA). Ciel : Poly Haven (CC0). Photos et documents anciens : domaine public. Photos récentes : Commons (CC BY-SA, GFDL). Enregistrements : domaine public (Musopen, US Army Band, archives 78 tours) et CC BY / CC BY-SA. Salles de musée et frise : créées pour ce cours.", 0, -45),
 ]))

# 9 ------------------------------------------------------------------ vidéo vie
S.append(scene("La vie de Tchaïkovski (vidéo 360°)",
 {"type": "video", "name": "tchai_vie_360.mp4", "ext": "mp4", "layout": "mono", "loop": False, "mute": False, "duration": 110, "thumb": thumb(f"{TP}/kazan.jpg")},
 "Regarde et écoute la vie de Tchaïkovski, de Saint-Pétersbourg à Moscou et New York, sur la valse du Lac des cygnes.",
 [
  info("Saint-Pétersbourg", "1850 : à 10 ans, il part étudier à Saint-Pétersbourg.", 0, -35, t0=0, t1=21.5),
  info("Le conservatoire", "1862 : il entre au conservatoire de Saint-Pétersbourg.", 0, -35, t0=21.5, t1=43),
  info("Moscou", "1866 : professeur au conservatoire de Moscou.", 0, -35, t0=43, t1=64.5),
  info("New York", "1891 : concert d'ouverture du Carnegie Hall.", 0, -35, t0=64.5, t1=86),
  info("1893", "La Symphonie Pathétique, puis sa mort à Saint-Pétersbourg.", 0, -35, t0=86),
  order("La vie de Tchaïkovski", "Remets dans l'ordre.", ["Naissance à Votkinsk", "Conservatoire de Saint-Pétersbourg", "Professeur à Moscou", "Concert à New York"], "1840, 1862, 1866, 1891.", 120, -20),
 ]))

course = {"id": uid(), "title": "Tchaïkovski, le romantisme russe et le ballet", "matiere": "Éducation musicale", "niveau": "4e", "voix": "fr-FR",
 "objectif": "Découvrir Tchaïkovski et le romantisme russe ; comprendre ce qu'est un ballet ; reconnaître des timbres (hautbois, célesta, harpe) et des danses (valse, trépak) dans Le Lac des cygnes et Casse-Noisette.",
 "updated": 0, "scenes": S}
if errors: print("\n".join(errors)); sys.exit(1)
json.dump(course, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False)
print("scènes", len(S), "points", sum(len(s["hotspots"]) for s in S))
