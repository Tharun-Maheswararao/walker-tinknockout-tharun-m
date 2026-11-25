#!/usr/bin/env python3
"""Remove the instructor's channel handle from the toolkit's GodotDevWorkbench renders (B02, B11).

GodotDevWorkbench.tsx (line 73 in _brutalist) hardcodes '@NikBearBrown' at the bottom right; this film must carry no
instructor name, persona, handle or credit line, and the shared toolkit is not ours to edit. After
runtime/scripts/remotion_scenes.py renders a beat, this keeps the untouched render as media/_work/<id>.remotion.mp4
and writes media/<id>.mp4 with that corner (x 3180-3720, y 1960-2090 of 3840x2160, empty page apart from the handle)
painted the page colour. Nothing else in the frame changes. Re-runnable: it always starts from the kept render.
Usage: mask_handle.py B02 B11
"""
import shutil, subprocess, sys
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
for bid in sys.argv[1:]:
    out = REEL / 'media' / f'{bid}.mp4'
    keep = REEL / 'media' / '_work' / f'{bid}.remotion.mp4'
    keep.parent.mkdir(parents=True, exist_ok=True)
    marker = REEL / 'media' / '_work' / f'{bid}.masked'
    if not marker.exists() or out.stat().st_mtime > marker.stat().st_mtime + 2:
        shutil.copy2(out, keep)                      # a fresh Remotion render: keep it untouched
    tmp = out.with_suffix('.tmp.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(keep), '-vf',
                    'drawbox=x=3180:y=1960:w=540:h=130:color=0xFAF9F5:t=fill', '-c:v', 'libx264', '-preset', 'medium',
                    '-crf', '14', '-pix_fmt', 'yuv420p', '-an', str(tmp)], check=True)
    tmp.replace(out)
    marker.write_text(f'masked from {keep.name}\n')
    print('masked', out)
