# Renders prop_room.tscn from several camera angles (front, behind, below, close-ups)
# for the A3 look-check evidence. Claude-made engine renders, not the student's screenshots.
#   godot --path godot --script res://tools/shot_prop_views.gd -- <out_dir>
extends SceneTree

const VIEWS := [
	["front_wide",   Vector3(0, 1.6, 5.5),   Vector3(0, 0.9, 0)],
	["behind_wide",  Vector3(0, 1.6, -5.5),  Vector3(0, 0.9, 0)],
	["below_wide",   Vector3(0, -2.5, 3.5),  Vector3(0, 0.8, 0)],
	["castle_close", Vector3(-0.6, 1.6, 3.2), Vector3(-2.2, 1.1, 0)],
	["windkey_close",Vector3(0.6, 0.8, 1.4), Vector3(0, 0.4, 0)],
	["toybox_close", Vector3(3.0, 1.3, 2.0), Vector3(2.0, 0.4, 0)],
]

func _initialize() -> void:
	var room: Node3D = (load("res://prop_room/prop_room.tscn") as PackedScene).instantiate()
	root.add_child(room)
	root.size = Vector2i(1920, 1080)
	var cam: Camera3D = room.get_node("Camera3D")
	var out: String = OS.get_cmdline_user_args()[0]
	await process_frame  # room must be inside the tree before look_at works
	for v in VIEWS:
		cam.look_at_from_position(v[1], v[2], Vector3.UP)
		for i in 5:
			await process_frame
		await RenderingServer.frame_post_draw
		var path := "%s/%s.png" % [out, v[0]]
		root.get_texture().get_image().save_png(path)
		print("SAVED ", path)
	quit()
