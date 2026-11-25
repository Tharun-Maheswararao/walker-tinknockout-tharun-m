#!/usr/bin/env python3
"""Write gamedev-evidence.json (schema 1, code-then-result-v1) for the A8 pitch film.

--game is the repo's godot/ folder, asserted identical to tag a7 (a0c95cc). The pitched system (option c) is the
fighter controller, its state machine and animation layer, the controller seam and the tests that pin it: those
files are components. Every other file is an exclusion with its reason (presentation, art, audio, props, earlier
assignments' tests): the pitch names them only as context. B02 and B11 are checked GodotDevWorkbench excerpts, each
followed by its visible result (B03 real play, B12 recorded test output). Adapted from the A7 film's make_evidence.py.
"""
import hashlib, json, subprocess
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
GAME = REPO / 'godot'
REV = 'a0c95cc'
assert subprocess.run(['git', '-C', str(REPO), 'diff', '--quiet', REV, '--', 'godot']).returncode == 0
assert not subprocess.run(['git', '-C', str(REPO), 'ls-files', '--others', '--exclude-standard', 'godot'],
                          capture_output=True, text=True).stdout.strip()


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


inv = sorted(p.relative_to(GAME).as_posix() for p in GAME.rglob('*')
             if p.is_file() and not any(x in ('.godot', '.git') for x in p.relative_to(GAME).parts)
             and p.suffix != '.uid')

COMPONENTS = {
    'fighter-state-machine': ('The 11-state Fighter (fighter.gd): the attack table in seconds (lines 41-45), step() on '
                              'the 60 Hz physics tick, hitboxes, hitstop, wind, and the five signals out. The system '
                              'the pitch proposes to package as Fighter.tscn.',
                              ['B00', 'B02', 'B03', 'B07', 'B09', 'B14']),
    'controller-seam': ('What drives a fighter today: main.gd creates both fighters in code, sets opponent and '
                        'spawn_cork, and calls step() in _simulate (lines 180-182); input actions from controls.gd '
                        '(J jab, K cutlass, S rewind); Rivet\'s deterministic rules in rivet_brain.gd. The coupling '
                        'the pitch names as its risk.', ['B03', 'B07', 'B11', 'B12']),
    'animation-layer': ('The A7 clips, jab_action and wind_key_cycle, put at state_t every tick by the fighter; one '
                        'authority per animated node.', ['B03', 'B07', 'B09', 'B14']),
    'pinning-tests': ('The suites that pin the system at a7 and that the pitch\'s first milestone must keep: pins (49), '
                      'structure (57), edges (70), re-run for this film.', ['B04', 'B08', 'B10', 'B12']),
}
COMP_FILES = {
    'fighter/fighter.gd': ['fighter-state-machine', 'animation-layer'],
    'game/main.gd': ['controller-seam'], 'game/controls.gd': ['controller-seam'],
    'fighter/rivet_brain.gd': ['controller-seam'],
    'animations/jab_action.tres': ['animation-layer'], 'animations/wind_key_cycle.tres': ['animation-layer'],
    'tests/test_a7_pins.gd': ['pinning-tests'], 'tests/test_a7_structure.gd': ['pinning-tests'],
    'tests/test_a7_edges.gd': ['pinning-tests'],
}


def reason(p):
    if p.startswith('assets/') or p.endswith('.import'):
        return 'Art, audio or import settings (A2 generated assets, A7 key sheets); context only, not the pitched system.'
    if p.startswith('shaders/') or 'tint' in p:
        return 'A5 shader presentation; named in the pitch as an existing skill (a5), not part of the pitched system.'
    if p.startswith('effects/'):
        return 'A6 particle presentation; named in the pitch as an existing skill (a6), not part of the pitched system.'
    if p.startswith('tests/'):
        return 'Earlier or narrower test (read-backs, A2-A6 suites); still passes at a7, not one of the three suites the pitch pins.'
    if p.startswith('previews/'):
        return 'A7 fixture scene (strips, key cycle); not part of the pitched system.'
    if p.startswith('props3d/') or p.startswith('prop'):
        return 'A3 3D prop room; not used by the fight.'
    return 'Part of the game at a7 outside the pitched fighter system (round flow, HUD, audio, tools, project settings).'


files, exclusions = [], []
for p in inv:
    if p in COMP_FILES:
        files.append({'path': p, 'sha256': sha(GAME / p), 'role': 'pitched system at a7', 'component_ids': COMP_FILES[p]})
    else:
        exclusions.append({'path': p, 'reason': reason(p)})
assert len(files) == len(COMP_FILES), set(COMP_FILES) - {f['path'] for f in files}
components = [{'id': cid, 'explanation': e, 'beat_ids': beats,
               'files': [f['path'] for f in files if cid in f['component_ids']]}
              for cid, (e, beats) in COMPONENTS.items()]

sheet = json.loads((REEL / 'beat_sheet.json').read_text())
beats = {b['beat_id']: b for b in sheet['beats']}
excerpts = []
for bid, b in beats.items():
    rem = b['shot'].get('remotion') or {}
    if rem.get('pattern') == 'GodotDevWorkbench':
        props = rem['props']
        path = props['path'].split('res://')[1].split('  ·')[0]
        a = props['startLine']
        n = len(props['code'].split('\n'))
        text = '\n'.join((GAME / path).read_text().splitlines()[a - 1:a - 1 + n])
        assert text == props['code'], bid
        excerpts.append({'beat_id': bid, 'path': path, 'start_line': a, 'end_line': a + n - 1, 'text': text})

PAIRS = [('B02', 'B03', 'media/B03.mp4',
          'Real play at a7 (scripted input, Movie Maker 60 fps): the jab\'s state_t crosses 0.07 s on its 5th tick '
          '(phase ACTIVE, box live); case 2 lands there and hitstop holds state_t for 5 ticks; the cutlass (K) lands '
          'on its 9th tick, where its 0.14 s startup ends. Readout from the capture log.'),
         ('B11', 'B12', 'media/B12.mp4',
          'test_a7_pins.gd drives the real main.tscn (main calls step) through the input path; re-run on a0c95cc at '
          '60 and at 30 fps: 49 checks, 0 failed each. The pitch\'s rule: the refactor is committed only if these '
          'pass with identical logs.')]
pairs = [{'code_beat': c, 'result_beat': r, 'observation': o, 'media': {'path': m, 'sha256': sha(REEL / m)}}
         for c, r, m, o in PAIRS]
for c, r, m, _ in PAIRS:
    assert list(beats).index(r) == list(beats).index(c) + 1 and beats[r]['shot']['evidence_media'] == m, c

cap = REEL / 'capture/play-4k60.mp4'
caps = [{'path': 'capture/play-4k60.mp4', 'sha256': sha(cap), 'fps': 60, 'size': '3840x2160', 'revision': REV,
         'tag': 'a7', 'input': 'SCRIPTED INPUT (_tools/film_a8_play.gd)',
         'method': 'Movie Maker, windowed, --disable-vsync --always-on-top --fixed-fps 60',
         'log': 'evidence/runs/play-capture-log.txt'}]
out = {'schema_version': 1, 'teaching_contract': 'code-then-result-v1',
       'game': {'package': 'walker-tinknockout-tharun-m', 'godot_folder': 'godot',
                'revision': sheet['metadata']['game']['revision'], 'tag': 'a7',
                'engine': '4.7.2.stable.official.ed1daf0bf', 'renderer': 'Forward+ (Vulkan/MoltenVK)'},
       'files': files, 'components': components, 'excerpts': excerpts, 'exclusions': exclusions,
       'code_result_pairs': pairs, 'engine_captures': caps}
(REEL / 'gamedev-evidence.json').write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
print(len(files), 'files,', len(exclusions), 'exclusions,', len(components), 'components,', len(excerpts),
      'excerpts,', len(pairs), 'pairs')
