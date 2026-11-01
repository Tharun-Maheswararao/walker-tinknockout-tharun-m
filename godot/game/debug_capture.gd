extends Node
## A5 "Use It": in-engine captures of Bolt's tint at the controlled values
## (CHANGE-BRIEF A5.3), using the handout's capture() function. Written by Claude.
##
## F9 in a real windowed run (debug builds only; reads the raw key, adds no
## input action) saves one PNG per value to evidence/a5/captures/:
##   0.0, 0.5, 1.0 (the controlled values) and 2.0 (the hint_range question).
## Hold Rewind (S) at round start so Bolt shows the rewind pose at x 200, facing
## right, as the predictions assume. The captures read the rendered frame at
## viewport resolution: real engine output, not an OS screenshot.

const VALUES := [0.0, 0.5, 1.0, 2.0]

var game          # main.gd
var busy := false

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_F9 and not busy:
		capture_all()

func out_dir() -> String:
	return ProjectSettings.globalize_path("res://").path_join("../evidence/a5/captures").simplify_path()

func bolt_driver() -> Node:
	for c in game.get_children():
		if c.get("fighter") == game.bolt and c.get("material") is ShaderMaterial:
			return c
	return null

func capture_all() -> void:
	busy = true
	var driver := bolt_driver()
	var mat: ShaderMaterial = game.bolt.sprite.material
	DirAccess.make_dir_recursive_absolute(out_dir())
	var b: Fighter = game.bolt
	print("capture: bolt x=%.1f facing=%d state=%s pose=%s | camera offset=%s rotation=%.3f | viewport %s"
		% [b.position.x, b.facing, Fighter.POSE[b.state], b.sprite.texture.resource_path.get_file(),
		game.cam.offset, game.cam.rotation, get_viewport().get_visible_rect().size])
	for v in VALUES:
		var path := out_dir().path_join("bolt_rewind_amount_%s.png" % String.num(v, 1))
		await capture(driver, mat, &"rewind_amount", v, path)
		print("capture: rewind_amount %.1f -> %s (readback %s)" % [v, path, mat.get_shader_parameter(&"rewind_amount")])
	busy = false

## The handout's capture function. Without set_process(false) the driver would
## overwrite the value before the frame draws.
func capture(driver: Node, mat: ShaderMaterial, param: StringName, value: float, path: String) -> void:
	driver.set_process(false)  # also set_physics_process(false) if the driver writes there
	mat.set_shader_parameter(param, value)
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png(path)
	driver.set_process(true)
