#!/usr/bin/env python3
"""Write gamedev-evidence.json (schema 1, code-then-result-v1) for the A7 animation film.

--game is the repo's godot/ folder at a5978c0 (asserted: the working tree has no godot/ changes against it).
Files added or changed for Assignment 7 (git diff 66c8cbc..a5978c0, 66c8cbc = tag a6) are components; every other
file is an exclusion only if it is byte-identical to a6 (checked here), because the earlier films explain it.
B03 and B07 use GodotDevWorkbench (checked excerpts, each followed by its result beat); the source-view composites
(B05, B09, B11, B13, B15, B17) are recorded in `source_view_code_result_pairs` (verbatim text + hashes; not checked
by verify_gamedev.py). Adapted from the A6 film's _tools/make_evidence.py.
"""
import hashlib, json, subprocess
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
GAME = REPO / 'godot'
PRE = '66c8cbc'
REV = 'a5978c0'

assert subprocess.run(['git', '-C', str(REPO), 'diff', '--quiet', REV, '--', 'godot']).returncode == 0


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def unchanged_since_pre(rel):
    r = subprocess.run(['git', '-C', str(REPO), 'diff', '--quiet', PRE, REV, '--', f'godot/{rel}'])
    return r.returncode == 0 and subprocess.run(
        ['git', '-C', str(REPO), 'cat-file', '-e', f'{PRE}:godot/{rel}'], capture_output=True).returncode == 0


inv = sorted(p.relative_to(GAME).as_posix() for p in GAME.rglob('*')
             if p.is_file() and not any(x in ('.godot', '.git') for x in p.relative_to(GAME).parts)
             and p.suffix != '.uid')

COMPONENTS = {
    'clip-a-cycle': ('Clip A, wind_key_cycle (the cycle): Sprite2D + AnimationPlayer discrete frame track, 8 keys at '
                     '8 fps, LOOP_LINEAR, no key at length; KeyAnimPlayer is the one writer of key_sprite.frame.',
                     ['B02', 'B13', 'B14', 'B20']),
    'clip-b-jab': ('Clip B, jab_action (the committing action): cutout rig keyed as resource text, three value tracks '
                   'on BodyPivot (position:x, rotation) and KeyBob (position:y), keys at frames 0/3/5/10/11/21 of the '
                   '60 fps phase table, LOOP_NONE, step 1/60; revisions 1 (transition) and 2 (frame-11 pose).',
                   ['B02', 'B03', 'B04', 'B09', 'B10', 'B15', 'B16', 'B17', 'B18', 'B19', 'B20']),
    'rig-and-clock': ('The named rig and its one authority per node in fighter.gd (_ready, _apply_pose), both players '
                      'MANUAL and put at state_t by _sync_clips at the end of step and on state_changed (the seam fix '
                      'advances forward); SteamMount (A6) now only reads KeyMount.',
                      ['B05', 'B06', 'B07', 'B08', 'B19', 'B20', 'B22']),
    'sheet': ('The 8 x 1 key sheets (84 x 60 cells) written by generate_key_sheets.gd from the A2 key art, their '
              'import sidecars and ATTRIBUTION.md (source, licence).', ['B11', 'B12', 'B24']),
    'fixtures': ('Fixtures, not part of the game: jab_preview (the strips r0-r2, --clocks) and key_cycle_preview (the '
                 'seam).', ['B10', 'B14', 'B16', 'B18']),
    'tests': ('A7 tests: the two read-backs (26, 58), structure and state (57), edges (70), pins (49), and the four '
              'planned pin updates in test_slice.gd and test_wind_steam_state.gd.', ['B04', 'B06', 'B21', 'B22']),
}


def assign(p):
    if p.startswith('animations/'):
        return (['clip-a-cycle'] if 'wind_key' in p else ['clip-b-jab']), 'A7 clip resource'
    if p in ('fighter/fighter.gd', 'effects/steam_mount.gd'):
        return ['rig-and-clock'], 'A7 rig, authority and clip sync / SteamMount follows KeyMount'
    if p.startswith('assets/props/key-') and 'sheet' in p or p == 'assets/props/ATTRIBUTION.md' or \
            p == 'tools/generate_key_sheets.gd':
        return ['sheet'], 'A7 key sheet / its import settings / generator / credits'
    if p.startswith('previews/jab_preview') or p.startswith('previews/key_cycle_preview'):
        return ['fixtures'], 'A7 fixture (not part of the game)'
    if p in ('tests/test_a7_edges.gd', 'tests/test_a7_pins.gd', 'tests/test_a7_structure.gd',
             'tests/test_jab_action_readback.gd', 'tests/test_wind_key_cycle_readback.gd', 'tests/test_slice.gd',
             'tests/test_wind_steam_state.gd'):
        return ['tests'], 'A7 test / planned pin update'
    return None, None


files, exclusions = [], []
for p in inv:
    comp, role = assign(p)
    if comp:
        files.append({'path': p, 'sha256': sha(GAME / p), 'role': role, 'component_ids': comp})
        continue
    assert unchanged_since_pre(p), 'not an unchanged pre-A7 file: ' + p
    exclusions.append({'path': p, 'reason': (
        f'Pre-Assignment-7 file, byte-identical to tag a6 ({PRE}); explained in the earlier films; A7 does not change '
        'it.')})

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

PAIRS = [('B03', 'B04', 'media/B04.mp4',
          'Mutation M1 renames the rotation track\'s property (rotatoin): the engine says nothing and the game runs '
          'with the track inert; only the read-back (exit 8) and the structure test on the real rig (exit 2) fail. '
          'Recorded output from evidence/a7/mutations/.'),
         ('B07', 'B08', 'media/B08.mp4',
          'Film capture (scripted input, isolated copy of a5978c0), case 2: the jab lands on e+5 and the logged clip '
          'position holds 0.0833 with state_t through the 5 hitstop ticks; Tharun\'s measured CLOCKS line: clip vs '
          'state_t largest gap 0.000000 s on 279 JAB ticks.')]
pairs = [{'code_beat': c, 'result_beat': r, 'observation': o, 'media': {'path': m, 'sha256': sha(REEL / m)}}
         for c, r, m, o in PAIRS]
for c, r, m, _ in PAIRS:
    assert list(beats).index(r) == list(beats).index(c) + 1 and beats[r]['shot']['evidence_media'] == m, c

SV = [('B05', 'B06', 'media/B06.mp4', 'test_a7_structure section A (re-run): after setup the only code writes to the '
       'rig are _apply_pose\'s FacingPivot.scale and KeyMount.position/visible; pose = clip value, largest gap 0.'),
      ('B09', 'B10', 'media/B10.mp4', 'Fixture strip r0 at each phase boundary: coil on 13, lunge on 15 (box opens), '
       'hold to 20, release on 21, idle on 31; Tharun\'s first look.'),
      ('B11', 'B12', 'media/B12.mp4', 'The two committed 672 x 60 sheets, 8 x 1 cells; cells 2 and 6 at the 0.15 '
       'minimum; cell centres 41.5 / 42.0 of 84 (A7-9c).'),
      ('B13', 'B14', 'media/B14.mp4', 'key_cycle_preview Movie Maker capture (fixture, made for this film): the key '
       'turns 0..7 and wraps 7 -> 0 five times; per-tick log readout.'),
      ('B15', 'B16', 'media/B16.mp4', 'r1 recovery sheet: frames 22-30 at the predicted values; Tharun: Keep.'),
      ('B17', 'B18', 'media/B18.mp4', 'r1 vs r2: frame-21 step -7.7 window px as predicted, steps 3.9 (predicted '
       '4.3); Tharun: Keep.')]
sv = []
for c, r, m, o in SV:
    p = beats[c]['shot']['panel']
    src = p.get('files')
    sv.append({'code_beat': c, 'result_beat': r,
               'sources': [{'path': f, 'start_line': a, 'end_line': z, 'sha256': sha(REPO / f),
                            'text': '\n'.join((REPO / f).read_text().splitlines()[a - 1:z])} for f, a, z in src],
               'observation': o, 'media': {'path': m, 'sha256': sha(REEL / m)}})
    assert list(beats).index(r) == list(beats).index(c) + 1, c

caps = []
for name, frames in (('capture/play-4k60.mp4', None), ('capture/key-cycle-4k60.mp4', None)):
    pth = REEL / name
    caps.append({'path': name, 'sha256': sha(pth), 'fps': 60, 'size': '3840x2160', 'revision': REV,
                 'method': 'Movie Maker, windowed, --disable-vsync --always-on-top --fixed-fps 60',
                 'log': 'evidence/runs/' + ('play-capture-log.txt' if 'play' in name else 'key-cycle-capture-log.txt')})
out = {'schema_version': 1, 'teaching_contract': 'code-then-result-v1',
       'game': {'package': 'walker-tinknockout-tharun-m', 'godot_folder': 'godot',
                'revision': sheet['metadata']['game']['revision'], 'docs_revision': REV,
                'engine': '4.7.2.stable.official.ed1daf0bf', 'renderer': 'Forward+ (Vulkan/MoltenVK)'},
       'files': files, 'components': components, 'excerpts': excerpts, 'exclusions': exclusions,
       'code_result_pairs': pairs, 'source_view_code_result_pairs': sv, 'engine_captures': caps}
(REEL / 'gamedev-evidence.json').write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
print(len(files), 'files,', len(exclusions), 'exclusions,', len(components), 'components,', len(excerpts),
      'excerpts,', len(pairs), '+', len(sv), 'pairs')
