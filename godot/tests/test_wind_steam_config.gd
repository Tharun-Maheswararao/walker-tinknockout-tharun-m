extends SceneTree
## Effect B configuration read-back (CHANGE-BRIEF B.3, B.1 mapping, B-R6, F1, F3).
##   ./scripts/run-test.sh test_wind_steam_config.gd 60
##
## Loads wind_steam.tscn and reads every setting the brief names back from the
## loaded resources, with the brief's values as the expected values, including
## the features Effect A doesn't use (B.1): amount_ratio, continuous emission
## and local coordinates. It proves configuration only: a headless run draws
## nothing, so it says nothing about how the steam looks.
## Exit code = number of failed checks.

const SCENE := "res://effects/wind_steam.tscn"

var failures := 0
var checks := 0

func ok(cond: bool, what: String) -> void:
	checks += 1
	if not cond:
		failures += 1
	print(("PASS  " if cond else "FAIL  ") + what)

func near(a: float, b: float) -> bool:
	return is_equal_approx(a, b)

func _initialize() -> void:
	print("== wind_steam.tscn (B.3)")
	var ps := load(SCENE) as PackedScene
	ok(ps != null, SCENE + " loads as a PackedScene")
	if ps == null:
		quit(failures)
		return
	var root := ps.instantiate()
	var e := root as GPUParticles2D
	ok(e != null, "root is a GPUParticles2D (one emitter, B.2)")
	if e == null:
		root.free()
		quit(failures)
		return

	print("-- node: emission and draw")
	ok(e.amount == 25, "amount 25, the fixed maximum (got %d)" % e.amount)
	ok(near(e.amount_ratio, 0.0), "amount_ratio 0.0 in the scene: dormant until wind < 25 (B.1, B-R6) (got %.2f)" % e.amount_ratio)
	ok(e.emitting, "emitting true: amount_ratio starts and stops it, emitting stays on (B-R1/B-R2)")
	ok(not e.one_shot, "one_shot false: continuous emission")
	ok(near(e.explosiveness, 0.0), "explosiveness 0.0 (got %.2f)" % e.explosiveness)
	ok(near(e.lifetime, 0.6), "lifetime 0.6 (got %.3f)" % e.lifetime)
	ok(e.local_coords, "local_coords true: puffs follow key_sprite")
	ok(e.visibility_rect == Rect2(-150, -150, 300, 300), "visibility_rect Rect2(-150, -150, 300, 300) (F3) (got %s)" % e.visibility_rect)
	ok(near(e.preprocess, 0.0), "preprocess 0.0 (got %.2f)" % e.preprocess)
	ok(not e.use_fixed_seed, "use_fixed_seed off in the effect scene (only the preview fixes it)")
	var tex := e.texture
	ok(tex != null and tex.resource_path == "res://effects/textures/steam_32.png", "texture res://effects/textures/steam_32.png")
	ok(tex != null and tex.get_width() == 32 and tex.get_height() == 32, "texture is 32 x 32")
	var m := e.material as CanvasItemMaterial
	ok(m != null and m.blend_mode == CanvasItemMaterial.BLEND_MODE_MIX, "draw material CanvasItemMaterial, blend MIX")

	print("-- process material")
	var pm := e.process_material as ParticleProcessMaterial
	ok(pm != null, "process_material is a ParticleProcessMaterial")
	if pm:
		ok(near(pm.lifetime_randomness, 0.3), "lifetime_randomness 0.3 (got %.2f)" % pm.lifetime_randomness)
		ok(pm.emission_shape == ParticleProcessMaterial.EMISSION_SHAPE_POINT, "emission shape point")
		ok(pm.direction.is_equal_approx(Vector3(0, -1, 0)), "direction (0, -1, 0) (got %s)" % pm.direction)
		ok(near(pm.spread, 30.0), "spread 30 (got %.1f)" % pm.spread)
		ok(near(pm.initial_velocity_min, 60.0) and near(pm.initial_velocity_max, 120.0),
			"initial_velocity 60 / 120 local (got %.1f / %.1f)" % [pm.initial_velocity_min, pm.initial_velocity_max])
		ok(pm.gravity.is_equal_approx(Vector3(0, -180, 0)), "gravity (0, -180, 0) local (got %s)" % pm.gravity)
		ok(near(pm.damping_min, 90.0) and near(pm.damping_max, 150.0), "damping 90 / 150 local (got %.1f / %.1f)" % [pm.damping_min, pm.damping_max])
		ok(near(pm.scale_min, 0.2) and near(pm.scale_max, 0.8), "scale 0.2 / 0.8 (got %.2f / %.2f)" % [pm.scale_min, pm.scale_max])
		var gt := pm.color_ramp as GradientTexture1D
		ok(gt != null and gt.gradient != null, "color_ramp is a GradientTexture1D with a Gradient")
		if gt and gt.gradient:
			var g := gt.gradient
			ok(g.get_point_count() == 2, "color_ramp has 2 points (got %d)" % g.get_point_count())
			if g.get_point_count() == 2:
				ok(near(g.get_offset(0), 0.0) and g.get_color(0).is_equal_approx(Color(0.85, 0.85, 0.85, 0.8)),
					"color_ramp point 0 = (0.85, 0.85, 0.85, 0.8) at 0.00 (got %s at %.2f)" % [g.get_color(0), g.get_offset(0)])
				ok(near(g.get_offset(1), 1.0) and g.get_color(1).is_equal_approx(Color(0.9, 0.9, 0.9, 0.0)),
					"color_ramp point 1 = (0.9, 0.9, 0.9, 0.0) at 1.00 (got %s at %.2f)" % [g.get_color(1), g.get_offset(1)])
		var ct := pm.scale_curve as CurveTexture
		ok(ct != null and ct.curve != null, "scale_curve is a CurveTexture with a Curve")
		if ct and ct.curve:
			var c := ct.curve
			ok(near(c.max_value, 3.0), "scale_curve max_value 3.0 (got %.1f)" % c.max_value)
			ok(c.point_count == 2, "scale_curve has 2 points (got %d)" % c.point_count)
			if c.point_count == 2:
				ok(c.get_point_position(0).is_equal_approx(Vector2(0, 1)), "scale_curve point 0 = (0, 1) (got %s)" % c.get_point_position(0))
				# F1: a point above max_value is silently stored at max_value
				ok(c.get_point_position(1).is_equal_approx(Vector2(1, 3)), "scale_curve point 1 = (1, 3), not clamped (F1) (got %s)" % c.get_point_position(1))
	root.free()
	print("\n%d checks, %d failed" % [checks, failures])
	quit(failures)
