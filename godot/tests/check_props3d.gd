# A3 headless check: loads each .glb and prop_room.tscn and prints what the
# importer actually produced, compared with CHANGE-BRIEF.md (Assignment 3).
#   timeout 120 godot --headless --path godot --script res://tests/check_props3d.gd --fixed-fps 60
# What it shows: size, base height, node scale/rotation, tallest axis,
# triangle count, colours, and which side the door/latch faces.
# What it does NOT show: whether the props look right, read as what they
# are, or suit the game's lighting. That is the human check.
extends SceneTree

const TOL := 0.01
const BRIEF := {
	"castle":  {"size": Vector3(1.80, 2.30, 0.82), "tall_axis": "Y", "budget": 200, "front_mat": "castle_door_brown"},
	"windkey": {"size": Vector3(0.60, 0.70, 0.14), "tall_axis": "Y", "budget": 250, "front_mat": ""},
	"toybox":  {"size": Vector3(1.26, 0.75, 0.76), "tall_axis": "", "budget": 100, "front_mat": "toybox_brass"},
}
var failures := 0

func check(ok: bool, label: String) -> void:
	print(("  PASS  " if ok else "  FAIL  ") + label)
	if not ok:
		failures += 1

func meshes(n: Node, out: Array) -> Array:
	if n is MeshInstance3D:
		out.append(n)
	for c in n.get_children():
		meshes(c, out)
	return out

# Transform of n relative to the scene root, built from local transforms so it
# works before the node is inside the tree (global_transform does not: a first
# version of this check used it, got the identity, and "passed" the room check
# without testing placement at all).
func to_root(n: Node) -> Transform3D:
	var t := Transform3D.IDENTITY
	while n != null and n != root:
		if n is Node3D:
			t = (n as Node3D).transform * t
		n = n.get_parent()
	return t

func world_aabb(node: Node3D) -> AABB:
	var box := AABB()
	var first := true
	for mi in meshes(node, []):
		var b: AABB = to_root(mi) * mi.get_aabb()
		box = b if first else box.merge(b)
		first = false
	return box

func _initialize() -> void:
	for name in BRIEF:
		var spec: Dictionary = BRIEF[name]
		print("\n== %s  (res://assets/props3d/%s.glb)" % [name, name])
		var ps: PackedScene = load("res://assets/props3d/%s.glb" % name)
		check(ps != null, "imports")
		if ps == null:
			continue
		var inst: Node3D = ps.instantiate()
		root.add_child(inst)
		var box := world_aabb(inst)
		var tris := 0
		var nodes_ok := true
		for mi in meshes(inst, []):
			print("  node %s scale=%s rotation_deg=%s" % [mi.name, mi.scale, mi.rotation_degrees])
			nodes_ok = nodes_ok and mi.scale.is_equal_approx(Vector3.ONE) and mi.rotation.is_zero_approx()
			var mesh: Mesh = mi.mesh
			for s in mesh.get_surface_count():
				var arr := mesh.surface_get_arrays(s)
				var idx: PackedInt32Array = arr[Mesh.ARRAY_INDEX]
				var n_tris := (idx.size() if idx.size() > 0 else (arr[Mesh.ARRAY_VERTEX] as PackedVector3Array).size()) / 3
				tris += n_tris
				var mat := mesh.surface_get_material(s)
				var sb := AABB()
				var verts: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
				for i in verts.size():
					sb = AABB(verts[i], Vector3.ZERO) if i == 0 else sb.expand(verts[i])
				var albedo: Color = mat.albedo_color if mat is BaseMaterial3D else Color.BLACK
				print("  surface %d %s albedo=#%s tris=%d centre_z=%.3f" % [s, mat.resource_name if mat else "none", albedo.to_html(false).to_upper(), n_tris, sb.get_center().z])
				if spec.front_mat != "" and mat and mat.resource_name == spec.front_mat:
					check(sb.get_center().z > 0.0, "%s is on the +Z (front) side" % spec.front_mat)
		print("  aabb size=%s  min_y=%.4f" % [box.size, box.position.y])
		var diff: Vector3 = (box.size - (spec.size as Vector3)).abs()
		check(diff.x <= TOL and diff.y <= TOL and diff.z <= TOL,
			"size %s matches brief %s within %.2f m" % [box.size, spec.size, TOL])
		check(absf(box.position.y) <= 0.005, "base at y=0 (min_y %.4f)" % box.position.y)
		check(inst.scale.is_equal_approx(Vector3.ONE) and nodes_ok, "scale (1,1,1) and rotation 0 on scene and mesh nodes")
		if spec.tall_axis != "":
			check(box.size.y >= box.size.x and box.size.y >= box.size.z, "tallest axis is Y (stands upright)")
		check(tris <= spec.budget, "triangles %d <= budget %d" % [tris, spec.budget])
		inst.free()

	print("\n== prop_room.tscn")
	var room: Node3D = (load("res://prop_room/prop_room.tscn") as PackedScene).instantiate()
	root.add_child(room)
	for name in BRIEF:
		var n: Node3D = room.get_node(name)
		var b := world_aabb(n)
		check(absf(b.position.y) <= 0.005, "%s sits on the floor in the room (world min_y %.4f, world x %.2f..%.2f)" % [name, b.position.y, b.position.x, b.end.x])
	check(room.get_node("Camera3D") is Camera3D and room.get_node("Sun") is DirectionalLight3D and room.get_node("Floor") is MeshInstance3D, "room has floor, one light, camera")
	print("\nRESULT: %s (%d failing)" % ["PASS" if failures == 0 else "FAIL", failures])
	quit(1 if failures > 0 else 0)
