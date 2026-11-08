extends SceneTree
## Effect A configuration read-back (CHANGE-BRIEF A.3a-A.3c, A-R1, A-R6).
##   ./scripts/run-test.sh test_impact_effect_config.gd 60
##
## Loads both effect scenes and reads every setting the brief names back from
## the loaded resources. The expected values are the brief's, so the test also
## catches drift between the brief and the scenes, and a Godot 3 name that left
## a value at its default. It proves configuration only: a headless run draws
## nothing, so it says nothing about how the effect looks.
## Exit code = number of failed checks.

const FULL := "res://effects/impact_effect.tscn"
const BLOCKED := "res://effects/impact_effect_blocked.tscn"

var failures := 0
var checks := 0

func ok(cond: bool, what: String) -> void:
	checks += 1
	if not cond:
		failures += 1
	print(("PASS  " if cond else "FAIL  ") + what)

func near(a: float, b: float) -> bool:
	return is_equal_approx(a, b)

func color_near(a: Color, b: Color) -> bool:
	return a.is_equal_approx(b)

func check_ramp(tag: String, pm: ParticleProcessMaterial, offsets: Array, colors: Array) -> void:
	var t := pm.color_ramp as GradientTexture1D
	ok(t != null and t.gradient != null, tag + " color_ramp is a GradientTexture1D with a Gradient")
	if t == null or t.gradient == null:
		return
	var g := t.gradient
	ok(g.get_point_count() == offsets.size(), "%s color_ramp has %d points (got %d)" % [tag, offsets.size(), g.get_point_count()])
	for i in mini(offsets.size(), g.get_point_count()):
		ok(near(g.get_offset(i), offsets[i]) and color_near(g.get_color(i), colors[i]),
			"%s color_ramp point %d = %s at %.2f (got %s at %.2f)" % [tag, i, colors[i], offsets[i], g.get_color(i), g.get_offset(i)])

func check_curve(tag: String, pm: ParticleProcessMaterial, points: Array, max_v: float) -> void:
	var t := pm.scale_curve as CurveTexture
	ok(t != null and t.curve != null, tag + " scale_curve is a CurveTexture with a Curve")
	if t == null or t.curve == null:
		return
	var c := t.curve
	ok(near(c.max_value, max_v), "%s scale_curve max_value %.1f (got %.1f)" % [tag, max_v, c.max_value])
	ok(c.point_count == points.size(), "%s scale_curve has %d points (got %d)" % [tag, points.size(), c.point_count])
	# reading the points back is the check for clamping (brief F1): a point above
	# max_value is silently stored at max_value
	for i in mini(points.size(), c.point_count):
		var p := c.get_point_position(i)
		ok(p.is_equal_approx(points[i]), "%s scale_curve point %d = %s (got %s)" % [tag, i, points[i], p])

func check_node(tag: String, e: GPUParticles2D, amount: int) -> ParticleProcessMaterial:
	ok(e != null, tag + " exists and is a GPUParticles2D")
	if e == null:
		return null
	ok(e.amount == amount, "%s amount %d (got %d)" % [tag, amount, e.amount])
	ok(e.one_shot, tag + " one_shot")
	ok(near(e.explosiveness, 1.0), "%s explosiveness 1.0 (got %.2f)" % [tag, e.explosiveness])
	ok(near(e.lifetime, 0.25), "%s lifetime 0.25 (got %.3f)" % [tag, e.lifetime])
	ok(not e.local_coords, tag + " local_coords false")
	ok(e.visibility_rect == Rect2(-100, -100, 200, 200), "%s visibility_rect default Rect2(-100, -100, 200, 200) (got %s)" % [tag, e.visibility_rect])
	ok(near(e.preprocess, 0.0), "%s preprocess 0.0 (got %.2f)" % [tag, e.preprocess])
	ok(not e.emitting, tag + " not emitting when the scene loads (A-R1)")
	ok(not e.use_fixed_seed, tag + " use_fixed_seed off in the effect scene (repeats must vary)")
	var pm := e.process_material as ParticleProcessMaterial
	ok(pm != null, tag + " process_material is a ParticleProcessMaterial")
	return pm

func check_blend(tag: String, e: GPUParticles2D, blend: int, name: String) -> void:
	var m := e.material as CanvasItemMaterial
	ok(m != null and m.blend_mode == blend, "%s draw material CanvasItemMaterial, blend %s" % [tag, name])

func check_shards(tag: String, e: GPUParticles2D, amount: int, colors: Array, smin: float, smax: float) -> void:
	var pm := check_node(tag, e, amount)
	if pm == null:
		return
	ok(pm.emission_shape == ParticleProcessMaterial.EMISSION_SHAPE_POINT, tag + " emission shape point")
	ok(near(pm.initial_velocity_min, 60.0) and near(pm.initial_velocity_max, 90.0),
		"%s initial_velocity 60 / 90 (got %.1f / %.1f)" % [tag, pm.initial_velocity_min, pm.initial_velocity_max])
	ok(near(pm.spread, 180.0), "%s spread 180 (got %.1f)" % [tag, pm.spread])
	ok(near(pm.angle_min, -180.0) and near(pm.angle_max, 180.0), "%s angle -180 / 180 (got %.1f / %.1f)" % [tag, pm.angle_min, pm.angle_max])
	ok(pm.gravity.is_equal_approx(Vector3(0, 400, 0)), "%s gravity (0, 400, 0) (got %s)" % [tag, pm.gravity])
	ok(near(pm.damping_min, 100.0) and near(pm.damping_max, 150.0), "%s damping 100 / 150 (got %.1f / %.1f)" % [tag, pm.damping_min, pm.damping_max])
	check_ramp(tag, pm, [0.0, 1.0], colors)
	ok(near(pm.scale_min, smin) and near(pm.scale_max, smax), "%s scale %.1f / %.1f (got %.2f / %.2f)" % [tag, smin, smax, pm.scale_min, pm.scale_max])
	check_curve(tag, pm, [Vector2(0.0, 1.0), Vector2(0.2, 1.2), Vector2(1.0, 0.4)], 2.0)
	var tex := e.texture
	ok(tex != null and tex.resource_path == "res://effects/textures/shard_8.png", tag + " texture res://effects/textures/shard_8.png")
	ok(tex != null and tex.get_width() == 8 and tex.get_height() == 8, tag + " texture is 8 x 8")
	check_blend(tag, e, CanvasItemMaterial.BLEND_MODE_MIX, "MIX")

func check_core(tag: String, e: GPUParticles2D, amount: int, offsets: Array, colors: Array, smin: float, smax: float) -> void:
	var pm := check_node(tag, e, amount)
	if pm == null:
		return
	ok(pm.emission_shape == ParticleProcessMaterial.EMISSION_SHAPE_POINT, tag + " emission shape point")
	ok(near(pm.initial_velocity_min, 10.0) and near(pm.initial_velocity_max, 20.0),
		"%s initial_velocity 10 / 20 (got %.1f / %.1f)" % [tag, pm.initial_velocity_min, pm.initial_velocity_max])
	ok(near(pm.spread, 180.0), "%s spread 180 (got %.1f)" % [tag, pm.spread])
	ok(pm.gravity.is_equal_approx(Vector3.ZERO), "%s gravity (0, 0, 0) (got %s)" % [tag, pm.gravity])
	ok(near(pm.damping_min, 50.0) and near(pm.damping_max, 80.0), "%s damping 50 / 80 (got %.1f / %.1f)" % [tag, pm.damping_min, pm.damping_max])
	check_ramp(tag, pm, offsets, colors)
	ok(near(pm.scale_min, smin) and near(pm.scale_max, smax), "%s scale %.1f / %.1f (got %.2f / %.2f)" % [tag, smin, smax, pm.scale_min, pm.scale_max])
	check_curve(tag, pm, [Vector2(0.0, 1.0), Vector2(0.2, 1.5), Vector2(1.0, 0.2)], 2.0)
	var tex := e.texture as GradientTexture2D
	ok(tex != null, tag + " texture is a GradientTexture2D")
	if tex != null:
		ok(tex.width == 16 and tex.height == 16, "%s texture 16 x 16 (got %d x %d)" % [tag, tex.width, tex.height])
		ok(tex.fill == GradientTexture2D.FILL_RADIAL, tag + " texture fill radial")
		ok(tex.fill_from.is_equal_approx(Vector2(0.5, 0.5)), "%s texture centred, fill_from (0.5, 0.5) (got %s)" % [tag, tex.fill_from])
	check_blend(tag, e, CanvasItemMaterial.BLEND_MODE_ADD, "ADD")

func check_scene(path: String, root_name: String) -> Node:
	var ps := load(path) as PackedScene
	ok(ps != null, path + " loads as a PackedScene")
	if ps == null:
		return null
	var root := ps.instantiate()
	ok(root is Node2D and root.name == root_name, "%s root is Node2D %s" % [path, root_name])
	ok(root is Node2D and (root as Node2D).z_index == 6, path + " root z_index 6, above the star at 5 (A-R6)")
	ok(root.get_child_count() == 2, "%s has two emitters (got %d)" % [path, root.get_child_count()])
	return root

func _initialize() -> void:
	print("== impact_effect.tscn (A.3a, A.3b)")
	var full := check_scene(FULL, "ImpactEffect")
	if full:
		check_shards("Shards", full.get_node_or_null("Shards") as GPUParticles2D, 16,
			[Color(0.25, 0.25, 0.28, 1.0), Color(0.1, 0.1, 0.1, 0.0)], 0.8, 1.2)
		check_core("Core", full.get_node_or_null("Core") as GPUParticles2D, 8, [0.0, 0.5, 1.0],
			[Color(0.0, 1.0, 1.0, 1.0), Color(0.0, 0.3, 0.8, 0.8), Color(0.0, 0.3, 0.7, 0.0)], 1.0, 1.2)
		full.free()
	print("== impact_effect_blocked.tscn (A.3c)")
	var blk := check_scene(BLOCKED, "ImpactEffectBlocked")
	if blk:
		check_shards("Blocked Shards", blk.get_node_or_null("Shards") as GPUParticles2D, 8,
			[Color(0.5, 0.5, 0.5, 1.0), Color(0.5, 0.5, 0.5, 0.0)], 0.5, 0.7)
		check_core("Blocked Core", blk.get_node_or_null("Core") as GPUParticles2D, 4, [0.0, 1.0],
			[Color(0.6, 0.6, 0.6, 0.8), Color(0.6, 0.6, 0.6, 0.0)], 0.5, 0.7)
		blk.free()
	print("\n%d checks, %d failed" % [checks, failures])
	quit(failures)
