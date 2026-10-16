# ASSET 2 "windkey" (CHANGE-BRIEF.md, Assignment 3, A3.2).
# The execute_blender_code bodies sent over Blender MCP, copied in the order they ran (calls 0-7).
# Each call ran on its own, so the material helper is repeated in the calls that create materials.
# Two read-only checks are left out: before call 0, one confirmed the open toybox.blend had no unsaved changes;
# after call 7, one read back the sidebar, Item tab, statistics overlay and shading settings.
# Call 0 saves over assets/blender/windkey.blend, and calls 6-7 save it again.
# Run in Blender's Text Editor, or headless:
#   blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_windkey.py

# ---------------------------------------------------------------------------
# Call 0: empty scene, metric units, 1 BU = 1 m; switch the open file to windkey.blend
import bpy

for ob in list(bpy.data.objects):
    bpy.data.objects.remove(ob, do_unlink=True)
for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
    for block in list(coll):
        if block.users == 0:
            coll.remove(block)

us = bpy.context.scene.unit_settings
us.system = 'METRIC'
us.scale_length = 1.0
us.length_unit = 'METERS'
bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)

bpy.ops.wm.save_as_mainfile(filepath="/Users/tharunmaheswararao/Documents/csye7270/walker-tinknockout-tharun-m/assets/blender/windkey.blend")

print("objects:", len(bpy.data.objects), "meshes:", len(bpy.data.meshes), "materials:", len(bpy.data.materials))
print("units:", us.system, us.scale_length, us.length_unit)
print("file:", bpy.data.filepath)

# ---------------------------------------------------------------------------
# Call 1: shaft — cylinder r 0.04, h 0.36, 8 sides, n-gon caps, Z 0-0.36, polished brass #C9A23A
import bpy

def flat_material(name, hex_rgb):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
    def lin(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    rgb = [lin(int(hex_rgb[i:i + 2], 16)) for i in (1, 3, 5)]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.5
    bsdf.inputs["Metallic"].default_value = 0.0
    mat.diffuse_color = (*rgb, 1.0)
    return mat

bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.04, depth=0.36,
                                    end_fill_type='NGON', location=(0.0, 0.0, 0.18))
shaft = bpy.context.active_object
shaft.name = "shaft"
shaft.data.materials.append(flat_material("key_brass", "#C9A23A"))

print(shaft.name, "dims", tuple(round(d, 4) for d in shaft.dimensions),
      "faces", len(shaft.data.polygons),
      "tris", sum(len(p.vertices) - 2 for p in shaft.data.polygons))

# ---------------------------------------------------------------------------
# Call 2: collar — cylinder r 0.07, h 0.04, 12 sides, n-gon caps, Z 0.36-0.40, dark brass #8C6A1E
import bpy

def flat_material(name, hex_rgb):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
    def lin(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    rgb = [lin(int(hex_rgb[i:i + 2], 16)) for i in (1, 3, 5)]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.5
    bsdf.inputs["Metallic"].default_value = 0.0
    mat.diffuse_color = (*rgb, 1.0)
    return mat

bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.07, depth=0.04,
                                    end_fill_type='NGON', location=(0.0, 0.0, 0.38))
collar = bpy.context.active_object
collar.name = "collar"
collar.data.materials.append(flat_material("key_brass_dark", "#8C6A1E"))

print(collar.name, "dims", tuple(round(d, 4) for d in collar.dimensions),
      "faces", len(collar.data.polygons),
      "tris", sum(len(p.vertices) - 2 for p in collar.data.polygons))

# ---------------------------------------------------------------------------
# Call 3: left bow lobe — cylinder r 0.15, depth 0.06, 16 sides, n-gon caps,
# rotated 90 deg about X (round faces point +/-Y), centre X = -0.15, Z = 0.55, brass; rotation applied
import bpy, math

bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.15, depth=0.06, end_fill_type='NGON',
                                    location=(-0.15, 0.0, 0.55), rotation=(math.radians(90), 0.0, 0.0))
lobe = bpy.context.active_object
lobe.name = "lobe_L"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
lobe.data.materials.append(bpy.data.materials["key_brass"])

print(lobe.name, "dims", tuple(round(d, 4) for d in lobe.dimensions),
      "rot", tuple(round(math.degrees(a), 3) for a in lobe.rotation_euler),
      "faces", len(lobe.data.polygons),
      "tris", sum(len(p.vertices) - 2 for p in lobe.data.polygons))

# ---------------------------------------------------------------------------
# Call 4: right bow lobe — cylinder r 0.15, depth 0.06, 16 sides, n-gon caps,
# rotated 90 deg about X (round faces point +/-Y), centre X = +0.15, Z = 0.55, brass; rotation applied
import bpy, math

bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.15, depth=0.06, end_fill_type='NGON',
                                    location=(0.15, 0.0, 0.55), rotation=(math.radians(90), 0.0, 0.0))
lobe = bpy.context.active_object
lobe.name = "lobe_R"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
lobe.data.materials.append(bpy.data.materials["key_brass"])

print(lobe.name, "dims", tuple(round(d, 4) for d in lobe.dimensions),
      "rot", tuple(round(math.degrees(a), 3) for a in lobe.rotation_euler),
      "faces", len(lobe.data.polygons),
      "tris", sum(len(p.vertices) - 2 for p in lobe.data.polygons))

# ---------------------------------------------------------------------------
# Call 5: join the four parts into "windkey", origin at base centre (0,0,0), apply rotation and scale
import bpy

parts = ["shaft", "collar", "lobe_L", "lobe_R"]
bpy.ops.object.select_all(action='DESELECT')
for name in parts:
    bpy.data.objects[name].select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects["shaft"]
bpy.ops.object.join()

key = bpy.context.active_object
key.name = "windkey"
key.data.name = "windkey"

bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
key.location = (0.0, 0.0, 0.0)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

xs = [v.co.x for v in key.data.vertices]
ys = [v.co.y for v in key.data.vertices]
zs = [v.co.z for v in key.data.vertices]
print("name", key.name, "mesh", key.data.name, "objects in scene", len(bpy.data.objects))
print("dims", tuple(round(d, 4) for d in key.dimensions))
print("x", round(min(xs), 4), round(max(xs), 4), "y", round(min(ys), 4), round(max(ys), 4),
      "z", round(min(zs), 4), round(max(zs), 4))
print("location", tuple(key.location), "rotation", tuple(key.rotation_euler), "scale", tuple(key.scale))
print("materials", [m.name for m in key.data.materials])
print("faces", len(key.data.polygons),
      "tris", sum(len(p.vertices) - 2 for p in key.data.polygons))

# ---------------------------------------------------------------------------
# Call 6: save the open file (windkey.blend)
import bpy

bpy.ops.wm.save_mainfile()
print("saved", bpy.data.filepath)

# ---------------------------------------------------------------------------
# Call 7: set up the 3D viewport for a screenshot (sidebar Item tab, statistics, material shading,
# windkey selected and framed), then save again
import bpy

key = bpy.data.objects["windkey"]
bpy.ops.object.select_all(action='DESELECT')
key.select_set(True)
bpy.context.view_layer.objects.active = key

done = 0
for window in bpy.context.window_manager.windows:
    for area in window.screen.areas:
        if area.type != 'VIEW_3D':
            continue
        space = area.spaces.active
        space.show_region_ui = True
        space.overlay.show_stats = True
        space.shading.type = 'MATERIAL'
        for region in area.regions:
            if region.type == 'UI':
                try:
                    region.active_panel_category = 'Item'
                except Exception as e:
                    print("Item tab not set:", e)
        win_region = next(r for r in area.regions if r.type == 'WINDOW')
        with bpy.context.temp_override(window=window, area=area, region=win_region):
            bpy.ops.view3d.view_selected()
        done += 1

bpy.ops.wm.save_mainfile()
print("viewports set up:", done, "active", bpy.context.view_layer.objects.active.name,
      "saved", bpy.data.filepath)
