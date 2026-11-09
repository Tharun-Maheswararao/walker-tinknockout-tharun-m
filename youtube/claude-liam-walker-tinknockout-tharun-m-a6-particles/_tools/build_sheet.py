#!/usr/bin/env python3
"""Author beat_sheet.json for the Tin Knockout Assignment 6 particle-effects film (walker mode).

Game source and docs shown: commit c844ab2 (HEAD when the film was built; asserted below, and every
shown file is asserted unchanged against c844ab2). Every excerpt is read from the files, so displayed
code is verbatim. Re-running keeps measured audio fields for beats whose narration did not change.
Modelled on the A5 film's _tools/build_sheet.py.
"""
import json, subprocess
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
GAME = REPO / 'godot'
SLUG = 'claude-liam-walker-tinknockout-tharun-m-a6-particles'
TITLE = 'Tin Knockout, Particle Effects'
REV = 'c844ab2'
REV_SAID = 'c eight four four a b two'

SHOWN = ['godot/effects/impact_effect.tscn', 'godot/effects/wind_steam.tscn', 'godot/effects/steam_mount.gd',
         'godot/game/main.gd', 'godot/shaders/particles_generated.gdshader', 'CHANGE-BRIEF.md', 'TUNING.md',
         'TEST-REPORT.md', 'FRICTIONAL.md', 'SOURCES.md', 'README.md', 'captures', 'evidence/a6', 'logs']
for f in SHOWN:
    s = subprocess.run(['git', '-C', str(REPO), 'diff', '--quiet', REV, '--', f])
    assert s.returncode == 0, f + ' differs from ' + REV


def lines(path, a, b, root=REPO):
    return '\n'.join((root / path).read_text().splitlines()[a - 1:b])


V = {'engine': 'kokoro', 'voice': 'am_onyx'}


def own(bid, act, role, narration, title, kind, show, anchors, est, **panel):
    """A composite of real files / recorded output / real engine capture, laid out by make_media.py."""
    return {'beat_id': bid, 'act': act, 'role_note': role, 'narration_text': narration,
            'shot': {'type': 'STILL', 'source': 'own', 'motion': 'hold', 'treatment': 'none',
                     'evidence_media': f'media/{bid}.mp4',
                     'show': show, 'anchors': anchors,
                     'panel': dict(kind=kind, title=title, **panel),
                     'note': 'Composite of real files, recorded output and real engine captures, built by '
                             '_tools/make_media.py; labels name the provenance of every embedded image.'},
            'estimated_duration_s': est, **V}


def godot_code(bid, role, narration, path, a, b, title, notes, cues, est, size=30):
    return {'beat_id': bid, 'act': 'MECHANISM', 'role_note': role, 'narration_text': narration,
            'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'hold',
                     'show': [{'at': '0.00', 'event': f'godot/{path}:{a}-{b} at reading size'}] +
                             [{'at': ph, 'event': f'line {ln}: {lab}'} for ln, lab, ph in cues],
                     'anchors': [[str(ln), ph] for ln, _, ph in cues],
                     'remotion': {'pattern': 'GodotDevWorkbench', 'props': {
                         'mode': 'code', 'title': title, 'project': 'walker-tinknockout-tharun-m',
                         'path': f'res://{path}  ·  lines {a}–{b}  ·  revision {REV}',
                         'source': f'Godot editor reconstruction · godot/{path} lines {a}–{b} at {REV}, verbatim',
                         'code': lines(path, a, b, GAME), 'startLine': a, 'codeFontSize': size,
                         'inspectorLabel': 'Source notes — not Inspector values',
                         'notes': notes,
                         'cues': [{'at': 0.0, 'line': ln, 'label': lab} for ln, lab, _ in cues],
                         'output': ['code → visible result next', 'Godot editor reconstruction'],
                         'durationSeconds': est}}},
            'estimated_duration_s': est, **V}


B = []

# ---------------------------------------------------------------- B00 walker cold open
B.append({
    'beat_id': 'B00', 'act': 'ASK',
    'role_note': 'COLD OPEN / walker B00 — ClaudeComposerAsk. Illustrative reconstruction, not a transcript.',
    'narration_text': (
        "Hola, this is Liam, in for Bear. Today we take apart assignment six of Tin Knockout, Tharun "
        "Maheswararao's game about tin wind-up toys boxing in an empty goldfish bowl. This time the game gets two "
        "particle effects. The prompt on screen is an illustrative reconstruction, not a saved transcript."),
    'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'type-on',
             'show': [{'at': '0.10', 'event': 'composer types the reconstructed Walker ask; output lines land'}],
             'remotion': {'pattern': 'ClaudeComposerAsk', 'props': {
                 'greeting': 'Hola, Liam',
                 'topic': 'WALKER · GAME DEVELOPMENT · ASSIGNMENT 6',
                 'segment': 'walker-tinknockout-tharun-m',
                 'command': ('Please use Walker to convert my game design document about tin wind-up toys boxing in '
                             'an empty goldfish bowl into two particle effects for my Godot game: a burst on every '
                             'hit, and steam from the back key when a fighter runs low on wind.'),
                 'runningText': 'reading the brief…',
                 'output': [
                     '■ walker-tinknockout-tharun-m  ·  Godot 4.7.2  ·  Forward+  ·  ' + REV,
                     '  impact_effect.tscn   two GPUParticles2D  ·  Shards MIX  ·  Core ADD',
                     '  wind_steam.tscn      one per fighter  ·  amount_ratio from wind',
                     '  textures             written by code  ·  no third-party art',
                     '  RECONSTRUCTED PROMPT — illustrative, not a transcript']}}},
    'estimated_duration_s': 17, **V})

# ---------------------------------------------------------------- B01 hesitant writer
B.append({
    'beat_id': 'B01', 'act': 'BLUF',
    'role_note': 'walker B01 — what was built and what the film explains. The correction is the misconception the '
                 'body dismantles: a headless run proves behaviour, not cost.',
    'lead_silence_s': 0.8,
    'narration_text': ("Tin Knockout got two particle effects: an impact burst on every hit, and steam when a "
                       "fighter's wind runs low. Headless tests prove their behaviour. How they look, and what they "
                       "cost the graphics card, no headless run can show."),
    'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'hold',
             'show': [{'at': '0.10', 'event': 'writer types the overview; "cost" is struck and corrected to "behaviour"'}],
             'remotion': {'pattern': 'BrutalistHesitantWriter', 'props': {
                 'text': 'Tin Knockout got an impact burst\nand wind steam.\nHeadless tests prove their cost.',
                 'triggerWords': 'cost', 'replacementWords': 'behaviour',
                 'charMs': 10, 'mistakeRate': 2, 'hesitateBetween': 4, 'seed': SLUG,
                 'face': 'serif', 'fontSize': 112, 'lineSpacing': 2.6, 'align': 'left', 'ink': '#2b2118'}}},
    'estimated_duration_s': 13, **V})

# ---------------------------------------------------------------- B02 game, effects, jobs, events
B.append(own('B02', 'SETUP',
    'The game, both effects, their jobs, and the event (A) and condition (B) that drive them '
    '(CHANGE-BRIEF A.1, B.1; main.gd).',
    "The game: two tin toys box on wind-up springs, and every attack spends wind. Effect A is an impact burst. "
    "Its job, in Tharun's brief, is to give each hit distinct visual weight and better readability across "
    "backgrounds. Its event is every impact, a melee hit or a cork hit, both arriving at main's on impact, with "
    "a blocked flag. Effect B is wind steam at the fighter's back key, a feedback loop. Its condition is wind "
    "below twenty-five, and its mapping: amount ratio equals twenty-five minus wind, over twenty-five, clamped "
    "between zero and one.",
    'Two Effects, Two Jobs', 'setup',
    [{'at': '0.00', 'event': 'two held frames from the film capture (scripted input), each with a zoom of the effect'},
     {'at': 'Effect A is', 'event': 'EFFECT A card lights: job, event, blocked variant'},
     {'at': 'Effect B is', 'event': 'EFFECT B card lights: job, value, condition, mapping'}],
    [['a', 'Effect A is'], ['b', 'Effect B is']], 32))

# ---------------------------------------------------------------- B03 emission / process / draw
B.append(own('B03', 'MECHANISM',
    'The three parts of a particle system, each with a scene-file line (impact_effect.tscn:86, 28, 37) and the '
    'visible result in the r1 strip; why the headless price is near zero (CLAUDE.md Headless facts).',
    "Every particle system has three parts. Emission decides how many particles are born, and when. Line "
    "eighty-six, explosiveness one: all sixteen shards are born at once, and the burst is on screen in frame ten "
    "itself. Process moves each particle over its life. Line twenty-eight, gravity four hundred: the shards fall "
    "into a ring below the fist. Draw decides how each particle is painted. Line thirty-seven, blend mode one, "
    "which is add: the core can only brighten. In this game the process runs on the graphics card. A headless "
    "run uses a dummy renderer that runs no GPU particle process and draws nothing, so a GPU effect's headless "
    "price is near zero by construction.",
    'Emission · Process · Draw', 'parts',
    [{'at': '0.00', 'event': 'three columns: one line of godot/effects/impact_effect.tscn each'},
     {'at': 'on screen in frame ten', 'event': 'EMISSION result: r1 frame 10, burst on screen at the trigger frame'},
     {'at': 'into a ring', 'event': 'PROCESS result: r1 frame 15, shards in a ring below the fist'},
     {'at': 'the core can only', 'event': 'DRAW result: r1 frame 12, the ADD core brightens the castle'},
     {'at': 'A headless run', 'event': 'headless fact (CLAUDE.md) lights'}],
    [['emit', 'on screen in frame ten'], ['proc', 'into a ring'], ['draw', 'the core can only'],
     ['head', 'A headless run']], 40,
    files=[['godot/effects/impact_effect.tscn', 86, 86], ['godot/effects/impact_effect.tscn', 28, 28],
           ['godot/effects/impact_effect.tscn', 36, 37]]))

# ---------------------------------------------------------------- B04 Effect A intent
B.append(own('B04', 'INTENT',
    'Effect A intent block, CHANGE-BRIEF A.2 (Tharun, drafted with Claude 3.5 Sonnet; corrections from Claude '
    'Code reviews), quoted verbatim.',
    "Effect A's intent, written before the build. Timing: a quarter-second life, an instant snap expansion, "
    "then a smooth fade. Contrast: a dark edge and a bright core, on separate emitters, the shards in mix and "
    "the core in add. That split came from Claude Code's review: an additive layer cannot draw a dark outline. "
    "Scale: about sixty pixels wide in the window. Variation: random angle, speed and rotation, so rapid "
    "repeated hits never look stamped.",
    'Effect A · The Intent', 'intentA',
    [{'at': '0.00', 'event': 'CHANGE-BRIEF A.2 rows quoted verbatim'},
     {'at': 'Contrast: a dark', 'event': 'Contrast row lights; brief authorship note on the split'},
     {'at': 'Scale: about sixty', 'event': 'Scale and Variation rows light'}],
    [['contrast', 'Contrast: a dark'], ['scale', 'Scale: about sixty']], 27))

# ---------------------------------------------------------------- B05 Effect A scene (checked excerpt)
B.append(godot_code('B05',
    'The Effect A scene as built: impact_effect.tscn:77-86, root and Shards node (checked excerpt).',
    "And here is how that intent landed in the scene file. Line seventy-seven: the root draws at z index six, "
    "above the kept star at five. Line eighty: the shards draw through their own material, which blends in mix. "
    "Lines eighty-two to eighty-six: sixteen shards, a quarter-second life, one shot, all born at once. Claude "
    "built this scene, unedited; every value comes from Tharun's brief, and no code sets them.",
    'effects/impact_effect.tscn', 77, 86, 'Effect A · The Scene',
    [{'label': 'Who', 'value': 'built by Claude Code · every value from Tharun\'s brief (SOURCES.md)'},
     {'label': 'Rule', 'value': 'effect settings live in scene files, not code (CLAUDE.md)'}],
    [(77, 'z_index 6: above the star at 5 (A-R6)', 'Line seventy-seven'),
     (80, 'Shards material: blend MIX', 'Line eighty'),
     (86, 'amount 16 · lifetime 0.25 · one shot · all at once', 'Lines eighty-two')], 25, size=28))

# ---------------------------------------------------------------- B06 Effect A first strip r0
B.append(own('B06', 'RESULT',
    'The first strip, r0 (fixture), with Tharun\'s first look (before Claude read it) and Claude\'s reading '
    '(TUNING.md Effect A).',
    "The first strip is a fixture: a preview scene with a fixed seed, a burst at frame ten and a second at "
    "frame eleven. Tharun looked first, before Claude read anything. The core flash, bright cyan, reads. The "
    "dark shards are a bit hard to make out. Claude's reading agreed and measured why: at frame fifteen the "
    "shards darken the castle by a median of only forty-one levels. The colour ramp fades alpha in a straight "
    "line, so two-thirds through life about a third is left. Frames twenty, thirty and fifty are empty, as the "
    "brief predicted.",
    'Effect A · The First Strip', 'stripA',
    [{'at': '0.00', 'event': 'captures/impact_effect/r0 frames 10, 12, 15, 20, 30, 50 (fixture, held frames, zoom)'},
     {'at': 'Tharun looked first', 'event': "Tharun's first look, verbatim"},
     {'at': "Claude's reading agreed", 'event': 'frame 15 ringed; Claude\'s reading: median drop 41'},
     {'at': 'Frames twenty, thirty', 'event': 'frames 20, 30, 50 marked empty'}],
    [['look', 'Tharun looked first'], ['read', "Claude's reading agreed"], ['empty', 'Frames twenty, thirty']], 33))

# ---------------------------------------------------------------- B07 Effect A revision 1: change + prediction
B.append(own('B07', 'MECHANISM',
    'Effect A revision 1: the one-setting change (impact_effect.tscn:8-9, git 45e986f) and Claude\'s '
    'frame-by-frame prediction written before the change (TUNING.md).',
    "Revision one changes one setting: the shards' colour ramp, lines eight and nine. A middle point at seven "
    "tenths keeps the charcoal fully opaque for most of the shard's life. Claude's prediction, written before "
    "any change: frame ten unchanged; frame twelve slightly darker; and at frame fifteen the median darkening "
    "rises from forty-one to ninety or more, with about the same count of dark pixels. The risk Claude named: "
    "the fade is squeezed into the last few frames, so the shards may blink out. Tharun approved the change.",
    'Effect A · Revision 1', 'revA',
    [{'at': '0.00', 'event': 'git diff 45e986f: impact_effect.tscn Gradient, old line and new lines 8-9'},
     {'at': "Claude's prediction", 'event': 'prediction card: frames 10, 12, 15, 20-50'},
     {'at': 'The risk Claude named', 'event': 'risk line lights: blink out'}],
    [['pred', "Claude's prediction"], ['risk', 'The risk Claude named']], 30,
    files=[['godot/effects/impact_effect.tscn', 7, 9]]))

# ---------------------------------------------------------------- B08 Effect A revision 1: r1 + verdict
B.append(own('B08', 'RESULT',
    'r0 vs r1 (captures/impact_effect/r0_vs_r1_sheet.png), Claude\'s comparison and Tharun\'s in-game verdict.',
    "r1, captured by Tharun with the same fixture and seed. Top row before, bottom row after. Frame fifteen: "
    "the median rose to one hundred and five point seven, so the median matches. The count does not: it rose by "
    "sixteen percent, because faint edge pixels now pass the threshold. Frame twelve: direction right, size "
    "wrong. Frame ten: almost; Claude had assumed the particles were zero frames old. The blink-out risk is "
    "something the strip cannot show, so it went to Tharun in the running game: they faded out smoothly, no "
    "snap or blink. His verdict: keep.",
    'Effect A · Before and After', 'cmpA',
    [{'at': '0.00', 'event': 'r0_vs_r1_sheet.png (top r0, bottom r1; frames 10, 12, 15, 20)'},
     {'at': 'Frame fifteen: the median', 'event': 'frame 15 column ringed; row: 41.3 → 105.7, Matches'},
     {'at': 'Frame twelve', 'event': 'rows for frames 12 and 10 light'},
     {'at': 'it went to Tharun', 'event': "Tharun's verdict, verbatim: Keep"}],
    [['f15', 'Frame fifteen: the median'], ['f12', 'Frame twelve'], ['verdict', 'it went to Tharun']], 33))

# ---------------------------------------------------------------- B09 Effect A wiring
B.append(own('B09', 'MECHANISM',
    'The event wiring: main.gd:228-238 _spawn_impact (Claude, plan approved step by step by Tharun).',
    "Now the event. Main's on impact keeps the star, the shake and the roll, then calls spawn impact. Line two "
    "twenty-nine picks the normal or the blocked scene from the blocked flag. Line two thirty-one makes the "
    "burst a child of Main at p, so a cork can free itself without taking the burst with it. And line two "
    "thirty-eight restarts each emitter after add child; the burst frees itself once both have finished. A "
    "fresh instance per hit, so rapid hits overlap instead of cutting each other off.",
    'Effect A · The Event', 'code',
    [{'at': '0.00', 'event': 'godot/game/main.gd:228-238 at reading size'},
     {'at': 'Line two twenty-nine', 'event': 'line 229 highlighted: normal or blocked scene'},
     {'at': 'Line two thirty-one', 'event': 'line 231 highlighted: child of Main at p'},
     {'at': 'thirty-eight restarts', 'event': 'line 238 highlighted: restart() after add_child'}],
    [['229', 'Line two twenty-nine'], ['231', 'Line two thirty-one'], ['238', 'thirty-eight restarts']], 27,
    path='godot/game/main.gd', segments=[[228, 238]],
    cues=[[229, 'normal or blocked scene, from the blocked flag (A-R5)'],
          [231, 'a child of Main at p: outlives the cork (A-R2, A-R4)'],
          [238, 'restart() after add_child; freed on finished (A-R3, F2)']],
    notes=[['Who', 'Claude, from plan step3a-plan.md, approved step by step by Tharun'],
           ['Kept', 'star, shake, roll and hitstop unchanged (brief C)']]))

# ---------------------------------------------------------------- B10 Effect A in play
B.append(own('B10', 'RESULT',
    'Effect A in play: Movie Maker capture made for this film, scripted input on an isolated copy of c844ab2 '
    '(capture/play-4k.mp4); rapid repeats, blocked variant, 0.25x replay.',
    "In play, from a scripted-input capture made for this film. Bolt taps jab each time he is ready, eight "
    "times; Rivet is the game's own brain. Every landed jab bursts. Every other jab, Rivet blocks, and that hit "
    "gets the smaller grey burst. Rivet's own hits on Bolt burst too. Again at quarter speed: each hit gets its "
    "own instance, and the counter shows how many are alive.",
    'Effect A · In Play', 'playA',
    [{'at': '0.00', 'event': 'capture/play-4k.mp4, the jab sequence at real speed, with a zoom on the hit point and '
                             'a per-frame readout from the capture log'},
     {'at': 'Again at quarter speed', 'event': 'labelled 0.25x replay'}],
    [['slow', 'Again at quarter speed']], 25))

# ---------------------------------------------------------------- B11 Effect B intent
B.append(own('B11', 'INTENT',
    'Effect B intent: CHANGE-BRIEF B.1 (job, value, condition, mapping, feature A does not use) and B.2 '
    '(timing, scale), quoted verbatim.',
    "Effect B is a feedback loop. Tharun's brief says players fighting at high speed cannot afford to look away "
    "from the sprites to check the dial, so the cue sits on the fighter's back, at the key. The value is wind, "
    "zero to one hundred. The condition: below twenty-five, the same threshold as the music's slowdown. The "
    "mapping: dormant at twenty-five and above, rising in a straight line to one at zero. And the feature "
    "Effect A doesn't use: amount ratio, which scales how many particles are emitted without restarting the "
    "system. Puffs should start around five pixels and grow to fifteen or twenty.",
    'Effect B · The Intent', 'intentB',
    [{'at': '0.00', 'event': 'CHANGE-BRIEF B.1 rows quoted verbatim'},
     {'at': 'The condition: below', 'event': 'Condition and Mapping rows light'},
     {'at': "Effect A doesn't use", 'event': 'Feature row lights: amount_ratio'},
     {'at': 'Puffs should start', 'event': 'B.2 scale row lights'}],
    [['cond', 'The condition: below'], ['feat', "Effect A doesn't use"], ['scale', 'Puffs should start']], 33))

# ---------------------------------------------------------------- B12 Effect B scene + mapping
B.append(own('B12', 'MECHANISM',
    'Effect B as built: wind_steam.tscn:35-43 (node) beside main.gd:69-70 and 241-242 (attach, mapping).',
    "The scene: one emitter. Amount twenty-five, the fixed maximum, and amount ratio zero: dormant. A life of "
    "six tenths of a second, and local coordinates on, so the puffs ride with the key. In main, line seventy: "
    "each time a fighter announces its wind, the steam's amount ratio is set from steam ratio. Lines two "
    "forty-one and two forty-two: twenty-five minus wind, over twenty-five, clamped. That is the only effect "
    "value any code sets.",
    'Effect B · The Scene and the Mapping', 'codeB',
    [{'at': '0.00', 'event': 'wind_steam.tscn:35-43 beside main.gd:69-70, 241-242'},
     {'at': 'Amount twenty-five', 'event': 'lines 37-38 highlighted: amount 25, amount_ratio 0.0'},
     {'at': 'A life of', 'event': 'lines 40, 42 highlighted: lifetime 0.6, local_coords true'},
     {'at': 'line seventy', 'event': 'main.gd line 70 highlighted'},
     {'at': 'Lines two forty-one', 'event': 'main.gd lines 241-242 highlighted'}],
    [['amt', 'Amount twenty-five'], ['life', 'A life of'], ['70', 'line seventy'], ['241', 'Lines two forty-one']],
    28, files=[['godot/effects/wind_steam.tscn', 35, 43], ['godot/game/main.gd', 69, 70],
               ['godot/game/main.gd', 241, 242]]))

# ---------------------------------------------------------------- B13 Effect B first strip
B.append(own('B13', 'RESULT',
    'The first steam strip, captures/wind_steam/r0 (fixture), Tharun\'s first look, and Claude\'s later size '
    'measurement (TUNING.md, TEST-REPORT A6-5c).',
    "The first steam strip, again a fixture: ratio one from frame ten, cut to zero at frame fifty. Frame forty "
    "is the steady plume; fifty-five, the tail fading; seventy, empty. Tharun's first look: fine white misty "
    "trails rising upward, and the entire steam rise is tall, roughly half of Bolt's height. Claude measured it "
    "afterwards at frame forty: eighteen by twenty-seven view pixels, about a quarter of Bolt's one hundred and "
    "twelve. That disagreement stands. We come back to it.",
    'Effect B · The First Strip', 'stripB',
    [{'at': '0.00', 'event': 'captures/wind_steam/r0 frames 12, 20, 40, 55, 70 (fixture, held frames, zoom)'},
     {'at': "Tharun's first look", 'event': "Tharun's first look, verbatim"},
     {'at': 'Claude measured it', 'event': "Claude's measurement: 18 x 27 view px, about 1/4 of Bolt"}],
    [['look', "Tharun's first look"], ['meas', 'Claude measured it']], 30))

# ---------------------------------------------------------------- B14 Effect B revision 1: cause, change, prediction
B.append(own('B14', 'MECHANISM',
    'Effect B revision 1: Tharun\'s in-game observation, the rewind strip r0 (fixture), the change '
    '(steam_mount.gd:31-35, Tharun\'s choice) and Claude\'s prediction (TUNING.md).',
    "Revision one came from play. Tharun, in game: the steam cut out immediately upon triggering the rewind "
    "state. The first strip never rewinds, so Claude added a rewind fixture. Its strip, r0, frame thirty-four: "
    "the whole plume collapses to a thin sliver. The key spins, its x scale swings down to fifteen percent, and "
    "the steam, its child, squashes with it. Tharun chose the fix: a holder, Steam Mount, over turning local "
    "coordinates off. Lines thirty-three to thirty-five copy the key's position, facing and visibility, but not "
    "its squash. Claude's prediction: r1 equals r0 wherever the key was full width, and at frame thirty-four, "
    "a full-width plume.",
    'Effect B · Revision 1', 'revB',
    [{'at': '0.00', 'event': "Tharun's in-game observation (TEST-REPORT A6-3), verbatim"},
     {'at': 'Its strip, r0', 'event': 'rewind strip r0 frames 31, 34, 38 (fixture, held frames, zoom); 34 ringed'},
     {'at': 'Tharun chose the fix', 'event': 'godot/effects/steam_mount.gd:31-35, lines 33-35 highlighted'},
     {'at': "Claude's prediction", 'event': 'prediction card'}],
    [['strip', 'Its strip, r0'], ['fix', 'Tharun chose the fix'], ['pred', "Claude's prediction"]], 40,
    files=[['godot/effects/steam_mount.gd', 31, 35]]))

# ---------------------------------------------------------------- B15 Effect B revision 1: r1 + verdict
B.append(own('B15', 'RESULT',
    'Rewind r0 vs r1 (captures/wind_steam_rewind/r0_vs_r1_sheet.png), Claude\'s comparison and Tharun\'s '
    'in-game verdict.',
    "r1, same fixture, seed and flags. Top row before, bottom row after. Frames twenty-eight and thirty-one: "
    "zero pixels differ. Frame thirty-four: one thousand and twenty-one pixels differ, all in a small box above "
    "the key, a full soft plume where r0 had a sliver. Every later frame: zero. It matches. But the strip "
    "under-shows the old flicker: only one of seven rewind frames caught the key narrow. So the verdict was "
    "Tharun's, in game: it kept going and tapered off smoothly instead of cutting out. Keep.",
    'Effect B · Before and After', 'cmpB',
    [{'at': '0.00', 'event': 'r0_vs_r1_sheet.png (top r0, bottom r1; frames 28-72)'},
     {'at': 'Frame thirty-four', 'event': 'frame 34 column ringed: 1021 px differ'},
     {'at': 'under-shows', 'event': 'note: 1 of 7 rewind frames caught the key narrow'},
     {'at': "Tharun's, in game", 'event': "Tharun's verdict, verbatim: Keep"}],
    [['f34', 'Frame thirty-four'], ['under', 'under-shows'], ['verdict', "Tharun's, in game"]], 30))

# ---------------------------------------------------------------- B16 Effect B in play: start, pause, stop
B.append(own('B16', 'RESULT',
    'Effect B in play, start / pause / stop: the same Movie Maker capture (scripted input), with Bolt\'s wind, '
    'amount_ratio and pause read from the capture log each frame; state-test rows B-R1..B-R4.',
    "In play, from the same scripted capture. After the seventh jab, Bolt's wind is sixteen: ratio point three "
    "six, and steam starts from the key. After the eighth, wind four: point eight four. Then pause. The fight "
    "freezes and the screen dims, but the steam keeps rising. It is the only thing that moves, because it "
    "inherits process mode always from Main. Play resumes, and Rivet lands a hit. Then rewind. Each click adds "
    "ten wind, the ratio steps down, point four four, point zero four, zero, and the puffs already alive fade "
    "out over their life instead of vanishing.",
    'Effect B · In Play', 'playB',
    [{'at': '0.00', 'event': 'capture/play-4k.mp4 from the 7th jab to the end, zoom on the key, readout of wind, '
                             'amount_ratio and paused from the capture log'},
     {'at': 'Then pause', 'event': 'PAUSED in the readout; puffs still move (the only pixels that change)'},
     {'at': 'Play resumes', 'event': 'Bolt HURT in the readout'},
     {'at': 'Then rewind', 'event': 'REWIND in the readout; ratio 0.84 -> 0.44 -> 0.04 -> 0'}],
    [['pause', 'Then pause'], ['rew', 'Then rewind']], 27))

# ---------------------------------------------------------------- B17 process shader
B.append(own('B17', 'MECHANISM',
    'Two annotated lines of the generated process shader (particles_generated.gdshader:258, 302 with 315) '
    'beside the brief settings they implement (B.3 spread 30.0, gravity (0, -180, 0)); Tharun\'s line '
    'references (TEST-REPORT "The process shader").',
    "Under the hood. Tharun converted Effect B's process material in the editor and saved the shader Godot "
    "wrote; the game does not use this copy. Line two fifty-eight: each new puff gets a random direction from "
    "spread, times its starting speed. That spread is the brief's thirty degrees, a half-angle. Line three oh "
    "two: force starts as gravity, and line three fifteen adds force times delta to the velocity. That gravity "
    "is the brief's minus one eighty. The numbers themselves live on the material, so the shader only declares "
    "them as uniforms.",
    'The Process Shader', 'shader',
    [{'at': '0.00', 'event': 'particles_generated.gdshader lines 258, 302, 315 beside CHANGE-BRIEF B.3 rows'},
     {'at': 'Line two fifty-eight', 'event': 'line 258 highlighted, linked to spread 30.0'},
     {'at': 'Line three oh', 'event': 'lines 302 and 315 highlighted, linked to gravity (0, -180, 0)'},
     {'at': 'The numbers themselves', 'event': "Tharun's note: the value lives on the material resource"}],
    [['258', 'Line two fifty-eight'], ['302', 'Line three oh'], ['mat', 'The numbers themselves']], 30,
    files=[['godot/shaders/particles_generated.gdshader', 258, 258], ['godot/shaders/particles_generated.gdshader', 302, 302],
           ['godot/shaders/particles_generated.gdshader', 315, 315], ['godot/shaders/particles_generated.gdshader', 7, 7],
           ['godot/shaders/particles_generated.gdshader', 43, 43]]))

# ---------------------------------------------------------------- B18 tests + mutations
B.append(own('B18', 'TESTS',
    'What the tests proved: counts (logs/, re-run for this film on a clean copy of c844ab2) and the mutations '
    '(evidence/a6/mutations/, TEST-REPORT A6-1..A6-3).',
    "What the tests proved, re-run for this film on a clean copy of c844ab2. The config tests read every brief "
    "value back from the scenes: one hundred thirty-six checks for Effect A and thirty-three for Effect B, none "
    "failed, including that spread of thirty and gravity of minus one eighty. The state tests drive real input: "
    "forty-four for A, thirty-seven for B. Then the mutations. A Godot three name: Godot loaded it with no "
    "warning, and the effect still fired, but one check failed. A value drift, sixteen shards to twelve: one "
    "failed. Never freeing a burst: five. Setting amount instead of amount ratio: eleven. And one did not "
    "fail: setting emitting before the burst entered the tree, because the predicted failure never happened.",
    'What the Tests Proved', 'tests',
    [{'at': '0.00', 'event': 'test counts from the re-run logs (evidence/runs/tests-c844ab2/)'},
     {'at': 'Then the mutations', 'event': 'mutation table with each FAIL line (evidence/a6/mutations/)'},
     {'at': 'And one did not', 'event': 'M3 row lights: 44 checks, 0 failed, not caught'}],
    [['mut', 'Then the mutations'], ['m3', 'And one did not']], 42))

# ---------------------------------------------------------------- B19 price vs budget
B.append(own('B19', 'TESTS',
    'Both prices against the budget: headless wall-clock price (evidence/a6/cost/cost_effects_60fps.log), the '
    'GPU budgets (CHANGE-BRIEF F) and the effects-off reference (evidence/a6/visual-profiler-vulkan.webp, '
    'Tharun); the GPU price is not measured (TEST-REPORT A6-5: open).',
    "And the price. The headless cost script includes an empty-scene control. The game without the effects "
    "costs about point zero two milliseconds a frame on the wall clock. Four bursts at once add point zero zero "
    "six, inside a spread of point zero one six. Full steam on both fighters: minus point zero zero zero seven. "
    "Neither can be told apart from the game without it, and two engine timers read zero throughout. The "
    "budgets are GPU budgets: Effect A under point five five milliseconds, Effect B under point two, against a "
    "point nine seven millisecond effects-off reference. The GPU price has not been measured yet. Those numbers "
    "are pending, and this film does not guess them. No headless run can show the look, or the GPU time.",
    'Two Prices, One Budget', 'price',
    [{'at': '0.00', 'event': 'cost_effects_60fps.log table, verbatim'},
     {'at': 'The budgets are GPU', 'event': 'budget card (CHANGE-BRIEF F) and the effects-off Visual Profiler '
                                            'screenshot (Tharun)'},
     {'at': 'The GPU price has not', 'event': 'GPU PRICE: PENDING (not measured) lights'}],
    [['budget', 'The budgets are GPU'], ['pending', 'The GPU price has not']], 40))

# ---------------------------------------------------------------- B20 mistakes and disagreements
B.append(own('B20', 'VERDICT',
    'Agent mistakes caught (CHANGE-BRIEF A6 revisions, TEST-REPORT A6-2, A6-3, TUNING.md) and the readings of '
    'Claude\'s where Tharun\'s verdict differs (TEST-REPORT A6-5c, Tharun\'s statement verbatim).',
    "Agent mistakes, caught. Claude cited main line two hundred for the cork's handler; it was one ninety-nine. "
    "Claude's first key list said R for rewind; it is S. Claude's first watch loop ran four times too fast. "
    "Claude's first state test compared two bursts after both were freed. And Claude's early probe was stated "
    "more broadly than the result supports. Where Tharun's verdict differs from Claude's readings: the shards "
    "looked bigger to him, though their scale is unchanged; and the steam looked like half of Bolt's height, "
    "against a measured quarter. In Tharun's words, he accepts the objective pixel measurements; however, he "
    "keeps his visual observation for gameplay evaluation. And once it went the other way: his first answer "
    "said the shards pop cleanly over the dark stretch, Claude measured forty-two against one hundred five, and "
    "he corrected it.",
    'Claude, Checked · Claude, Overruled', 'against',
    [{'at': '0.00', 'event': 'five agent mistakes, each with its record'},
     {'at': "Where Tharun's verdict", 'event': 'A6-5c rows: shard size, steam size'},
     {'at': "In Tharun's words", 'event': "Tharun's statement, verbatim"},
     {'at': 'the other way', 'event': 'dark-stretch row: corrected after measurement'}],
    [['diff', "Where Tharun's verdict"], ['words', "In Tharun's words"], ['other', 'the other way']], 45))

# ---------------------------------------------------------------- B21 credits
B.append(own('B21', 'CREDITS',
    'Human and AI contributions as SOURCES.md "Who did what (A6)", shown verbatim; texture sources '
    '(godot/effects/textures/ATTRIBUTION.md); drafting help (Claude 3.5 Sonnet).',
    "Who did what, as SOURCES dot m d records it. Tharun chose both effects and every value in the brief, "
    "drafting with Claude three point five Sonnet, and wrote every dated revision. He reviewed CLAUDE dot m d, "
    "took the Visual Profiler screenshot, ran every Movie Maker capture and both config mutations, approved "
    "each wiring step and tuning change, gave every first look and in-game verdict, and converted the process "
    "shader. Claude Code wrote the facts sheet and probes, built both effect scenes, the texture scripts, the "
    "tests, the fixtures, the wiring and Steam Mount, read and measured every strip, and drafted the docs. Both "
    "textures are written by code; there is no third-party art.",
    'Who Did What (A6)', 'credits',
    [{'at': '0.00', 'event': 'SOURCES.md "Who did what (A6)" verbatim, two columns'},
     {'at': 'Claude Code wrote', 'event': 'Claude column lights'},
     {'at': 'Both textures', 'event': 'texture sources (ATTRIBUTION.md) light'}],
    [['claude', 'Claude Code wrote'], ['tex', 'Both textures']], 40))

# ---------------------------------------------------------------- B22 verdict
B.append({
    'beat_id': 'B22', 'act': 'VERDICT',
    'role_note': 'VERDICT — checked by numbers / by eye, open (GPU price), uncertain, one next step; revision shown.',
    'narration_text': (
        f"The verdict, at revision {REV_SAID}. Checked by numbers: every brief value read back, the rules in the "
        "state tests, five mutations caught, and one honestly not. Checked by eye: Tharun's first looks, both "
        "tuning verdicts, both backgrounds, scene load and the arena walls. Still open: the GPU price. Still "
        "uncertain: Effect A's shards lose most of their contrast over the dark stretch; Rivet rarely steams, "
        "because his brain rewinds at the same threshold; and whether a hidden emitter keeps simulating has not "
        "been checked. One next step: take the GPU price in the GPU price fixture, effect off against on at its "
        "heaviest, for each effect, against its budget."),
    'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'hold',
             'show': [{'at': '0.10', 'event': 'verdict artifact lines land'}],
             'remotion': {'pattern': 'ClaudeVerdictArtifact', 'props': {
                 'artifactTitle': 'walker-tinknockout-tharun-m · Assignment 6',
                 'artifactHeading': 'VERDICT · revision ' + REV,
                 'brandLabel': 'WALKER · GODOT 4.7.2 · FORWARD+',
                 'artifactLines': [
                     'CHECKED — numbers: config 136/0 · 33/0, state 44/0 · 37/0',
                     '  mutations: 5 caught, 1 not (M3: the failure never happened)',
                     'CHECKED — by eye (Tharun): first looks, both verdicts, backgrounds',
                     'OPEN  GPU price: Visual Profiler, not measured yet',
                     'UNCERTAIN  shards faint over the dark stretch (42 vs 105)',
                     'UNCERTAIN  Rivet rarely steams · hidden emitter not checked',
                     'NEXT  GPU price per effect in gpu_price.tscn, vs its budget']}}},
    'estimated_duration_s': 36, **V})

# ---------------------------------------------------------------- B23 your turn
B.append({
    'beat_id': 'B23', 'act': 'YOUR_TURN',
    'role_note': 'YOUR TURN — a useful Walker prompt read aloud, one bounded change + prediction first, texture '
                 'source, revision; Liam signs off before the locked outro.',
    'narration_text': (
        "Your turn. Here is a useful Walker prompt. Please use Walker to give Effect A's shards a lighter rim for "
        "dark backgrounds, and before you capture anything, tell me what you predict frame fifteen's shard "
        "darkening will be over the dark stretch and over the castle. Write the prediction first; a strip only "
        "means something against one. Then a person looks, in game. The textures here are written by code. This "
        f"voice is Kokoro text to speech. The source shown is revision {REV_SAID}. Liam, in for Bear."),
    'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'type-on',
             'show': [{'at': '0.10', 'event': 'composer types the suggested prompt; prediction rule and credits land'}],
             'remotion': {'pattern': 'ClaudeComposerAsk', 'props': {
                 'greeting': 'Your turn.',
                 'topic': 'WALKER · YOUR TURN',
                 'segment': 'one bounded change',
                 'command': ("Please use Walker to give Effect A's shards a lighter rim for dark backgrounds, and "
                             "before you capture anything, tell me what you predict frame 15's shard darkening will "
                             "be over the dark stretch and over the castle."),
                 'runningText': 'over to you…',
                 'output': [
                     '■ prediction first: frame 15 now reads 42 (dark) and 105 (castle)',
                     '■ then a person looks, in game',
                     '  TEXTURES  written by code: generate_shard_texture.gd, generate_steam_texture.gd',
                     '  SOURCE    game revision ' + REV,
                     '  VOICE     Liam — Kokoro am_onyx, AI text-to-speech']}}},
    'estimated_duration_s': 30, **V})

# ---------------------------------------------------------------- B24 outro
B.append({
    'beat_id': 'B24', 'act': 'OUTRO', 'kind': 'outro_voice',
    'role_note': 'OUTRO-LOCK — exact title, @NikBearBrown, slug-seeded mascot. Spoken, never scored; 1.0 s silent tail.',
    'narration_text': f'{TITLE}. At Nik Bear Brown.',
    'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'hold',
             'show': [{'at': '0.10', 'event': 'locked title card'}],
             'remotion': {'pattern': 'ClaudeTitleOutro', 'props': {'title': TITLE, 'slug': SLUG}}},
    'estimated_duration_s': 5, **V})

meta = {
    'title': TITLE, 'slug': SLUG,
    'topic': 'WALKER · GAME DEVELOPMENT · ASSIGNMENT 6', 'kind': 'godot-gamedev', 'playlist': 'Walker',
    'brand': 'claude-liam', 'audience': 'CSYE 7270 reviewers and Walker users',
    'register': 'Teardown', 'engine': 'kokoro', 'voice': 'am_onyx', 'voice_kokoro': 'am_onyx',
    'palette': 'claude', 'style_preset': 'claude', 'aspect_ratio': '16:9', 'captions': False,
    'channel_title': '@NikBearBrown', 'channel': '@NikBearBrown',
    'presenter': 'Liam (in for Bear)', 'persona': 'Liam (in for Bear)',
    'episode_id': 'walker-tinknockout-tharun-m-a6', 'mode': 'walker',
    'game': {'name': 'walker-tinknockout-tharun-m', 'revision': subprocess.run(
                 ['git', '-C', str(REPO), 'rev-parse', REV], capture_output=True, text=True).stdout.strip(),
             'docs_revision': REV, 'godot_path': 'godot',
             'engine_version': '4.7.2.stable.official.ed1daf0bf', 'renderer': 'Forward+ (Vulkan/MoltenVK)'},
    'student': 'Tharun Maheswararao', 'course': 'CSYE 7270 Fall 2026 · Assignment 6',
    'note': ('Walker-mode godot-gamedev film of the A6 particle effects. Game source and docs shown: c844ab2. '
             'Strips are fixture captures (godot/previews/, fixed seed) taken by Tharun; the in-play footage is one '
             'Movie Maker capture made for this film on an isolated copy of c844ab2 (scripted input). The Visual '
             'Profiler screenshot is Tharun\'s. The GPU price is not measured and is shown as pending. B00 is an '
             'illustrative reconstruction; code views are labelled reconstructions / source views.'),
}

old = {}
p = REEL / 'beat_sheet.json'
if p.exists():
    for b in json.loads(p.read_text())['beats']:
        old[b['beat_id']] = b
for b in B:
    o = old.get(b['beat_id'])
    if o and o.get('narration_text') == b.get('narration_text'):
        for k in ('actual_duration_s', 'audio_file', 'outro_tail_s', 'lead_silence_baked', 'voice_duration_s'):
            if k in o:
                b[k] = o[k]
    ro, rn = (o or {}).get('shot', {}).get('remotion') or {}, b['shot'].get('remotion') or {}
    if ro.get('rendered') and rn:
        strip = lambda d: {k: v for k, v in d.get('props', {}).items() if k not in ('durationSeconds', 'cues')}
        if ro.get('pattern') == rn.get('pattern') and strip(ro) == strip(rn):
            rn['rendered'] = ro['rendered']
p.write_text(json.dumps({'metadata': meta, 'beats': B}, indent=1, ensure_ascii=False) + '\n')
print('wrote', p, len(B), 'beats', sum(len(b.get('narration_text', '').split()) for b in B), 'words')
