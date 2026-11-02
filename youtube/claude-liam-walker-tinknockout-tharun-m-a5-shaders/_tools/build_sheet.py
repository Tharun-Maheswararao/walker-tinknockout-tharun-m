#!/usr/bin/env python3
"""Author beat_sheet.json for the Tin Knockout Assignment 5 shaders film (walker mode).

Game source shown: commit 2e6946d. Later commits change only evidence/docs, the comment-only
annotation of standard_generated.gdshader (e4c188f, Tharun) and one capture tool (b2b8780);
asserted below. Every excerpt is read from the files so displayed code is verbatim.
Re-running keeps measured audio fields for beats whose narration did not change.
"""
import json, subprocess
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
GAME = REPO / 'godot'
SLUG = 'claude-liam-walker-tinknockout-tharun-m-a5-shaders'
TITLE = 'Tin Knockout, Shaders and Materials'
REV = '2e6946d'

d = subprocess.run(['git', '-C', str(REPO), 'diff', '--name-only', REV, 'HEAD', '--', 'godot', 'assets', 'tools'],
                   capture_output=True, text=True, check=True).stdout.split()
assert set(d) <= {'godot/shaders/standard_generated.gdshader', 'godot/tools/a5_capture_side_by_side.gd',
                  'godot/tools/a5_capture_side_by_side.gd.uid'}, d
for f in ('godot/shaders/rewind_tint.gdshader', 'godot/shaders/painted_tin.gdshader',
          'godot/fighter/rewind_tint_driver.gd', 'godot/prop_room/materials/toybox_fresh.tres',
          'godot/prop_room/materials/toybox_worn.tres'):
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


def src_code(bid, role, narration, path, segments, title, notes, cues, est):
    """Source view built by make_media.py (code_box): verbatim lines, wraps instead of clipping."""
    show = [{'at': '0.00', 'event': f'{path}:' + ', '.join(f'{a}-{b}' for a, b in segments) + ' at reading size'}] + \
           [{'at': ph, 'event': f'line {ln} highlighted: {lab}'} for ln, lab, ph in cues]
    return own(bid, 'MECHANISM', role, narration, title, 'code', show, [[str(ln), ph] for ln, _, ph in cues], est,
               path=path, segments=segments, notes=notes, cues=[[ln, lab] for ln, lab, _ in cues],
               code=['\n'.join(lines(path, a, b).splitlines()) for a, b in segments])


B = []

# ---------------------------------------------------------------- B00 walker cold open
B.append({
    'beat_id': 'B00', 'act': 'ASK',
    'role_note': 'COLD OPEN / walker B00 — ClaudeComposerAsk. Illustrative reconstruction, not a transcript.',
    'narration_text': (
        "Merhaba, this is Liam, in for Bear. Today we take apart assignment five of Tin Knockout, Tharun "
        "Maheswararao's game about tin wind-up toys boxing in an empty goldfish bowl. This time the game gets "
        "shaders and materials. The prompt on screen is an illustrative reconstruction, not a saved transcript."),
    'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'type-on',
             'show': [{'at': '0.10', 'event': 'composer types the reconstructed Walker ask; output lines land'}],
             'remotion': {'pattern': 'ClaudeComposerAsk', 'props': {
                 'greeting': 'Merhaba, Liam',
                 'topic': 'WALKER · GAME DEVELOPMENT · ASSIGNMENT 5',
                 'segment': 'walker-tinknockout-tharun-m',
                 'command': ('Please use Walker to convert my game design document about tin wind-up toys boxing in '
                             'an empty goldfish bowl into two shaders for my Godot game: a blue tint that marks '
                             'REWIND, the vulnerable window, and painted tin for the toy box in the prop room.'),
                 'runningText': 'reading the brief…',
                 'output': [
                     '■ walker-tinknockout-tharun-m  ·  Godot 4.7.2  ·  Forward+  ·  ' + REV,
                     '  rewind_tint.gdshader   canvas_item  ·  Bolt and Rivet',
                     '  painted_tin.gdshader   spatial  ·  toy box, two materials',
                     '  Metal Plate textures   Poly Haven  ·  Rob Tuytel  ·  CC0',
                     '  RECONSTRUCTED PROMPT — illustrative, not a transcript']}}},
    'estimated_duration_s': 17, **V})

# ---------------------------------------------------------------- B01 hesitant writer
B.append({
    'beat_id': 'B01', 'act': 'BLUF',
    'role_note': 'walker B01 — what was built and what the film explains. The correction is the misconception the '
                 'body dismantles: a headless test proves timing, not looks.',
    'lead_silence_s': 0.8,
    'narration_text': ("Tin Knockout got a blue REWIND tint and a painted-tin toy box. Headless tests prove how the "
                       "tint fades, frame by frame. How it looks took windowed captures and a person's eyes. "
                       "This film shows both."),
    'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'hold',
             'show': [{'at': '0.10', 'event': 'writer types the overview; "looks" is struck and corrected to "fades"'}],
             'remotion': {'pattern': 'BrutalistHesitantWriter', 'props': {
                 'text': 'Tin Knockout got a REWIND tint\nand a painted-tin toy box.\nHeadless tests prove how it looks.',
                 'triggerWords': 'looks', 'replacementWords': 'fades',
                 'charMs': 10, 'mistakeRate': 2, 'hesitateBetween': 4, 'seed': SLUG,
                 'face': 'serif', 'fontSize': 114, 'lineSpacing': 2.6, 'align': 'left', 'ink': '#2b2118'}}},
    'estimated_duration_s': 12, **V})

# ---------------------------------------------------------------- B02 game / state / object
B.append(own('B02', 'SETUP',
    'The game, the state the effect communicates (REWIND, the vulnerable window) and the textured object.',
    "The game: two tin toys box on wind-up springs. The state is REWIND: a fighter cranks its key and is open, "
    "and a hit there does one and a half times the damage. That is the vulnerable window, and the tint has to say "
    "punish now. Here it is in Tharun's own screenshot from play, both fighters blue. The object is the toy box "
    "in the prop room, which gets a textured shader.",
    'Game · State · Object', 'setup',
    [{'at': '0.00', 'event': 'OS screenshot during play (Tharun) beside three cards'},
     {'at': 'The state is', 'event': 'STATE card lights: REWIND, the vulnerable window, 1.5x damage'},
     {'at': "Tharun's own screenshot", 'event': 'ring on the two blue fighters'},
     {'at': 'The object is', 'event': 'OBJECT card lights: toy box in prop_room.tscn, in-engine capture'}],
    [['state', 'The state is'], ['shot', "Tharun's own screenshot"], ['object', 'The object is']], 24))

# ---------------------------------------------------------------- B03 Q1 code: rewind_tint
B.append(godot_code('B03',
    'Q1 what a shader does — rewind_tint.gdshader:7-8; the colour line from CHANGE-BRIEF A5.2.',
    "Question one: what does a shader do? It is a small program the graphics card runs for every pixel it draws. "
    "Line three declares rewind amount, a number the game sets from outside. Line seven opens fragment, which runs "
    "once for each pixel of the sprite. And line eight is the colour line from the brief: mix the sprite's colour "
    "toward the blue tint, by rewind amount times strength. Claude suggested that line. Tharun typed it.",
    'shaders/rewind_tint.gdshader', 1, 9, 'Q1 · What a Shader Does',
    [{'label': 'CHANGE-BRIEF A5.2 · colour line', 'value': 'written in the brief before the shader existed'},
     {'label': 'Who', 'value': 'suggested by Claude Code · typed by Tharun (SOURCES.md)'}],
    [(3, 'rewind_amount: 0 to 1, set from outside', 'Line three declares'),
     (7, 'fragment(): runs once per pixel', 'Line seven opens'),
     (8, 'the colour line: mix toward the tint', 'line eight is')], 25, size=28))

# ---------------------------------------------------------------- B04 result: controlled values
B.append(own('B04', 'RESULT',
    'Controlled-value captures beside the hand predictions (CHANGE-BRIEF A5.3, pixel-samples.txt).',
    "The result, in real engine captures at controlled values, from a scripted-input run. Tharun predicted two "
    "pixels by hand, on paper: Bolt's chest and helmet. At zero and at one half, all twelve channels match exactly. "
    "At one, four channels read one lower, all among the five whose predictions sat exactly on a half before "
    "rounding. And at two, set from code, both pixels are pure tint. So hint range does not clamp a value set from code.",
    'The Colour Line, Measured', 'pixels',
    [{'at': '0.00', 'event': 'four in-engine captures (scripted input) with pixel A and B marked'},
     {'at': 'At zero and at one half', 'event': 'columns 0.0 and 0.5 light: predicted = captured'},
     {'at': 'At one, four channels', 'event': 'column 1.0 lights: four channels −1'},
     {'at': 'And at two', 'event': 'column 2.0 lights: pure tint (90, 160, 255)'}],
    [['half', 'At zero and at one half'], ['one', 'At one, four channels'], ['two', 'And at two']], 26))

# ---------------------------------------------------------------- B05 code: the driver
B.append(src_code('B05',
    'The driver lines — rewind_tint_driver.gd: one material per fighter, target, move_toward × delta.',
    "The driver feeds that number. Claude wrote it, in an agent session, from a prompt Tharun approved. Line nineteen "
    "gives each fighter its own material, so Rivet's rewind never tints Bolt. Line twenty-seven sets the target: one "
    "in REWIND, zero otherwise. Line twenty-nine moves toward it, faster going up, slower coming down, times delta, "
    "so the fade runs in game time, not frames.",
    'godot/fighter/rewind_tint_driver.gd', [[17, 30]], 'The Driver',
    [{'label': 'Who', 'value': 'Claude, agent session 2 (driver and test); prompt approved by Tharun'},
     {'label': 'Brief A5.2 R2', 'value': 'fade-in 0.15 s · fade-out 0.30 s'},
     {'label': 'Boundary', 'value': 'reads fighter.state, never writes game state'}],
    [(19, 'one ShaderMaterial per fighter (R6)', 'Line nineteen'),
     (27, 'target: 1 in REWIND, else 0', 'Line twenty-seven'),
     (29, 'move_toward at 1/0.15 or 1/0.30 per s × delta', 'Line twenty-nine')], 24))

# ---------------------------------------------------------------- B06 result: the effect in play (motion)
B.append(own('B06', 'RESULT',
    'The effect in play: a scripted-input Movie Maker capture made for this film (capture/rewind-4k.mp4).',
    "Here is that in motion, a scripted-input capture made for this film. The rewind key goes down, and within a "
    "few frames Bolt turns blue. Then Rivet punches him. REWIND ends in a hit, and the tint fades out over three "
    "tenths of a second. Again, at quarter speed, with the value the driver set on each frame.",
    'The Tint in Play', 'motion',
    [{'at': '0.00', 'event': 'capture/rewind-4k.mp4 frames 70–220 at real speed, logged rewind_amount readout'},
     {'at': 'Again, at quarter speed', 'event': 'labelled 0.25× replay of frames 82–122'}],
    [['slow', 'Again, at quarter speed']], 18))

# ---------------------------------------------------------------- B07 Q2 code: one shader, two materials
B.append(own('B07', 'MECHANISM',
    'Q2 how a material differs from a shader — painted_tin.gdshader uniforms; toybox_fresh.tres / toybox_worn.tres.',
    "Question two: how is a material different from a shader? The shader is the program, and it declares the "
    "knobs: painted tin, lines eight to thirteen. A material is one saved set of values for those knobs. Toybox "
    "fresh and toybox worn both point at the same shader, on line eleven, and differ on lines fifteen and sixteen: "
    "paint roughness and wear amount.",
    'Q2 · One Shader, Two Materials', 'materials',
    [{'at': '0.00', 'event': 'painted_tin.gdshader:7-14 beside toybox_fresh.tres:9-16 and toybox_worn.tres:9-16'},
     {'at': 'lines eight to thirteen', 'event': 'shader lines 8–13 highlighted'},
     {'at': 'on line eleven', 'event': 'line 11 of both .tres highlighted'},
     {'at': 'lines fifteen and sixteen', 'event': 'lines 15–16 of both .tres highlighted'}],
    [['knobs', 'lines eight to thirteen'], ['shader', 'on line eleven'], ['values', 'lines fifteen and sixteen']], 22,
    files=[['godot/shaders/painted_tin.gdshader', 7, 14],
           ['godot/prop_room/materials/toybox_fresh.tres', 9, 16],
           ['godot/prop_room/materials/toybox_worn.tres', 9, 16]]))

# ---------------------------------------------------------------- B08 result: edit checks
B.append(own('B08', 'RESULT',
    'One shader, two materials: shader edit vs material edit (evidence/a5/captures/toybox/edit_checks/).',
    "The proof is an edit test. Tharun changed the shader's u v scale default from two point five to six. Both boxes "
    "changed; the castle did not. Then, with the shader restored, he changed only the worn material's wear amount, "
    "from point five five to point two. Only the worn box changed, mostly bare metal back to red paint. Edit the "
    "shader, and every material follows. Edit a material, and one object changes.",
    'Shader Edit vs Material Edit', 'edits',
    [{'at': '0.00', 'event': 'before: fresh and worn boxes side by side (in-engine capture)'},
     {'at': "Tharun changed the shader's", 'event': 'after shader edit lights: both changed (88 px, 1622 px)'},
     {'at': 'he changed only', 'event': 'after material edit lights: worn only (6698 px)'}],
    [['shader', "Tharun changed the shader's"], ['material', 'he changed only']], 25))

# ---------------------------------------------------------------- B09 Q3 code: texture is information
B.append(src_code('B09',
    'Q3 why a texture is information — painted_tin.gdshader:3-5 hints; line 20 roughness as the wear mask.',
    "Question three: why is a texture information, not just a picture? Painted tin samples three images of Poly "
    "Haven's Metal Plate, by Rob Tuytel, released C C zero. Line three is colour, marked source colour, so Godot "
    "decodes it from s R G B. Line four is a normal map: its pixels store directions, not colours. Line five is "
    "roughness, plain numbers. And line twenty turns that roughness into the wear mask: where the plate is rough, "
    "the paint has worn through.",
    'godot/shaders/painted_tin.gdshader', [[1, 5], [16, 25]], 'Q3 · A Texture Is Information',
    [{'label': 'Textures', 'value': 'Poly Haven "Metal Plate" · Rob Tuytel · CC0 · four 1k PNGs'},
     {'label': 'Who', 'value': 'skeleton suggested by Claude; Tharun typed the file and filled every blank'},
     {'label': 'Normal map', 'value': '_nor_gl (OpenGL convention)'}],
    [(3, 'colour: source_color, decoded from sRGB', 'Line three is colour'),
     (4, 'normal map: hint_normal, directions', 'Line four is'),
     (5, 'roughness: plain data, no colour hint', 'Line five is'),
     (20, 'roughness becomes the wear mask', 'line twenty turns')], 30))

# ---------------------------------------------------------------- B10 result: hint experiment
B.append(own('B10', 'RESULT',
    'The hint experiment, predicted vs measured (hint_quads.png, hint-samples.txt; CHANGE-BRIEF A5.4).',
    "The hint experiment makes that visible. One three-pixel P N G, values sixty-four, one twenty-eight and one "
    "ninety-two, on two quads. The top quad samples it as colour, the bottom as data. Tharun predicted, by hand: "
    "the top shows the file unchanged; the bottom shows one thirty-seven, one eighty-eight and two twenty-five. "
    "Measured: exactly those six numbers. Same bytes, different meaning, and only the hint decides.",
    'The Hint Experiment', 'hint',
    [{'at': '0.00', 'event': 'hint_quads.png (in-engine capture) beside the prediction table'},
     {'at': 'Tharun predicted', 'event': 'predicted column lights'},
     {'at': 'Measured: exactly', 'event': 'measured column lights: 6 of 6 equal'}],
    [['pred', 'Tharun predicted'], ['meas', 'Measured: exactly']], 25))

# ---------------------------------------------------------------- B11 result: interface sweep
B.append(own('B11', 'RESULT',
    'The interface sweep (evidence/a5/captures/toybox/sweep_contact_sheet.png) and Tharun\'s read (TEST-REPORT A5-7).',
    "And the interface sweep: each uniform of the fresh material at its minimum, default and maximum, one at a time, "
    "with the worn box unchanged as the control. Tharun's read: paint colour, wear, normal depth and u v scale each "
    "do one visible job. Paint roughness barely shows at this distance, which points at an open question.",
    'The Interface Sweep', 'sweep',
    [{'at': '0.00', 'event': 'sweep_contact_sheet.png (in-engine captures, windowed)'},
     {'at': 'Paint roughness barely', 'event': 'paint_roughness row ringed'}],
    [['rough', 'Paint roughness barely']], 18))

# ---------------------------------------------------------------- B12 Q4 code: the language
B.append(own('B12', 'MECHANISM',
    'Q4 the Godot shading language — standard_generated.gdshader lines 7 and 19 (annotated by Tharun) beside '
    'painted_tin.gdshader lines 3 and 4; shader_type, hints, built-ins (LANGUAGE-NOTES.md).',
    "Question four: what is the Godot shading language? A G L S L-style language with the plumbing done for you. "
    "Shader type picks the pipeline: canvas item for the sprite, spatial for the box. Hints tell the engine how to "
    "feed a uniform, and built-ins like COLOR and ALBEDO arrive ready. On the left, the shader Godot generated from "
    "a standard material, with Tharun's notes. Line seven reads albedo as colour; line nineteen reads the normal map "
    "as data. On the right, the same jobs in painted tin, lines three and four.",
    'Q4 · The Godot Shading Language', 'language',
    [{'at': '0.00', 'event': 'shader_type / hints / built-ins cards (LANGUAGE-NOTES.md)'},
     {'at': 'On the left', 'event': 'standard_generated.gdshader lines 7 and 19 with Tharun\'s annotations'},
     {'at': 'On the right', 'event': 'painted_tin.gdshader lines 3 and 4 linked to them'}],
    [['left', 'On the left'], ['right', 'On the right']], 30,
    files=[['godot/shaders/standard_generated.gdshader', 7, 7], ['godot/shaders/standard_generated.gdshader', 19, 19],
           ['godot/shaders/painted_tin.gdshader', 3, 3], ['godot/shaders/painted_tin.gdshader', 4, 4]]))

# ---------------------------------------------------------------- B13 result: tests + mutations
B.append(own('B13', 'TESTS',
    'What the tests proved: counts and the three mutations (evidence/a5/mutations/, TEST-REPORT "Assignment 5").',
    "What the tests proved. Test rewind tint: fifty of fifty checks at thirty, sixty and one hundred forty-four frames "
    "per second, sampled every frame through real input. Test materials: fifty-five of fifty-five, and again after "
    "deleting the import cache. The existing suites still pass: twenty-five checks with zero failed, and the props "
    "check, PASS. Then Tharun broke the shaders three ways, restoring them each time. A deleted semicolon: five "
    "failures. A renamed uniform: two. Source colour removed from line three: one. Each was caught, but only by the "
    "uniform-list and source checks; the driver's own checks kept passing.",
    'What the Tests Proved', 'tests',
    [{'at': '0.00', 'event': 'test counts (TEST-REPORT Assignment 5)'},
     {'at': 'Then Tharun broke', 'event': 'mutation diffs and their FAIL lines (evidence/a5/mutations/)'},
     {'at': 'Each was caught', 'event': '"45 and 48 driver checks still passed" highlighted'}],
    [['mut', 'Then Tharun broke'], ['caught', 'Each was caught']], 36))

# ---------------------------------------------------------------- B14 result: headless limits
B.append(own('B14', 'TESTS',
    'What no headless run can show (evidence/a5/headless-facts.txt; TEST-REPORT A5-13).',
    "And what no headless run can show. The headless probe sets rewind amount to two and reads back two: it stores "
    "the number and says nothing about a pixel. Headless runs draw no image at all. Only the windowed capture showed "
    "that two meant pure blue, and only Tharun's eyes judged the look.",
    'What No Headless Run Shows', 'headless',
    [{'at': '0.00', 'event': 'evidence/a5/headless-facts.txt lines 1–12'},
     {'at': 'reads back two', 'event': 'line 9 highlighted: set 2.0 -> readback 2.0'},
     {'at': 'Only the windowed', 'event': 'capture at 2.0 beside it'}],
    [['read', 'reads back two'], ['win', 'Only the windowed']], 16))

# ---------------------------------------------------------------- B15 credits
B.append(own('B15', 'CREDITS',
    'Human and AI contributions exactly as SOURCES.md "Who did what (A5)", shown verbatim on screen.',
    "Who did what, as SOURCES dot m d records it. Tharun accepted Claude's proposed design decisions and material "
    "plan, and computed the pixel, contrast and hint predictions by hand. He wrote the failure cases and short "
    "answers, typed all three shaders from Claude's recorded suggestions, ran the three mutations, reviewed the "
    "audit, converted the material in the editor, made both edits, took the OS screenshot and playtested. Claude "
    "proposed the design and material plan, set up the textures, ran the agent sessions that wrote the driver and "
    "test, fixed two test bugs, wrote the probes, builders and capture tools, ran the audit, made and measured every "
    "capture, and drafted the docs.",
    'Who Did What (A5)', 'credits',
    [{'at': '0.00', 'event': 'SOURCES.md "Who did what (A5)" verbatim, two columns'},
     {'at': 'Claude proposed the design', 'event': 'Claude column lights'}],
    [['claude', 'Claude proposed the design']], 40))

# ---------------------------------------------------------------- B16 verdict
B.append({
    'beat_id': 'B16', 'act': 'VERDICT',
    'role_note': 'VERDICT — checked by numbers / by eye, agent mistakes caught (A5-10), uncertain (M5, start delay), '
                 'one next step; revision shown.',
    'narration_text': (
        "The verdict, at game revision two e six nine four six d. Checked by numbers: the fades, retrigger, both "
        "pauses and one material per fighter, at three frame rates; and eighteen hand predictions, fourteen exact and "
        "four off by one. Checked by eye: Tharun's look at the captures and in play. Six agent mistakes were caught, "
        "among them a test that read the frame rate from arguments the engine had already consumed. Still uncertain: "
        "painted tin never writes metallic, so worn metal may read as grey paint; and REWIND starts on the sixty hertz "
        "physics tick, so the fade can begin up to a sixtieth of a second after the press. One next step: write "
        "metallic from the wear mask, then sweep and look again."),
    'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'hold',
             'show': [{'at': '0.10', 'event': 'verdict artifact lines land'}],
             'remotion': {'pattern': 'ClaudeVerdictArtifact', 'props': {
                 'artifactTitle': 'walker-tinknockout-tharun-m · Assignment 5',
                 'artifactHeading': 'VERDICT · revision ' + REV,
                 'brandLabel': 'WALKER · GODOT 4.7.2 · FORWARD+',
                 'artifactLines': [
                     'CHECKED — numbers (headless, every frame, 30 / 60 / 144 fps)',
                     '  fades 0.15 s / 0.30 s · extend · both pauses · own material',
                     '  18 hand predictions: 14 exact, 4 off by one',
                     'CHECKED — the look (Tharun): captures, sweep, playtest',
                     'AGENT MISTAKES CAUGHT — 6 (TEST-REPORT A5-10)',
                     'UNCERTAIN  no METALLIC: worn metal may read as grey paint (M5)',
                     'UNCERTAIN  fade can start up to 1/60 s after the press',
                     'NEXT  METALLIC from the wear mask; sweep and look again']}}},
    'estimated_duration_s': 36, **V})

# ---------------------------------------------------------------- B17 your turn
B.append({
    'beat_id': 'B17', 'act': 'YOUR_TURN',
    'role_note': 'YOUR TURN — a useful Walker prompt read aloud, one bounded change + prediction, texture source, '
                 'revision; Liam signs off before the locked outro.',
    'narration_text': (
        "Your turn. Here is a useful Walker prompt. Please use Walker to make painted tin write metallic from the wear "
        "mask, and before you run anything, tell me which row of the interface sweep you predict will change. My "
        "prediction: the wear amount row, with worn areas reading as metal; the paint colour row should barely move. "
        "Then a person looks. The texture is Metal Plate by Rob Tuytel, from Poly Haven, C C zero. This voice is "
        "Kokoro text to speech. The source shown is revision two e six nine four six d. Liam, in for Bear."),
    'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'type-on',
             'show': [{'at': '0.10', 'event': 'composer types the suggested prompt; prediction and credits land'}],
             'remotion': {'pattern': 'ClaudeComposerAsk', 'props': {
                 'greeting': 'Your turn.',
                 'topic': 'WALKER · YOUR TURN',
                 'segment': 'one bounded change',
                 'command': ('Please use Walker to make painted_tin.gdshader write METALLIC from the wear mask, and '
                             'before you run anything, tell me which row of the interface sweep you predict will change.'),
                 'runningText': 'over to you…',
                 'output': [
                     '■ prediction, written first: wear_amount row; paint_color row barely moves',
                     '■ then a person looks at the new sweep',
                     '  TEXTURE  Poly Haven "Metal Plate" · Rob Tuytel · CC0',
                     '  SOURCE   game revision ' + REV,
                     '  VOICE    Liam — Kokoro am_onyx, AI text-to-speech']}}},
    'estimated_duration_s': 30, **V})

# ---------------------------------------------------------------- B18 outro
B.append({
    'beat_id': 'B18', 'act': 'OUTRO', 'kind': 'outro_voice',
    'role_note': 'OUTRO-LOCK — exact title, @NikBearBrown, slug-seeded mascot. Spoken, never scored; 1.0 s silent tail.',
    'narration_text': f'{TITLE}. At Nik Bear Brown.',
    'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'hold',
             'show': [{'at': '0.10', 'event': 'locked title card'}],
             'remotion': {'pattern': 'ClaudeTitleOutro', 'props': {'title': TITLE, 'slug': SLUG}}},
    'estimated_duration_s': 5, **V})

meta = {
    'title': TITLE, 'slug': SLUG,
    'topic': 'WALKER · GAME DEVELOPMENT · ASSIGNMENT 5', 'kind': 'godot-gamedev', 'playlist': 'Walker',
    'brand': 'claude-liam', 'audience': 'CSYE 7270 reviewers and Walker users',
    'register': 'Teardown', 'engine': 'kokoro', 'voice': 'am_onyx', 'voice_kokoro': 'am_onyx',
    'palette': 'claude', 'style_preset': 'claude', 'aspect_ratio': '16:9', 'captions': False,
    'channel_title': '@NikBearBrown', 'channel': '@NikBearBrown',
    'presenter': 'Liam (in for Bear)', 'persona': 'Liam (in for Bear)',
    'episode_id': 'walker-tinknockout-tharun-m-a5', 'mode': 'walker',
    'game': {'name': 'walker-tinknockout-tharun-m', 'revision': subprocess.run(
                 ['git', '-C', str(REPO), 'rev-parse', REV], capture_output=True, text=True).stdout.strip(),
             'docs_revision': '93aedd9', 'godot_path': 'godot',
             'engine_version': '4.7.2.stable.official.ed1daf0bf', 'renderer': 'Forward+ (Vulkan/MoltenVK)'},
    'student': 'Tharun Maheswararao', 'course': 'CSYE 7270 Fall 2026 · Assignment 5',
    'note': ('Walker-mode godot-gamedev film of the A5 shaders and materials. Game source shown: 2e6946d; '
             'standard_generated.gdshader shown as annotated by Tharun (e4c188f, comments only); docs and evidence '
             'read at 93aedd9. Shader results are real engine output: the committed windowed captures '
             '(scripted input, Claude-made) and one Movie Maker capture made for this film on an isolated copy of '
             '2e6946d (scripted input). The OS screenshot is Tharun\'s. B00 is an illustrative reconstruction; code '
             'views are labelled reconstructions / source views.'),
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
