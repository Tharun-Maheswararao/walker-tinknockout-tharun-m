extends SceneTree
## A5 Use It: toy-box captures in a real windowed run (CHANGE-BRIEF A5.5
## lighting: the prop room as A3 left it). Written by Claude.
##   godot --path godot --script res://tools/a5_capture_toybox.gd
## 1. toyboxes_side_by_side.png: fresh (x 2.0) and worn (x 3.35), as committed.
## 2. Interface sweep: each painted_tin uniform at its minimum, the shader's
##    default and its maximum, set at RUNTIME on the fresh material only. The
##    .tres files are never saved, so nothing on disk changes.

const FRESH := "res://prop_room/materials/toybox_fresh.tres"
const SWEEP := [
	["paint_color", Color(0, 0, 0), Color(0.710, 0.188, 0.165), Color(1, 1, 1)],
	["paint_roughness", 0.0, 0.35, 1.0],
	["wear_amount", 0.0, 0.1, 1.0],
	["normal_depth", 0.0, 1.0, 2.0],
	["uv_scale", 0.5, 2.5, 8.0],
]

var dir: String

func _initialize() -> void:
	call_deferred("run")

func shot(name: String) -> void:
	for i in 3:
		await process_frame
	await RenderingServer.frame_post_draw
	root.get_viewport().get_texture().get_image().save_png(dir.path_join(name))
	print("saved ", name)

func run() -> void:
	dir = ProjectSettings.globalize_path("res://").path_join("../evidence/a5/captures/toybox").simplify_path()
	DirAccess.make_dir_recursive_absolute(dir)
	var room: Node3D = (load("res://prop_room/prop_room.tscn") as PackedScene).instantiate()
	root.add_child(room)
	for i in 10:
		await process_frame
	await shot("toyboxes_side_by_side.png")
	var fresh: ShaderMaterial = load(FRESH)
	for row in SWEEP:
		var param: String = row[0]
		var saved = fresh.get_shader_parameter(param)
		for i in 3:
			fresh.set_shader_parameter(param, row[i + 1])
			await shot("sweep_%s_%s.png" % [param, ["min", "default", "max"][i]])
		fresh.set_shader_parameter(param, saved)
	quit()
