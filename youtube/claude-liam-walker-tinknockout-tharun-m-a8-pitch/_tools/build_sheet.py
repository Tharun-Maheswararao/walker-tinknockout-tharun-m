#!/usr/bin/env python3
"""Author beat_sheet.json for Tharun's Assignment 8 final-project pitch film (Tin Knockout Fighter Kit).

Source of every claim: pitch/PROJECT-BRIEF.md (Tharun's seven answers, in order) and pitch/EXISTS-FACTS.md, at
fcb873c. Game source shown: tag a7 (a0c95cc). Every excerpt is read with `git show a0c95cc:<path>`, so displayed
code is verbatim at that tag. Narration is first person, as Tharun (Kokoro am_onyx voice). Past tense only for what
exists at a named tag; everything else is "will". Pictures of things that do not exist are labelled CONSTRUCTED.
Re-running keeps measured audio fields for beats whose narration did not change. Adapted from the A7 film's
_tools/build_sheet.py.
"""
import json, subprocess
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
SLUG = 'claude-liam-walker-tinknockout-tharun-m-a8-pitch'
TITLE = 'Tin Knockout Fighter Kit'
REV = 'a0c95cc'           # tag a7
DOCS = 'fcb873c'          # pitch/ brief and facts

assert subprocess.run(['git', '-C', str(REPO), 'rev-parse', 'a7^{commit}'], capture_output=True,
                      text=True).stdout.strip().startswith(REV)
for f in ['godot', 'scripts']:
    assert subprocess.run(['git', '-C', str(REPO), 'diff', '--quiet', REV, '--', f]).returncode == 0, f
for f in ['pitch/PROJECT-BRIEF.md', 'pitch/EXISTS-FACTS.md']:
    assert subprocess.run(['git', '-C', str(REPO), 'diff', '--quiet', DOCS, '--', f]).returncode == 0, f


def at_rev(path):
    return subprocess.run(['git', '-C', str(REPO), 'show', f'{REV}:{path}'], capture_output=True, text=True,
                          check=True).stdout


def lines(path, a, b):
    return '\n'.join(at_rev(path).splitlines()[a - 1:b])


V = {'engine': 'kokoro', 'voice': 'am_onyx'}


def own(bid, act, role, narration, title, show, anchors, est, evidence=True, **extra):
    """A composite laid out by _tools/make_media.py from real captures, real files, recorded output, or (labelled
    CONSTRUCTED on screen) a proposal drawing."""
    shot = {'type': 'STILL', 'source': 'own', 'motion': 'hold', 'treatment': 'none',
            'show': show, 'anchors': anchors, 'panel': {'title': title},
            'note': 'Composite built by _tools/make_media.py; every embedded image and every drawn proposal is '
                    'labelled on screen with its provenance (REAL PLAY a7 / RECORDED OUTPUT / CONSTRUCTED).'}
    if evidence:
        shot['evidence_media'] = f'media/{bid}.mp4'
    b = {'beat_id': bid, 'act': act, 'role_note': role, 'narration_text': narration, 'shot': shot,
         'estimated_duration_s': est, **V}
    b.update(extra)
    return b


def godot_code(bid, role, narration, path, a, b, title, notes, cues, est, size=30):
    """Checked excerpt (GodotDevWorkbench). path is relative to godot/."""
    return {'beat_id': bid, 'act': 'MECHANISM', 'role_note': role, 'narration_text': narration,
            'shot': {'type': 'GRAPHIC', 'source': 'remotion', 'motion': 'hold',
                     'show': [{'at': '0.00', 'event': f'godot/{path}:{a}-{b} at reading size'}] +
                             [{'at': ph, 'event': f'line {ln}: {lab}'} for ln, lab, ph in cues],
                     'anchors': [[str(ln), ph] for ln, _, ph in cues],
                     'remotion': {'pattern': 'GodotDevWorkbench', 'props': {
                         'mode': 'code', 'title': title, 'project': 'walker-tinknockout-tharun-m',
                         'path': f'res://{path}  ·  lines {a}–{b}  ·  tag a7 ({REV})',
                         'source': f'Godot editor reconstruction · godot/{path} lines {a}–{b} at a7 ({REV}), verbatim',
                         'code': lines('godot/' + path, a, b), 'startLine': a, 'codeFontSize': size,
                         'inspectorLabel': 'Source notes — not Inspector values',
                         'notes': notes,
                         'cues': [{'at': 0.0, 'line': ln, 'label': lab} for ln, lab, _ in cues],
                         'output': ['exists at tag a7 · code → result next', 'Godot editor reconstruction'],
                         'durationSeconds': est}}},
            'estimated_duration_s': est, **V}


B = [
    own('B00', 'WHAT', 'Q1 what it is, one sentence (BRIEF §1). Real play at a7, scripted input: the jab landing.',
        "I'm Tharun Maheswararao. My final project is the Tin Knockout Fighter Kit: a fighter controller and "
        "animation state machine for Godot four, where every move is written in frames and pinned by tests a "
        "stranger can rerun. This is my game at tag a seven, from scripted input.",
        'Tin Knockout Fighter Kit',
        [{'at': '0.00', 'event': 'title and one sentence over real a7 play (Movie Maker, scripted input)'}],
        [], 18),
    own('B01', 'WHAT', 'Q1 the artifact and its form when done (BRIEF §1): macOS training-room build and the '
                       'reusable Fighter.tscn. Neither exists: the picture is CONSTRUCTED.',
        "When it's done, it will be two things: a mac O S build of a training room, where you fight a dummy with "
        "a frame-data overlay; and the fighter as a reusable scene, Fighter dot T S C N. Neither exists yet. This "
        "picture is a proposal.",
        'What It Will Be',
        [{'at': '0.00', 'event': 'CONSTRUCTED: two proposal panels, the build and the scene'},
         {'at': 'Neither exists yet', 'event': 'NOT BUILT YET stamp lands'}],
        [['stamp', 'Neither exists yet']], 15, evidence=False),
    godot_code('B02', 'Q2 why care (BRIEF §2): feel written in frames. fighter.gd:41-45 at a7, the attack table; '
                      'the measured ticks are EXISTS-FACTS §3 (probe_phase_ticks).',
               "Why care? Because here, feel is written down. Line forty-two: the jab's startup, active and "
               "recovery, in seconds, measured at five, six and ten ticks. Line forty-three: the slower cutlass.",
               'fighter/fighter.gd', 41, 45, 'Feel, Written Down',
               [{'label': 'Measured (headless, a7)', 'value': 'jab 5 / 6 / 10 ticks · cutlass 9 / 7 / 18 ticks'},
                {'label': 'Source', 'value': 'evidence/a7/probes/probe_phase_ticks_60fps.txt'}],
               [(42, 'the jab: startup 0.07, active 0.10, recovery 0.18 s', 'Line forty-two'),
                (43, 'the cutlass: 0.14, 0.12, 0.30 s', 'Line forty-three')], 13),
    own('B03', 'WHY', 'Q2 result of B02: the jab whiff, the jab landing with hitstop, and the cutlass (K), real '
                      'play at a7, scripted input; readout from the capture log. Clock gap: TEST-REPORT A7-9e.',
        "In play: the jab's box opens on its fifth tick. When it lands, hitstop holds both fighters, and the "
        "animation holds with them, because each clip is put at the state timer every tick. On my Apple M four, "
        "that gap measured zero seconds. Press K, and the cutlass lands nine ticks in.",
        'The Frames, In Play',
        [{'at': '0.00', 'event': 'case 1 jab whiff, real speed'},
         {'at': 'When it lands', 'event': 'case 2 jab lands: 0.25x replay through hitstop'},
         {'at': 'Press K', 'event': 'case 3 cutlass lands on its ninth tick: 0.5x replay'}],
        [['land', 'When it lands'], ['k', 'Press K']], 20),
    own('B04', 'WHY', 'Q2: the frames are checked. The three a7 suites re-run for this film on an isolated copy of '
                      'a0c95cc; count lines quoted from those logs.',
        "So the frames and the animation can't drift apart without a test failing. Re-run on a clean copy of a "
        "seven: pins, forty-nine checks; structure, fifty-seven; edges, seventy. None failed. Every new move will "
        "join them.",
        'Checked, Not Eyeballed',
        [{'at': '0.00', 'event': 'terminal: the three count lines, recorded output'},
         {'at': 'Every new move', 'event': 'WILL line: each new move joins the same suites'}],
        [['will', 'Every new move']], 14),
    own('B05', 'GIVES', 'Q3 what it gives (BRIEF §3). CONSTRUCTED overlay drawn over a real a7 frame; the command '
                        'line is real and runs today.',
        "What will it give you? Open the build, press J, and the overlay will draw the jab's frames as they "
        "happen. Then run one command, and see the same frames confirmed by tests.",
        'What It Will Give You',
        [{'at': '0.00', 'event': 'real a7 frame with a CONSTRUCTED overlay bar: startup 5 / active 6 / recovery 10'},
         {'at': 'Then run one command', 'event': 'the real command and its real count line'}],
        [['cmd', 'Then run one command']], 12, evidence=False),
    own('B06', 'DIFFERENT', 'Q4 different (BRIEF §4): Street Fighter 6 and Tekken 8 named in text only (games Tharun '
                            'has played); no footage or art from them.',
        "I've played Street Fighter six and Tekken eight. They're far larger, finished games, and this doesn't "
        "compete with them. Their frame data is something a player reads. Here, a programmer can open the state "
        "machine that makes the frames, and rerun the tests that prove them.",
        'Different From What I Play',
        [{'at': '0.00', 'event': 'left: SF6 and Tekken 8, named only'},
         {'at': 'Here, a programmer', 'event': 'right: the state machine and the tests'}],
        [['here', 'Here, a programmer']], 16, evidence=False),
    own('B07', 'DIFFERENT', 'Q4 its own mechanic (BRIEF §4): the wind-up spring. Real play at a7, scripted input: '
                            'Bolt holds S, the key turns, wind climbs.',
        "And Tin Knockout has its own mechanic: a wind-up spring that every move drains. You rewind it by holding "
        "S, and you're open while you crank.",
        'Its Own Mechanic',
        [{'at': '0.00', 'event': 'case 4: Bolt holds S, real speed; wind readout from the log'}], [], 9),
    own('B08', 'WHO', 'Q5 who opens it and the first sixty seconds (BRIEF §5). Steps 1-4 are WILL; the second path '
                      'is real recorded output today.',
        "My target role is gameplay programmer. The reader is a lead engineer or hiring manager, with sixty "
        "seconds. They'll double-click the build, land in the training room with no menu, press J to see the jab "
        "counted, then K for the cutlass's different timing. Today, one command already prints seventy checks, "
        "zero failed.",
        'The First Sixty Seconds',
        [{'at': '0.00', 'event': 'role and reader'},
         {'at': "They'll double-click", 'event': 'four WILL steps light in turn'},
         {'at': 'Today, one command', 'event': 'TODAY: the real command and count line'}],
        [['s1', "They'll double-click"], ['s2', 'land in the training'], ['s3', 'press J'], ['s4', 'then K'],
         ['today', 'Today, one command']], 18, evidence=False),
    own('B09', 'PROVES', 'Q6 what it proves (BRIEF §6), each with its tag and TEST-REPORT record.',
        "What does it prove? Animation and state: one authority per animated node, clips synced to the state "
        "timer. Verification: pins before and after a change, edge tests at every boundary, mutations in git "
        "worktrees, and a seam bug a fixture log caught after the suite passed it. Profiling: two clocks, measured "
        "on the M four. And shaders and particles that read the fighter, and never write it.",
        'What It Proves',
        [{'at': '0.00', 'event': 'ledger row: animation and state'},
         {'at': 'Verification', 'event': 'row: verification habits'},
         {'at': 'Profiling', 'event': 'row: profiling'},
         {'at': 'And shaders', 'event': 'row: shaders and particles'}],
        [['v', 'Verification:'], ['p', 'Profiling'], ['s', 'And shaders']], 22, evidence=False),
    own('B10', 'SCOPE', 'Q7 in, out, first (BRIEF §7).',
        "Out: netcode, a second character's art, more arenas, saving. In: the reusable scene; an animated cutlass, "
        "block and hurt; an input buffer; the overlay; the training room; and the mac export. First, the fighter "
        "will run as its own scene against a still dummy, and the three a seven suites will give the same counts "
        "against it.",
        'In, Out, First',
        [{'at': '0.00', 'event': 'OUT column'}, {'at': 'In:', 'event': 'IN column'},
         {'at': 'First,', 'event': 'FIRST: the check that says it ran'}],
        [['in', 'In: the'], ['first', 'First, the']], 18, evidence=False),
    godot_code('B11', 'Q7 the risk (BRIEF §7): main.gd drives the fighter. main.gd:180-182 at a7; lines 61 and 80-81 '
                      'as source notes.',
               "What could sink it? Today, main dot G D drives the fighter: line one eighty-one calls its step, and "
               "main also sets its opponent and its cork spawner. Untangling that could silently move a frame "
               "boundary.",
               'game/main.gd', 180, 182, 'What Could Sink It',
               [{'label': 'Line 61', 'value': 'f.spawn_cork = _spawn_cork'},
                {'label': 'Lines 80–81', 'value': 'bolt.opponent = rivet · rivet.opponent = bolt'}],
               [(181, "main calls the fighter's step every physics tick", 'line one eighty-one')], 12, size=34),
    own('B12', 'RISK', 'Result of B11: the mitigation. test_a7_pins.gd (which runs main.tscn) re-run at 60 and 30 '
                       'on a0c95cc, recorded output; plus the renderer risk (BRIEF §7).',
        "So the pins come first: they lock every boundary at sixty and at thirty frames a second, and the "
        "refactor won't be committed unless they pass with identical logs. And since the game renders with "
        "Forward plus on Vulkan, the Mac build will be tested on the M four before I claim anything. No web build.",
        'What I Will Do About It',
        [{'at': '0.00', 'event': 'pins at 60 and at 30, recorded output'},
         {'at': 'And since the game', 'event': 'second risk: Forward+ on Vulkan, no web build'}],
        [['vk', 'And since the game']], 17),
    own('B13', 'WHY_ME', 'Q8 why this project (BRIEF §8): a mix, with tags for the existing skills.',
        "Why this project? A mix. I already have shaders, particles and a pinned state machine, and I've directed "
        "an agent with scoped plans. New to me: a reusable scene, an input buffer, an overlay, and a desktop export "
        "with a measured frame rate. And I'll test whether an AnimationTree helps by building the cutlass both "
        "ways.",
        'Why This Project',
        [{'at': '0.00', 'event': 'HAVE column, with tags'}, {'at': 'New to me', 'event': 'NEW column'},
         {'at': "And I'll test", 'event': 'UNKNOWN: the AnimationTree comparison'}],
        [['new', 'New to me'], ['unk', "And I'll test"]], 17, evidence=False),
    own('B14', 'CLOSE', 'Closing lists (BRIEF "Exists today" / "Will exist").',
        "Exists today: the playable slice, at a two; the eleven-state fighter, the animated jab and key cycle, and "
        "their passing tests, at a seven; shaders at a five, particles at a six. Will exist: the reusable scene "
        "and training room, three more animated moves, the buffer, the overlay, and a measured mac build.",
        'Exists Today · Will Exist',
        [{'at': '0.00', 'event': 'EXISTS TODAY column, each with its tag'},
         {'at': 'Will exist', 'event': 'WILL EXIST column'}],
        [['will', 'Will exist']], 17, evidence=False),
    own('B15', 'OUTRO', 'Closing title card: the film title and the student. No instructor handle or credit line '
                        '(task rule); spoken, no music; 1.0 s silent tail.',
        f'{TITLE}. Tharun Maheswararao.',
        TITLE, [{'at': '0.00', 'event': 'title card'}], [], 4, evidence=False, kind='outro_voice'),
]

meta = {
    'title': TITLE, 'slug': SLUG,
    'topic': 'CSYE 7270 · FINAL PROJECT PITCH', 'kind': 'godot-gamedev', 'playlist': 'Walker',
    'brand': 'claude-liam', 'audience': 'CSYE 7270 reviewers; a lead gameplay engineer or hiring manager',
    'register': 'Pitch, first person', 'engine': 'kokoro', 'voice': 'am_onyx', 'voice_kokoro': 'am_onyx',
    'palette': 'claude', 'style_preset': 'claude', 'aspect_ratio': '16:9', 'captions': False,
    'channel_title': '', 'channel': 'Tharun Maheswararao',
    'presenter': 'Tharun Maheswararao, first person (Kokoro am_onyx voice)',
    'persona': 'Tharun Maheswararao, first person (Kokoro am_onyx voice)',
    'episode_id': 'walker-tinknockout-tharun-m-a8', 'mode': 'walker (pitch adaptation)',
    'game': {'name': 'walker-tinknockout-tharun-m', 'revision': subprocess.run(
                 ['git', '-C', str(REPO), 'rev-parse', REV], capture_output=True, text=True).stdout.strip(),
             'tag': 'a7', 'docs_revision': DOCS, 'godot_path': 'godot',
             'engine_version': '4.7.2.stable.official.ed1daf0bf', 'renderer': 'Forward+ (Vulkan/MoltenVK)'},
    'student': 'Tharun Maheswararao', 'course': 'CSYE 7270 Fall 2026 · Assignment 8 · final project pitch',
    'note': ('Pitch film for the Tin Knockout Fighter Kit (option c, a gameplay system). Script from '
             'pitch/PROJECT-BRIEF.md at fcb873c, in its order. Gameplay is real play captured with Movie Maker from '
             'an isolated git archive of tag a7 (a0c95cc), scripted input, labelled. The training room, the '
             'frame-data overlay and Fighter.tscn do not exist: their pictures are labelled CONSTRUCTED. The walker '
             'bookends are adapted for a pitch: no reconstructed Claude prompt or response is shown, and the '
             'closing card carries the film title and the student only.'),
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
