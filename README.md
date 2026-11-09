# Atelier 360

Atelier 360 sert à créer des **cours immersifs en 360°** pour les casques **Meta Quest 3S**. Il fonctionne aussi sur tout casque ou navigateur compatible WebXR.

L'enseignant compose ses scènes dans le navigateur, place des points d'intérêt et des activités, puis exporte un site que les élèves ouvrent dans le navigateur du casque, sans application à installer.

Projet réalisé au **Collège du Sacré-Cœur d'Halluin** (Nord).

## Ce que permet l'Atelier

- **Scènes 360°** : 7 décors intégrés (studio, espace, océan, montagne, désert, forêt, banquise), vos photos 360° ou vos vidéos 360° (mono ou stéréo).
- **Points d'information** avec texte, image et audio.
- **Activités notées** :
  - QCM et vrai/faux ;
  - remettre des éléments dans l'ordre ;
  - associer par paires ;
  - « Trouve-le dans la scène » : l'élève vise le bon endroit et a 3 essais.
- **Points synchronisés avec la vidéo** : chaque point peut apparaître et disparaître à un moment précis.
- **Lecture audio** des textes et des quiz par la voix de synthèse de l'appareil, ou par vos propres enregistrements.
- **Confort et inclusion** : texte simplifié, grand texte, contraste renforcé, voix lente. Ces réglages sont mémorisés sur chaque casque.
- **Export d'un site complet** : un portail qui liste les cours, avec un QR code par cours. L'export d'un cours seul est aussi possible.
- **Suivi des résultats** : chaque élève saisit son prénom ou un numéro, et ses résultats sont envoyés à Netlify Forms. Sans connexion, ils restent sur le casque jusqu'à la connexion suivante.
- **Fiche enseignant au format Word** : déroulé, corrigé complet, durée estimée.

## Utilisation

1. Ouvrez `index.html` dans un navigateur récent (Chrome, Edge, Firefox).
   - Version en ligne : https://atelier360-editeur.netlify.app (mise à jour automatiquement à chaque modification du dépôt)
2. Créez ou modifiez un cours. Vos cours sont enregistrés **dans votre navigateur**. Pensez à utiliser régulièrement « Fichier › Enregistrer le cours (.json) » pour en garder une copie.
3. Cliquez sur **Exporter pour le casque › Site complet**, puis décompressez le fichier .zip.
4. Mettez le dossier en ligne sur un hébergement **https**, obligatoire pour le mode réalité virtuelle. Par exemple : glissez le dossier dans l'onglet *Deploys* d'un projet [Netlify](https://app.netlify.com/drop).
5. Dans le casque, ouvrez l'adresse du site dans **Meta Quest Browser**, choisissez le cours, puis touchez **Entrer en réalité virtuelle**.

Pour recevoir les résultats des élèves, activez la détection des formulaires dans le projet Netlify (*Forms › Enable form detection*). Les résultats apparaissent dans *Forms › resultats*, et un export CSV est possible.

## Voix dans le casque Meta Quest

Le navigateur du Meta Quest ne dispose pas de voix de synthèse : un texte lu « par l'appareil » y reste muet. Le lecteur utilise donc en priorité des **fichiers audio pré-enregistrés** (`cours/<nom>/audio/*.mp3` et `audio/voix.js`), avec une voix neuronale française [Piper](https://github.com/rhasspy/piper) (voix *siwis*, licence CC BY 4.0).

Pour les fabriquer après un export du site complet :

```bash
pip install piper-tts playwright && playwright install chromium
# voix : https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-fr_FR-siwis-medium.tar.bz2
python3 outils/voix360.py <dossier-du-site> fr_FR-siwis-medium.onnx fr_FR-siwis-medium.onnx.json
```

Le script ouvre chaque cours, récupère toutes les phrases que le lecteur peut prononcer (textes, consignes, réponses, bilans) et crée un fichier par phrase. Sur ordinateur, sans ces fichiers, la voix du système prend le relais. Les enregistrements faits par l'enseignant sont toujours prioritaires.

## Fonctions réservées à la version Claude

L'Atelier a été conçu avec l'assistant Claude d'Anthropic. Ouvert directement depuis GitHub, il fonctionne entièrement, **sauf** les fonctions qui font appel à Claude ou à son espace de partage :

- la génération d'un cours à partir d'un sujet ou de documents (PDF, images, vidéos) ;
- la version simplifiée (FALC) produite automatiquement ;
- les conseils de mise en œuvre dans la fiche enseignant ;
- la bibliothèque de cours partagée entre collègues.

Ces boutons sont masqués lorsqu'ils ne sont pas disponibles. Les versions simplifiées peuvent toujours être écrites à la main : case « Afficher les champs simplifiés ».

## Contenu du dépôt

| Fichier | Rôle |
|---|---|
| `index.html` | L'Atelier : éditeur, lecteur 360° et export, dans un seul fichier |
| `outils/voix360.py` | Fabrique les fichiers audio des cours pour le casque |
| `netlify.toml` | Configuration de la mise en ligne automatique sur Netlify |
| `aframe.min.js` | Moteur WebXR [A-Frame 1.6.0](https://aframe.io) (licence MIT), intégré aux exports pour qu'ils fonctionnent même sur un réseau filtré |

Bibliothèques chargées depuis un CDN :

- A-Frame : réalité virtuelle ;
- JSZip : fichiers .zip et .docx ;
- pdf.js : lecture des PDF ;
- qrcode-generator : QR codes, intégré dans la page.

## Licence

Code publié sous licence MIT (voir `LICENSE`) : libre d'utilisation, de modification et de redistribution, y compris dans d'autres établissements.
