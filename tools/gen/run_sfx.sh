#!/bin/zsh
# Generate candidates for the six event sounds in CHANGE-BRIEF section 2.
cd "$(dirname $0)/../.."
PY=../_genai/.venv/bin/python
g() { $PY tools/gen/gen_audio.py sfx --id $1 --seconds $2 --steps 40 --seeds 1-3 --prompt "$3" 2>&1 | grep -E "^wrote|Error"; }
g SFX-JAB     1.0 "a single hollow metallic clang of a small tin toy being punched"
g SFX-REWIND  1.0 "a single sharp mechanical ratchet click of a wind-up toy key"
g SFX-POP     1.0 "a cork popping out of a toy pop gun"
g SFX-CUTLASS 1.5 "a small metal sword striking a tin can, metallic shing and clank"
g SFX-BELL    2.5 "a small brass bell rung once, ding, boxing ring bell"
g SFX-EMPTY   2.5 "a clockwork spring unwinding and slowing down, whirring then a soft metal clunk"
echo SFX DONE
