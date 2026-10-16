# ASSET 3 "toybox" (CHANGE-BRIEF.md, Assignment 3, A3.2) — SCRIPT ROUTE, not MCP.
# Run headless from the repo root:
#   blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_toybox.py
import os, sys
import bpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import empty_metric_scene, flat_material, box, join_at_origin

empty_metric_scene()
body = box("body", (1.20, 0.70, 0.65), (0, 0, 0.325), flat_material("toybox_red", "#B5302A"))
lid = box("lid", (1.26, 0.76, 0.10), (0, 0, 0.70), flat_material("toybox_cream", "#E8DCC0"))
band = box("band", (1.22, 0.72, 0.08), (0, 0, 0.34), flat_material("toybox_navy", "#23395B"))
# Latch on the -Y (front) face just under the lid: Y -0.38..-0.35, Z 0.53-0.65
latch = box("latch", (0.12, 0.03, 0.12), (0, -0.365, 0.59), flat_material("toybox_brass", "#C9A23A"))

join_at_origin("toybox", [body, lid, band, latch])
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath("assets/blender/toybox.blend"))
