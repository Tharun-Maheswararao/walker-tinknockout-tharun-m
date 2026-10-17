#!/usr/bin/env python3
"""Write gamedev-evidence.json (schema 1, code-then-result-v1) for the A3 props film.

--game is the repo's godot/ folder (identical to commit 1d93dcb). Files added for Assignment 3 are
components; the Assignment 2 slice files are exclusions only if they are byte-identical to the A2
revision 64c037a (checked here), because the A2 film explains them and this film does not.
Blender scripts live outside godot/, so their code->result pairs are recorded separately in
`blender_code_result_pairs` (not checked by verify_gamedev.py).
"""
import hashlib, json, subprocess
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
GAME = REPO / 'godot'
REV = '1d93dcb'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def unchanged_since_a2(rel):
    r = subprocess.run(['git', '-C', str(REPO), 'diff', '--quiet', '64c037a', REV, '--', f'godot/{rel}'])
    return r.returncode == 0 and subprocess.run(
        ['git', '-C', str(REPO), 'cat-file', '-e', f'64c037a:godot/{rel}'], capture_output=True).returncode == 0


inv = sorted(p.relative_to(GAME).as_posix() for p in GAME.rglob('*')
             if p.is_file() and not any(x in ('.godot', '.git') for x in p.relative_to(GAME).parts)
             and p.suffix != '.uid')

COMPONENTS = {
    'props-glb': ('The three exported props (castle, windkey, toybox) as binary glTF with +Y Up, and their Godot '
                  'import settings (scene importer, root scale 1.0). Built in Blender from primitives: castle and '
                  'windkey through the Blender MCP, toybox by the script route; the toybox band green is the '
                  "student's hand edit (08f96cd).", ['B17', 'B18', 'B20']),
    'prop-room': ('prop_room.tscn: floor, one DirectionalLight3D, the saved Camera3D at (0, 1.6, 5.5) and the three '
                  'instanced props at x = -2.2, 0 and 2.0.', ['B17', 'B18']),
    'check': ('tests/check_props3d.gd: headless check of size vs brief (±0.01 m), base at y = 0, scale/rotation, '
              'tallest axis, triangle budget, albedo and front side, plus placement in the room via to_root(); '
              'its first version falsely passed the room check (global_transform outside the tree).',
              ['B19', 'B20', 'B21', 'B22']),
    'render-tools': ('tools/shot_prop_room.gd and tools/shot_prop_views.gd: Claude-made engine renders of the prop '
                     'room (evidence/godot/prop_room.png and the six views); the views script first hit the same '
                     'not-inside-tree mistake.', ['B02', 'B23', 'B24']),
}


def assign(p):
    if p.startswith('assets/props3d/'):
        return ['props-glb'], 'A3 prop .glb export / its Godot import settings'
    if p == 'prop_room/prop_room.tscn':
        return ['prop-room'], 'A3 saved 3D scene'
    if p == 'tests/check_props3d.gd':
        return ['check'], 'A3 headless check script'
    if p in ('tools/shot_prop_room.gd', 'tools/shot_prop_views.gd'):
        return ['render-tools'], 'A3 render tool (evidence, not loaded by the game)'
    return None, None


files, exclusions = [], []
for p in inv:
    comp, role = assign(p)
    if comp:
        files.append({'path': p, 'sha256': sha(GAME / p), 'role': role, 'component_ids': comp})
        continue
    assert unchanged_since_a2(p), 'not an unchanged A2 file: ' + p
    exclusions.append({'path': p, 'reason': (
        'Assignment 2 slice file, byte-identical to revision 64c037a (git diff 64c037a 1d93dcb is empty for it) '
        'and explained in the Assignment 2 film; not part of the three A3 props, which are not yet connected '
        'to the 2D game.')})

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

PAIRS = [
    ('B17', 'B18', 'media/B18.mp4',
     'Movie Maker take of the unchanged prop_room.tscn (isolated copy of 1d93dcb): saved camera 0-4 s, then the same '
     'camera orbits; castle left at x -2.2, key at the origin, toy box right at x 2; every base meets the floor and '
     'its shadow; door and latch face the front; the back of the castle is plain.'),
    ('B19', 'B20', 'media/B20.mp4',
     'Recorded headless output of tests/check_props3d.gd on an isolated copy: RESULT: PASS (0 failing); AABB sizes '
     'equal the brief (Godot Y = height), min_y 0.0000, tris 156/192/48 under 200/250/100, room x ranges, band '
     'albedo #2E7D32; identical to evidence/check_props3d.txt.'),
    ('B21', 'B22', 'media/B22.mp4',
     'Re-creation on a throwaway copy: with line 46 using mi.global_transform, Godot logs !is_inside_tree() and every '
     'room check still PASSes with the castle at x -0.90..0.90 (identity) instead of -3.10..-1.30; a parse error '
     'prints no RESULT line and exits 0.'),
]
pairs = [{'code_beat': c, 'result_beat': r, 'observation': o, 'media': {'path': m, 'sha256': sha(REEL / m)}}
         for c, r, m, o in PAIRS]

BLENDER_PAIRS = [
    ('B07', 'B08', 'tools/blender/build_castle.py', 47, 52, 'media/B08.mp4',
     "The MCP look tool's four views from the student's live session (evidence/blender/03-castle-mcp-look.png): "
     'pink keep, two 12-sided towers, teal cone roofs, dark door on the front.'),
    ('B09', 'B10', 'tools/blender/build_castle.py', 171, 180, 'media/B10.mp4',
     "Student's own screenshot 07: castle at location 0, rotation 0°, scale 1.000, 1.8 × 0.82 × 2.3 m, origin at the base."),
    ('B11', 'B12', 'tools/blender/build_windkey.py', 98, 103, 'media/B12.mp4',
     "Student's own screenshot 06: MCP-built windkey, rotation 0°, scale 1.000, 0.6 × 0.14 × 0.7 m, Triangles 192 / 192."),
    ('B13', 'B14', 'tools/blender/build_toybox.py', 9, 17, 'media/B14.mp4',
     "Student's own screenshot 04: script-route toybox.blend with the navy band from line 12, rotation 0°, scale 1.000, Solid view."),
]
bpairs = []
for c, r, path, a, z, m, o in BLENDER_PAIRS:
    text = '\n'.join((REPO / path).read_text().splitlines()[a - 1:z])
    assert beats[c]['shot']['panel']['code'] == text and beats[r]['shot']['evidence_media'] == m, c
    bpairs.append({'code_beat': c, 'result_beat': r, 'source': {'path': path, 'start_line': a, 'end_line': z,
                   'sha256': sha(REPO / path), 'text': text}, 'observation': o,
                   'media': {'path': m, 'sha256': sha(REEL / m)}})

out = {'schema_version': 1, 'teaching_contract': 'code-then-result-v1',
       'game': {'package': 'walker-tinknockout-tharun-m', 'godot_folder': 'godot',
                'revision': '1d93dcb89ebd16f1d09d423b2787087bebcded5a', 'docs_revision': 'fd99467',
                'engine': '4.7.2.stable.official.ed1daf0bf', 'blender': '5.2.2 LTS'},
       'files': files, 'components': components, 'excerpts': excerpts, 'exclusions': exclusions,
       'code_result_pairs': pairs, 'blender_code_result_pairs': bpairs}
(REEL / 'gamedev-evidence.json').write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
print(len(files), 'files,', len(exclusions), 'exclusions,', len(components), 'components,', len(excerpts),
      'excerpts,', len(pairs), '+', len(bpairs), 'pairs')
