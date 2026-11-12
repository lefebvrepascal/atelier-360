# Fabrication d'un cours Atelier 360 à partir d'une demande d'enseignant

Ce dossier rassemble la chaîne qui transforme une demande, faite sur la page « Demander un cours 360° », en cours publié dans l'application, rangé avec sa matière et sa classe.
Les cours déjà publiés (Histoire, Éducation musicale, Physique-chimie, Anglais, SVT…) ont tous été faits ainsi ; `exemples/` contient leurs scripts.

## 1. Lire la demande

Les demandes sont dans la base de la page « Demander un cours 360° » (artefact claude.ai), collection `demandes`.
Chaque document contient : `matiere`, `niveau` (6e à 3e), `langue` (fr-FR, en-GB, es-ES, de-DE, it-IT), `duree` (courte ≈ 30 min et 4-5 scènes ; moyenne ≈ 1 h et 7-8 scènes ; longue ≈ 1 h 40 et 10-11 scènes), `prompt`, `objectifs`, `options`, `vigilance`, `echeance`, `statut`, `lien`, `note`.

- Traiter les demandes `statut = "attente"`, la plus ancienne d'abord.
- Passer la demande à `"fabrication"` au début, à `"publie"` avec `lien` à la fin.
- Si la demande est trop vague ou impossible (pas d'image libre, sujet inadapté à l'âge), mettre `"preciser"` et écrire dans `note` ce qu'il faut préciser, en une ou deux phrases.

## 2. Cahier des charges d'un cours

**Contenu**
- Programme officiel du niveau demandé ; faits vérifiés (dates, chiffres, noms) ; vocabulaire adapté à l'âge.
- Chaque scène : un texte d'accueil (≤ 400 caractères), 5 à 12 points d'intérêt.
- Points d'information (titre + texte ≤ 400 caractères + image si possible), lus par la voix.
- Activités dans presque chaque scène : QCM, vrai/faux, remettre dans l'ordre, associer par paires, défi « trouve-le » (cible précise dans la photo 360°). Question ≤ 240, réponse ≤ 90, explication ≤ 300 caractères.
- Dernière scène : bilan avec activités de synthèse et un point « Crédits » (sources et licences).
- Contenus sensibles : jamais d'images de cadavres ou de violence explicite ; préférer lieux de mémoire, schémas, témoignages. Respecter le champ `vigilance`.
- Option `simplifie` : remplir aussi `introS`, `textS`, `questionS`, `explanationS` (phrases courtes, mots simples).

**Images et médias (licences libres uniquement)**
- Photos 360° réelles : Wikimedia Commons (rechercher « equirectangular », « 360 panorama », « Kugelpanorama »), Poly Haven (CC0). Panoramas partiels : `pwall.py` (écran panoramique honnête) ou `panos_mz.fill` (complète sol et ciel).
- Œuvres, documents, photos d'archives : Commons (domaine public, CC0, CC BY, CC BY-SA), vérifier `LicenseShortName` et noter l'auteur dans `credits.json`.
- Salles de musée : `gallery2.py` (œuvres accrochées avec cartels, titre sur le mur du fond).
- Vidéos : Commons (archives), Pexels (licence Pexels). Projetées sur un écran dans un 360° avec `screen360.py` (en deux étapes pour éviter le manque de mémoire). Vidéo 360° commentée : `mkvideo.py` (voix Piper + musique originale de `music.py`).
- Sons : extraits du domaine public ou CC (discours, enregistrements anciens), mono, mp3.
- Molécules 3D (point de type `mol`) : `molgen.py` (RDKit) ; réactions avec conservation des atomes.
- Voyage dans les échelles (scène `zoom`, mode `quilt`) : `exemples/gen_quilt.py` (images carrées emboîtées, position de l'image suivante `cx`, `cy`).
- Le réseau de la machine de fabrication est souvent filtré : télécharger les médias avec le workflow GitHub `exemples/medias.yml` (branche `medias-revolution-360`, résultat sur une branche orpheline `…-outN`), avec des reprises en cas d'erreur.

**Mise en forme du fichier de cours** : voir `helpers.py` (`pano`, `info`, `quiz`, `vf`, `order`, `match`, `find`, `scene`) et les exemples. Angle `az` : 0 = centre de la photo, positif à droite ; `el` positif vers le haut. Vérifier les chevauchements avec `overlap.py cours.json 9`.

## 3. Exporter, publier, vérifier

1. `python3 export_cours.py cours.json export.zip 3:video.mp4` (l'éditeur du dépôt fait l'export ; les numéros sont les scènes vidéo).
2. `python3 publier.py <site> export.zip <médias> <url des médias>` : copie le cours, sort les vidéos, ajoute la carte et regroupe la page d'accueil par matière.
3. `python3 voix360_multi.py <site> <slug>` : voix Piper (fr : siwis, en : lessac), seules les phrases nouvelles sont synthétisées.
4. Mettre en ligne le site, et le dossier des médias s'il a changé (en-têtes CORS `Access-Control-Allow-Origin: *` sur les vidéos).
5. Vérifier en ligne : la carte apparaît dans la bonne matière, la page du cours se charge, les vidéos répondent.
6. Mettre la demande à `"publie"` avec le lien du cours.

## Hébergement

Le site entier fait près de 1 Go. Chaque mise en ligne par Netlify renvoie tout le site et consomme des crédits : en novembre 2026 le compte a atteint sa limite (« account credit usage exceeded »).
Avant de mettre la file d'attente en service, choisir : offre Netlify supérieure (vidéos sur le site séparé `atelier360-medias`), ou GitHub Pages (envois partiels gratuits, vidéos dans un second dépôt, 1 Go par site).
