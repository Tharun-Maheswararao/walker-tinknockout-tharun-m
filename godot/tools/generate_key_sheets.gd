extends SceneTree
## Writes the A7 wind-key sprite sheets (CHANGE-BRIEF.md §2) from the committed
## key art, one sheet per fighter:
##   godot/assets/props/key-bolt.png  -> godot/assets/props/key-bolt-sheet.png
##   godot/assets/props/key-rivet.png -> godot/assets/props/key-rivet-sheet.png
## Recipe (the brief's "turn-squash projection", nothing added):
##   - 8 cells of 84x60 in one row (672x60, hframes 8, vframes 1);
##   - cell k is the key turned theta = k * 45 degrees about its vertical spindle;
##   - width factor w = max(0.15, |cos(theta)|): the key is resized to
##     round(84 * w) x 60, so it never vanishes at 90 and 270 degrees;
##   - for 90 < theta < 270 (cells 3, 4, 5) the key is mirrored (flip_x);
##   - each resized key is centred horizontally (and vertically: same 60 px
##     height) in its cell on a transparent background.
## The resize filter (Lanczos) is Claude's choice; the brief does not name one.
##   godot --headless --path godot --script res://tools/generate_key_sheets.gd
## Then run `godot --headless --path godot --import` once so Godot imports them.
## Written by Claude (A7 Step 3). The source PNGs are never modified.

const CELL := Vector2i(84, 60)
const FRAMES := 8
const MIN_W := 0.15
const SKINS := ["bolt", "rivet"]

func _initialize() -> void:
	var problems := 0
	for skin in SKINS:
		var src_path := "res://assets/props/key-%s.png" % skin
		var out_path := "res://assets/props/key-%s-sheet.png" % skin
		var src := Image.load_from_file(ProjectSettings.globalize_path(src_path))
		if src == null or src.get_size() != CELL:
			print("PROBLEM: %s is not %dx%d" % [src_path, CELL.x, CELL.y])
			problems += 1
			continue
		src.convert(Image.FORMAT_RGBA8)
		var sheet := Image.create(CELL.x * FRAMES, CELL.y, false, Image.FORMAT_RGBA8)
		sheet.fill(Color(0, 0, 0, 0))
		for k in FRAMES:
			var theta := deg_to_rad(k * 45.0)
			var w := maxf(MIN_W, absf(cos(theta)))
			var cw := int(round(CELL.x * w))
			var cell := src.duplicate() as Image
			cell.resize(cw, CELL.y, Image.INTERPOLATE_LANCZOS)
			var deg := k * 45
			if deg > 90 and deg < 270:
				cell.flip_x()
			var x := k * CELL.x + (CELL.x - cw) / 2
			sheet.blit_rect(cell, Rect2i(Vector2i.ZERO, Vector2i(cw, CELL.y)), Vector2i(x, 0))
			print("%s cell %d: theta %3d deg, width factor %.3f -> %2d px, mirrored %s, at x %d" % [skin, k, deg, w, cw, deg > 90 and deg < 270, x])
		var err := sheet.save_png(ProjectSettings.globalize_path(out_path))
		print("%s -> %s (%dx%d) %s" % [src_path, out_path, sheet.get_width(), sheet.get_height(), "ok" if err == OK else "ERROR %d" % err])
		if err != OK:
			problems += 1
	quit(problems)
