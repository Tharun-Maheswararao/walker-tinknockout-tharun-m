#!/usr/bin/env python3
"""Write gamedev-evidence.json (schema 1, code-then-result-v1) for the A6 particle-effects film.

--game is the repo's godot/ folder at c844ab2 (HEAD; the working tree has no godot/ changes, asserted).
Files added or changed for Assignment 6 (git diff f4dda68..c844ab2, f4dda68 = tag a5) are components; every other
file is an exclusion only if it is byte-identical to a5 (checked here), because the earlier films explain it.
Only B05 uses GodotDevWorkbench (the checked excerpt); the source-view composites (B07, B09, B12, B14, B17; B03 shows each line and its strip result in the same beat) are
recorded separately in `source_view_code_result_pairs` (verbatim text + hashes; not checked by verify_gamedev.py).
Adapted from the A5 film's _tools/make_evidence.py.
"""
import hashlib, json, subprocess
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
GAME = REPO / 'godot'
PRE = 'f4dda68'
REV = 'c844ab2'

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
    'effect-a': ('Effect A, impact burst: impact_effect.tscn (Shards MIX, Core ADD; tuned Shards ramp, revision 1) and '
                 'impact_effect_blocked.tscn, instanced per impact by main._spawn_impact (blocked flag, child of Main '
                 'at p, restart() after add_child, freed on finished).',
                 ['B02', 'B03', 'B05', 'B06', 'B07', 'B08', 'B09', 'B10']),
    'effect-b': ('Effect B, wind steam: wind_steam.tscn (amount 25, amount_ratio 0, local_coords) on SteamMount '
                 '(steam_mount.gd; follows the key but not its rewind squash, revision 1), attached and driven in '
                 'main.gd (steam_ratio = clamp((25 - wind) / 25, 0, 1)).', ['B02', 'B12', 'B13', 'B14', 'B15', 'B16']),
    'textures': ('Both particle textures written by code: generate_shard_texture.gd -> shard_8.png, '
                 'generate_steam_texture.gd -> steam_32.png, import sidecars and ATTRIBUTION.md.', ['B21', 'B23']),
    'fixtures': ('Strip fixtures, not part of the game: impact_preview, steam_preview, steam_rewind_preview (fixed seed); '
                 'gpu_price fixture and the F10 vsync key (debug_vsync.gd) for the open GPU price.',
                 ['B06', 'B13', 'B14', 'B19', 'B22']),
    'process-shader': ('particles_generated.gdshader: Effect B\'s ParticleProcessMaterial converted in the editor by '
                       'Tharun; not used by the game.', ['B17']),
    'tests': ('test_impact_effect_config (136), test_impact_effect_state (44), test_wind_steam_config (33), '
              'test_wind_steam_state (37), cost_effects (headless wall-clock price).', ['B18', 'B19']),
}


def assign(p):
    if p in ('effects/impact_effect.tscn', 'effects/impact_effect_blocked.tscn', 'game/main.gd'):
        return ['effect-a', 'effect-b'] if p == 'game/main.gd' else ['effect-a'], 'A6 Effect A scene / wiring'
    if p in ('effects/wind_steam.tscn', 'effects/steam_mount.gd'):
        return ['effect-b'], 'A6 Effect B scene / mount'
    if p.startswith('effects/textures/') or p in ('tools/generate_shard_texture.gd', 'tools/generate_steam_texture.gd'):
        return ['textures'], 'A6 code-written texture / its script / credits'
    if p.startswith('previews/') or p == 'game/debug_vsync.gd':
        return ['fixtures'], 'A6 fixture (not part of the game) / vsync debug key'
    if p == 'shaders/particles_generated.gdshader':
        return ['process-shader'], 'A6 generated process shader (Tharun, editor)'
    if p in ('tests/test_impact_effect_config.gd', 'tests/test_impact_effect_state.gd', 'tests/test_wind_steam_config.gd',
             'tests/test_wind_steam_state.gd', 'tests/cost_effects.gd'):
        return ['tests'], 'A6 headless test / cost script'
    return None, None


files, exclusions = [], []
for p in inv:
    comp, role = assign(p)
    if comp:
        files.append({'path': p, 'sha256': sha(GAME / p), 'role': role, 'component_ids': comp})
        continue
    assert unchanged_since_pre(p), 'not an unchanged pre-A6 file: ' + p
    exclusions.append({'path': p, 'reason': (
        f'Pre-Assignment-6 file, byte-identical to tag a5 ({PRE}); explained in the earlier films; A6 does not change '
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

PAIRS = [('B05', 'B06', 'media/B06.mp4',
          'Fixture strip r0 (impact_preview.tscn, fixed seed, captured by Tharun): the burst is on screen in frame 10 '
          'itself (explosiveness 1.0, one shot), 16 shards fall into a ring below the fist, frames 20, 30, 50 empty '
          '(lifetime 0.25); the shards are faint at frame 15 (median drop 41).')]
pairs = [{'code_beat': c, 'result_beat': r, 'observation': o, 'media': {'path': m, 'sha256': sha(REEL / m)}}
         for c, r, m, o in PAIRS]

SV = [('B07', 'B08', 'media/B08.mp4', 'r0 vs r1: frame 15 median darkening 41.3 -> 105.7; count +16 %; frames 20+ '
       'pixel-identical; Tharun in game: faded smoothly, Keep.'),
      ('B09', 'B10', 'media/B10.mp4', 'Movie Maker capture (scripted input, isolated copy of c844ab2): every landed jab '
       'bursts, every other jab is blocked and gets the grey burst, Rivet\'s hits burst too; node counts from the log.'),
      ('B12', 'B13', 'media/B13.mp4', 'Fixture strip D.2 r0: plume at frame 40, tail at 55, empty at 70; Tharun: half '
       'of Bolt\'s height; Claude measured about a quarter.'),
      ('B14', 'B15', 'media/B15.mp4', 'Rewind r0 vs r1: only frame 34 differs (1021 px), a full plume where r0 had a '
       'sliver; Tharun in game: tapered off smoothly, Keep.'),
      ('B17', 'B18', 'media/B18.mp4', 'test_wind_steam_config reads spread 30 and gravity (0, -180, 0) back from the '
       'material the generated shader declares; 33 checks, 0 failed.')]
sv = []
for c, r, m, o in SV:
    p = beats[c]['shot']['panel']
    src = p.get('files') or [[p['path'], a, z] for a, z in p['segments']]
    sv.append({'code_beat': c, 'result_beat': r,
               'sources': [{'path': f, 'start_line': a, 'end_line': z, 'sha256': sha(REPO / f),
                            'text': '\n'.join((REPO / f).read_text().splitlines()[a - 1:z])} for f, a, z in src],
               'observation': o, 'media': {'path': m, 'sha256': sha(REEL / m)}})
    assert list(beats).index(r) == list(beats).index(c) + 1, c

cap = REEL / 'capture' / 'play-4k.mp4'
out = {'schema_version': 1, 'teaching_contract': 'code-then-result-v1',
       'game': {'package': 'walker-tinknockout-tharun-m', 'godot_folder': 'godot',
                'revision': sheet['metadata']['game']['revision'], 'docs_revision': REV,
                'engine': '4.7.2.stable.official.ed1daf0bf', 'renderer': 'Forward+ (Vulkan/MoltenVK)'},
       'files': files, 'components': components, 'excerpts': excerpts, 'exclusions': exclusions,
       'code_result_pairs': pairs, 'source_view_code_result_pairs': sv,
       'engine_capture': {'path': 'capture/play-4k.mp4', 'sha256': sha(cap), 'frames': 382, 'fps': 30,
                          'size': '3840x2160', 'revision': REV, 'method': 'Movie Maker, windowed, scripted input',
                          'log': 'evidence/runs/play-capture-log.txt'}}
(REEL / 'gamedev-evidence.json').write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
print(len(files), 'files,', len(exclusions), 'exclusions,', len(components), 'components,', len(excerpts),
      'excerpts,', len(pairs), '+', len(sv), 'pairs')
