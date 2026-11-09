extends SceneTree
## Writes the Effect B steam texture (CHANGE-BRIEF B.3): a 32x32 soft steam
## puff, light grey inside with a darker soft ring toward the edge (B.2: "a
## dark core/outline" so it does not wash out on the bright castle), alpha
## falling smoothly to 0 at the edge. The ring and alpha shapes below are
## Claude's reading of the brief, not values the brief gives.
##   godot --headless --path godot --script res://tools/generate_steam_texture.gd
## Then run `godot --headless --path godot --import` once so Godot imports it.
## Texture written by code (no source, no model); this script is its provenance.

const SIZE := 32
const OUT := "res://effects/textures/steam_32.png"
const INSIDE := 0.95       # light grey at the centre
const RING := 0.55         # darker grey toward the edge (the outline)
const RING_FROM := 0.45    # ring starts at this fraction of the radius
const RING_TO := 0.85      # and is fully dark here
const FADE_FROM := 0.7     # alpha starts falling here
const PEAK_ALPHA := 0.9

func _initialize() -> void:
	var img := Image.create(SIZE, SIZE, false, Image.FORMAT_RGBA8)
	var c := (SIZE - 1) / 2.0
	for y in SIZE:
		for x in SIZE:
			var d := Vector2(x - c, y - c).length() / (SIZE / 2.0)
			var g := lerpf(INSIDE, RING, smoothstep(RING_FROM, RING_TO, d))
			var a := PEAK_ALPHA * (1.0 - smoothstep(FADE_FROM, 1.0, d))
			img.set_pixel(x, y, Color(g, g, g, a))
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT.get_base_dir()))
	var err := img.save_png(OUT)
	print("wrote %s (%dx%d), error %d" % [OUT, SIZE, SIZE, err])
	quit(err)
