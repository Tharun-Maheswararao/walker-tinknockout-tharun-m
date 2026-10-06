"""Build ASSET-LOG.md from tools/gen/gen-log.jsonl (every generation, machine-logged)
plus the hand-written judgement below (outcome + reason per batch / accepted file).
Also writes small rejected-output contact sheets to design/rejected/.
  python tools/gen/build_asset_log.py
"""
import json
from collections import OrderedDict
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[2]
rows = [json.loads(l) for l in (REPO / "tools/gen/gen-log.jsonl").read_text().splitlines()]

# (asset, tag) -> (outcome, reason).  Outcome: rejected | accepted | edited | partial
JUDGE = {
    ("CHAR-REF", ""): ("rejected", "Photoreal toy photos, not the flat illustrated sprite of CONCEPT art direction; no eyes (rule 2); fingered hands (rule 6). Prompt was over CLIP's 77-token limit, so 'plain light grey background' was silently dropped. s1 = black (fp16 NaN on MPS)."),
    ("CHAR-REF", "v2"): ("rejected", "Style now right (cartoon sprite), but helmets red not brass (palette), no eyes in the window, mostly three-quarter not profile."),
    ("CHAR-REF", "v3"): ("rejected", "The word 'porthole' framed the WHOLE picture inside a porthole (concept bleed). s4 was first with eyes through the glass."),
    ("CHAR-REF", "v4"): ("rejected", "'face window' fixed the framing but the gold leaked onto the whole suit (attribute binding); still no eyes."),
    ("CHAR-REF", "v5-i2i-st0.5"): ("rejected", "Switched to img2img from the code sketch. Output copies the crude sketch (flat, arms lost). Strengths 0.5/0.6/0.7 gave identical images: turbo img2img runs int(steps x strength) = 2 steps for all three (setting mistake)."),
    ("CHAR-REF", "v5-i2i-st0.6"): ("rejected", "Same as st0.5 (same effective step count)."),
    ("CHAR-REF", "v5-i2i-st0.7"): ("rejected", "Same as st0.5 (same effective step count)."),
    ("CHAR-REF", "v6-i2i-st0.75"): ("accepted s40 / rejected rest", "s40 ACCEPTED as the reference (human decision, option 1 of 4 finalists): brass helmet ~40 % of height, one face window, red riveted suit, mitten gloves, steel boots, profile facing right. Fails rule 2 (empty glass) -> EDIT: eyes painted. Back 'key' reads as a black nozzle -> key made a separate prop (PROP-KEY). s41-43 drift (other helmets / goggles)."),
    ("CHAR-REF", "v6-i2i-st0.85"): ("rejected", "Near-identical to st0.75 (3 effective steps either way)."),
    ("CHAR-REF", "v6-i2i-st0.92"): ("rejected", "Near-identical to st0.75."),
    ("CHAR-REF", "v7-eyes"): ("rejected (finalists s44, s48, s50)", "Eyes prompt: s44 classic helmet but fingers, no key, several windows; s48 two goggles (breaks one-porthole rule); s50 two windows, key held as a staff. Kept as finalists, not chosen."),
    ("CHAR-IDLE", ""): ("rejected", "Pose pass v1 (plain sketch inits): each seed a different diver - predicted failure F1 confirmed. Batch stopped after 3-5 poses."),
    ("CHAR-WALK", ""): ("rejected", "Pose pass v1: F1 drift."),
    ("CHAR-JAB", ""): ("rejected", "Pose pass v1: F1 drift; jab pose ignored (fist raised, not extended)."),
    ("CHAR-CUTLASS", ""): ("rejected", "Pose pass v1: F1 drift."),
    ("CHAR-POP", ""): ("rejected", "Pose pass v1: F1 drift."),
    ("CHAR-BLOCK", ""): ("rejected", "Pose pass v1: stopped (F1 already shown)."),
    ("CHAR-IDLE", "v3-st0.75"): ("rejected", "Pose pass v3 test (more noise): richer paint like CHAR-REF but identity drift returns (yellow body, cyclops eye). Chose consistency (v2) over detail."),
    ("CHAR-IDLE", "v3-st0.85"): ("rejected", "As v3-st0.75."),
    ("CHAR-JAB", "v3-st0.75"): ("rejected", "As CHAR-IDLE v3."),
    ("CHAR-JAB", "v3-st0.85"): ("rejected", "As CHAR-IDLE v3."),
    ("ENV-BOWL", ""): ("rejected", "'goldfish bowl' pulled in fish and water in all 8; 'night' ignored (daytime teal). s1 black (NaN)."),
    ("ENV-BOWL", "v2"): ("accepted s4 / rejected rest", "Avoided the word 'goldfish'. s4 ACCEPTED: night toy shop, glass bowl with castle and plants, sand floor at 80 % height used as the arena floor. Still seen from outside the bowl (concept said inside) - accepted as framing; listed as a limitation. Others: no bowl / no floor / pink overload."),
    ("PROP-KEY", ""): ("accepted s3", "s3: two-loop wind-up key. s2 a door key, s4 a keyring; s1 black."),
    ("WPN-CUTLASS", ""): ("accepted s3", "s2 has a pirate's face drawn on it (an extra character), s4 is a dagger; s1 black."),
    ("WPN-POPGUN", ""): ("accepted s4", "s2 and s3 look like real revolvers - breaks the 'toy weapons, not realistic' decision; s4 bright red/yellow toy. s1 black."),
    ("PROP-CORK", ""): ("edited s4", "Model drew a bottle every time; the cork was CROPPED out of s4's bottle neck."),
    ("SFX-JAB", ""): ("rejected", "Seed-shaped envelopes fill the whole 1 s; multiple hits."),
    ("SFX-JAB", "v2"): ("accepted v2_s5", "Claude's signal-analysis pick (user asked Claude to choose; Claude cannot hear): sharpest single hit, tonal, ~95 ms ring. evidence/sfx-scores-v2.txt."),
    ("SFX-CUTLASS", ""): ("accepted s2", "Scorer ranked v2_s5 first but its 13 ms decay is a tick, not a 'shing'; s2 rings 205 ms, bright (overrode the scorer)."),
    ("SFX-CUTLASS", "v2"): ("rejected", "Long multi-hit clips; v2_s5 too short (see SFX-CUTLASS s2)."),
    ("SFX-POP", ""): ("accepted s1", "3 ms attack (fastest), short body."),
    ("SFX-POP", "v2"): ("rejected", "Slower attacks / multiple hits."),
    ("SFX-REWIND", ""): ("rejected", "Longer than one click after trimming."),
    ("SFX-REWIND", "v2"): ("accepted v2_s5", "46 ms single click after trim, brightest."),
    ("SFX-EMPTY", "v2"): ("edited v2_s2", "No candidate fell in pitch (pitch_drop ~1.0). v2_s2 = most tonal whirr; EDIT: speed glide 1.0 -> 0.55 (tools/edit/pitch_fall.py), pitch_drop now 1.18."),
    ("SFX-BELL", ""): ("rejected", "No candidate rings: best (s1) is a 16 ms tick."),
    ("SFX-BELL", "v2"): ("accepted v2_s13", "New prompt. v2_s13: 12 ms attack, 1.47 s tonal ring. Scorer penalised its 'hits' (the ring's shimmer) - overrode."),
    ("MUS-WALTZ", ""): ("accepted s2 (loop cut)", "s2 gives the cleanest 8-bar loop: seam jump 0.0095, level match; s1 seam jump 0.059, s3 spectral score 0.057. Loop cut by tools/edit/cut_loop.py; human listening of 3 repetitions in TEST-REPORT."),
    ("SMOKE", ""): ("test", "Smoke test of AudioLDM2 after the transformers-5 compatibility patch; deleted."),
}
for p in ["WALK", "JAB", "CUTLASS", "POP", "BLOCK", "REWIND", "HURT", "EMPTY", "KO", "IDLE"]:
    JUDGE.setdefault((f"CHAR-{p}", "v2-st0.6"), ("accepted s43", "Pose pass v2 (inits copy the accepted reference; 8 steps): one seed (s43) for every pose = most uniform character. EDITS: rembg, eyes painted, scaled/anchored to the hurtbox."))
    JUDGE.setdefault((f"CHAR-{p}", "v2-st0.7"), ("rejected", "More detail but more drift between poses than st0.6."))
JUDGE[("CHAR-WIN", "v2-st0.6")] = ("accepted s42", "s43 missing the raised fist (fails its own spec); s42 is the only one with the arm up - seed deviation noted. Same edits as other poses.")
JUDGE[("CHAR-WIN", "v2-st0.7")] = ("rejected", "No raised fist / drift.")

USED = {
    "CHAR-REF": "design reference only (raw/edits/CHAR-REF-eyes.png)",
    "ENV-BOWL": "godot/assets/env/bowl.png", "PROP-KEY": "godot/assets/props/key-bolt.png, key-rivet.png (recolour)",
    "WPN-CUTLASS": "godot/assets/props/cutlass.png", "WPN-POPGUN": "godot/assets/props/popgun.png", "PROP-CORK": "godot/assets/props/cork.png",
    "SFX-JAB": "godot/assets/sfx/jab.ogg (also cork impact, pitch 1.25)", "SFX-CUTLASS": "godot/assets/sfx/cutlass.ogg", "SFX-POP": "godot/assets/sfx/pop.ogg",
    "SFX-REWIND": "godot/assets/sfx/rewind.ogg", "SFX-EMPTY": "godot/assets/sfx/empty.ogg", "SFX-BELL": "godot/assets/sfx/bell.ogg",
    "MUS-WALTZ": "godot/assets/music/waltz.ogg",
}
for p in ["idle", "walk", "jab", "cutlass", "pop", "block", "rewind", "hurt", "empty", "ko", "win"]:
    USED[f"CHAR-{p.upper()}"] = f"godot/assets/fighters/bolt/{p}.png + rivet/{p}.png (recolour)"

groups: "OrderedDict[tuple, list]" = OrderedDict()
for r in rows:
    groups.setdefault((r["asset_id"], r.get("tag", "")), []).append(r)

out = ["# ASSET-LOG — every generation, Tin Knockout",
       "",
       "Built by `tools/gen/build_asset_log.py` from `tools/gen/gen-log.jsonl`. The JSONL is written by the generator scripts at generation time (exact prompt, seed, steps, size, strength, init image, model revision); the outcome/reason column is the human + Claude judgement recorded afterwards. To reproduce any row, run the generator with the same arguments (see SOURCES.md). Rejected outputs are kept as contact sheets in `design/rejected/` (full-size raws are not committed).",
       "",
       f"**{len(rows)} generations** in {len(groups)} batches.",
       "",
       "| Asset ID | Batch | Model (mode) | Prompt | Seeds | Settings | Outcome | Reason (judged against sheet / storyboard / pillars) | Where used |",
       "|---|---|---|---|---|---|---|---|---|"]
for (aid, tag), rs in groups.items():
    r0 = rs[0]
    seeds = ", ".join(str(r["seed"]) for r in rs)
    if r0["mode"] in ("txt2img", "img2img"):
        sz = r0["size"] if isinstance(r0["size"], list) else [r0["size"], r0["size"]]
        st = f"{sz[0]}x{sz[1]}, steps {r0['steps']}, cfg 0"
        if r0["mode"] == "img2img":
            st += f", strength {r0['strength']}, init `{r0['init']}`"
    elif r0["mode"] == "sfx":
        st = f"{r0['seconds']} s, steps {r0['steps']}, cfg {r0['guidance_scale']}, neg \"{r0['negative_prompt']}\""
    else:
        st = f"{r0['seconds']} s, {r0['max_new_tokens']} tokens, cfg {r0['guidance_scale']}, sampling"
    model = f"{r0['model'].split('/')[-1]} ({r0['mode']})"
    oc, why = JUDGE.get((aid, tag), ("?", ""))
    prompt = r0["prompt"].replace("|", "/")
    out.append(f"| {aid} | {tag or 'v1'} | {model} | {prompt} | {seeds} | {st} | **{oc}** | {why} | {USED.get(aid, '') if 'accepted' in oc or 'edited' in oc else ''} |")

out += ["", "## Edits applied to accepted outputs", "",
        "| Asset | Edit | Tool |", "|---|---|---|",
        "| CHAR-REF | two dot eyes painted on the empty glass (rule 2) | `tools/edit/paint_eyes.py` |",
        "| CHAR-* (11 poses) | background removed (rembg u2net); eyes painted at the glass position computed from the init sketch (half-closed for EMPTY, X for KO); scaled so standing height = 336 px (3x 112) with feet at (240,435) of a 480x450 canvas | `tools/edit/process_sprites.py` |",
        "| RIVET-* | palette recolour of every accepted Bolt pose: red -> verdigris (hue 0.45), brass -> copper (hue 0.065) | `process_sprites.py: recolour_rivet` |",
        "| PROP-KEY | rembg, rotated 90 deg CCW, scaled to 60 px tall; Rivet copy recoloured | `tools/edit/process_props.py` |",
        "| WPN-CUTLASS | rembg, rotated 40 deg CW (blade points right), 151 px long | `process_props.py` |",
        "| WPN-POPGUN | rembg, mirrored (barrel points right), 100 px | `process_props.py` |",
        "| PROP-CORK | cropped out of a generated bottle, rembg, 30 px | `process_props.py` |",
        "| ENV-BOWL | none (768x432 as generated; scaled to the 640x360 viewport by Godot) | — |",
        "| SFX-* | trimmed to start just before the loudest hit, max length per event, 30 ms fade-out, normalised to -1 dBFS, exported OGG Vorbis | `tools/edit/trim_sfx.py` |",
        "| SFX-EMPTY | + falling speed glide 1.0 -> 0.55 | `tools/edit/pitch_fall.py` |",
        "| MUS-WALTZ | 8-bar loop (5.88-16.63 s of s2) at zero crossings, 8 ms tail-into-head crossfade, OGG Vorbis, loop flag on | `tools/edit/cut_loop.py` |",
        ]
(REPO / "ASSET-LOG.md").write_text("\n".join(out) + "\n")

# rejected contact sheets, downscaled
dst = REPO / "design" / "rejected"
dst.mkdir(parents=True, exist_ok=True)
for f in sorted((REPO / "raw" / "sheets").glob("*.png")):
    im = Image.open(f).convert("RGB")
    im.thumbnail((1100, 1100))
    im.save(dst / (f.stem + ".jpg"), quality=78)
print("ASSET-LOG.md rows:", len(groups), "| sheets:", len(list(dst.glob('*.jpg'))))
