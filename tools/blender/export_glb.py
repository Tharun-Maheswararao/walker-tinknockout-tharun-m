# Export the open .blend as binary glTF with +Y Up (A3 export step, all three assets).
#   blender -b assets/blender/<asset>.blend --python-exit-code 1 --python tools/blender/export_glb.py -- godot/assets/props3d/<asset>.glb
import os, sys
import bpy
out = os.path.abspath(sys.argv[sys.argv.index("--") + 1])
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', export_yup=True, export_apply=True)
print("EXPORTED", out, os.path.getsize(out), "bytes")
