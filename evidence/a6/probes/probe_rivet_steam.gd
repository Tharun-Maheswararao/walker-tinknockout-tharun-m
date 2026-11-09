extends SceneTree
# Probe (not committed): real game, real Rivet brain, Bolt idle. Logs Rivet's
# wind, state, steam ratio and visibility for 30 s at 60 fps.
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	var main = load("res://game/main.tscn").instantiate()
	root.add_child(main)
	for i in 3: await physics_frame
	main._set_round(main.R.INTRO)
	var steam: GPUParticles2D
	for c in main.rivet.key_sprite.get_children():
		if c is GPUParticles2D: steam = c
	var on_frames := 0
	var on_visible := 0
	var on_rewind := 0
	var minw := 100.0
	var maxr := 0.0
	for f in 1800:
		await physics_frame
		main.bolt.hp = 100.0   # keep the round going
		minw = minf(minw, main.rivet.wind)
		maxr = maxf(maxr, steam.amount_ratio)
		if steam.amount_ratio > 0.0:
			on_frames += 1
			if steam.is_visible_in_tree(): on_visible += 1
			if main.rivet.state == Fighter.S.REWIND: on_rewind += 1
		if f % 120 == 0:
			print("t %4.1fs  rivet wind %5.1f  state %2d  ratio %.2f  visible %s  key scale.x %.2f" % [f / 60.0, main.rivet.wind, main.rivet.state, steam.amount_ratio, steam.is_visible_in_tree(), main.rivet.key_sprite.scale.x])
	print("Rivet min wind %.1f, max ratio %.2f; steam on for %d frames (%.1f s), visible on %d of them, %d of them in REWIND" % [minw, maxr, on_frames, on_frames / 60.0, on_visible, on_rewind])
	quit()
