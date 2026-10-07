#!/usr/bin/env python3
"""Write gamedev-evidence.json (schema 1, code-then-result-v1) from the frozen project."""
import hashlib, json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
GAME = REEL.parents[1] / 'godot'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


inv = sorted(p.relative_to(GAME).as_posix() for p in GAME.rglob('*')
             if p.is_file() and not any(x in ('.godot', '.git') for x in p.relative_to(GAME).parts)
             and p.suffix != '.uid')

COMPONENTS = {
    'fighter': ('Fighter state machine (IDLE/WALK/JAB/CUTLASS/POP/BLOCK/REWIND/HURT/EMPTY/KO/WIN), spring/wind '
                'economy, hitboxes and the code-created Sprite2D presentation. Emits signals only; never touches audio.',
                ['B04', 'B06', 'B07']),
    'sfx': ('Event sounds: audio/sfx.gd listens to hit_landed, projectile_fired, rewind_tick and state_changed and '
            'plays one AudioLDM 2 sound per event; the six OGG files and their import settings.',
            ['B08', 'B09']),
    'music': ('MusicGen waltz loop and its controller: quiet on title, full in fight, pitch 0.85 below 25% spring, '
              'low-pass on pause via the Music bus effect, stops on KO.',
              ['B08', 'B12', 'B13']),
    'fighter-art': ('SDXL-Turbo fighter poses (Bolt; Rivet = palette recolour), 480x450 canvases with the feet at '
                    '(240,435), plus anchors.json for key/hand/muzzle positions.',
                    ['B03', 'B05']),
    'props-env': ('Bowl background, winding keys, cutlass, pop-gun and cork textures (SDXL-Turbo, edited).',
                  ['B02', 'B03']),
    'round-flow': ('main.gd round flow (TITLE→INTRO→FIGHT→KO), player input reading, collision gap, corks, hit '
                   'sparks/shake; main.tscn holds only the root node (everything else is created in code); '
                   'controls.gd autoload registers input actions; hud.gd draws health bars and spring dials; '
                   'rivet_brain.gd is Rivet\'s deterministic pattern controller; cork.gd the projectile.',
                   ['B02', 'B07', 'B09', 'B14']),
    'tests': ('tests/test_slice.gd: 25 headless checks through real input, including muted run == unmuted run.',
              ['B11', 'B12']),
    'film-tools': ('tools/capture_film.gd (scripted-input Movie Maker driver for fight-4k) and tools/shots.gd '
                   '(in-engine screenshots, some POSED).',
                   ['B05', 'B07', 'B09']),
}


def assign(p):
    if p == 'fighter/fighter.gd':
        return ['fighter'], 'runtime script: fighter state machine and presentation'
    if p.startswith('audio/sfx.gd') or p.startswith('assets/sfx/'):
        return ['sfx'], 'sound-effect listener / AudioLDM 2 sound asset or its import settings'
    if p.startswith('audio/music.gd') or p.startswith('assets/music/') or p == 'default_bus_layout.tres':
        return ['music'], 'music controller / MusicGen loop / Music+SFX bus layout with PauseMuffle low-pass'
    if p.startswith('assets/fighters/'):
        return ['fighter-art'], 'fighter pose texture, import settings or anchor data'
    if p.startswith('assets/props/') or p.startswith('assets/env/'):
        return ['props-env'], 'prop or environment texture / import settings'
    if p in ('game/main.gd', 'game/main.tscn', 'game/controls.gd', 'project.godot', 'ui/hud.gd',
             'fighter/rivet_brain.gd', 'fighter/cork.gd'):
        return ['round-flow'], 'runtime script, scene or project configuration'
    if p.startswith('tests/'):
        return ['tests'], 'headless test script'
    if p.startswith('tools/'):
        return ['film-tools'], 'evidence capture tool (not loaded by the game)'
    return None, None


files, exclusions = [], []
for p in inv:
    comp, role = assign(p)
    if p == '.gitignore':
        exclusions.append({'path': p, 'reason': 'Version-control ignore list (.godot/, *.import.tmp); not loaded by the engine and not part of the playable system.'})
        continue
    assert comp, p
    files.append({'path': p, 'sha256': sha(GAME / p), 'role': role, 'component_ids': comp})

components = [{'id': cid, 'explanation': e, 'beat_ids': beats,
               'files': [f['path'] for f in files if cid in f['component_ids']]}
              for cid, (e, beats) in COMPONENTS.items()]

sheet = json.loads((REEL / 'beat_sheet.json').read_text())
beats = {b['beat_id']: b for b in sheet['beats']}
SPANS = {'B04': ('fighter/fighter.gd', 71, 74), 'B06': ('fighter/fighter.gd', 206, 214),
         'B08': ('audio/sfx.gd', 30, 36), 'B11': ('tests/test_slice.gd', 207, 212)}
excerpts = []
for bid, (p, a, b) in SPANS.items():
    text = '\n'.join((GAME / p).read_text().splitlines()[a - 1:b])
    assert beats[bid]['shot']['remotion']['props']['code'] == text, bid
    excerpts.append({'beat_id': bid, 'path': p, 'start_line': a, 'end_line': b, 'text': text})

PAIRS = [
    ('B04', 'B05', 'evidence/B05-before-after.png',
     'Same posed jab, before vs after sprite.centered = false: before, both toys are drawn up-left of their green '
     'hurtboxes while the winding keys stay at the feet; after, the art stands inside the box.'),
    ('B06', 'B07', 'media/B07.mp4',
     'fight-4k 10.5–23.5 s: Bolt holds S (REWIND, "rewinding" tag), stands still while the key spins and his '
     'spring dial climbs; Rivet lands hits; later both fighters rewind side by side.'),
    ('B08', 'B09', 'media/B09.mp4',
     'fight-4k 1.8–18.9 s: jab exchange with sparks/hitstop, BLOCK and HURT poses, Bolt\'s pop-gun shot, then '
     'the EMPTY tag; each event is one emitted signal (sounds heard in B10, not under narration).'),
    ('B11', 'B12', 'evidence/B12-test-output.png',
     'Recorded output of a fresh isolated run: 25 checks, 0 failed; muted and unmuted end states identical; '
     'check_seam.py PASS; engine exit warnings shown as printed.'),
]
pairs = [{'code_beat': c, 'result_beat': r, 'observation': o,
          'media': {'path': m, 'sha256': sha(REEL / m)}} for c, r, m, o in PAIRS]

out = {'schema_version': 1, 'teaching_contract': 'code-then-result-v1',
       'game': {'package': 'walker-tinknockout-tharun-m', 'godot_folder': 'godot', 'revision': '64c037a',
                'engine': '4.7.2.stable.official.ed1daf0bf'},
       'files': files, 'components': components, 'excerpts': excerpts, 'exclusions': exclusions,
       'code_result_pairs': pairs}
(REEL / 'gamedev-evidence.json').write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
print(len(files), 'files,', len(exclusions), 'exclusions,', len(components), 'components')
