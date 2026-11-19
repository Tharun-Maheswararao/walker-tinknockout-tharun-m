extends SceneTree
# A7 Step 1 probe (Claude, 2026-11-19): confirms the handout's Headless-facts lines
# on this Mac before Tharun adds them to CLAUDE.md. Not a test; writes only user://.
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	# 1. A headless run advances clips and reads their structure.
	var holder := Node2D.new()
	var target := Node2D.new()
	target.name = "Target"
	holder.add_child(target)
	var ap := AnimationPlayer.new()
	holder.add_child(ap)
	root.add_child(holder)
	var a := Animation.new()
	a.length = 1.0
	var t := a.add_track(Animation.TYPE_VALUE)
	a.track_set_path(t, NodePath("Target:position:x"))
	a.track_insert_key(t, 0.0, 0.0)
	a.track_insert_key(t, 1.0, 100.0)
	var lib := AnimationLibrary.new()
	lib.add_animation("probe", a)
	ap.add_animation_library("", lib)
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	ap.play("probe")
	ap.advance(0.5)
	print("1. headless advance(0.5): Target.position.x = %.3f (expect 50), current_animation=%s pos=%.3f" % [target.position.x, ap.current_animation, ap.current_animation_position])
	# 2. Key times are 32-bit floats after a .tres round trip.
	var b := Animation.new()
	var bt := b.add_track(Animation.TYPE_VALUE)
	b.track_set_path(bt, NodePath("Target:frame"))
	for f in [3, 5, 11, 21]:
		b.track_insert_key(bt, f / 60.0, f)
	print("2a. before save: key 1 time == 5/60.0 -> %s (%.17f)" % [b.track_get_key_time(bt, 1) == 5 / 60.0, b.track_get_key_time(bt, 1)])
	ResourceSaver.save(b, "user://probe_keys.tres")
	var c: Animation = ResourceLoader.load("user://probe_keys.tres", "", ResourceLoader.CACHE_MODE_IGNORE)
	for k in c.track_get_key_count(0):
		var want: float = [3, 5, 11, 21][k] / 60.0
		var got := c.track_get_key_time(0, k)
		print("2b. after .tres round trip: key %d time %.17f vs %.17f  == %s  |diff| %.10f  within half a frame %s" % [k, got, want, got == want, absf(got - want), absf(got - want) < 0.5 / 60.0])
	print("2c. .tres text: ", Array(FileAccess.get_file_as_string("user://probe_keys.tres").split("\n")).filter(func(l): return "times" in l))
	# 3. value_track_get_update_mode on a non-value track.
	var d := Animation.new()
	var pt := d.add_track(Animation.TYPE_POSITION_3D)
	print("3. update mode on a POSITION_3D track (expect an error line above/below and CONTINUOUS=0): %d" % d.value_track_get_update_mode(pt))
	quit(0)
