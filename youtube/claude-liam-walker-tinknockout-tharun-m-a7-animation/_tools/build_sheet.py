#!/usr/bin/env python3
"""Author beat_sheet.json for the Tin Knockout Assignment 7 animation film (walker mode).

Game source and docs shown: commit a5978c0. Every shown file is asserted unchanged between the working
tree and a5978c0 when this runs, and every excerpt is read from `git show a5978c0:<path>`, so displayed
code is verbatim at that revision. Re-running keeps measured audio fields for beats whose narration did
not change. Modelled on the A6 film's _tools/build_sheet.py.
"""
import json, subprocess
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
SLUG = 'claude-liam-walker-tinknockout-tharun-m-a7-animation'
TITLE = 'Tin Knockout, Animation'
REV = 'a5978c0'
REV_SAID = 'a five nine seven eight c zero'

SHOWN = ['godot/animations', 'godot/fighter/fighter.gd', 'godot/tools/generate_key_sheets.gd', 'godot/assets/props',
         'godot/previews', 'godot/tests', 'godot/game/main.gd', 'CHANGE-BRIEF.md', 'TUNING.md', 'TEST-REPORT.md',
         'FRICTIONAL.md', 'SOURCES.md', 'README.md', 'CLAUDE.md', 'captures/jab_action', 'evidence/a7', 'logs']
for f in SHOWN:
    s = subprocess.run(['git', '-C', str(REPO), 'diff', '--quiet', REV, '--', f])
    assert s.returncode == 0, f + ' differs from ' + REV


def at_rev(path):
    return subprocess.run(['git', '-C', str(REPO), 'show', f'{REV}:{path}'], capture_output=True, text=True,
                          check=True).stdout


def lines(path, a, b):
    """Lines a..b (1-based, inclusive) of path (repo-relative) at REV."""
    return '\n'.join(at_rev(path).splitlines()[a - 1:b])


V = {'engine': 'kokoro', 'voice': 'am_onyx'}


def own(bid, act, role, narration, title, kind, show, anchors, est, **panel):
    """A composite of real files / recorded output / real engine captures, laid out by make_media.py."""
    return {'beat_id': bid, 'act': act, 'role_note': role, 'narration_text': narration,
            'shot': {'type': 'STILL', 'source': 'own', 'motion': 'hold', 'treatment': 'none',
                     'evidence_media': f'media/{bid}.mp4',
                     'show': show, 'anchors': anchors,
                     'panel': dict(kind=kind, title=title, **panel),
                     'note': 'Composite of real files, recorded output and real engine captures, built by '
                             '_tools/make_media.py; labels name the provenance of every embedded image.'},
            'estimated_duration_s': est, **V}


def godot_code(bid, role, narration, path, a, b, title, notes, cues, est, size=30):
    """Checked excerpt (GodotDevWorkbench). path is relative to godot/."""
    return {'beat_id': bid, 'act': 'MECHANISM', 'role_note': role, 'narration_text': narration,
            'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'hold',
                     'show': [{'at': '0.00', 'event': f'godot/{path}:{a}-{b} at reading size'}] +
                             [{'at': ph, 'event': f'line {ln}: {lab}'} for ln, lab, ph in cues],
                     'anchors': [[str(ln), ph] for ln, _, ph in cues],
                     'remotion': {'pattern': 'GodotDevWorkbench', 'props': {
                         'mode': 'code', 'title': title, 'project': 'walker-tinknockout-tharun-m',
                         'path': f'res://{path}  ·  lines {a}–{b}  ·  revision {REV}',
                         'source': f'Godot editor reconstruction · godot/{path} lines {a}–{b} at {REV}, verbatim',
                         'code': lines('godot/' + path, a, b), 'startLine': a, 'codeFontSize': size,
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
        "Hola, this is Liam, in for Bear. Today we take apart assignment seven of Tin Knockout, Tharun "
        "Maheswararao's game about tin wind-up toys boxing in an empty goldfish bowl. This time the toys get two "
        "animation clips. The prompt on screen is an illustrative reconstruction, not a saved transcript."),
    'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'type-on',
             'show': [{'at': '0.10', 'event': 'composer types the reconstructed Walker ask; output lines land'}],
             'remotion': {'pattern': 'ClaudeComposerAsk', 'props': {
                 'greeting': 'Hola, Liam',
                 'topic': 'WALKER · GAME DEVELOPMENT · ASSIGNMENT 7',
                 'segment': 'walker-tinknockout-tharun-m',
                 'command': ('Please use Walker to convert my game design document about tin wind-up toys boxing in '
                             'an empty goldfish bowl into two animation clips for my Godot game: the wind key turning '
                             'while a fighter rewinds, and a jab with a wind-up, a held punch and a return.'),
                 'runningText': 'reading the brief…',
                 'output': [
                     '■ walker-tinknockout-tharun-m  ·  Godot 4.7.2  ·  Forward+  ·  ' + REV,
                     '  wind_key_cycle   Sprite2D + frame track  ·  8 frames at 8 fps  ·  loops',
                     '  jab_action       cutout rig keyed as resource text  ·  60 fps  ·  commits',
                     '  clock            both players MANUAL, put at state_t every tick',
                     '  RECONSTRUCTED PROMPT — illustrative, not a transcript']}}},
    'estimated_duration_s': 17, **V})

# ---------------------------------------------------------------- B01 hesitant writer
B.append({
    'beat_id': 'B01', 'act': 'BLUF',
    'role_note': 'walker B01 — what was built and what the film explains. The correction is the misconception the '
                 'body dismantles: the clips run on the physics tick (state_t), not the display clock.',
    'lead_silence_s': 0.8,
    'narration_text': ("Tin Knockout got two clips: a wind key that turns while a fighter rewinds, and a jab that "
                       "commits. Both run on the physics clock, not the display's: every tick, each clip is put "
                       "where the fighter's state timer says. Tests prove the timing. Whether the motion reads, "
                       "only eyes can say."),
    'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'hold',
             'show': [{'at': '0.10', 'event': 'writer types the overview; "display" is struck and corrected to '
                                               '"physics"'}],
             'remotion': {'pattern': 'BrutalistHesitantWriter', 'props': {
                 'text': 'Tin Knockout got a turning key\nand a committing jab.\nBoth run on the display clock.',
                 'triggerWords': 'display', 'replacementWords': 'physics',
                 'charMs': 10, 'mistakeRate': 2, 'hesitateBetween': 4, 'seed': SLUG,
                 'face': 'serif', 'fontSize': 112, 'lineSpacing': 2.6, 'align': 'left', 'ink': '#2b2118'}}},
    'estimated_duration_s': 14, **V})

# ---------------------------------------------------------------- B02 the game, both clips
B.append(own('B02', 'SETUP',
    'The game, both clips, their routes, what loops and what commits (TEST-REPORT "The two clips", CHANGE-BRIEF §1), '
    'with held frames from the film capture.',
    "The game: two tin toys box on wind-up springs, and every attack spends wind. Clip A, wind key cycle, is the "
    "cycle. Its route: a Sprite two D sliced into eight frames, driven by an animation player's frame track. It "
    "loops: eight keys at eight frames a second, one turn a second, while the fighter rewinds. Clip B, jab action, "
    "is the committing action. Its route: a cutout rig keyed as resource text, two named pivots, Body Pivot and "
    "Key Bob. It commits: twenty-one frames at sixty, no loop, and nothing the player presses can stop it.",
    'Two Clips, Two Routes', 'setup',
    [{'at': '0.00', 'event': 'two held frames from the film capture (scripted input): the lunge, and the key turning'},
     {'at': 'Clip A, wind', 'event': 'CLIP A card lights: route, node, authority, loops'},
     {'at': 'Clip B, jab', 'event': 'CLIP B card lights: route, nodes, authority, commits'}],
    [['a', 'Clip A, wind'], ['b', 'Clip B, jab']], 34))

# ---------------------------------------------------------------- B03 Q1: what a clip is (checked excerpt)
B.append(godot_code('B03',
    'Question 1, what a clip is: one value track of jab_action.tres (lines 22-30, BodyPivot:rotation), as text.',
    "First question: what is a clip? Here, a clip is text. Line twenty-two is a track's path: a node, Body Pivot, "
    "then a property on it, rotation. Line twenty-six holds six key times, one at each phase boundary. Line "
    "twenty-seven, each segment's easing. Line twenty-nine, the values in radians: back to minus point one, forward "
    "to point one two. Nothing checks that path when the file loads.",
    'animations/jab_action.tres', 22, 30, 'Q1 · What a Clip Is',
    [{'label': 'Who', 'value': 'keys from Tharun\'s phase table (CHANGE-BRIEF §4); .tres written by Claude Code'},
     {'label': 'Rule', 'value': 'clips are resources, never built in code at runtime (CLAUDE.md, Ownership)'}],
    [(22, 'path = node : property', 'Line twenty-two'),
     (26, 'six key times: frames 0, 3, 5, 10, 11, 21', 'Line twenty-six'),
     (27, 'outgoing easing, one per key', 'Line twenty-seven'),
     (29, 'values in radians', 'Line twenty-nine')], 30, size=30))

# ---------------------------------------------------------------- B04 Q1 result: mutation M1
B.append(own('B04', 'RESULT',
    'Why a renamed property fails silently: mutation M1 (evidence/a7/mutations/README.md, its logs; TEST-REPORT A7-5).',
    "Rename that property by two swapped letters, rotatoin, and the engine says nothing. The game ran with the "
    "rotation track inert, and no warning. Only the read-back caught it: track problems, Body Pivot has no property "
    "rotatoin. Eight of forty-eight checks failed. The structure test caught it again on the real Bolt and Rivet. A "
    "track's path is a promise the loader never checks.",
    'Q1 · A Renamed Property', 'm1',
    [{'at': '0.00', 'event': 'the M1 change: jab_action.tres track 1 path, rotation -> rotatoin'},
     {'at': 'the engine says nothing', 'event': '"What the engine said": nothing (README, verbatim)'},
     {'at': 'Only the read-back', 'event': 'FAIL lines from M1-test_jab_action_readback.log; exit 8'},
     {'at': 'The structure test', 'event': 'M1-test_a7_structure.log, exit 2'}],
    [['silent', 'the engine says nothing'], ['rb', 'Only the read-back'], ['st', 'The structure test']], 26))

# ---------------------------------------------------------------- B05 Q2: one authority (source view)
B.append(own('B05', 'MECHANISM',
    'Question 2, one authority: the rig vars and their one writer each (fighter.gd:67-73) and _apply_pose\'s writes '
    '(fighter.gd:306, 313, 315).',
    "Second question: who writes each node? Lines sixty-seven to seventy-three name one writer per rig node. Facing "
    "Pivot, the body sprite and Key Mount: apply pose. Body Pivot and Key Bob: the fighter animation player, through "
    "jab action. The key sprite's frame: the key animation player. Line three oh six is apply pose writing facing to "
    "Facing Pivot, so a positive x in the clip always means forward. Line three thirteen puts the key's anchor with "
    "no facing factor.",
    'Q2 · One Writer per Node', 'auth',
    [{'at': '0.00', 'event': 'godot/fighter/fighter.gd:67-73 and :306-315 at reading size'},
     {'at': 'Facing Pivot, the body', 'event': '_apply_pose rows highlighted (67, 69, 70, 73)'},
     {'at': 'Body Pivot and Key Bob', 'event': 'FighterAnimPlayer rows highlighted (68, 71)'},
     {'at': "The key sprite's frame", 'event': 'KeyAnimPlayer row highlighted (72)'},
     {'at': 'Line three oh six', 'event': 'line 306 highlighted, then 313'}],
    [['ap', 'Facing Pivot, the body'], ['fa', 'Body Pivot and Key Bob'], ['ka', "The key sprite's frame"],
     ['306', 'Line three oh six']], 32,
    files=[['godot/fighter/fighter.gd', 64, 73], ['godot/fighter/fighter.gd', 305, 315]]))

# ---------------------------------------------------------------- B06 Q2 result: the source scan
B.append(own('B06', 'RESULT',
    'The structure test\'s source scan (test_a7_structure.gd section A, re-run for this film on a clean copy of '
    'a5978c0) and the pose-equals-clip check; a held frame of the lunge from the film capture with its logged pose.',
    "The structure test reads every script and lists every assignment to a rig node, by function. Re-run for this "
    "film: after setup, the only writes are apply pose's Facing Pivot scale, and Key Mount's position and "
    "visibility. Body Pivot and Key Bob are never written by code, and nothing writes the key's frame. On every jab "
    "tick, the pose equals the clip's own value at the state timer: largest gap, zero.",
    'Q2 · The Source Scan', 'scan',
    [{'at': '0.00', 'event': 'test_a7_structure_60fps.log section A, verbatim (re-run)'},
     {'at': 'after setup, the only', 'event': 'per-tick writes line highlighted'},
     {'at': 'On every jab', 'event': 'B1 line: largest gap 0.00000; held frame of the lunge, x +14.00 from the log'}],
    [['after', 'after setup, the only'], ['gap', 'On every jab']], 26))

# ---------------------------------------------------------------- B07 Q3: two clocks (checked excerpt)
B.append(godot_code('B07',
    'Question 3, the two clocks: _sync_clips (fighter.gd:346-356), the jab half; both players MANUAL '
    '(fighter.gd:339).',
    "Third question: which clock? Both players are manual, line three thirty-nine: they move only when sync clips "
    "puts them somewhere. Line three forty-seven: sync clips runs at the end of step, so hitstop's early return and "
    "the pause flag, which skip step, freeze both clips. Line three fifty-one: the jab plays only in the jab state. "
    "Line three fifty-four seeks it to the state timer, clamped to its length.",
    'fighter/fighter.gd', 346, 356, 'Q3 · The Two Clocks',
    [{'label': 'Line 339', 'value': 'callback_mode_process = ANIMATION_CALLBACK_MODE_PROCESS_MANUAL (both players)'},
     {'label': 'Called', 'value': 'last in step() (line 197) and on state_changed (line 115)'}],
    [(347, 'called at the end of step(): pause and hitstop skip it', 'Line three forty-seven'),
     (351, 'jab_action only in JAB', 'Line three fifty-one'),
     (354, 'clip position = state_t, clamped', 'Line three fifty-four')], 28, size=24))

# ---------------------------------------------------------------- B08 Q3 result: hitstop hold + CLOCKS
B.append(own('B08', 'RESULT',
    'The clip frozen with state_t through hitstop in the film capture (case 2, ticks e+4..e+12, logged clip position), '
    'and Tharun\'s measured CLOCKS line (TEST-REPORT A7-9e, verbatim).',
    "In play. The jab lands on its fifth tick. For the next five ticks, hitstop holds the state timer, and the clip "
    "holds frame five with it: the logged clip position stays at point zero eight three three. Then measured by "
    "Tharun, in a window running free: the display at about one hundred twenty-nine frames a second, physics at "
    "sixty ticks, and the clip against the state timer, on two hundred seventy-nine jab ticks: largest gap, zero. "
    "The picture trails gameplay by under one tick.",
    'Q3 · One Clock, Measured', 'clocks',
    [{'at': '0.00', 'event': 'film capture, case 2: nine consecutive ticks e+4..e+12, zoomed on Bolt, each with its '
                             'logged state_t and clip position'},
     {'at': 'holds frame five', 'event': 'ticks e+5..e+10 ringed: clip position 0.0833 held'},
     {'at': 'Then measured', 'event': 'CLOCKS line (Tharun, jab_preview --loop --clocks), verbatim'}],
    [['hold', 'holds frame five'], ['meas', 'Then measured']], 32))

# ---------------------------------------------------------------- B09 Q4: phase table beside key times
B.append(own('B09', 'MECHANISM',
    'Question 4, feel in frames: CHANGE-BRIEF §4 phase table at 60 fps beside evidence/a7/jab_action_keys.md.',
    "Fourth question: feel, in frames. Tharun's phase table, at sixty frames a second: startup, frames zero to four; "
    "active, the box live, five to ten; recovery, eleven to twenty; idle on twenty-one. Beside it, each key's time "
    "in the resource: a key at every boundary. Frame three, the coil: minus six pixels. Frame five, the lunge: plus "
    "fourteen, held to ten. Frame eleven, the release. The times are stored as thirty-two-bit floats, so the "
    "read-back compares them within half a frame.",
    'Q4 · Feel in Frames', 'phase',
    [{'at': '0.00', 'event': 'CHANGE-BRIEF §4 phase rows (verbatim) beside jab_action_keys.md key rows (verbatim)'},
     {'at': 'Beside it', 'event': 'key table lights'},
     {'at': 'Frame three', 'event': 'keys 1, 2-3, 4 highlighted in turn'},
     {'at': 'The times are stored', 'event': 'float note lights'}],
    [['keys', 'Beside it'], ['f3', 'Frame three'], ['f5', 'Frame five'], ['f11', 'Frame eleven'],
     ['float', 'The times are stored']], 34,
    files=[['CHANGE-BRIEF.md', 76, 80], ['evidence/a7/jab_action_keys.md', 5, 12]]))

# ---------------------------------------------------------------- B10 Q4 result: the r0 strip
B.append(own('B10', 'RESULT',
    'The strip at each phase boundary: captures/jab_action/r0 frames 9, 10, 13, 14, 15, 20, 21, 31 (fixture, '
    'captured by Tharun) with the logged pose; Tharun\'s first look (TUNING.md, verbatim).',
    "The strip is a fixture: the real fighter alone at x two oh seven over the light stretch, the jab on frame ten, "
    "captured by Tharun at sixty. Frame thirteen, the coil. Fifteen, the box opens: the lunge, the largest move in "
    "the clip. Twenty, the last active frame, the same pose. Twenty-one, recovery begins. Thirty-one, idle. Tharun's "
    "first look, written before Claude read the strip: the fighter's whole body leans back first, then pushes "
    "forward with the punch arm already extended as part of the jab picture, holds briefly, and pulls back to the "
    "starting stance.",
    'Q4 · The Strip, r0', 'strip',
    [{'at': '0.00', 'event': 'r0 frames 9, 10, 13, 14, 15, 20, 21, 31 (fixture, held frames, zoom) with the log pose'},
     {'at': 'Frame thirteen', 'event': 'frames 13, 15, 20, 21, 31 ringed in turn'},
     {'at': "Tharun's first look", 'event': "Tharun's first look, verbatim"}],
    [['f13', 'Frame thirteen'], ['f15', 'Fifteen, the box'], ['f20', 'Twenty, the last'], ['f21', 'Twenty-one, recovery'],
     ['f31', 'Thirty-one, idle'], ['look', "Tharun's first look"]], 38))

# ---------------------------------------------------------------- B11 the sheet: generator (source view)
B.append(own('B11', 'MECHANISM',
    'The sheet\'s slicing as built: godot/tools/generate_key_sheets.gd:37-47 (Claude), the recipe from CHANGE-BRIEF §2 '
    '(Tharun).',
    "The sheet. Tharun's recipe, in Claude's generator script: eight cells of eighty-four by sixty, in one row. "
    "Line thirty-nine: cell k is the key turned k times forty-five degrees, its width scaled by the cosine, never "
    "below fifteen percent, so the edge stays legible. Line forty-four: cells three to five are mirrored, the back "
    "half of the turn. Line forty-seven blits each one, centred, into the sheet.",
    'The Sheet · Its Recipe', 'gen',
    [{'at': '0.00', 'event': 'godot/tools/generate_key_sheets.gd:37-47 at reading size'},
     {'at': 'Line thirty-nine', 'event': 'line 39 highlighted'},
     {'at': 'Line forty-four', 'event': 'lines 44-45 highlighted'},
     {'at': 'Line forty-seven', 'event': 'line 47 highlighted'}],
    [['39', 'Line thirty-nine'], ['44', 'Line forty-four'], ['47', 'Line forty-seven']], 26,
    files=[['godot/tools/generate_key_sheets.gd', 37, 47]]))

# ---------------------------------------------------------------- B12 the sheet itself
B.append(own('B12', 'RESULT',
    'The two committed sheets (godot/assets/props/key-*-sheet.png), sliced 8 x 1 with cell numbers; the cell-centre '
    'measurement (TEST-REPORT A7-9c); source and licence (ATTRIBUTION.md, SOURCES.md A7).',
    "The result: two sheets, six hundred seventy-two by sixty, eight cells by one. Cells two and six are the key "
    "edge-on, at the fifteen percent minimum. Measured, every cell is centred at x forty-one and a half or forty-two, "
    "of eighty-four, so the key does not wander. The source art is Tharun's key from assignment two, made with SDXL "
    "Turbo from his prompt, under the Stability AI Non-Commercial Research Community License. Each sheet is a "
    "derivative, made by resizing and mirroring only.",
    'The Sheet · Sliced 8 × 1', 'sheet',
    [{'at': '0.00', 'event': 'key-bolt-sheet.png and key-rivet-sheet.png, nearest-neighbour enlarged, grid 8 x 1'},
     {'at': 'Cells two and six', 'event': 'cells 2 and 6 ringed'},
     {'at': 'Measured, every cell', 'event': 'A7-9c measurement line'},
     {'at': 'The source art', 'event': 'ATTRIBUTION.md source and licence'}],
    [['edge', 'Cells two and six'], ['meas', 'Measured, every cell'], ['src', 'The source art']], 32))

# ---------------------------------------------------------------- B13 the frame track (source view)
B.append(own('B13', 'MECHANISM',
    'The frame track that reads the sheet: godot/animations/wind_key_cycle.tres:3-19.',
    "The frame track that reads the sheet. Line six: loop mode one, linear. Line seven: a step of one eighth of a "
    "second. Line eleven: the path ends at key sprite, colon, frame. Line seventeen: update one, discrete. Frame is "
    "an integer, so on continuous updates the track would sweep through every cell in between. Line fifteen: eight "
    "keys at k over eight, and none at the length, one second: frame zero is not repeated at the seam.",
    'The Cycle · Its Frame Track', 'track',
    [{'at': '0.00', 'event': 'godot/animations/wind_key_cycle.tres:3-19 at reading size'},
     {'at': 'Line six', 'event': 'lines 6-7 highlighted'},
     {'at': 'Line eleven', 'event': 'line 11 highlighted'},
     {'at': 'Line seventeen', 'event': 'line 17 highlighted; CHANGE-BRIEF §11 answer 2'},
     {'at': 'Line fifteen', 'event': 'lines 5 and 15 highlighted: no key at length'}],
    [['6', 'Line six'], ['11', 'Line eleven'], ['17', 'Line seventeen'], ['15', 'Line fifteen']], 30,
    files=[['godot/animations/wind_key_cycle.tres', 3, 19]]))

# ---------------------------------------------------------------- B14 the cycle turning (fixture capture)
B.append(own('B14', 'RESULT',
    'The key turning in REWIND: Movie Maker capture of godot/previews/key_cycle_preview.tscn (FIXTURE) made for this '
    'film on the isolated copy, with its per-tick log; Tharun\'s seam check (TEST-REPORT A7-9a, verbatim).',
    "In motion, a fixture made for this film: the real fighter held in rewind, his wind topped back to fifty every "
    "tick, so the key never reaches full and turns without stopping, one turn a second. Each cell holds seven or "
    "eight ticks. Watch the wrap from seven to zero, at every turn. Tharun's check, in his words: the key rotation "
    "stays continuous across the wrap without a visible jump at the seam.",
    'The Cycle · Turning', 'cycle',
    [{'at': '0.00', 'event': 'key_cycle_preview capture at real speed, zoom on the key, readout from its log'},
     {'at': 'Watch the wrap', 'event': 'labelled 0.25x replay of a wrap'},
     {'at': "Tharun's check", 'event': "Tharun's seam check, verbatim"}],
    [['wrap', 'Watch the wrap'], ['check', "Tharun's check"]], 26))

# ---------------------------------------------------------------- B15 revision 1: reading, change, prediction
B.append(own('B15', 'MECHANISM',
    'jab_action revision 1: Claude\'s reading of r0 (TUNING.md), the r0 log frames 22-31, the one change (git '
    '8a9dbed, jab_action.tres transitions) and Claude\'s prediction written before it.',
    "Two revisions, each predicted before the change. Revision one came from Claude's reading of r0: the ease-out "
    "from frame eleven covers most of the distance by frame twenty-six. Frames twenty-seven to thirty barely move, "
    "then frame thirty-one swaps to the idle image. Stop, then snap. The one change, approved by Tharun: key four's "
    "outgoing transition, from point five, ease-out, to one, linear. The prediction: frames twenty-two to thirty "
    "step evenly, seven point two down to point eight pixels, still moving on frame thirty.",
    'Revision 1 · Claude\'s Reading', 'rev1',
    [{'at': '0.00', 'event': "Claude's reading of r0 (TUNING.md, verbatim) beside logs/jab_preview_r0.log frames 22-31"},
     {'at': 'The one change', 'event': 'git 8a9dbed: transitions line, before and after'},
     {'at': 'The prediction', 'event': "Claude's prediction, verbatim"}],
    [['chg', 'The one change'], ['pred', 'The prediction']], 34,
    files=[['godot/animations/jab_action.tres', 15, 15]]))

# ---------------------------------------------------------------- B16 revision 1 result
B.append(own('B16', 'RESULT',
    'r1 (captures/jab_action/r1_recovery_sheet.png, fixture, Tharun), Claude\'s comparison, and Tharun\'s revision 1 '
    'verdict and observation in the running game (TUNING.md, verbatim).',
    "r1, captured by Tharun with the same fixture. The log shows exactly those values, and the frames the change "
    "should not touch are byte-identical to r0. Matched. Tharun's verdict, in the running game: Keep. The return "
    "carries into the stance. And in the same note he opened revision two: the retraction pop is still noticeable, "
    "especially up close.",
    'Revision 1 · Result', 'res1',
    [{'at': '0.00', 'event': 'r1_recovery_sheet.png (fixture, held frames)'},
     {'at': 'The log shows', 'event': "Claude's comparison rows: yes"},
     {'at': "Tharun's verdict", 'event': "Tharun's verdict, verbatim: Keep"},
     {'at': 'he opened revision', 'event': "Tharun's 'Opens revision 2', verbatim"}],
    [['cmp', 'The log shows'], ['verdict', "Tharun's verdict"], ['open', 'he opened revision']], 24))

# ---------------------------------------------------------------- B17 revision 2: Tharun's observation, change, prediction
B.append(own('B17', 'MECHANISM',
    'jab_action revision 2: opened by Tharun\'s play observation; where the pop comes from; the change (git a1d6072, '
    'jab_action.tres values lines 17, 29, 41) and Claude\'s prediction (TUNING.md).',
    "Revision two came from Tharun's play, not from Claude's reading. Claude's r0 reading had not flagged it. Claude "
    "traced the pop to clip frames ten to eleven: in one frame the body drops from fourteen pixels to eight, and the "
    "helmet moves minus twenty-three window pixels, against about two and a half per frame through the rest of the "
    "recovery. The change, approved by Tharun: the recovery-onset pose, plus twelve pixels, point one radians, minus "
    "one point seven five. The prediction: a step of about minus eight, then steps of about four point three.",
    'Revision 2 · Tharun\'s Observation', 'rev2',
    [{'at': '0.00', 'event': "Tharun's play observation, verbatim"},
     {'at': 'Claude traced the pop', 'event': "Claude's account: frames 10 -> 11, -23 window px (TUNING.md)"},
     {'at': 'The change, approved', 'event': 'git a1d6072: the three values lines, before and after'},
     {'at': 'The prediction', 'event': "Claude's prediction, verbatim"}],
    [['trace', 'Claude traced the pop'], ['chg', 'The change, approved'], ['pred', 'The prediction']], 36,
    files=[['godot/animations/jab_action.tres', 17, 17], ['godot/animations/jab_action.tres', 29, 29],
           ['godot/animations/jab_action.tres', 41, 41]]))

# ---------------------------------------------------------------- B18 revision 2 result
B.append(own('B18', 'RESULT',
    'r1 vs r2 (captures/jab_action/r1_vs_r2_sheet.png, fixture, Tharun), Claude\'s comparison (TUNING.md), Tharun\'s '
    'revision 2 observation in the running game (TUNING.md, verbatim) and the recorded verdict (TEST-REPORT A7-8).',
    "r2, beside r1. Frame twenty-one's helmet step: minus seven point seven. Matched. The later steps: three point "
    "four to four point three, mean three point nine. Claude overestimated by about ten percent: partly. The "
    "predicted cost arrived too: the step into the idle picture on frame thirty-one grew to minus thirty point one. "
    "Tharun, up close against Rivet: the retraction feels less jarring and less like a sudden snap-back than before. "
    "Recorded verdict: keep.",
    'Revision 2 · Result', 'res2',
    [{'at': '0.00', 'event': 'r1_vs_r2_sheet.png, frames 20, 21, 26, 30, 31 (fixture)'},
     {'at': "Frame twenty-one's", 'event': 'frame 21 column ringed; comparison row: yes'},
     {'at': 'The later steps', 'event': 'comparison row: partly'},
     {'at': 'The predicted cost', 'event': 'comparison row: frame 31 -30.1'},
     {'at': 'Tharun, up close', 'event': "Tharun's observation, verbatim; Verdict (Tharun): Keep (A7-8)"}],
    [['f21', "Frame twenty-one's"], ['steps', 'The later steps'], ['cost', 'The predicted cost'],
     ['tharun', 'Tharun, up close']], 32))

# ---------------------------------------------------------------- B19 in play: whiff and land
B.append(own('B19', 'RESULT',
    'jab_action in the running game: whiff and landed hit with hitstop. Movie Maker capture made for this film, '
    'scripted input, isolated copy of a5978c0 (capture/play-4k60.mp4), readout from its log.',
    "Now the running game: a capture made for this film, at sixty frames a second, so every tick is drawn. Bolt's "
    "keys go through the real input path. Rivet follows a stand-in plan, the edge test's method, and between cases "
    "their positions are set. First, a whiff at ninety pixels, at half speed: coil, lunge, hold, return. Then a jab "
    "at seventy, at quarter speed: it lands on its fifth tick, and both toys freeze for five ticks of hitstop.",
    'Both Clips in Play · The Jab', 'play1',
    [{'at': '0.00', 'event': 'capture from FIGHT through cases 1-2 at real speed (every 2nd tick), zoom, readout'},
     {'at': 'First, a whiff', 'event': 'labelled 0.5x replay of case 1'},
     {'at': 'Then a jab', 'event': 'labelled 0.25x replay of case 2'}],
    [['whiff', 'First, a whiff'], ['land', 'Then a jab']], 28))

# ---------------------------------------------------------------- B20 in play: interrupts + rewind
B.append(own('B20', 'RESULT',
    'Interrupts in startup (e+3), active (e+7) and recovery (e+15) by Rivet\'s cutlass, and the key turning in REWIND '
    'then holding at full wind; same capture.',
    "Now the interrupts, timed as the edge test times them: Rivet's cutlass lands on its ninth tick, so it is "
    "requested nine ticks before the hit. In startup, on the jab's third tick. In active, on the seventh. In "
    "recovery, on the fifteenth. Each time, jab to hurt on the hit tick, and the rig snaps to rest; no pose is left "
    "hanging. Last, Bolt holds S at forty wind. The key turns, six clicks to full wind, a turn and a half, then "
    "holds, and goes back to frame zero on release.",
    'Both Clips in Play · Interrupts and Rewind', 'play2',
    [{'at': '0.00', 'event': 'cases 3-5 side by side, synchronised on the jab start, 0.25x, looped; readout per case'},
     {'at': 'In startup', 'event': 'case 3 panel ringed'}, {'at': 'In active', 'event': 'case 4 panel ringed'},
     {'at': 'In recovery', 'event': 'case 5 panel ringed'}, {'at': 'Each time', 'event': 'all three ringed'},
     {'at': 'Last, Bolt holds', 'event': 'case 6: REWIND, zoom on the key, wind and key frame from the log'}],
    [['start', 'In startup'], ['act', 'In active'], ['rec', 'In recovery'], ['each', 'Each time'],
     ['rew', 'Last, Bolt holds']], 34))

# ---------------------------------------------------------------- B21 tests: read-backs, mutations, limits
B.append(own('B21', 'TESTS',
    'What the read-backs proved (counts re-run for this film on a clean copy of a5978c0), the mutations that failed '
    'them (TEST-REPORT A7-4, A7-5) and what no headless run can show (CLAUDE.md Headless facts).',
    "What the tests proved, re-run for this film on a clean copy. The key cycle's read-back: twenty-six checks, none "
    "failed. The jab's: fifty-eight. Structure and state: fifty-seven, at sixty and at thirty. Edges: seventy. Pins: "
    "forty-nine. Then the mutations, each in its own worktree. M one, the renamed property: exits eight and two. M "
    "two, the cycle's loop mode set to none: two. M three, a frame key of eight, past the sheet: five. The engine "
    "printed a plain error there, which the wrapper does not fail on. M four, an empty import cache, passed, as "
    "expected, because nothing here is imported. And the limit: a headless run draws nothing, so whether the motion "
    "reads is not observable there.",
    'What the Tests Proved', 'tests',
    [{'at': '0.00', 'event': 'counts from the re-run logs (evidence/runs/tests-a5978c0/)'},
     {'at': 'Then the mutations', 'event': 'mutation table M1-M4 (TEST-REPORT A7-5)'},
     {'at': 'M four, an empty', 'event': 'M4 row lights: passed, explained'},
     {'at': 'And the limit', 'event': 'CLAUDE.md headless fact, verbatim'}],
    [['mut', 'Then the mutations'], ['m4', 'M four, an empty'], ['limit', 'And the limit']], 44))

# ---------------------------------------------------------------- B22 agent mistakes, the seam bug
B.append(own('B22', 'VERDICT',
    'Agent mistakes caught (TEST-REPORT A7-11), including the seam bug (A7-9a, evidence/a7/seam/): the structure test '
    'before and after the fix.',
    "Agent mistakes, caught. Claude's expectations in the pins were wrong twice: the defender's hitstop, and empty's "
    "ninety-seven ticks. The structure test's first draft flagged a read as a write. The edge test expected idle "
    "before a hit on tick twenty-one; the jab ends and the hit lands on the same tick. And the biggest: Claude's sync "
    "clips sought the key backwards across the wrap. The fixture's first log showed seven, one, zero at every wrap "
    "after the first, while the suite was green: the structure test stopped at one and a half turns. The fix moves "
    "forward. A six-turn regression failed three checks before it, and none after.",
    'Claude, Checked', 'mistakes',
    [{'at': '0.00', 'event': 'A7-11 mistakes, each with its record'},
     {'at': 'And the biggest', 'event': 'seam bug card: cause, why the suite was green'},
     {'at': 'A six-turn regression', 'event': 'structure B7 before (3 failed) and after (0 failed), log lines'}],
    [['seam', 'And the biggest'], ['reg', 'A six-turn regression']], 42))

# ---------------------------------------------------------------- B23 Tharun overruled Claude; his checks
B.append(own('B23', 'VERDICT',
    'Claude\'s reading Tharun overruled (TEST-REPORT A7-9f) and Tharun\'s human checks (A7-9b, c, d) and his own words '
    '(FRICTIONAL.md "In my words"), all verbatim.',
    "Where Tharun's eyes overruled Claude's reading. Claude read r0 as a stall, then a snap. Tharun, in play, found "
    "the retraction pop on frame twenty-one, which Claude's reading did not flag; his observation drove revision two. "
    "His checks, in his words: startup, hold, and return read as distinct moments. Both clips remain readable over "
    "both light and dark backgrounds, with clear enough contrast to follow the motion. And in his own account: "
    "writing my first look before reading the strip taught me how easy it is to project motion that isn't actually "
    "drawn.",
    'Claude, Overruled', 'against',
    [{'at': '0.00', 'event': 'A7-9f table rows, verbatim'},
     {'at': 'His checks', 'event': 'A7-9b, A7-9c, A7-9d HUMAN CHECK quotes, verbatim'},
     {'at': 'in his own account', 'event': 'FRICTIONAL.md In my words, verbatim'}],
    [['checks', 'His checks'], ['words', 'in his own account']], 38))

# ---------------------------------------------------------------- B24 credits
B.append(own('B24', 'CREDITS',
    'Human and AI contributions as SOURCES.md "Who did what (A7)", shown verbatim; the brief\'s drafting note '
    '(SOURCES.md A7, verbatim); sheet source and licence.',
    "Who did what, as SOURCES dot m d records it. Tharun chose both clips, the routes, the sixty-frame phase table "
    "with its poses and easing, the eight-frame cycle and its sheet recipe, the authority layout and the interrupt "
    "rules, and wrote the two dated revisions. He swapped in the wrapper, approved the step five plan and the seam "
    "fix, ran every capture, wrote the first look and both verdicts, and did the human checks and the two-clocks "
    "measurement. Claude Code wrote the facts sheet and probes, the sheet generator, both clips, the tests, the "
    "wiring and both previews; ran the mutations; found and fixed the seam bug, with approval; read the strips and "
    "wrote the predictions; and drafted the docs. The brief was drafted and refined across four review rounds with "
    "Claude Code in the terminal.",
    'Who Did What (A7)', 'credits',
    [{'at': '0.00', 'event': 'SOURCES.md "Who did what (A7)" verbatim, two columns'},
     {'at': 'Claude Code wrote', 'event': 'Claude column lights'},
     {'at': 'The brief was drafted', 'event': 'drafting note and sheet licence (SOURCES.md A7) light'}],
    [['claude', 'Claude Code wrote'], ['brief', 'The brief was drafted']], 48))

# ---------------------------------------------------------------- B25 verdict
B.append({
    'beat_id': 'B25', 'act': 'VERDICT',
    'role_note': 'VERDICT — checked by numbers / by eye, uncertain (A7-12), one next step; revision shown.',
    'narration_text': (
        f"The verdict, at revision {REV_SAID}. Checked by numbers: both read-backs, structure, edges and pins at their "
        "counts; three mutations caught, and the fourth honestly not, because nothing here is imported. Checked by "
        "eye, by Tharun: the seam, the jab in play, registration and both backgrounds; two revisions, both kept. "
        "Still uncertain: the jab picture appears five frames before the hitbox, from the art per state, outside the "
        "clips; mashing J shows the idle image for one frame between jabs; and in the game a rewind fills within two "
        "and a half turns, so five wraps were watched in the fixture. One next step: a startup image, so the arm stays "
        "back until the box opens."),
    'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'hold',
             'show': [{'at': '0.10', 'event': 'verdict artifact lines land'}],
             'remotion': {'pattern': 'ClaudeVerdictArtifact', 'props': {
                 'artifactTitle': 'walker-tinknockout-tharun-m · Assignment 7',
                 'artifactHeading': 'VERDICT · revision ' + REV,
                 'brandLabel': 'WALKER · GODOT 4.7.2 · FORWARD+',
                 'artifactLines': [
                     'CHECKED — numbers: read-backs 26/0 · 58/0, structure 57/0',
                     '  edges 70/0 · pins 49/0 · mutations M1–M3 caught, M4 passed',
                     'CHECKED — by eye (Tharun): seam, jab in play, registration',
                     '  both backgrounds · revisions 1 and 2: Keep, Keep',
                     'UNCERTAIN  jab picture 5 frames before the hitbox (art per state)',
                     'UNCERTAIN  1 idle frame between mashed jabs · rewind fills ≤ 2.5 turns',
                     'NEXT  a startup image for the jab (drawing), then a new strip']}}},
    'estimated_duration_s': 36, **V})

# ---------------------------------------------------------------- B26 your turn
B.append({
    'beat_id': 'B26', 'act': 'YOUR_TURN',
    'role_note': 'YOUR TURN — a useful Walker prompt read aloud, one bounded change + prediction first, sheet source, '
                 'revision; Liam signs off before the locked outro.',
    'narration_text': (
        "Your turn. Here is a useful Walker prompt. Please use Walker to move jab action's coil key from frame three "
        "to frame two, and before you capture anything, tell me what you predict the strip will show on frames twelve "
        "to fifteen. Write the prediction first; a strip only means something against one. Then a person looks, in "
        "play. The key sheets derive from SDXL Turbo art under a non-commercial licence. This voice is Kokoro text to "
        f"speech. The source shown is revision {REV_SAID}. Liam, in for Bear."),
    'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'type-on',
             'show': [{'at': '0.10', 'event': 'composer types the suggested prompt; prediction rule and credits land'}],
             'remotion': {'pattern': 'ClaudeComposerAsk', 'props': {
                 'greeting': 'Your turn.',
                 'topic': 'WALKER · YOUR TURN',
                 'segment': 'one bounded change',
                 'command': ("Please use Walker to move jab_action's coil key from frame 3 to frame 2, and before you "
                             "capture anything, tell me what you predict the strip will show on frames 12 to 15."),
                 'runningText': 'over to you…',
                 'output': [
                     '■ prediction first, then the strip, then a person looks in play',
                     '■ the read-backs still need a key at every phase boundary',
                     '  SHEETS   derived from SDXL-Turbo key art · non-commercial licence',
                     '  SOURCE   game revision ' + REV,
                     '  VOICE    Liam — Kokoro am_onyx, AI text-to-speech']}}},
    'estimated_duration_s': 30, **V})

# ---------------------------------------------------------------- B27 outro
B.append({
    'beat_id': 'B27', 'act': 'OUTRO', 'kind': 'outro_voice',
    'role_note': 'OUTRO-LOCK — exact title, @NikBearBrown, slug-seeded mascot. Spoken, never scored; 1.0 s silent tail.',
    'narration_text': f'{TITLE}. At Nik Bear Brown.',
    'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'hold',
             'show': [{'at': '0.10', 'event': 'locked title card'}],
             'remotion': {'pattern': 'ClaudeTitleOutro', 'props': {'title': TITLE, 'slug': SLUG}}},
    'estimated_duration_s': 5, **V})

meta = {
    'title': TITLE, 'slug': SLUG,
    'topic': 'WALKER · GAME DEVELOPMENT · ASSIGNMENT 7', 'kind': 'godot-gamedev', 'playlist': 'Walker',
    'brand': 'claude-liam', 'audience': 'CSYE 7270 reviewers and Walker users',
    'register': 'Teardown', 'engine': 'kokoro', 'voice': 'am_onyx', 'voice_kokoro': 'am_onyx',
    'palette': 'claude', 'style_preset': 'claude', 'aspect_ratio': '16:9', 'captions': False,
    'channel_title': '@NikBearBrown', 'channel': '@NikBearBrown',
    'presenter': 'Liam (in for Bear)', 'persona': 'Liam (in for Bear)',
    'episode_id': 'walker-tinknockout-tharun-m-a7', 'mode': 'walker',
    'game': {'name': 'walker-tinknockout-tharun-m', 'revision': subprocess.run(
                 ['git', '-C', str(REPO), 'rev-parse', REV], capture_output=True, text=True).stdout.strip(),
             'docs_revision': REV, 'godot_path': 'godot',
             'engine_version': '4.7.2.stable.official.ed1daf0bf', 'renderer': 'Forward+ (Vulkan/MoltenVK)'},
    'student': 'Tharun Maheswararao', 'course': 'CSYE 7270 Fall 2026 · Assignment 7',
    'note': ('Walker-mode godot-gamedev film of the A7 animation clips. Game source and docs shown: a5978c0. The jab '
             'strips r0-r2 are fixture captures (godot/previews/jab_preview.tscn) taken by Tharun; two Movie Maker '
             'captures were made for this film on an isolated copy of a5978c0: the game with scripted input '
             '(Bolt through the real input path, Rivet a stand-in plan, positions set between cases) and the '
             'key_cycle_preview fixture. B00 is an illustrative reconstruction; code views are labelled '
             'reconstructions / source views.'),
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
        if 'cue_times' in o.get('shot', {}):
            b['shot']['cue_times'] = o['shot']['cue_times']
    ro, rn = (o or {}).get('shot', {}).get('remotion') or {}, b['shot'].get('remotion') or {}
    if ro.get('rendered') and rn:
        strip = lambda d: {k: v for k, v in d.get('props', {}).items() if k not in ('durationSeconds', 'cues')}
        if ro.get('pattern') == rn.get('pattern') and strip(ro) == strip(rn):
            rn['rendered'] = ro['rendered']
            if 'durationSeconds' in ro['props']:
                rn['props']['durationSeconds'] = ro['props']['durationSeconds']
            if 'cues' in ro['props']:
                rn['props']['cues'] = ro['props']['cues']
p.write_text(json.dumps({'metadata': meta, 'beats': B}, indent=1, ensure_ascii=False) + '\n')
print('wrote', p, len(B), 'beats', sum(len(b.get('narration_text', '').split()) for b in B), 'words')
