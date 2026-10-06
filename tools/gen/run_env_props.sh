#!/bin/zsh
# Environment + props (txt2img). Background prompt asks for a LIGHTER band at
# fighter height (CHARACTER-SHEET palette check / predicted failure F4).
cd "$(dirname $0)/../.."
PY=../_genai/.venv/bin/python
$PY tools/gen/gen_image.py --id ENV-BOWL --width 768 --height 432 --seeds 1-8 --prompt "2d cartoon game background, side view inside an empty glass goldfish bowl at night, pale aquarium gravel floor, small pink plastic castle, green plastic seaweed, soft blue moonlight glowing through the curved glass, bright hazy middle, flat colors, no characters" 2>&1 | grep -E "Error"
$PY tools/gen/gen_image.py --id PROP-KEY --seeds 1-4 --prompt "2d cartoon game sprite, a shiny brass wind-up toy key with two round loops, side view, bold black outline, flat colors, centered, plain light grey background" 2>&1 | grep -E "Error"
$PY tools/gen/gen_image.py --id WPN-CUTLASS --seeds 1-4 --prompt "2d cartoon game sprite, a small tin toy pirate cutlass sword lying horizontal, blade pointing right, bold black outline, flat colors, plain light grey background" 2>&1 | grep -E "Error"
$PY tools/gen/gen_image.py --id WPN-POPGUN --seeds 1-4 --prompt "2d cartoon game sprite, a tin toy cork pop gun, side view, barrel pointing right, red and silver, bold black outline, flat colors, plain light grey background" 2>&1 | grep -E "Error"
$PY tools/gen/gen_image.py --id PROP-CORK --seeds 1-4 --prompt "2d cartoon game sprite, a single small bottle cork, side view, bold black outline, flat colors, centered, plain light grey background" 2>&1 | grep -E "Error"
for id in ENV-BOWL PROP-KEY WPN-CUTLASS WPN-POPGUN PROP-CORK; do $PY tools/gen/contact.py raw/sheets/$id.png raw/$id/*.png --thumb 220; done
echo ENV PROPS DONE
