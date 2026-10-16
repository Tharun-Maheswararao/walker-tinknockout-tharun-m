# ASSET 2 "windkey" (CHANGE-BRIEF.md, Assignment 3, A3.2) — SCRIPT ROUTE, not MCP. Superseded by the MCP build in build_windkey.py; kept for comparison.
# Run headless from the repo root:
#   blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_windkey_script_route.py
import math, os, sys
import bpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import empty_metric_scene, flat_material, join_at_origin

empty_metric_scene()
brass = flat_material("key_brass", "#C9A23A")
dark = flat_material("key_brass_dark", "#8C6A1E")

# Shaft: cylinder r 0.04, h 0.36, 8 sides, Z 0-0.36
bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.04, depth=0.36, end_fill_type='NGON', location=(0, 0, 0.18))
shaft = bpy.context.active_object; shaft.name = "shaft"; shaft.data.materials.append(brass)
# Collar: cylinder r 0.07, h 0.04, 12 sides, Z 0.36-0.40
bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.07, depth=0.04, end_fill_type='NGON', location=(0, 0, 0.38))
collar = bpy.context.active_object; collar.name = "collar"; collar.data.materials.append(dark)
# Bow lobes: cylinders r 0.15, depth 0.06, 16 sides, rotated 90 deg about X (faces point +-Y), X = +-0.15, Z = 0.55
lobes = []
for side, x in (("L", -0.15), ("R", 0.15)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.15, depth=0.06, end_fill_type='NGON',
                                        location=(x, 0, 0.55), rotation=(math.radians(90), 0, 0))
    lobe = bpy.context.active_object; lobe.name = "lobe_" + side; lobe.data.materials.append(brass)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    lobes.append(lobe)

join_at_origin("windkey", [shaft, collar] + lobes)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath("assets/blender/windkey.blend"))
