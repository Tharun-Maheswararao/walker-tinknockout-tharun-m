extends SceneTree
## A5 Use It: captures the hint-experiment quads in a real windowed run and
## samples the middle of each band. Written by Claude.
##   godot --path godot --script res://tools/a5_capture_hint.gd
## Quad S (top) samples with source_color; quad D (bottom) without. Both show
## the same 3x1 PNG (64, 128, 192), unshaded, Linear tonemap at exposure 1.0.

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	var scene: Node3D = (load("res://hint_experiment/hint_experiment.tscn") as PackedScene).instantiate()
	root.add_child(scene)
	for i in 10:
		await process_frame
	await RenderingServer.frame_post_draw
	var img := root.get_viewport().get_texture().get_image()
	var path := ProjectSettings.globalize_path("res://").path_join("../evidence/a5/captures/hint_quads.png").simplify_path()
	img.save_png(path)
	# Orthographic camera, size 2.6 m tall: px per metre = height / 2.6.
	var h := img.get_height()
	var w := img.get_width()
	var ppm := h / 2.6
	print("hint capture %dx%d -> %s (renderer %s)" % [w, h, path, RenderingServer.get_current_rendering_method()])
	for q in [["S (source_color)", 0.6], ["D (data)", -0.6]]:
		var y := roundi(h / 2.0 - q[1] * ppm)
		var vals := []
		for band in [-1, 0, 1]:
			var c := img.get_pixel(roundi(w / 2.0 + band * ppm), y)
			vals.append([c.r8, c.g8, c.b8])
		print("quad %s at y=%d: bands 64/128/192 display %s" % [q[0], y, vals])
	quit()
