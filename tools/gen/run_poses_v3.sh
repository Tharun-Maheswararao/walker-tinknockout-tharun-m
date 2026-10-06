#!/bin/zsh
# Pose pass v3: same as v2 but strength 0.75/0.85 with 4 steps (3 effective) - richer paint like CHAR-REF.
# Changes: init sketches now copy the accepted CHAR-REF's features (raw/inits-ref,
# make_inits.py --ref); prompt names those features; 8 steps so a lower strength
# still repaints the flat sketch (turbo img2img runs int(steps*strength) steps).
cd "$(dirname $0)/../.."
PY=../_genai/.venv/bin/python
BASE="2d cartoon game sprite of a tin wind-up toy deep sea diver, polished brass helmet with two antennae, red enamel tin suit with rivets, yellow mitten gloves, steel boots, bold black outline, cel shaded, plain light grey background"
typeset -A W
W=(idle "boxing stance, fists up" walk "walking forward mid stride" jab "throwing a straight punch forward"
   cutlass "swinging arm forward and down" pop "arm stretched straight forward aiming" block "both arms raised guarding his face"
   rewind "hunched over reaching behind his back" hurt "knocked backwards recoiling from a hit" empty "slumped forward, arms hanging limp, exhausted"
   ko "lying flat on his back knocked out" win "one fist raised high in victory")
for p in ${@:-idle walk jab cutlass pop block rewind hurt empty ko win}; do
  ID="CHAR-${p:u}"
  for st in 0.75 0.85; do
    $PY tools/gen/gen_image.py --id $ID --tag v3-st$st --init raw/inits-ref/$p.png --strength $st --steps 4 --seeds 40-43 --prompt "${W[$p]}, $BASE" 2>&1 | grep -E "Error"
  done
  $PY tools/gen/contact.py raw/sheets/$ID-v3.png raw/inits-ref/$p.png raw/$ID/${ID}_v3*.png --thumb 180
done
echo POSES V3 DONE
