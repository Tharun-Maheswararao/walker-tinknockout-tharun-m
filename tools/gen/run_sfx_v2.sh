#!/bin/zsh
# SFX pass v2: v1 clips filled the whole 1 s with seed-shaped envelopes. Generate
# 2 s clips with new seeds; the hit is then trimmed out (tools/edit/trim_sfx.py).
cd "$(dirname $0)/../.."
PY=../_genai/.venv/bin/python
g() { $PY tools/gen/gen_audio.py sfx --id $1 --tag v2 --seconds $2 --steps 50 --seeds $3 --prompt "$4" 2>&1 | grep -E "^wrote|Error"; }
g SFX-EMPTY   2.5 1-4 "a clockwork spring unwinding and slowing down, whirring then a soft metal clunk"
g SFX-JAB     2.0 4-7 "one loud hollow metal clang, a small tin toy hit once, short impact"
g SFX-REWIND  2.0 4-7 "a wind-up toy key being turned, mechanical ratchet clicking"
g SFX-POP     2.0 4-7 "a single loud cork pop from a toy pop gun"
g SFX-CUTLASS 2.0 4-7 "a sword slash whoosh followed by a metallic clang on tin"
echo SFX V2 DONE
