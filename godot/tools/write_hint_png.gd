extends SceneTree
## A5 hint experiment: writes the 3x1 test texture whose texels are the greys
## 64, 128 and 192 (CHANGE-BRIEF A5.4). Written by Claude.
##   godot --headless --path godot --script res://tools/write_hint_png.gd
## Import it lossless with no mipmaps (compress/mode=0, mipmaps/generate=false).

const OUT := "res://assets/textures/hint/hint_greys_3x1.png"
const GREYS := [64, 128, 192]

func _initialize() -> void:
	var img := Image.create(GREYS.size(), 1, false, Image.FORMAT_RGB8)
	for x in GREYS.size():
		var g: int = GREYS[x]
		img.set_pixel(x, 0, Color8(g, g, g))
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT.get_base_dir()))
	var err := img.save_png(OUT)
	var back := Image.load_from_file(ProjectSettings.globalize_path(OUT))
	var read := []
	for x in back.get_width():
		read.append(back.get_pixel(x, 0).r8)
	print("wrote %s (err %d): %dx%d, red channel read back %s" % [OUT, err, back.get_width(), back.get_height(), read])
	quit(0 if err == OK and read == GREYS else 1)
