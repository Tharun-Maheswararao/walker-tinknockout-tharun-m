# ASSET 1 "castle" (CHANGE-BRIEF.md, Assignment 3, A3.2).
# The execute_blender_code bodies sent over Blender MCP, copied in the order they ran (calls 0-7).
# Each call ran on its own, so the material helper is repeated in the calls that create materials.
# Run in Blender's Text Editor, or headless:
#   blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_castle.py

# ---------------------------------------------------------------------------
# Call 0: empty scene, metric units, 1 BU = 1 m
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

print("objects:", len(bpy.data.objects), "meshes:", len(bpy.data.meshes), "materials:", len(bpy.data.materials))
print("units:", us.system, us.scale_length, us.length_unit)

# ---------------------------------------------------------------------------
# Call 1: keep — cube 1.20 x 0.80 x 1.40 m, Z 0-1.40, faded aquarium pink #D98BA0
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

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.70))
keep = bpy.context.active_object
keep.name = "keep"
keep.scale = (1.20, 0.80, 1.40)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
keep.data.materials.append(flat_material("castle_pink", "#D98BA0"))

print(keep.name, "dims", tuple(round(d, 4) for d in keep.dimensions),
      "faces", len(keep.data.polygons),
      "tris", sum(len(p.vertices) - 2 for p in keep.data.polygons))

# ---------------------------------------------------------------------------
# Call 2: left tower — cylinder r 0.30, h 1.80, 12 sides, n-gon caps, X = -0.60, Z 0-1.80, pink
import bpy

bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.30, depth=1.80,
                                    end_fill_type='NGON', location=(-0.60, 0.0, 0.90))
tower = bpy.context.active_object
tower.name = "tower_L"
tower.data.materials.append(bpy.data.materials["castle_pink"])

print(tower.name, "dims", tuple(round(d, 4) for d in tower.dimensions),
      "faces", len(tower.data.polygons),
      "tris", sum(len(p.vertices) - 2 for p in tower.data.polygons))

# ---------------------------------------------------------------------------
# Call 3: right tower — cylinder r 0.30, h 1.80, 12 sides, n-gon caps, X = +0.60, Z 0-1.80, pink
import bpy

bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.30, depth=1.80,
                                    end_fill_type='NGON', location=(0.60, 0.0, 0.90))
tower = bpy.context.active_object
tower.name = "tower_R"
tower.data.materials.append(bpy.data.materials["castle_pink"])

print(tower.name, "dims", tuple(round(d, 4) for d in tower.dimensions),
      "faces", len(tower.data.polygons),
      "tris", sum(len(p.vertices) - 2 for p in tower.data.polygons))

# ---------------------------------------------------------------------------
# Call 4: left roof — cone r 0.30, h 0.50, 12 sides, n-gon base, X = -0.60, Z 1.80-2.30, verdigris teal #3E8E86
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

bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.30, radius2=0.0, depth=0.50,
                                end_fill_type='NGON', location=(-0.60, 0.0, 2.05))
roof = bpy.context.active_object
roof.name = "roof_L"
roof.data.materials.append(flat_material("castle_teal", "#3E8E86"))

print(roof.name, "dims", tuple(round(d, 4) for d in roof.dimensions),
      "faces", len(roof.data.polygons),
      "tris", sum(len(p.vertices) - 2 for p in roof.data.polygons))

# ---------------------------------------------------------------------------
# Call 5: right roof — cone r 0.30, h 0.50, 12 sides, n-gon base, X = +0.60, Z 1.80-2.30, teal
import bpy

bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.30, radius2=0.0, depth=0.50,
                                end_fill_type='NGON', location=(0.60, 0.0, 2.05))
roof = bpy.context.active_object
roof.name = "roof_R"
roof.data.materials.append(bpy.data.materials["castle_teal"])

print(roof.name, "dims", tuple(round(d, 4) for d in roof.dimensions),
      "faces", len(roof.data.polygons),
      "tris", sum(len(p.vertices) - 2 for p in roof.data.polygons))

# ---------------------------------------------------------------------------
# Call 6: door — cube 0.40 x 0.04 x 0.70 m on the keep's -Y face (Y = -0.40),
# protruding 0.02 (spans Y -0.42 to -0.38), Z 0-0.70, dark brown #3A2A20
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

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -0.40, 0.35))
door = bpy.context.active_object
door.name = "door"
door.scale = (0.40, 0.04, 0.70)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
door.data.materials.append(flat_material("castle_door_brown", "#3A2A20"))

print(door.name, "dims", tuple(round(d, 4) for d in door.dimensions),
      "faces", len(door.data.polygons),
      "tris", sum(len(p.vertices) - 2 for p in door.data.polygons))

# ---------------------------------------------------------------------------
# Call 7: join the six parts into "castle", origin at base centre (0,0,0), apply rotation and scale
import bpy

parts = ["keep", "tower_L", "tower_R", "roof_L", "roof_R", "door"]
bpy.ops.object.select_all(action='DESELECT')
for name in parts:
    bpy.data.objects[name].select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects["keep"]
bpy.ops.object.join()

castle = bpy.context.active_object
castle.name = "castle"
castle.data.name = "castle"

bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
castle.location = (0.0, 0.0, 0.0)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

zs = [v.co.z for v in castle.data.vertices]
xs = [v.co.x for v in castle.data.vertices]
ys = [v.co.y for v in castle.data.vertices]
print("name", castle.name, "objects in scene", len(bpy.data.objects))
print("dims", tuple(round(d, 4) for d in castle.dimensions))
print("x", round(min(xs), 4), round(max(xs), 4), "y", round(min(ys), 4), round(max(ys), 4),
      "z", round(min(zs), 4), round(max(zs), 4))
print("location", tuple(castle.location), "rotation", tuple(castle.rotation_euler), "scale", tuple(castle.scale))
print("materials", [m.name for m in castle.data.materials])
print("faces", len(castle.data.polygons),
      "tris", sum(len(p.vertices) - 2 for p in castle.data.polygons))
