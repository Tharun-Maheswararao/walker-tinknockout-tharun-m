# Renders prop_room.tscn once (with a window) and saves a PNG for evidence.
#   godot --path godot --script res://tools/shot_prop_room.gd -- ../evidence/godot/prop_room.png
extends SceneTree

func _initialize() -> void:
	root.add_child((load("res://prop_room/prop_room.tscn") as PackedScene).instantiate())
	root.size = Vector2i(1920, 1080)
	for i in 10:
		await process_frame
	await RenderingServer.frame_post_draw
	var out: String = OS.get_cmdline_user_args()[0]
	root.get_texture().get_image().save_png(out)
	print("SAVED ", out)
	quit()
