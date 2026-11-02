#!/usr/bin/env python3
"""Write gamedev-evidence.json (schema 1, code-then-result-v1) for the A5 shaders film.

--game is the repo's godot/ folder at 93aedd9: identical to 2e6946d except the comment-only annotation of
shaders/standard_generated.gdshader (e4c188f) and tools/a5_capture_side_by_side.gd (b2b8780). Files added or
changed for Assignment 5 (git diff 23a0363..HEAD) are components; every other file is an exclusion only if it is
byte-identical to the pre-A5 revision 23a0363 (checked here), because earlier films explain it.
Only B03 uses GodotDevWorkbench; the source-view composites (B05, B07, B09, B12) are recorded separately in
`source_view_code_result_pairs` (verbatim text + hashes; not checked by verify_gamedev.py).
"""
import hashlib, json, subprocess
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
GAME = REPO / 'godot'
PRE = '23a0363'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def unchanged_since_pre(rel):
    r = subprocess.run(['git', '-C', str(REPO), 'diff', '--quiet', PRE, 'HEAD', '--', f'godot/{rel}'])
    return r.returncode == 0 and subprocess.run(
        ['git', '-C', str(REPO), 'cat-file', '-e', f'{PRE}:godot/{rel}'], capture_output=True).returncode == 0


inv = sorted(p.relative_to(GAME).as_posix() for p in GAME.rglob('*')
             if p.is_file() and not any(x in ('.godot', '.git') for x in p.relative_to(GAME).parts)
             and p.suffix != '.uid')

COMPONENTS = {
    'rewind-tint': ('REWIND tint: rewind_tint.gdshader (canvas_item; colour line suggested by Claude, typed by Tharun) on '
                    'one ShaderMaterial per fighter, fed by rewind_tint_driver.gd (Claude, agent session) from '
                    'fighter.state with move_toward x delta; attached in main.gd; F9 debug captures in debug_capture.gd.',
                    ['B03', 'B04', 'B05', 'B06']),
    'painted-tin': ('painted_tin.gdshader (spatial; skeleton suggested by Claude, typed and filled by Tharun) with three '
                    'Poly Haven Metal Plate samplers (colour, normal, roughness as wear mask); two materials '
                    'toybox_fresh / toybox_worn; Use External wiring in toybox.glb.import and the second toy box in '
                    'prop_room.tscn; audit in MATERIALS.md.', ['B02', 'B07', 'B08', 'B09', 'B11']),
    'language': ('Hint experiment (hint_experiment.gdshader, the 3x1 PNG, two materials and scene) and the editor-'
                 'generated standard_generated.gdshader annotated by Tharun.', ['B10', 'B12']),
    'tests': ('test_rewind_tint.gd (agent; R1-R6 at 30/60/144 through real input), test_materials.gd (Claude audit), '
              'and the normal-map calibration/check scripts.', ['B13', 'B14']),
    'capture-tools': ('Claude-made windowed capture tools and resource builders (tools/a5_*.gd, make_*.gd, '
                      'write_hint_png.gd); evidence only, not loaded by the game.', ['B04', 'B08', 'B10', 'B11']),
    'project': ('project.godot: reordered rendering lines only (the A5 import pass); renderer and settings unchanged.',
                ['B13']),
}


def assign(p):
    if p in ('shaders/rewind_tint.gdshader', 'fighter/rewind_tint_driver.gd', 'game/main.gd', 'game/debug_capture.gd'):
        return ['rewind-tint'], 'A5 REWIND tint shader / driver / attachment'
    if p in ('shaders/painted_tin.gdshader', 'assets/props3d/toybox.glb.import', 'prop_room/prop_room.tscn',
             'MATERIALS.md') or p.startswith('prop_room/materials/') or p.startswith('assets/textures/metal_plate/'):
        return ['painted-tin'], 'A5 textured shader, materials, textures and wiring'
    if p.startswith('hint_experiment/') or p.startswith('assets/textures/hint/') or p in (
            'shaders/hint_experiment.gdshader', 'shaders/standard_generated.gdshader'):
        return ['language'], 'A5 hint experiment / generated shader'
    if p in ('tests/test_rewind_tint.gd', 'tests/test_materials.gd', 'tests/calibrate_normal_map.gd',
             'tests/normal_map_check.gd'):
        return ['tests'], 'A5 headless tests'
    if p.startswith('tools/a5_') or p in ('tools/make_hint_scene.gd', 'tools/make_toybox_materials.gd',
                                          'tools/write_hint_png.gd'):
        return ['capture-tools'], 'A5 capture / builder tool (evidence, not loaded by the game)'
    if p == 'project.godot':
        return ['project'], 'project settings'
    return None, None


files, exclusions = [], []
for p in inv:
    comp, role = assign(p)
    if comp:
        files.append({'path': p, 'sha256': sha(GAME / p), 'role': role, 'component_ids': comp})
        continue
    assert unchanged_since_pre(p), 'not an unchanged pre-A5 file: ' + p
    exclusions.append({'path': p, 'reason': (
        f'Pre-Assignment-5 file, byte-identical to revision {PRE} (git diff {PRE} HEAD is empty for it) and explained '
        'in the earlier films; A5 does not change it.')})

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
          'In-engine captures (scripted input) at rewind_amount 0.0 / 0.5 / 1.0 / 2.0: the colour line output at '
          "Bolt's chest and helmet equals Tharun's hand predictions (12 of 12 channels at 0 and 0.5; four channels -1 "
          'at 1.0); at 2.0 both pixels are the pure tint (90, 160, 255).')]
pairs = [{'code_beat': c, 'result_beat': r, 'observation': o, 'media': {'path': m, 'sha256': sha(REEL / m)}}
         for c, r, m, o in PAIRS]

SV = [('B05', 'B06', 'media/B06.mp4', 'Movie Maker capture (scripted input, isolated copy of 2e6946d): Bolt tints '
       'blue within 5 frames of the press, Rivet hits him (REWIND -> HURT) and the tint fades out from 1.0; readout '
       'from the per-frame log.'),
      ('B07', 'B08', 'media/B08.mp4', 'Edit checks: the shader edit changed both boxes (88 px, 1622 px); the material '
       'edit changed only the worn box (6698 px); castle 0 px both times.'),
      ('B09', 'B10', 'media/B10.mp4', 'Hint experiment capture: quad S shows 64/128/192, quad D 137/188/225, exactly '
       "as Tharun predicted by hand."),
      ('B12', 'B13', 'media/B13.mp4', 'Recorded test output, including m3: removing source_color from painted_tin '
       'line 3 fails 1 of 55 checks.')]
sv = []
for c, r, m, o in SV:
    p = beats[c]['shot']['panel']
    src = p.get('files') or [[('godot/' if not p['path'].startswith('godot/') else '') + p['path'], a, z]
                             for a, z in p['segments']]
    sv.append({'code_beat': c, 'result_beat': r,
               'sources': [{'path': f, 'start_line': a, 'end_line': z, 'sha256': sha(REPO / f),
                            'text': '\n'.join((REPO / f).read_text().splitlines()[a - 1:z])} for f, a, z in src],
               'observation': o, 'media': {'path': m, 'sha256': sha(REEL / m)}})
    assert beats[r]['shot']['evidence_media'] == m and list(beats)[list(beats).index(c) + 1] == r, c

out = {'schema_version': 1, 'teaching_contract': 'code-then-result-v1',
       'game': {'package': 'walker-tinknockout-tharun-m', 'godot_folder': 'godot',
                'revision': sheet['metadata']['game']['revision'], 'docs_revision': '93aedd9',
                'engine': '4.7.2.stable.official.ed1daf0bf', 'renderer': 'Forward+ (Vulkan/MoltenVK)'},
       'files': files, 'components': components, 'excerpts': excerpts, 'exclusions': exclusions,
       'code_result_pairs': pairs, 'source_view_code_result_pairs': sv}
(REEL / 'gamedev-evidence.json').write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
print(len(files), 'files,', len(exclusions), 'exclusions,', len(components), 'components,', len(excerpts),
      'excerpts,', len(pairs), '+', len(sv), 'pairs')
