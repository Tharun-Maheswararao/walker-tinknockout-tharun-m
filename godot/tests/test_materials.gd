extends SceneTree
## A5 materials audit test (prompts/a5/prompt-3-audit.txt; tables in
## godot/MATERIALS.md). Written by Claude in the interactive desktop session:
## the claude -p route was blocked by the account's spend limit.
##   scripts/run-test.sh test_materials.gd 60
##
## Pins what the audit found: shader paths, sampler hints (read from the source
## text, because the uniform list reports every sampler as a plain Texture2D),
## each material's uniform values and texture paths, the import settings (read
## with ConfigFile), the glb's Use External mapping, the scenes' wiring and
## environment, and the uniform lists from get_shader_uniform_list().
## Headless limit: nothing is drawn, so nothing here says how anything LOOKS.
## Prints one PASS/FAIL line per check; exits 1 on any failure.

const Curl := preload("res://tests/normal_map_check.gd")

const TIN := "res://shaders/painted_tin.gdshader"
const HINT := "res://shaders/hint_experiment.gdshader"
const TEX := "res://assets/textures/metal_plate/metal_plate_%s_1k.png"
const HINT_PNG := "res://assets/textures/hint/hint_greys_3x1.png"
const FRESH := "res://prop_room/materials/toybox_fresh.tres"
const WORN := "res://prop_room/materials/toybox_worn.tres"
const HINT_S := "res://hint_experiment/hint_source_color.tres"
const HINT_D := "res://hint_experiment/hint_data.tres"
# Threshold from the calibration (logs/calibrate_normal_map_60fps.log):
# the known-good GL file reads 0.0658 under GL and 1.9342 under DX.
const CURL_REAL := 0.5

var failures := 0
var checks := 0

func _initialize() -> void:
	shader_contracts()
	sampler_hints()
	toybox_materials()
	hint_materials()
	import_settings()
	glb_use_external()
	prop_room_wiring()
	hint_scene()
	normal_map_curl()
	print("\n%d checks, %d failed" % [checks, failures])
	quit(1 if failures > 0 else 0)

func ok(cond: bool, what: String) -> void:
	checks += 1
	if not cond:
		failures += 1
	print(("PASS  " if cond else "FAIL  ") + what)

## name -> type, from the engine (a parse failure gives an empty list)
func uniform_types(path: String) -> Dictionary:
	var d := {}
	for u in (load(path) as Shader).get_shader_uniform_list():
		d[u.name] = u.type
	return d

## The hint list written after the colon of `uniform sampler2D <name> : ...;`
func sampler_hints_in_source(path: String, sampler: String) -> PackedStringArray:
	var re := RegEx.new()
	re.compile("uniform\\s+sampler2D\\s+" + sampler + "\\s*(?::\\s*([^;]*))?;")
	var m := re.search(FileAccess.get_file_as_string(path))
	var out := PackedStringArray()
	if m:
		for h in m.get_string(1).split(",", false):
			out.append(h.strip_edges())
	return out

func tex_path(mat: ShaderMaterial, param: String) -> String:
	var t = mat.get_shader_parameter(param)
	return t.resource_path if t is Texture2D else "<none>"

# ---------------------------------------------------------------- shaders
func shader_contracts() -> void:
	var tin := uniform_types(TIN)
	print("      painted_tin uniforms: ", tin)
	ok(tin.size() == 8, "painted_tin parses: 8 uniforms listed (3 samplers + 5 values), got %d" % tin.size())
	for s in ["metal_albedo", "metal_normal", "metal_rough"]:
		ok(tin.get(s) == TYPE_OBJECT, "painted_tin: %s is a sampler (type 24)" % s)
	ok(tin.get("paint_color") == TYPE_COLOR, "painted_tin: paint_color is vec4 : source_color (type 20)")
	for f in ["paint_roughness", "wear_amount", "normal_depth", "uv_scale"]:
		ok(tin.get(f) == TYPE_FLOAT, "painted_tin: %s is a float" % f)
	var src := FileAccess.get_file_as_string(TIN)
	ok(src.find("group_uniforms paint;") != -1 and src.find("group_uniforms metal;") != -1, "painted_tin: group_uniforms paint and metal in the source")

	var hint := uniform_types(HINT)
	print("      hint_experiment uniforms: ", hint)
	ok(hint.size() == 3 and hint.get("grey_as_colour") == TYPE_OBJECT and hint.get("grey_as_data") == TYPE_OBJECT and hint.get("use_colour_sampler") == TYPE_BOOL,
		"hint_experiment parses: grey_as_colour, grey_as_data (samplers), use_colour_sampler (bool)")
	ok(FileAccess.get_file_as_string(HINT).find("render_mode unshaded;") != -1, "hint_experiment: render_mode unshaded in the source")

func sampler_hints() -> void:
	var a := sampler_hints_in_source(TIN, "metal_albedo")
	var n := sampler_hints_in_source(TIN, "metal_normal")
	var r := sampler_hints_in_source(TIN, "metal_rough")
	print("      hints as written: metal_albedo %s | metal_normal %s | metal_rough %s" % [a, n, r])
	ok("source_color" in a, "colour sampler metal_albedo has source_color (sampled as colour)")
	ok("hint_normal" in n and not "source_color" in n, "normal sampler metal_normal has hint_normal, no source_color")
	ok(not "source_color" in r and not "hint_normal" in r, "data sampler metal_rough has neither source_color nor hint_normal (read as stored)")
	var hc := sampler_hints_in_source(HINT, "grey_as_colour")
	var hd := sampler_hints_in_source(HINT, "grey_as_data")
	print("      hints as written: grey_as_colour %s | grey_as_data %s" % [hc, hd])
	ok("source_color" in hc and "filter_nearest" in hc, "grey_as_colour: source_color, filter_nearest")
	ok(not "source_color" in hd and "filter_nearest" in hd, "grey_as_data: filter_nearest only, no source_color")

# ---------------------------------------------------------------- materials
func toybox_materials() -> void:
	var f: ShaderMaterial = load(FRESH)
	var w: ShaderMaterial = load(WORN)
	ok(f.shader.resource_path == TIN and w.shader.resource_path == TIN, "toybox_fresh and toybox_worn both use %s" % TIN)
	for m in [f, w]:
		var label: String = m.resource_path.get_file()
		ok(tex_path(m, "metal_albedo") == TEX % "diff", "%s binds metal_albedo -> %s" % [label, tex_path(m, "metal_albedo")])
		ok(tex_path(m, "metal_normal") == TEX % "nor_gl", "%s binds metal_normal -> %s (the GL map)" % [label, tex_path(m, "metal_normal")])
		ok(tex_path(m, "metal_rough") == TEX % "rough", "%s binds metal_rough -> %s" % [label, tex_path(m, "metal_rough")])
		ok(m.get_shader_parameter("paint_color") == null and m.get_shader_parameter("normal_depth") == null and m.get_shader_parameter("uv_scale") == null,
			"%s leaves paint_color, normal_depth, uv_scale unset (shader defaults apply)" % label)
	ok(is_equal_approx(f.get_shader_parameter("wear_amount"), 0.05) and is_equal_approx(f.get_shader_parameter("paint_roughness"), 0.30),
		"toybox_fresh: wear_amount 0.05, paint_roughness 0.30")
	ok(is_equal_approx(w.get_shader_parameter("wear_amount"), 0.55) and is_equal_approx(w.get_shader_parameter("paint_roughness"), 0.70),
		"toybox_worn: wear_amount 0.55, paint_roughness 0.70")
	ok(f != w, "two distinct material resources")

func hint_materials() -> void:
	var s: ShaderMaterial = load(HINT_S)
	var d: ShaderMaterial = load(HINT_D)
	ok(s.shader.resource_path == HINT and d.shader.resource_path == HINT, "both hint materials use %s" % HINT)
	for m in [s, d]:
		ok(tex_path(m, "grey_as_colour") == HINT_PNG and tex_path(m, "grey_as_data") == HINT_PNG,
			"%s binds the same PNG to both samplers" % m.resource_path.get_file())
	ok(s.get_shader_parameter("use_colour_sampler") == true, "hint_source_color: use_colour_sampler = true")
	ok(d.get_shader_parameter("use_colour_sampler") == false, "hint_data: use_colour_sampler = false")

# ---------------------------------------------------------------- imports
func import_cfg(res_path: String) -> ConfigFile:
	var c := ConfigFile.new()
	c.load(res_path + ".import")
	return c

func import_settings() -> void:
	# [compress/mode, compress/normal_map, mipmaps/generate] from CHANGE-BRIEF A5.5 and A5.4
	var want := {
		TEX % "diff": [2, 2, true], TEX % "nor_gl": [2, 1, true], TEX % "rough": [2, 2, true],
		TEX % "nor_dx": [2, 1, true], HINT_PNG: [0, 2, false],
	}
	for p in want:
		var img: Image = (load(p) as Texture2D).get_image()
		print("      %s imported as Image format %d (%s), %dx%d, mipmaps %s" % [p.get_file(), img.get_format(),
			{Image.FORMAT_RGB8: "RGB8", Image.FORMAT_DXT1: "DXT1", Image.FORMAT_RGTC_RG: "RGTC_RG"}.get(img.get_format(), "?"),
			img.get_width(), img.get_height(), img.has_mipmaps()])
		var c := import_cfg(p)
		var got := [c.get_value("params", "compress/mode"), c.get_value("params", "compress/normal_map"), c.get_value("params", "mipmaps/generate")]
		ok(got == want[p], "%s import: compress/mode, normal_map, mipmaps = %s (want %s)" % [p.get_file(), got, want[p]])
		ok(c.get_value("params", "detect_3d/compress_to") == 0, "%s import: detect_3d/compress_to = 0 (Disabled)" % p.get_file())

func glb_use_external() -> void:
	var c := import_cfg("res://assets/props3d/toybox.glb")
	var subs: Dictionary = c.get_value("params", "_subresources", {})
	var red: Dictionary = subs.get("materials", {}).get("toybox_red", {})
	ok(red.get("use_external/enabled", false) == true and red.get("use_external/path", "") == FRESH,
		"toybox.glb.import: toybox_red -> Use External %s" % red.get("use_external/path", "<none>"))
	ok(c.get_value("params", "meshes/ensure_tangents") == true, "toybox.glb.import: meshes/ensure_tangents = true (the normal map needs tangents)")

# ---------------------------------------------------------------- scenes
func prop_room_wiring() -> void:
	var room: Node3D = (load("res://prop_room/prop_room.tscn") as PackedScene).instantiate()
	root.add_child(room)   # in the tree, as check_props3d.gd does; freeing it outside the tree printed an engine ERROR
	var a: MeshInstance3D = room.get_node("toybox/toybox")
	var b: MeshInstance3D = room.get_node("toybox_worn/toybox")
	ok(a.get_active_material(0).resource_path == FRESH, "prop_room: toybox surface 0 = toybox_fresh (through Use External)")
	ok(b.get_surface_override_material(0) != null and b.get_active_material(0).resource_path == WORN, "prop_room: toybox_worn surface 0 = toybox_worn (surface override)")
	ok(a.get_active_material(1) == b.get_active_material(1), "prop_room: both boxes keep the same cream lid material (slot 1 untouched)")
	var env: Environment = room.get_node("WorldEnvironment").environment
	print("      prop_room env: tonemap %d, exposure %.2f, ssao %s, ssil %s, sdfgi %s, glow %s, fog %s; Sun energy %.2f, shadows %s"
		% [env.tonemap_mode, env.tonemap_exposure, env.ssao_enabled, env.ssil_enabled, env.sdfgi_enabled, env.glow_enabled, env.fog_enabled,
		(room.get_node("Sun") as DirectionalLight3D).light_energy, (room.get_node("Sun") as DirectionalLight3D).shadow_enabled])
	ok(not env.ssao_enabled and not env.ssil_enabled and not env.sdfgi_enabled and not env.glow_enabled and not env.fog_enabled,
		"prop_room: SSAO, SSIL, SDFGI, glow and fog off (CHANGE-BRIEF A5.5 lighting)")
	room.queue_free()

func hint_scene() -> void:
	var sc: Node3D = (load("res://hint_experiment/hint_experiment.tscn") as PackedScene).instantiate()
	var env: Environment = sc.get_node("WorldEnvironment").environment
	ok(env.tonemap_mode == Environment.TONE_MAPPER_LINEAR and env.tonemap_exposure == 1.0, "hint scene: Linear tonemap (%d) at exposure %.1f" % [env.tonemap_mode, env.tonemap_exposure])
	ok(not env.glow_enabled and not env.fog_enabled and not env.volumetric_fog_enabled and not env.adjustment_enabled, "hint scene: glow, fog, volumetric fog and adjustments off")
	ok((sc.get_node("Quad_S_source_color") as MeshInstance3D).material_override.resource_path == HINT_S, "hint scene: Quad_S uses hint_source_color.tres")
	ok((sc.get_node("Quad_D_data") as MeshInstance3D).material_override.resource_path == HINT_D, "hint scene: Quad_D uses hint_data.tres")
	sc.free()

# ---------------------------------------------------------------- texture data
func normal_map_curl() -> void:
	for conv in ["nor_gl", "nor_dx"]:
		var img := Image.load_from_file(ProjectSettings.globalize_path(TEX % conv))
		var gl: float = Curl.curl_ratio(img, false, 4)
		var dx: float = Curl.curl_ratio(img, true, 4)
		print("      curl_ratio %s: GL convention %.4f, DX convention %.4f" % [conv, gl, dx])
		if conv == "nor_gl":
			ok(gl < CURL_REAL and dx > 2.0 - CURL_REAL, "bound normal map is a real surface in the GL convention Godot expects (%.4f < %.1f; DX %.4f)" % [gl, CURL_REAL, dx])
