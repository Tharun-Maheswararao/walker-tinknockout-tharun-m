#!/usr/bin/env python3
"""Author beat_sheet.json for the Tin Knockout gamedev film.

Excerpts are read from the frozen Godot project so displayed code is verbatim.
Re-running preserves measured audio fields (actual_duration_s, audio_file) and
render stamps for beats whose narration did not change.
"""
import json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
GAME = REEL.parents[1] / 'godot'
SLUG = 'claude-liam-walker-tinknockout-tharun-m-gamedev'
TITLE = 'Tin Knockout, Taken Apart'
REV = '64c037a'


def lines(path, a, b):
    return '\n'.join((GAME / path).read_text().splitlines()[a - 1:b])


def capture_qc():
    return {
        'contrast_regions': [{'label': 'film-label-top', 'box': [0.06, 0.055, 0.94, 0.108]},
                             {'label': 'film-label-bottom', 'box': [0.06, 0.894, 0.94, 0.94]}],
        'contrast_reason': (
            'Real Godot gameplay (Movie Maker, 3840x2160) inset to 90% on the cream ground. '
            'The frame average is dominated by the game\'s own painted bowl and shop shelves; '
            'that is the game\'s art, not a scrim over text. The film\'s own readable text is the '
            'ink-on-cream label lines above and below the inset, so those regions are what is measured.'),
    }


def code_beat(bid, role, narration, path, a, b, title, notes, cue_lines, est):
    return {
        'beat_id': bid, 'act': 'MECHANISM', 'role_note': role,
        'narration_text': narration,
        'shot': {
            'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'hold',
            'show': [{'at': '0.10', 'event': f'{path}:{a}-{b} at reading size'}],
            'remotion': {'pattern': 'GodotDevWorkbench', 'props': {
                'mode': 'code', 'title': title, 'project': 'walker-tinknockout-tharun-m',
                'path': f'res://{path}  ·  lines {a}–{b}  ·  revision {REV}',
                'source': f'Godot editor reconstruction · godot/{path} lines {a}–{b} at {REV}, verbatim',
                'code': lines(path, a, b), 'startLine': a, 'codeFontSize': 30 if b - a > 8 else 34,
                'inspectorLabel': 'Source notes — not Inspector values',
                'notes': notes,
                'cues': [{'at': 0.0, 'line': l, 'label': lab} for l, lab in cue_lines],
                'output': ['code → visible result next', 'Godot editor reconstruction'],
                'durationSeconds': est}}},
        'estimated_duration_s': est, 'engine': 'kokoro', 'voice': 'am_onyx',
    }


def still_beat(bid, act, role, narration, media, evidence, est, event):
    return {
        'beat_id': bid, 'act': act, 'role_note': role, 'narration_text': narration,
        'shot': {'type': 'STILL', 'source': 'own', 'motion': 'hold', 'treatment': 'none',
                 'evidence_media': evidence,
                 'show': [{'at': '0.05', 'event': event}],
                 'note': f'Composite of real files, built by _tools/make_media.py; shown as {media}.'},
        'estimated_duration_s': est, 'engine': 'kokoro', 'voice': 'am_onyx',
    }


def capture_beat(bid, role, narration, window, est, event):
    return {
        'beat_id': bid, 'act': 'RESULT', 'role_note': role, 'narration_text': narration,
        'shot': {'type': 'SCREEN', 'capture_kind': 'godot-movie-maker gameplay capture (CAPTURE)', 'source': 'godot-movie-maker', 'motion': 'hold',
                 'capture_clip': 'fight', 'label': 'SCRIPTED INPUT',
                 'capture_window_s': window,
                 'evidence_media': f'media/{bid}.mp4',
                 'show': [{'at': '0.05', 'event': event}]},
        'qc': capture_qc(),
        'estimated_duration_s': est, 'engine': 'kokoro', 'voice': 'am_onyx',
    }


B = []

B.append({
    'beat_id': 'B00', 'act': 'ASK',
    'role_note': 'COLD OPEN / walker B00 — ClaudeComposerAsk. Illustrative reconstruction, not a transcript.',
    'narration_text': (
        "Hola, this is Liam, in for Bear. Today we take apart Tin Knockout, Tharun Maheswararao's Godot slice "
        "for assignment two: a tin wind-up diver toy boxing his repainted twin in a goldfish bowl, after the toy "
        "shop closes. The prompt on screen is an illustrative reconstruction, not a saved transcript."),
    'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'type-on',
             'show': [{'at': '0.10', 'event': 'card lands on cream'}],
             'remotion': {'pattern': 'ClaudeComposerAsk', 'props': {
                 'greeting': 'Hola, Liam',
                 'topic': 'WALKER · GAME DEVELOPMENT',
                 'segment': 'walker-tinknockout-tharun-m',
                 'command': ('Please use Walker to convert my game design document about a tin wind-up '
                             'deep-sea-diver toy who boxes his repainted twin in an empty goldfish bowl after '
                             'the toy shop closes, where every move unwinds his spring, into a playable Godot slice.'),
                 'runningText': 'reading the GDD…',
                 'output': [
                     '■ walker-tinknockout-tharun-m  ·  Godot 4.7.2  ·  ' + REV,
                     '  PLAYER   Bolt  ·  OPPONENT  Rivet (pattern, not AI)',
                     '  SPRING   every move costs wind  ·  hold S to rewind',
                     '  ASSETS   SDXL-Turbo art · AudioLDM 2 SFX · MusicGen waltz',
                     '  RECONSTRUCTED PROMPT — illustrative, not a transcript']}}},
    'estimated_duration_s': 20, 'engine': 'kokoro', 'voice': 'am_onyx',
})

B.append({
    'beat_id': 'B01', 'act': 'BLUF',
    'role_note': 'walker B01 — what was built and what this film explains. Hesitant writer; the correction is the misconception the body dismantles (sound does not drive the fight).',
    'lead_silence_s': 0.8,
    'narration_text': (
        "Tin Knockout is one round of toy boxing where every move costs wind. The fight drives the sounds, "
        "never the other way round. So this film reads a few lines of code, then shows you what each one does on screen."),
    'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'hold',
             'show': [{'at': '0.10', 'event': 'card lands on cream'}],
             'remotion': {'pattern': 'BrutalistHesitantWriter', 'props': {
                 'text': ('Tin Knockout: one round of toy boxing\nwhere every move costs wind.\n'
                          'Sound decides the fight.'),
                 'triggerWords': 'decides',
                 'replacementWords': 'follows',
                 'charMs': 18, 'mistakeRate': 3, 'hesitateBetween': 8,
                 'seed': SLUG,
                 'face': 'serif', 'fontSize': 110, 'lineSpacing': 2.1, 'align': 'left',
                 'ink': '#2b2118'}}},
    'estimated_duration_s': 16, 'engine': 'kokoro', 'voice': 'am_onyx',
})

B.append(still_beat(
    'B02', 'CONCEPT', 'Concept and the four pillars, plainly, over a real engine frame.',
    ("The concept, plainly. You are Bolt, a tin wind-up deep-sea-diver toy. Rivet is the same toy, repainted "
     "copper and verdigris. The spring in your back is your stamina. Every punch, cutlass swing and cork "
     "pop-gun shot unwinds it, and so does walking. Hold S to rewind: one ratchet click per quarter turn, "
     "ten wind each, but rewinding locks you in place. Run down to zero and the toy stalls, empty. Get hit "
     "while rewinding or empty, and you are knocked down. Four pillars: every move costs wind, tin you can "
     "hear, read the fight at a glance, and toys after closing."),
    'media/B02.png', 'evidence/B02-concept-pillars.png', 34,
    'real 4K engine frame beside the four CONCEPT.md pillars'))

B.append(still_beat(
    'B03', 'ASSET_TRACE', 'One asset traced design → prompt → raw → edits → in-engine: CHAR-JAB.',
    ("One asset, traced end to end: the jab. It starts as a spec: pose P04 on a pose sheet Claude drew in "
     "code, and panel three of the storyboard. That pose became a flat init sketch. SDXL-Turbo, image to "
     "image, at strength zero point six, eight steps, seed forty-three, turned it into this raw five twelve "
     "square output, from the prompt on screen. The first pose batch drifted off-model, the failure predicted "
     "as F1, so it was rejected and redone against one reference image, which Tharun picked from four "
     "finalists. Then an edit script removed the background with rembg, painted two eyes on the helmet "
     "glass, and scaled him to three hundred thirty-six pixels, feet at two forty, four thirty-five. Rivet is "
     "the same file, recoloured. And in the engine, the jab lands."),
    'media/B03.png', 'evidence/B03-jab-asset-trace.png', 45,
    'spec → init → candidates → raw → edited → in-engine, with prompt and settings'))

B.append(code_beat(
    'B04', 'Cause → effect, the cause: sprite.centered = false in fighter.gd.',
    ("Here is the cause and effect. In fighter dot g d, line seventy-two creates the sprite, and line "
     "seventy-three sets centered to false. Every pose is drawn on a four eighty by four fifty canvas with "
     "the feet at two forty, four thirty-five, and line two sixty-seven already offsets the sprite by minus "
     "those feet. Leave it centred, and the art is shifted twice."),
    'fighter/fighter.gd', 71, 74, 'The Sprite Anchor Fix',
    [{'label': 'FEET (line 261)', 'value': 'Vector2(240, 435)\nfeet inside each 480×450 canvas'},
     {'label': 'line 267', 'value': 'sprite.offset = -FEET'},
     {'label': 'Before the fix', 'value': 'centred AND offset:\nshifted twice'}],
    [(72, 'Sprite2D created in code (not in main.tscn)'), (73, 'centered = false: offset alone places the feet')],
    20))

B.append(still_beat(
    'B05', 'RESULT', 'Result of B04: before/after posed engine renders with the F1 hitbox overlay.',
    ("And here is the result. The green boxes are the hurtboxes, drawn by the F1 debug overlay. Both shots are "
     "posed: the fighters were placed, then a real jab input. On the left, before the fix, both toys are drawn "
     "about eighty pixels up and left of their own hurtboxes, while the winding keys stay put, so a toy would be "
     "hit where it is not drawn. On the right, after that one line, the art stands inside the box it is hit by."),
    'media/B05.png', 'evidence/B05-before-after.png', 24,
    'before (sprite offset bug) vs after, same posed jab, hitbox overlay on'))

B.append(code_beat(
    'B06', 'Spring mechanism: _rewind turns the key, adds wind per quarter turn, emits rewind_tick.',
    ("Now the spring. This function runs while S is held. Line two oh eight turns the key three hundred and "
     "sixty degrees a second. Every ninety degrees, line two eleven adds ten wind, and line two thirteen emits "
     "rewind tick: one ratchet click per quarter turn. Line two oh seven stops the clicks once the spring is "
     "full. Nothing here plays a sound. It only announces the click."),
    'fighter/fighter.gd', 206, 214, 'Rewinding the Spring',
    [{'label': 'CRANK_DEG_PER_S (line 30)', 'value': '360.0'},
     {'label': 'WIND_PER_CLICK (line 31)', 'value': '10.0  (one quarter-turn)'},
     {'label': 'Inside _rewind() (202–214)', 'value': 'step() calls it while\nstate == REWIND (S held)'}],
    [(208, 'the key turns 360° per second'), (211, '+10 wind per 90°'), (213, 'emit rewind_tick — no audio here'),
     (206, 'full spring: no more clicks')],
    22))

B.append(capture_beat(
    'B07', 'Result of B06: real capture, Bolt rewinding (REWIND state), locked in place, HUD spring dial.',
    ("Scripted input, real engine. Bolt's spring dial is in the red. He holds S, the key on his back spins and "
     "the dial climbs, but he is locked in place, and Rivet's hits land. Then both toys stand still and "
     "rewind, side by side."),
    [10.5, None], 13, 'Bolt at the left wall: HURT, REWIND, both fighters rewinding, then the walk back in'))

B.append(code_beat(
    'B08', 'Sound wiring: sfx.gd listens to gameplay signals.',
    ("Here is how sound is wired. In s f x dot g d, watch connects to the fighter's signals. Line thirty-one: "
     "hit landed plays the jab or cutlass sound, pitched lower when blocked. Line thirty-two: projectile fired "
     "plays the pop. Line thirty-three: each rewind tick plays one ratchet click. Lines thirty-four to "
     "thirty-six: entering EMPTY plays the stall. Gameplay never calls this node."),
    'audio/sfx.gd', 30, 36, 'Sound Listens, Gameplay Decides',
    [{'label': 'Signals (fighter.gd 13–16)', 'value': 'state_changed · hit_landed\nprojectile_fired · rewind_tick'},
     {'label': 'Bell', 'value': 'main.gd: round_changed → FIGHT, KO'},
     {'label': 'Music (music.gd)', 'value': 'pitch 0.85 below 25% spring\nlow-pass on pause · stops on KO'}],
    [(31, 'hit_landed → jab / cutlass sound'), (32, 'projectile_fired → pop'), (33, 'rewind_tick → one click'),
     (35, 'EMPTY entered → stall sound')],
    24))

B.append(capture_beat(
    'B09', 'Result of B08: real capture, the opening exchange — JAB, BLOCK, HURT, POP, EMPTY states; announces the un-narrated segment.',
    ("From the opening bell: Bolt jabs, Rivet jabs back, and every contact sparks and freezes for a few "
     "frames. Then Bolt backs away and fires the cork pop-gun, and that shot empties his spring. Each of those "
     "is one signal and one sound. Next is the same round with no narration at all, so you hear only the game."),
    [1.8, None], 19, 'title → ROUND 1 → FIGHT, jab exchange, pop-gun shot, EMPTY'))

B.append({
    'beat_id': 'B10', 'act': 'GAME_AUDIO',
    'role_note': 'UN-NARRATED: the slice\'s own mixed audio (Movie Maker PCM → AAC), whole scripted round. No narration_text by design.',
    'kind': 'source_report', 'clock': 'source', 'audio_policy': 'preserve',
    'shot': {'type': 'SCREEN', 'capture_kind': 'godot-movie-maker gameplay capture (CAPTURE)', 'source': 'godot-movie-maker', 'motion': 'hold',
             'capture_clip': 'fight', 'label': 'GAME AUDIO — NO NARRATION · SCRIPTED INPUT',
             'capture_window_s': [0.0, 24.433],
             'show': [{'at': '0.00', 'event': 'full take, game audio only: bell, jabs, cutlass, pop, ratchet clicks, EMPTY, waltz, KO bell'}]},
    'qc': capture_qc(),
})

B.append(code_beat(
    'B11', 'Tests: muted run == unmuted run.',
    ("The tests. The slice has twenty-five checks in test slice dot g d. This one runs the same scripted fight "
     "twice: line two oh eight unmuted, line two oh nine with both buses muted. It prints both end states, and "
     "line two twelve requires them to be identical: health, wind, positions and round state."),
    'tests/test_slice.gd', 207, 212, 'Muted Must Equal Unmuted',
    [{'label': 'scripted_fight() (190–205)', 'value': 'real Input taps; returns\nhp, wind, x, round state'},
     {'label': 'What it cannot prove', 'value': 'that a person can read\nthe fight with sound off'}],
    [(208, 'run 1: unmuted'), (209, 'run 2: Music and SFX buses muted'), (212, 'end states must be identical')],
    20))

B.append(still_beat(
    'B12', 'RESULT', 'Result of B11: the recorded test output from an isolated copy, plus the seam check.',
    ("Here is the real output, from a fresh run on an isolated copy. Twenty-five checks, zero failed, and the "
     "muted and unmuted end states match number for number. The first ever run had eight failures. The cause "
     "was the test's own setup order: Rivet fired a cork before the test froze him. The setup was fixed, a "
     "one and a half second pop-gun cooldown was added at round start, and no expected value changed. The "
     "music loop seam check passes too. The engine's exit warnings are shown as printed."),
    'media/B12.png', 'evidence/B12-test-output.png', 28,
    'recorded test_slice.gd output and check_seam.py output'))

B.append({
    'beat_id': 'B13', 'act': 'VERDICT',
    'role_note': 'VERDICT — tested vs uncertain; models per asset; revision shown.',
    'narration_text': (
        "The verdict, at revision six four c zero three a. Tested: twenty-five automated checks pass, the music "
        "loop seam passes, and a muted run ends in exactly the same state as an unmuted one. Tharun's own playtest, "
        "sound on and then muted, is recorded in TEST-REPORT dot m d. He found the music fine on its own and the "
        "muted slice still readable, but the game and the characters very simple, and the mix full of metal sounds. "
        "On checking, that came from the dense tin effects, the rewind clicks and clangs, not the music. Uncertain: "
        "Claude picked those sound effects by signal analysis, because Tharun asked it to choose, and Claude cannot "
        "hear. The bowl is seen from outside, though the concept says inside. Rivet is a pattern, not an AI. The eyes "
        "are hand-painted on every pose, and the win pose uses a different seed. This 4K take also differs from the "
        "headless dry run, because physics stepping changes under fixed f p s. Models: all art is SDXL-Turbo, under "
        "Stability's non-commercial research licence. The six sound effects are AudioLDM 2, C C BY N C S A. The "
        "waltz is MusicGen small, C C BY N C. All ran locally on an Apple M4."),
    'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'hold',
             'show': [{'at': '0.10', 'event': 'card lands on cream'}],
             'remotion': {'pattern': 'ClaudeVerdictArtifact', 'props': {
                 'artifactTitle': 'walker-tinknockout-tharun-m',
                 'artifactHeading': 'VERDICT · revision ' + REV,
                 'brandLabel': 'WALKER · GODOT 4.7.2',
                 'artifactLines': [
                     'TESTED',
                     '  25 checks, 0 failed · seam PASS · muted == unmuted',
                     '  Tharun playtest (TEST-REPORT.md): muted still readable',
                     '  mix "full of metal sounds": the dense tin SFX',
                     'UNCERTAIN',
                     '  SFX picked by signal analysis, not by ear',
                     '  bowl seen from outside · Rivet is a pattern',
                     '  eyes hand-painted · win pose: other seed',
                     '  4K take differs from headless dry run',
                     'MODELS  art SDXL-Turbo · SFX AudioLDM 2 · music MusicGen-small']}}},
    'estimated_duration_s': 55, 'engine': 'kokoro', 'voice': 'am_onyx',
})

B.append({
    'beat_id': 'B14', 'act': 'YOUR_TURN',
    'role_note': 'YOUR TURN — a useful Walker prompt read aloud, one bounded change + prediction, credits, revision; Liam signs off before the locked outro.',
    'narration_text': (
        "Your turn. Here is a useful Walker prompt. Please use Walker to change rivet brain dot g d so a cornered "
        "Rivet blocks instead of rewinding when Bolt is closer than one hundred seventy pixels, add one test for "
        "it, and state your prediction before you run it. Mine: Rivet gets knocked down while rewinding less "
        "often, and rounds last longer. Write yours down first, then run the tests. Tharun's own next step is just "
        "as bounded: a quieter rewind click and a lower effects mix, then richer character art. Toward the full "
        "game, add a real opponent AI and weapon pickups from the toy box. Credits, plainly. Tharun "
        "chose the game and the weapons, rejected reusing his assignment one character, picked Bolt, picked the "
        "reference image from four finalists, and approved the documents. Claude Code wrote the prompts, code, "
        "tests and edit scripts, picked the poses by the character sheet's rules, and picked the sounds by signal "
        "analysis. This voice is Kokoro text to speech. The source shown is revision six four c zero three a. "
        "Liam, in for Bear."),
    'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'type-on',
             'show': [{'at': '0.10', 'event': 'card lands on cream'}],
             'remotion': {'pattern': 'ClaudeComposerAsk', 'props': {
                 'greeting': 'Your turn.',
                 'topic': 'WALKER · YOUR TURN + CREDITS',
                 'segment': 'one bounded change',
                 'command': ('Please use Walker to change rivet_brain.gd so a cornered Rivet blocks instead of '
                             'rewinding when Bolt is closer than 170 px, add one test for it, and state your '
                             'prediction before you run it.'),
                 'runningText': 'over to you…',
                 'output': [
                     '■ prediction, written first',
                     '  Rivet is knocked down while rewinding less often',
                     "■ Tharun's next step: quieter rewind click, lower SFX mix",
                     '■ credits  ·  revision ' + REV,
                     '  HUMAN  Tharun — game, weapons, Bolt, reference pick, approvals',
                     '  AI     Claude Code — prompts, code, tests, edits, pose + SFX picks',
                     '  VOICE  Liam — Kokoro am_onyx, AI text-to-speech']}}},
    'estimated_duration_s': 55, 'engine': 'kokoro', 'voice': 'am_onyx',
})

B.append({
    'beat_id': 'B15', 'act': 'OUTRO', 'kind': 'outro_voice',
    'role_note': 'OUTRO-LOCK — exact title, @NikBearBrown, slug-seeded mascot. Spoken, never scored; 1.0 s silent tail.',
    'narration_text': f'{TITLE}. At Nik Bear Brown.',
    'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'hold',
             'show': [{'at': '0.10', 'event': 'card lands on cream'}],
             'remotion': {'pattern': 'ClaudeTitleOutro', 'props': {'title': TITLE, 'slug': SLUG}}},
    'estimated_duration_s': 5, 'engine': 'kokoro', 'voice': 'am_onyx',
})

for b in B:
    b.pop('_cue_words', None)

meta = {
    'title': TITLE, 'slug': SLUG,
    'topic': 'WALKER · GAME DEVELOPMENT', 'kind': 'godot-gamedev', 'playlist': 'Walker',
    'brand': 'claude-liam', 'audience': 'CSYE 7270 reviewers and Walker users',
    'register': 'Teardown', 'engine': 'kokoro', 'voice': 'am_onyx', 'voice_kokoro': 'am_onyx',
    'palette': 'claude', 'style_preset': 'claude', 'aspect_ratio': '16:9', 'captions': False,
    'channel_title': '@NikBearBrown', 'channel': '@NikBearBrown',
    'presenter': 'Liam (in for Bear)', 'persona': 'Liam (in for Bear)',
    'episode_id': 'walker-tinknockout-tharun-m', 'mode': 'walker',
    'game': {'name': 'walker-tinknockout-tharun-m', 'revision': REV,
             'godot_path': 'godot', 'engine_version': '4.7.2.stable.official.ed1daf0bf'},
    'student': 'Tharun Maheswararao', 'course': 'CSYE 7270 Fall 2026 · Assignment 2',
    'note': ('Walker-mode godot-gamedev film of walker-tinknockout-tharun-m at revision 64c037a. Gameplay is native '
             '3840x2160 Godot Movie Maker capture driven by scripted input through Input.action_press/release '
             '(no state writes). B10 is the un-narrated game-audio segment (clock=source, audio_policy=preserve). '
             'B00 is an illustrative reconstruction, not a transcript. Editor views are labelled reconstructions.'),
}

old = {}
p = REEL / 'beat_sheet.json'
if p.exists():
    for b in json.loads(p.read_text())['beats']:
        old[b['beat_id']] = b
for b in B:
    o = old.get(b['beat_id'])
    if o and o.get('narration_text') == b.get('narration_text'):
        for k in ('actual_duration_s', 'audio_file', 'render_duration_s'):
            if k in o:
                b[k] = o[k]
    if o and 'remotion' in b['shot'] and (o['shot'].get('remotion') or {}).get('rendered'):
        if json.dumps(o['shot']['remotion'].get('props'), sort_keys=True) == json.dumps(b['shot']['remotion'].get('props'), sort_keys=True):
            b['shot']['remotion']['rendered'] = o['shot']['remotion']['rendered']
p.write_text(json.dumps({'metadata': meta, 'beats': B}, indent=1, ensure_ascii=False) + '\n')
print('wrote', p, len(B), 'beats')
