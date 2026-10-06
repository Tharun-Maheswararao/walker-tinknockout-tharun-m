#!/bin/zsh
# MUS-WALTZ: generate longer than needed (30 s) and cut a loop at a bar boundary later.
cd "$(dirname $0)/../.."
../_genai/.venv/bin/python tools/gen/gen_audio.py music --id MUS-WALTZ --seconds 30 --seeds 1-3 --prompt "a gentle music box and carnival organ waltz in 3/4 time, playful and slightly eerie toy shop at night, steady tempo, instrumental" 2>&1 | grep -E "^wrote|Error"
echo MUSIC DONE
