#!/usr/bin/env python3
"""Author beat_sheet.json for the Tin Knockout Assignment 3 props film (walker mode).

Game source shown: commit 1d93dcb. Docs/evidence read from the working tree at fd99467
(docs-only commits 0bc2b4d and fd99467 after 1d93dcb; godot/, assets/, tools/ unchanged,
asserted below). Every excerpt is read from the frozen files so displayed code is verbatim.
Re-running keeps measured audio fields for beats whose narration did not change.
"""
import json, subprocess
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
GAME = REPO / 'godot'
SLUG = 'claude-liam-walker-tinknockout-tharun-m-a3-props'
TITLE = 'Tin Knockout, Three Props in Blender'
REV = '1d93dcb'
DOCS = 'fd99467'

d = subprocess.run(['git', '-C', str(REPO), 'diff', '--stat', REV, 'HEAD', '--', 'godot', 'assets', 'tools'],
                   capture_output=True, text=True, check=True).stdout.strip()
assert d == '', 'game source differs from ' + REV + ':\n' + d
d = subprocess.run(['git', '-C', str(REPO), 'status', '--porcelain', '--', 'godot', 'assets', 'tools', 'evidence'],
                   capture_output=True, text=True, check=True).stdout.strip()
assert d == '', 'uncommitted changes in game source/evidence:\n' + d


def lines(path, a, b, root=REPO):
    return '\n'.join((root / path).read_text().splitlines()[a - 1:b])


V = {'engine': 'kokoro', 'voice': 'am_onyx'}


def own(bid, act, role, narration, title, kind, show, anchors, est, **panel):
    """A composite of real files / recorded output, laid out by make_media.py (typed STILL like
    the A2 reel's composites; GATE T is run on its designed text by selfcheck.py with the real
    images masked)."""
    return {'beat_id': bid, 'act': act, 'role_note': role, 'narration_text': narration,
            'shot': {'type': 'STILL', 'source': 'own', 'motion': 'hold', 'treatment': 'none',
                     'evidence_media': f'media/{bid}.mp4',
                     'show': show, 'anchors': anchors,
                     'panel': dict(kind=kind, title=title, **panel),
                     'note': 'Composite of real files and recorded output, built by _tools/make_media.py; '
                             'labels name the provenance of every embedded image.'},
            'estimated_duration_s': est, **V}


def blender_code(bid, role, narration, path, a, b, title, notes, cues, est, caption):
    show = [{'at': '0.00', 'event': f'{path}:{a}-{b} at reading size'}] + \
           [{'at': ph, 'event': f'line {ln} highlighted: {lab}'} for ln, lab, ph in cues]
    return own(bid, 'MECHANISM', role, narration, title, 'blender_code', show,
               [[str(ln), ph] for ln, _, ph in cues], est,
               path=path, start_line=a, end_line=b, code=lines(path, a, b),
               notes=notes, cues=[[ln, lab] for ln, lab, _ in cues], caption=caption)


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
        "Merhaba, this is Liam, in for Bear. Today we take apart assignment three of Tin Knockout, Tharun "
        "Maheswararao's game about tin wind-up toys boxing in an empty goldfish bowl. This time the game gets three "
        "3D props, built in Blender and checked in Godot. The prompt on screen is an illustrative reconstruction, "
        "not a saved transcript."),
    'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'type-on',
             'show': [{'at': '0.10', 'event': 'composer types the reconstructed Walker ask; output lines land'}],
             'remotion': {'pattern': 'ClaudeComposerAsk', 'props': {
                 'greeting': 'Merhaba, Liam',
                 'topic': 'WALKER · GAME DEVELOPMENT · ASSIGNMENT 3',
                 'segment': 'walker-tinknockout-tharun-m',
                 'command': ('Please use Walker to convert my game design document about tin wind-up toys boxing in '
                             'an empty goldfish bowl into three 3D props for my Godot game: a sunken-castle ornament, '
                             'a spare winding key and a tin toy box, sized against Bolt at 1.80 m.'),
                 'runningText': 'reading the brief…',
                 'output': [
                     '■ walker-tinknockout-tharun-m  ·  Godot 4.7.2  ·  Blender 5.2.2  ·  ' + REV,
                     '  castle   1.80 × 0.82 × 2.30 m  ·  156 tris  ·  Blender MCP',
                     '  windkey  0.60 × 0.14 × 0.70 m  ·  192 tris  ·  Blender MCP',
                     '  toybox   1.26 × 0.76 × 0.75 m  ·   48 tris  ·  script route',
                     '  RECONSTRUCTED PROMPT — illustrative, not a transcript']}}},
    'estimated_duration_s': 22, **V})

# ---------------------------------------------------------------- B01 hesitant writer
B.append({
    'beat_id': 'B01', 'act': 'BLUF',
    'role_note': ('walker B01 — what was built and what the film explains. The correction is the misconception the '
                  'body dismantles: a headless check proves measurements, not looks.'),
    'lead_silence_s': 0.8,
    'narration_text': (
        "Tin Knockout got three 3D props: a castle, a key and a toy box. The headless check proves they measure "
        "right. Whether they look right took a person, and this film shows both."),
    'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'hold',
             'show': [{'at': '0.10', 'event': 'writer types the overview; "look right" is struck and corrected to "measure right"'}],
             'remotion': {'pattern': 'BrutalistHesitantWriter', 'props': {
                 'text': 'Tin Knockout got three 3D props:\na castle, a key and a toy box.\nThe check proves they look right.',
                 'triggerWords': 'look',
                 'replacementWords': 'measure',
                 'charMs': 10, 'mistakeRate': 2, 'hesitateBetween': 4,
                 'seed': SLUG, 'face': 'serif', 'fontSize': 108, 'lineSpacing': 2.6, 'align': 'left',
                 'ink': '#2b2118'}}},
    'estimated_duration_s': 11, **V})

# ---------------------------------------------------------------- B02 assets
B.append(own(
    'B02', 'ASSETS', 'The game, the three assets, their jobs and sizes at character scale, over the real engine render.',
    ("Here is the real engine render of the prop room, all three props on its floor. Everything is sized against "
     "Bolt, one point eight metres tall. The castle is the sunken-castle ornament, the landmark that says goldfish "
     "bowl, at two point three metres. The windkey is a spare brass winding key, a collectible that would refill "
     "Bolt's spring. The toy box is where weapon pickups would come from. Its lid sits at Bolt's waist."),
    'Three Props, Each With a Job', 'assets',
    [{'at': '0.00', 'event': 'evidence/godot/prop_room.png (real engine render) with the concept line'},
     {'at': 'Bolt, one point eight', 'event': 'scale rule: Bolt = 1.80 m'},
     {'at': 'The castle is', 'event': 'castle card lights: environment · 1.80 × 0.82 × 2.30 m · why'},
     {'at': 'The windkey is', 'event': 'windkey card lights: collectible · 0.60 × 0.14 × 0.70 m · why'},
     {'at': 'The toy box is', 'event': 'toybox card lights: weapon-pickup prop · 1.26 × 0.76 × 0.75 m · why'}],
    [['bolt', 'Bolt, one point eight'], ['castle', 'The castle is'], ['windkey', 'The windkey is'],
     ['toybox', 'The toy box is']], 30))

# ---------------------------------------------------------------- B03 brief first
B.append(own(
    'B03', 'BRIEF', 'The A3 brief (3ef263b) committed before any building; what it fixes; its predicted failures.',
    ("The brief came first. Commit three e f two six three adds it before the first build commit. Tharun chose the "
     "three assets and the scale. Claude drafted the numbers, colours and failure cases, and Tharun accepted them "
     "unchanged. It fixes what the checks test later: size within one centimetre, the base at zero, triangle "
     "budgets, and which way the front faces. And it predicts seven ways this could go wrong."),
    'The Brief Came First', 'brief',
    [{'at': '0.00', 'event': 'git log of the A3 commits, oldest first'},
     {'at': 'Commit three', 'event': '3ef263b highlighted, above bec93b5 (first build commit)'},
     {'at': 'Tharun chose', 'event': 'authorship line from the brief header'},
     {'at': 'It fixes what', 'event': 'A3.1 ground rules appear'},
     {'at': 'And it predicts', 'event': 'A3.3 predicted failures F1–F7 appear'}],
    [['log', 'Commit three'], ['author', 'Tharun chose'], ['rules', 'It fixes what'], ['fails', 'And it predicts']],
    28))

# ---------------------------------------------------------------- B04 setup
B.append(own(
    'B04', 'SETUP', "Setup frictions from FRICTIONAL.md (A3), with the student's own connected screenshot.",
    ("Setup took three fixes, all logged. The chapter's claude m c p add line failed: dash e takes several values, so "
     "it swallowed the server name. Install add-on failed until Blender had been opened once. Enabling the add-on "
     "needed a full Blender restart. Then this, Tharun's own screenshot: connected on port nine eight seven six, "
     "which Claude found bound to one two seven dot zero dot zero dot one only. Even so, the first get scene info "
     "call said, could not connect to Blender. Four minutes later, it worked."),
    'Setup: Three Fixes, Then a Retry', 'setup',
    [{'at': '0.00', 'event': "student's own screenshot 01 (MCP connected) at left; fix list at right"},
     {'at': "The chapter's", 'event': 'fix 1: claude mcp add -e swallowed the name'},
     {'at': 'Install add-on', 'event': 'fix 2: install-addon needed Blender opened once'},
     {'at': 'Enabling the add-on', 'event': 'fix 3: full restart'},
     {'at': 'Then this', 'event': 'ring on "Connected on port 9876"; 127.0.0.1 only'},
     {'at': 'Even so', 'event': 'first get_scene_info: "Could not connect to Blender"; worked 4 min later'}],
    [['f1', "The chapter's"], ['f2', 'Install add-on'], ['f3', 'Enabling the add-on'], ['shot', 'Then this'],
     ['retry', 'Even so']], 34))

# ---------------------------------------------------------------- B05 window
B.append(own(
    'B05', 'WINDOW', "The student's Learn-the-window screenshot: Scale 1.000 but 2 m dimensions -> A3-F1.",
    ("Tharun's own screenshot, from learning the window. The default cube reads scale one, but its dimensions are "
     "two metres on every side. Claude pointed that out, and it became predicted failure F one: wrong size by a "
     "factor of two. Scale one does not mean one metre."),
    'Learning the Window: the 2 m Cube', 'window',
    [{'at': '0.00', 'event': "student's own screenshot 02"},
     {'at': 'reads scale one', 'event': 'ring on Scale 1.000, zoomed'},
     {'at': 'but its dimensions', 'event': 'ring moves to Dimensions 2 m'},
     {'at': 'Claude pointed', 'event': 'A3-F1 card'}],
    [['scale', 'reads scale one'], ['dims', 'but its dimensions'], ['f1', 'Claude pointed']], 17))

# ---------------------------------------------------------------- B06 the real castle prompt
B.append(own(
    'B06', 'PROMPT', 'The real castle prompt the student pasted, verbatim, from the castle session transcript.',
    ("This is the real prompt Tharun pasted for the castle, word for word. It points Claude at the brief. It asks "
     "for get scene info and a proposal before any building. Then one execute blender code call per part, with a "
     "scene check after each. It ends with the look tool, the triangle count, a list of asset libraries not to "
     "touch, and one more request: say what you could not verify."),
    'The Prompt Tharun Pasted', 'prompt',
    [{'at': '0.00', 'event': 'the verbatim prompt as pasted (line breaks kept)'},
     {'at': 'It points Claude', 'event': 'line: Read CHANGE-BRIEF.md first'},
     {'at': 'It asks', 'event': 'lines: get_scene_info, propose the steps, do not build yet'},
     {'at': 'Then one', 'event': 'lines: one execute_blender_code call per object, get_scene_info after each'},
     {'at': 'It ends', 'event': 'lines: look tool, triangle count, banned libraries'},
     {'at': 'one more request', 'event': 'line: Say what you could not verify'}],
    [['brief', 'It points Claude'], ['propose', 'It asks'], ['calls', 'Then one'], ['end', 'It ends'],
     ['verify', 'one more request']], 27))

# ---------------------------------------------------------------- B07/B08 castle call 1 -> look tool
CASTLE_CAP = (f'Source file, verbatim · tools/blender/build_castle.py at {REV} · the execute_blender_code bodies the '
              'MCP session ran in Tharun\'s live Blender, copied in order · not an editor recording')
B.append(blender_code(
    'B07', 'Code: build_castle.py call 1, the keep — size=1.0 cube, scale, apply, flat pink.',
    ("What it built, one call per part, copied into build castle dot p y. Call one, the keep. Line forty-seven "
     "adds a cube of size one, not the default two, centred at height zero point seven, so its base sits on zero. "
     "Line fifty scales it to the brief's size, and line fifty-one applies that scale, so the object goes back to "
     "scale one. Line fifty-two gives it the faded aquarium pink."),
    'tools/blender/build_castle.py', 47, 52, 'Castle, Call 1: the Keep',
    [['Brief (A3.2)', 'keep: cube 1.20 × 0.80 × 1.40 m\ncolour #D98BA0'],
     ['Default cube', "Blender's default cube is 2 m\n(screenshot 02 · A3-F1)"],
     ['Route', 'Blender MCP · execute_blender_code\ncall 1 of 8 (calls 0–7)']],
    [(47, 'size=1.0 cube, centred at z 0.70', 'Line forty-seven'),
     (50, 'scale to 1.20 × 0.80 × 1.40', 'Line fifty scales'),
     (51, 'apply: the mesh carries the size, scale back to 1', 'line fifty-one'),
     (52, 'flat material castle_pink #D98BA0', 'Line fifty-two')], 25, CASTLE_CAP))

B.append(own(
    'B08', 'RESULT', "Result of B07: the MCP look tool's real four-view image from the student's live session.",
    ("And this is what the M C P's look tool returned from Tharun's live Blender session: four views of the "
     "finished castle. The pink keep, two twelve-sided towers with teal cone roofs, and the dark door on the "
     "front. The session reported one point eight by zero point eight two by two point three metres, and one "
     "hundred fifty-six triangles, under the budget of two hundred."),
    'Result: What the Look Tool Saw', 'look',
    [{'at': '0.00', 'event': "evidence/blender/03-castle-mcp-look.png, labelled 'Blender MCP look tool, student's live session'"},
     {'at': 'The pink keep', 'event': 'callout: keep (call 1)'},
     {'at': 'two twelve-sided', 'event': 'callout: towers, 12 sides (calls 2–3); roofs (calls 4–5)'},
     {'at': 'and the dark door', 'event': 'callout: door on the front (call 6)'},
     {'at': 'The session reported', 'event': 'numbers: 1.80 × 0.82 × 2.30 m · 156 / 200 tris'}],
    [['keep', 'The pink keep'], ['towers', 'two twelve-sided'], ['door', 'and the dark door'],
     ['numbers', 'The session reported']], 22))

# ---------------------------------------------------------------- B09/B10 castle call 7 -> student's sidebar
B.append(blender_code(
    'B09', 'Code: build_castle.py call 7 — join, origin to the world origin (base centre), apply.',
    ("Call seven joins the six parts. Line one seventy-one joins them into one object, named castle. Lines one "
     "seventy-seven and one seventy-eight put the origin at the 3D cursor, the world origin, which is the centre "
     "of the underside. Line one eighty applies rotation and scale. That origin decides whether the castle floats, "
     "sinks or sits."),
    'tools/blender/build_castle.py', 171, 180, 'Castle, Call 7: Join and Origin',
    [['Brief (A3.1)', 'origin: centre of the underside,\nat world (0, 0, 0); lowest point Z = 0'],
     ['Predicted', 'A3-F3 floats or sinks\nA3-F4 unapplied scale/rotation']],
    [(171, 'join the six parts into one object', 'Line one seventy-one'),
     (177, 'cursor at the world origin', 'Lines one seventy-seven'),
     (178, 'origin moved to the cursor', 'which is the centre'),
     (180, 'apply rotation and scale', 'Line one eighty')], 22, CASTLE_CAP))

B.append(own(
    'B10', 'RESULT', "Result of B09: the student's own screenshot of the MCP-built castle's sidebar (fd99467).",
    ("Tharun's own screenshot of the M C P-built castle, selected in his Blender. The Item tab: location zero, "
     "rotation zero, scale one, and dimensions one point eight by zero point eight two by two point three metres. "
     "The origin dot sits at the base. The statistics overlay was off in this shot, so the triangle count comes "
     "from the session, not from this picture."),
    'Result: the Castle in Tharun\'s Blender', 'castle_sidebar',
    [{'at': '0.00', 'event': "student's own screenshot 07 (castle sidebar)"},
     {'at': 'location zero', 'event': 'ring on Location 0 / Rotation 0° / Scale 1.000'},
     {'at': 'and dimensions', 'event': 'ring on Dimensions 1.8 × 0.82 × 2.3 m'},
     {'at': 'The origin dot', 'event': 'ring on the origin at the base'},
     {'at': 'The statistics', 'event': 'note: Statistics overlay off — no triangle count in this shot'}],
    [['xform', 'location zero'], ['dims', 'and dimensions'], ['origin', 'The origin dot'], ['stats', 'The statistics']],
    20))

# ---------------------------------------------------------------- B11/B12 windkey lobes -> student's sidebar
B.append(blender_code(
    'B11', 'Code: build_windkey.py call 3 — a bow lobe rotated 90° about X, rotation applied before the join.',
    ("The key went through the M C P too, in a later session. Its trap is the bow. Lines ninety-eight and "
     "ninety-nine add each round lobe rotated ninety degrees about X, so its faces point forward and back. Line one "
     "oh two applies that rotation to the part, before the join, so it cannot leak into the whole key."),
    'tools/blender/build_windkey.py', 98, 103, 'Windkey, Call 3: a Bow Lobe',
    [['Brief (A3.2)', 'lobes: cylinders r 0.15, depth 0.06,\n16 sides, rotated 90° about X'],
     ['Predicted', 'A3-F2: the lobe rotation leaks\ninto the whole object'],
     ['Route', 'Blender MCP, 2026-10-16 session\n(call 4 is the mirror, X = +0.15)']],
    [(98, '16-sided cylinder, r 0.15, depth 0.06', 'Lines ninety-eight'),
     (99, 'rotation 90° about X: faces point ±Y', 'rotated ninety degrees'),
     (102, 'apply rotation to this part only', 'Line one oh two')], 19,
    f'Source file, verbatim · tools/blender/build_windkey.py at {REV} · MCP execute_blender_code body · not an editor recording'))

B.append(own(
    'B12', 'RESULT', "Result of B11: the student's own screenshot of the MCP-built windkey (0bc2b4d).",
    ("Tharun's own screenshot of the M C P-built key. Rotation zero, scale one, zero point six by zero point one "
     "four by zero point seven metres, and the statistics overlay at one hundred ninety-two triangles. Getting "
     "here, auto mode denied call zero, which clears the scene and saves over windkey dot blend. Tharun approved "
     "it himself. The numbers match the superseded script-route key exactly."),
    'Result: the Key in Tharun\'s Blender', 'windkey_sidebar',
    [{'at': '0.00', 'event': "student's own screenshot 06 (windkey sidebar, Material Preview)"},
     {'at': 'Rotation zero', 'event': 'ring on Rotation 0° / Scale 1.000 / Dimensions'},
     {'at': 'and the statistics', 'event': 'ring on Triangles 192 / 192'},
     {'at': 'auto mode denied', 'event': 'card: auto mode denied call 0; Tharun approved it (FRICTIONAL)'},
     {'at': 'The numbers match', 'event': 'card: script-route first key gave identical numbers'}],
    [['xform', 'Rotation zero'], ['tris', 'and the statistics'], ['denied', 'auto mode denied'],
     ['same', 'The numbers match']], 24))

# ---------------------------------------------------------------- B13/B14 toybox script -> student's screenshot
B.append(blender_code(
    'B13', 'Code: build_toybox.py (script route) — four boxes; line 12 is the navy band.',
    ("The toy box took the script route: headless Blender running build toybox dot p y, with helpers from common "
     "dot p y. Four boxes, each one call to box, with a size, a centre and a flat colour. Line twelve is the band: "
     "hash two three three nine five B, navy. Line seventeen saves toybox dot blend."),
    'tools/blender/build_toybox.py', 9, 17, 'Toy Box: the Script Route',
    [['Route', 'headless: blender -b --factory-startup\n--python-exit-code 1 --python …'],
     ['box() in _common.py 26–33', 'cube size 1 → scale → apply\n→ one flat material'],
     ['Brief (A3.2)', 'band 1.22 × 0.72 × 0.08 m\nnavy #23395B']],
    [(10, 'body: red #B5302A', 'Four boxes'),
     (12, 'band: navy #23395B', 'Line twelve'),
     (17, 'save assets/blender/toybox.blend', 'Line seventeen')], 18,
    f'Source file, verbatim · tools/blender/build_toybox.py at {REV} · script route (no MCP) · not an editor recording'))

B.append(own(
    'B14', 'RESULT', "Result of B13: the student's own screenshot of toybox.blend before the hand edit (navy band).",
    ("Here is that file, open in Tharun's Blender, his own screenshot from before the hand edit. Red body, cream "
     "lid, brass latch, and line twelve's navy band. Rotation zero and scale one in the properties. This view is "
     "Solid shading. Keep that in mind for the edit."),
    'Result: the Box in Tharun\'s Blender', 'toybox_before',
    [{'at': '0.00', 'event': "student's own screenshot 04 (before)"},
     {'at': "line twelve's navy", 'event': 'ring on the navy band'},
     {'at': 'Rotation zero', 'event': 'ring on Rotation 0° / Scale 1.000'},
     {'at': 'This view is', 'event': 'ring on the viewport shading buttons (Solid)'}],
    [['band', "line twelve's navy"], ['xform', 'Rotation zero'], ['solid', 'This view is']], 15))

# ---------------------------------------------------------------- B15/B16 hand edit
B.append(own(
    'B15', 'HAND_EDIT', "The student's hand edit: before/after screenshots 04 and 05.",
    ("Then the hand edit, Tharun's own, in Blender's window. He switched the viewport to Material Preview, after first "
     "mistaking the X Y Z gizmo for the shading buttons. In the Material tab he picked slot toybox navy and set "
     "Base Color to hash two E seven D three two, green. The size stayed one point two six by zero point seven six "
     "by zero point seven five, scale one. He saved, Claude re-exported, and the Godot check now reads that green."),
    'The Hand Edit: Navy to Green', 'hand_edit',
    [{'at': '0.00', 'event': "student's own screenshots 04 (before) and 05 (after), side by side"},
     {'at': 'Material Preview', 'event': 'ring on the shading buttons in 05; gizmo marked as the thing he first tried'},
     {'at': 'In the Material tab', 'event': 'ring on slot toybox_navy and the green Base Color'},
     {'at': 'The size stayed', 'event': 'ring on Dimensions 1.26 × 0.76 × 0.75 m, Scale 1.000'},
     {'at': 'the Godot check', 'event': 'check line: surface 2 toybox_navy albedo=#2E7D32 (08f96cd)'}],
    [['shade', 'Material Preview'], ['mat', 'In the Material tab'], ['size', 'The size stayed'],
     ['check', 'the Godot check']], 27))

B.append(own(
    'B16', 'HAND_EDIT', "The student's own lesson (0bc2b4d), and two loose ends Claude noticed.",
    ("In Tharun's own words: Editing the hand taught me that Blender's interface relies on coordinating specific "
     "Properties tabs, color pickers, and viewport shading modes just to see surface changes take effect in real "
     "time. Two loose ends, which Claude noticed. The slot is still named toybox navy, though it is green. And "
     "build toybox dot p y still says navy on line twelve, so re-running the script would save navy back over the "
     "hand edit."),
    'What the Edit Taught, and Left Behind', 'lesson',
    [{'at': '0.00', 'event': "the student's sentence, quoted and attributed (BLENDER-NOTES.md, 0bc2b4d)"},
     {'at': 'Two loose ends', 'event': "Claude's observations panel appears"},
     {'at': 'The slot is', 'event': 'check line: surface 2 toybox_navy albedo=#2E7D32'},
     {'at': 'And build toybox', 'event': 'build_toybox.py line 12 (#23395B) and line 17 (save)'}],
    [['loose', 'Two loose ends'], ['slot', 'The slot is'], ['script', 'And build toybox']], 26))

# ---------------------------------------------------------------- B17/B18 prop room -> orbit
B.append(godot_code(
    'B17', 'Code: prop_room.tscn — light, saved camera, the three instanced props and their x positions.',
    ("Into Godot. Each dot blend was exported as G L B with plus Y up, so Blender's Z-up arrives as Godot's Y-up. In "
     "prop room dot t s c n, line thirty-three is the saved camera, five and a half metres out. Line thirty-seven "
     "instances the castle, and line thirty-eight moves it to x minus two point two. The key, line forty, stays at "
     "the origin. Line forty-three puts the toy box at x two."),
    'prop_room/prop_room.tscn', 33, 43, 'The Prop Room',
    [{'label': 'tools/blender/export_glb.py', 'value': 'export_yup=True\n(Blender Z-up → Godot Y-up)'},
     {'label': 'Brief (A3.1)', 'value': 'front: Blender −Y\n→ Godot +Z'}],
    [(33, 'Camera3D: saved camera at (0, 1.6, 5.5)', 'line thirty-three'),
     (37, 'castle.glb instanced', 'Line thirty-seven'),
     (38, 'castle at x = −2.2', 'line thirty-eight'),
     (40, 'windkey at the origin', 'The key, line forty'),
     (43, 'toybox at x = 2.0', 'Line forty-three')], 26, size=25))

B.append({
    'beat_id': 'B18', 'act': 'RESULT',
    'role_note': ('Result of B17: real engine output — Godot Movie Maker 3840x2160 of the unchanged prop_room.tscn '
                  'on an isolated copy of 1d93dcb; saved camera for 4 s, then a film script orbits that camera. '
                  'Not the student\'s look check.'),
    'narration_text': (
        "Real engine output, recorded with Godot's Movie Maker from an isolated copy. The scene file is unchanged. "
        "First the saved camera, then a film script swings that same camera around the room. Every base meets the "
        "floor and its own shadow. The door and the latch face the front. From behind, the castle is plain, and "
        "nothing has a hole."),
    'shot': {'type': 'SCREEN', 'capture_kind': 'godot-movie-maker engine capture (CAPTURE)',
             'source': 'godot-movie-maker', 'motion': 'hold', 'capture_clip': 'orbit',
             'label': 'REAL ENGINE · camera orbit added by a film script · not the look check',
             'capture_window_s': [0.0, None],
             'evidence_media': 'media/B18.mp4',
             'show': [{'at': '0.00', 'event': 'saved Camera3D view of the three props'},
                      {'at': '4.0 s', 'event': 'the same camera orbits; bases and shadows on the floor; back of the castle'}]},
    'qc': {'contrast_regions': [{'label': 'film-label-top', 'box': [0.06, 0.06, 0.94, 0.105]},
                                {'label': 'film-label-bottom', 'box': [0.06, 0.895, 0.94, 0.94]}],
           'contrast_reason': ('Real Godot 3D render (Movie Maker, 3840x2160) inset on the cream ground; the frame '
                               'average is the scene\'s own dark-blue background and floor. The film\'s own text is the '
                               'ink-on-cream label lines above and below the inset, so those regions are measured.')},
    'estimated_duration_s': 22, **V})

# ---------------------------------------------------------------- B19/B20 check -> headless numbers
B.append(godot_code(
    'B19', 'Code: check_props3d.gd lines 83–90 — size vs brief, base, scale/rotation, upright, triangle budget.',
    ("The headless check, which Claude wrote. For each imported prop, lines eighty-three to eighty-five compare "
     "the bounding box with the brief, within one centimetre. Line eighty-six requires the base at y zero. Line "
     "eighty-seven requires scale one and rotation zero. Line ninety compares the triangles with the budget. And "
     "lines six and seven of the same file say what it does not show: whether the props look right."),
    'tests/check_props3d.gd', 83, 90, 'The Headless Check',
    [{'label': 'TOL (line 10)', 'value': '0.01 m'},
     {'label': 'Header, lines 6–7', 'value': 'does NOT show:\nwhether they look right'}],
    [(84, 'size within TOL of the brief', 'lines eighty-three'),
     (86, 'base at y = 0 (±0.005 m)', 'Line eighty-six'),
     (87, 'scale (1,1,1), rotation 0', 'eighty-seven requires'),
     (90, 'triangles ≤ budget', 'Line ninety')], 25, size=25))

B.append(own(
    'B20', 'RESULT', 'Result of B19: the headless output beside the brief, from an isolated copy of 1d93dcb today.',
    ("Run headless on an isolated copy of revision one d nine three d c b: RESULT, pass, zero failing, identical to "
     "the recorded output. Godot is Y-up, so its middle number is the height. Every size matches the brief, every "
     "base is at zero, and in the room the castle spans x minus three point one to minus one point three. And the "
     "toy box band reads hash two E seven D three two."),
    'Result: Headless Numbers Beside the Brief', 'headless',
    [{'at': '0.00', 'event': 'table: brief vs headless AABB, min_y, tris, per prop'},
     {'at': 'RESULT, pass', 'event': 'RESULT: PASS (0 failing)'},
     {'at': 'Godot is Y-up', 'event': 'AABB column highlighted; Y = height'},
     {'at': 'in the room', 'event': 'room placement lines highlighted'},
     {'at': 'toy box band', 'event': 'albedo line toybox_navy #2E7D32'}],
    [['pass', 'RESULT, pass'], ['yup', 'Godot is Y-up'], ['room', 'in the room'], ['band', 'toy box band']], 25))

# ---------------------------------------------------------------- B21/B22 to_root -> repro
B.append(godot_code(
    'B21', 'Code: check_props3d.gd lines 30–40 — the to_root() fix and the comment recording the false pass.',
    ("What Claude got wrong. The comment on lines thirty to thirty-three records it. Claude's first version of "
     "this check read global transform on props that were not yet inside the scene tree. Godot logged an error and "
     "returned the identity. Line thirty-four is the fix. To root builds the transform from local transforms, "
     "parent by parent, which works before the node is in the tree."),
    'tests/check_props3d.gd', 30, 40, 'What Claude Got Wrong: the Room Check',
    [{'label': 'TEST-REPORT A3-8', 'value': 'first version: false PASS\nfor the room check'},
     {'label': 'Used at line 46', 'value': 'to_root(mi)\n* mi.get_aabb()'}],
    [(31, 'the comment records the false pass', 'The comment on'),
     (34, 'to_root(): the fix', 'Line thirty-four'),
     (38, 'parent by parent, local transforms', 'To root builds')], 24, size=24))

B.append(own(
    'B22', 'RESULT', 'Result of B21: the bug re-created on a throwaway copy vs the fixed run; and a parse error exiting 0.',
    ("To show it, Claude re-created that bug on a throwaway copy, swapping line forty-six back to global transform. "
     "The engine errors appear, and still every room check passes, with the castle measured at x minus zero point "
     "nine to zero point nine, the origin, instead of minus three point one. It tested nothing. Second trap, on the "
     "right: a parse error prints no RESULT line, and Godot still exits zero. Read the RESULT line, not the exit "
     "code."),
    'Result: a Pass That Tested Nothing', 'repro',
    [{'at': '0.00', 'event': 'left: re-created bug output (RE-CREATION FOR THIS FILM)'},
     {'at': 'The engine errors', 'event': 'ERROR !is_inside_tree() lines highlighted'},
     {'at': 'with the castle', 'event': 'castle x −0.90..0.90 vs fixed −3.10..−1.30'},
     {'at': 'Second trap', 'event': 'right: parse error output, no RESULT line, exit 0'}],
    [['errors', 'The engine errors'], ['castle', 'with the castle'], ['parse', 'Second trap']], 29))

B.append(own(
    'B23', 'WRONG', 'Two more Claude mistakes from the record: the render script, and the unseen proposal.',
    ("Two more, from the record. The render script for the six views hit the same not-inside-the-tree mistake, so "
     "its first view used the wrong camera. It was fixed and re-rendered. And in the castle session, Claude's "
     "step-by-step proposal never appeared in the chat, yet Tharun replied, approved. The calls did follow the "
     "brief. But he approved a plan he had not seen."),
    'Two More Mistakes', 'wrong',
    [{'at': '0.00', 'event': 'two cards with the source documents named'},
     {'at': 'The render script', 'event': 'card 1: shot_prop_views.gd lines 21–23 (fix) + TEST-REPORT A3-7'},
     {'at': 'And in the castle', 'event': "card 2: Tharun's reply quoted from FRICTIONAL.md"}],
    [['render', 'The render script'], ['proposal', 'And in the castle']], 21))

# ---------------------------------------------------------------- B24 human look check
B.append(own(
    'B24', 'LOOK', "The student's human look check (no screenshot) beside Claude's six-angle renders and observations.",
    ("The look, which numbers cannot check. Tharun opened the prop room in the Godot editor, orbited the props, ran "
     "it with F six, and said: everything works fine. He took no screenshot. These six angles are Claude's renders, "
     "not his. Claude's own notes: the cream lid reads near-white under this light, and the key is small beside "
     "the castle. That matches the brief's sizes, but whether it reads at game size is untested."),
    'The Look: Tharun\'s Check, Claude\'s Renders', 'look_check',
    [{'at': '0.00', 'event': "left: Tharun's check, quoted; right: Claude's six renders (contact sheet)"},
     {'at': 'He took no', 'event': "label: Claude-made renders, not the student's screenshots"},
     {'at': 'the cream lid', 'event': 'ring on the near-white lid in the toybox close-up'},
     {'at': 'and the key is small', 'event': 'ring on the key beside the castle in the front view'}],
    [['noshot', 'He took no'], ['lid', 'the cream lid'], ['key', 'and the key is small']], 26))

# ---------------------------------------------------------------- B25 verdict
B.append({
    'beat_id': 'B25', 'act': 'VERDICT',
    'role_note': 'VERDICT — what was checked (numbers / look), what is uncertain, one next step; revision shown.',
    'narration_text': (
        "The verdict, at revision one d nine three d c b. Checked by numbers, headless: size, origin, scale, "
        "upright, the front at plus Z, triangles and colours, for all three props. Checked by eye: Tharun's look in "
        "the editor. Still uncertain: whether the style and lighting suit Tin Knockout, the near-white lid, and "
        "whether the key reads at game size. The prop room is not yet in the 2D game. One next step: a darker cream "
        "lid, then the check and the look again."),
    'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'hold',
             'show': [{'at': '0.10', 'event': 'verdict artifact lines land'}],
             'remotion': {'pattern': 'ClaudeVerdictArtifact', 'props': {
                 'artifactTitle': 'walker-tinknockout-tharun-m · Assignment 3',
                 'artifactHeading': 'VERDICT · revision ' + REV,
                 'brandLabel': 'WALKER · BLENDER 5.2.2 · GODOT 4.7.2',
                 'artifactLines': [
                     'CHECKED — numbers (headless, RESULT: PASS)',
                     '  size ±0.01 m · base y = 0 · scale 1, rotation 0',
                     '  upright · front at +Z · tris 156 / 192 / 48 · colours',
                     'CHECKED — the look (Tharun): "everything works fine"',
                     'UNCERTAIN',
                     '  style and lighting · cream lid reads near-white',
                     '  readability at game size · not yet in the 2D game',
                     'NEXT  a darker cream lid; re-run the check and the look']}}},
    'estimated_duration_s': 30, **V})

# ---------------------------------------------------------------- B26 your turn
B.append({
    'beat_id': 'B26', 'act': 'YOUR_TURN',
    'role_note': ('YOUR TURN — a useful Walker prompt read aloud, one bounded change + prediction, human/AI credits '
                  '(SOURCES.md "Assignment 3"), revision; Liam signs off before the locked outro.'),
    'narration_text': (
        "Your turn. Here is a useful Walker prompt. Please use Walker to add one check to check props 3 d dot g d "
        "that compares every surface's albedo with the hex colours in the change brief, and tell me which surface "
        "you predict will fail before you run it. My prediction: the toy box band, because the brief still says navy "
        "and the hand edit made it green. Then a person decides: revise the brief, or revert the edit. Credits, "
        "plainly. Claude wrote all the Blender code, the Godot scene and check, and the docs. Tharun chose the assets "
        "and the scale, reviewed and accepted the brief, learned the window and took the screenshots, ran and "
        "approved the M C P sessions, made the hand edit, and did the look check. This voice is Kokoro text to "
        "speech. The source shown is revision one d nine three d c b. Liam, in for Bear."),
    'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'type-on',
             'show': [{'at': '0.10', 'event': 'composer types the suggested prompt; prediction and credits land'}],
             'remotion': {'pattern': 'ClaudeComposerAsk', 'props': {
                 'greeting': 'Your turn.',
                 'topic': 'WALKER · YOUR TURN + CREDITS',
                 'segment': 'one bounded check',
                 'command': ("Please use Walker to add one check to check_props3d.gd that compares every surface's "
                             'albedo with the hex colours in CHANGE-BRIEF.md A3.2, and tell me which surface you '
                             'predict will fail before you run it.'),
                 'runningText': 'over to you…',
                 'output': [
                     '■ prediction, written first: the toy box band (brief: navy · .glb: green)',
                     '■ credits  ·  revision ' + REV,
                     '  CLAUDE  all Blender code · Godot scene + check · docs',
                     '  THARUN  assets + scale · accepted brief · window + screenshots',
                     '          ran/approved MCP sessions · hand edit · look check',
                     '  VOICE   Liam — Kokoro am_onyx, AI text-to-speech']}}},
    'estimated_duration_s': 55, **V})

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
    'topic': 'WALKER · GAME DEVELOPMENT · ASSIGNMENT 3', 'kind': 'godot-gamedev', 'playlist': 'Walker',
    'brand': 'claude-liam', 'audience': 'CSYE 7270 reviewers and Walker users',
    'register': 'Teardown', 'engine': 'kokoro', 'voice': 'am_onyx', 'voice_kokoro': 'am_onyx',
    'palette': 'claude', 'style_preset': 'claude', 'aspect_ratio': '16:9', 'captions': False,
    'channel_title': '@NikBearBrown', 'channel': '@NikBearBrown',
    'presenter': 'Liam (in for Bear)', 'persona': 'Liam (in for Bear)',
    'episode_id': 'walker-tinknockout-tharun-m-a3', 'mode': 'walker',
    'game': {'name': 'walker-tinknockout-tharun-m', 'revision': '1d93dcb89ebd16f1d09d423b2787087bebcded5a',
             'docs_revision': DOCS, 'godot_path': 'godot',
             'engine_version': '4.7.2.stable.official.ed1daf0bf', 'blender_version': '5.2.2 LTS'},
    'student': 'Tharun Maheswararao', 'course': 'CSYE 7270 Fall 2026 · Assignment 3',
    'note': ('Walker-mode godot-gamedev film of the A3 props. Game source shown: 1d93dcb; docs and student evidence '
             'read at fd99467 (docs-only commits 0bc2b4d, fd99467). Real Blender images are the student\'s own '
             'screenshots (01, 02, 04, 05, 06, 07) and the MCP look tool image (03) from the student\'s live session. '
             'Godot images are real engine output: repo renders by shot_prop_room.gd / shot_prop_views.gd (Claude-made) '
             'and a Movie Maker orbit captured for this film on an isolated copy. B00 is an illustrative '
             'reconstruction; B06 is the real pasted castle prompt. Editor views are labelled reconstructions.'),
}

old = {}
p = REEL / 'beat_sheet.json'
if p.exists():
    for b in json.loads(p.read_text())['beats']:
        old[b['beat_id']] = b
for b in B:
    o = old.get(b['beat_id'])
    if o and o.get('narration_text') == b.get('narration_text'):
        for k in ('actual_duration_s', 'audio_file', 'outro_tail_s', 'lead_silence_baked'):
            if k in o:
                b[k] = o[k]
    ro, rn = (o or {}).get('shot', {}).get('remotion') or {}, b['shot'].get('remotion') or {}
    if ro.get('rendered') and rn:
        strip = lambda d: {k: v for k, v in d.get('props', {}).items() if k not in ('durationSeconds', 'cues')}
        if ro.get('pattern') == rn.get('pattern') and strip(ro) == strip(rn):
            rn['rendered'] = ro['rendered']
p.write_text(json.dumps({'metadata': meta, 'beats': B}, indent=1, ensure_ascii=False) + '\n')
print('wrote', p, len(B), 'beats', sum(len(b.get('narration_text', '').split()) for b in B), 'words')
