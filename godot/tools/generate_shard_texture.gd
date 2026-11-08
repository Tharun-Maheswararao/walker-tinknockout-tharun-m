extends SceneTree
## Writes the Effect A shard texture (CHANGE-BRIEF A.3a): an 8x8 tin shard,
## light tin inside, one-pixel dark rim, transparent outside.
##   godot --headless --path godot --script res://tools/generate_shard_texture.gd
## Then run `godot --headless --path godot --import` once so Godot imports it.
## Texture written by code (no source, no model); this script is its provenance.

const SIZE := 8
const OUT := "res://effects/textures/shard_8.png"
const TIN := Color(0.85, 0.87, 0.90, 1.0)
const RIM := Color(0.15, 0.15, 0.17, 1.0)
# an irregular four-sided shard, in pixel coordinates
const SHAPE := [Vector2(0.5, 5.5), Vector2(3.0, 0.5), Vector2(7.5, 2.0), Vector2(5.0, 7.5)]

func _initialize() -> void:
	var poly := PackedVector2Array(SHAPE)
	var inside := func(x: int, y: int) -> bool:
		if x < 0 or y < 0 or x >= SIZE or y >= SIZE:
			return false
		return Geometry2D.is_point_in_polygon(Vector2(x + 0.5, y + 0.5), poly)
	var img := Image.create(SIZE, SIZE, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	for y in SIZE:
		for x in SIZE:
			if not inside.call(x, y):
				continue
			var edge: bool = not (inside.call(x - 1, y) and inside.call(x + 1, y) and inside.call(x, y - 1) and inside.call(x, y + 1))
			img.set_pixel(x, y, RIM if edge else TIN)
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT.get_base_dir()))
	var err := img.save_png(OUT)
	print("wrote %s (%dx%d), error %d" % [OUT, SIZE, SIZE, err])
	quit(err)
