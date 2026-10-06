#!/bin/zsh
# Derive every Bolt pose from its Claude-drawn sketch (raw/inits/<pose>.png)
# with the same base prompt + seeds that produced the accepted reference
# (CHAR-REF v6 s40). Pose wording is placed FIRST so it survives CLIP's 77-token cut.
cd "$(dirname $0)/../.."
PY=../_genai/.venv/bin/python
BASE="2d cartoon game sprite of a tin wind-up toy deep sea diver, polished brass helmet, glass face window, red enamel tin suit with rivets, steel boots, mitten gloves, bold black outline, cel shaded, plain light grey background"
typeset -A W
W=(idle "boxing stance, fists up" walk "walking forward mid stride" jab "throwing a straight punch forward"
   cutlass "swinging arm forward and down" pop "arm stretched straight forward aiming" block "both arms raised guarding his face"
   rewind "hunched over reaching behind his back" hurt "knocked backwards recoiling from a hit" empty "slumped forward, arms hanging limp, exhausted"
   ko "lying flat on his back knocked out" win "one fist raised high in victory")
for p in idle walk jab cutlass pop block rewind hurt empty ko win; do
  ID="CHAR-${p:u}"
  $PY tools/gen/gen_image.py --id $ID --init raw/inits/$p.png --strength 0.75 --steps 4 --seeds 40-45 --prompt "${W[$p]}, $BASE" 2>&1 | grep -E "wrote|Error"
  $PY tools/gen/contact.py raw/sheets/$ID.png raw/inits/$p.png raw/$ID/*.png --thumb 200
done
echo POSES DONE
