extends SceneTree
## Calibrates normal_map_check.gd on the Poly Haven Metal Plate pair before the
## audit trusts it (handout Step 3). The GL file should read low with
## directx = false and near 2 with directx = true; the DX file the reverse.
##   scripts/run-test.sh calibrate_normal_map.gd 60
## Prints the ratios; the threshold is set from these numbers, not by feel.
## Exit code = number of failed checks.

const Check := preload("res://tests/normal_map_check.gd")
const DIR := "res://assets/textures/metal_plate/"

var failures := 0

func _initialize() -> void:
	var r := {}
	for conv in ["gl", "dx"]:
		var path := ProjectSettings.globalize_path(DIR + "metal_plate_nor_%s_1k.png" % conv)
		var img := Image.load_from_file(path)
		print("%s: %dx%d format %d" % [path.get_file(), img.get_width(), img.get_height(), img.get_format()])
		for dx in [false, true]:
			var ratio: float = Check.curl_ratio(img, dx, 4)
			r["%s_%s" % [conv, "dx" if dx else "gl"]] = ratio
			print("  curl_ratio(%s file, directx=%s, stride 4) = %.4f" % [conv, dx, ratio])
	ok(r.gl_gl < r.gl_dx, "GL file reads lower under the GL convention (%.4f) than under DX (%.4f)" % [r.gl_gl, r.gl_dx])
	ok(r.dx_dx < r.dx_gl, "DX file reads lower under the DX convention (%.4f) than under GL (%.4f)" % [r.dx_dx, r.dx_gl])
	print("\n%d failed" % failures)
	quit(failures)

func ok(cond: bool, what: String) -> void:
	if not cond:
		failures += 1
	print(("PASS  " if cond else "FAIL  ") + what)
