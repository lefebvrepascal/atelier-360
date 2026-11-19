set -x
mkdir -p medias
S=https://atelier360-sacre-coeur.netlify.app; C=le-muscle-a-l-effort-energie-et-circulation-sangui
{ echo "accueil: $(curl -s -o /tmp/a.html -w '%{http_code}' $S/)"; grep -c "cours/$C/" /tmp/a.html; grep -o "<h2[^>]*>[^<]*</h2>" /tmp/a.html;
  echo "cours: $(curl -s -o /tmp/c.html -w '%{http_code} %{size_download}' $S/cours/$C/)";
  echo "voix: $(curl -s -o /dev/null -w '%{http_code}' $S/cours/$C/audio/voix.js)";
  curl -sI -H "Origin: $S" https://atelier360-medias.netlify.app/$C/sang-360-dd7w.mp4 | grep -i -E "^HTTP|content-length|access-control-allow-origin";
  echo "ancien cours: $(curl -s -o /dev/null -w '%{http_code}' $S/cours/le-muscle-et-l-effort/)"; } > medias/verif.txt 2>&1
cat medias/verif.txt
