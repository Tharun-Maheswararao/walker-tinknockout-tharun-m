# Shared helpers for the A3 script-route builds (build_windkey.py, build_toybox.py).
import bpy

def empty_metric_scene():
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    us = bpy.context.scene.unit_settings
    us.system, us.scale_length, us.length_unit = 'METRIC', 1.0, 'METERS'
    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)

def flat_material(name, hex_rgb):
    """Flat colour in the Principled BSDF Base Color (what glTF exports)."""
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
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

def box(name, size, location, mat):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    ob.data.materials.append(mat)
    return ob

def join_at_origin(name, parts):
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    ob = bpy.context.active_object
    ob.name = ob.data.name = name
    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    ob.location = (0.0, 0.0, 0.0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    me = ob.data
    zs = [v.co.z for v in me.vertices]
    print("RESULT", name, "dims", tuple(round(d, 4) for d in ob.dimensions),
          "zmin", round(min(zs), 4), "rot", tuple(ob.rotation_euler), "scale", tuple(ob.scale),
          "tris", sum(len(p.vertices) - 2 for p in me.polygons),
          "materials", [m.name for m in me.materials])
    return ob
