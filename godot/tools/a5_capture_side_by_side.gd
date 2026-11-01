extends SceneTree
## A5 Use It: one side-by-side capture of both toy boxes, named on the command
## line, for the "one shader, two materials" edit checks. Written by Claude.
##   godot --path godot --script res://tools/a5_capture_side_by_side.gd -- <name>
## Saves evidence/a5/captures/toybox/edit_checks/<name>.png and a 2x crop.

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	var args := OS.get_cmdline_user_args()
	var name: String = args[0] if args.size() > 0 else "side_by_side"
	var dir := ProjectSettings.globalize_path("res://").path_join("../evidence/a5/captures/toybox/edit_checks").simplify_path()
	DirAccess.make_dir_recursive_absolute(dir)
	root.add_child((load("res://prop_room/prop_room.tscn") as PackedScene).instantiate())
	for i in 10:
		await process_frame
	await RenderingServer.frame_post_draw
	var img := root.get_viewport().get_texture().get_image()
	img.save_png(dir.path_join(name + ".png"))
	var crop := img.get_region(Rect2i(740, 480, 290, 105))
	crop.resize(580, 210, Image.INTERPOLATE_NEAREST)
	crop.save_png(dir.path_join(name + "_crop2x.png"))
	print("saved %s/%s.png" % [dir, name])
	quit()
