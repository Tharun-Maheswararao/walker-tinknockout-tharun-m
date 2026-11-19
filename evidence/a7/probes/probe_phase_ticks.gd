extends SceneTree
# A7 brief-facts probe (Claude, 2026-11-19). Not a test; changes nothing.
# Real main.tscn in FIGHT, Rivet's brain frozen, input injected with
# Input.parse_input_event (InputEventKey, physical keycode, as controls.gd binds).
# Logs, AFTER main's physics step each tick: tick, process frame, Bolt's state,
# state_t, whether the attack box is live, hitstop. Then the animation API defaults.
# Run: godot --headless --fixed-fps <60|30> --path godot --script <abs path to this file>

class TickLog extends Node:
	var game
	var rows := []
	var tick := 0
	func _ready(): process_physics_priority = 1000   # after main (priority 0)
	func _physics_process(_dt):
		var b = game.bolt
		rows.append("%3d  f%-4d %-8s t=%.6f box=%s hitstop=%.4f" % [tick, Engine.get_process_frames(),
			Fighter.S.keys()[b.state], b.state_t, "LIVE" if b.attack_box().has_area() else "-", b.hitstop])
		tick += 1

class FrozenBrain:
	func think(_dt): pass

func key(code: int, down: bool) -> void:
	var ev := InputEventKey.new()
	ev.physical_keycode = code
	ev.pressed = down
	Input.parse_input_event(ev)

func scenario(title: String, bolt_x: float, rivet_x: float, code: int, ticks: int) -> void:
	var main = load("res://game/main.tscn").instantiate()
	root.add_child(main)
	for i in 3: await process_frame
	main.brain = FrozenBrain.new()
	main._set_round(main.R.INTRO)
	while main.round_state != main.R.FIGHT: await physics_frame
	main.bolt.position.x = bolt_x
	main.rivet.position.x = rivet_x
	for i in 5: await physics_frame
	var log := TickLog.new()
	log.game = main
	main.add_child(log)
	await physics_frame
	key(code, true)
	await process_frame
	key(code, false)
	while log.tick < ticks: await physics_frame
	print("\n== %s (bolt x %d, rivet x %d) Engine.physics_ticks_per_second=%d" % [title, bolt_x, rivet_x, Engine.physics_ticks_per_second])
	for r in log.rows: print(r)
	main.queue_free()
	await process_frame

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	await scenario("JAB, whiff", 200, 440, KEY_J, 28)
	await scenario("JAB, lands on idle Rivet", 390, 440, KEY_J, 34)
	await scenario("CUTLASS, whiff", 200, 440, KEY_K, 40)
	print("\n== API defaults (4.7.2)")
	var ap := AnimationPlayer.new()
	var at := AnimationTree.new()
	var an := Animation.new()
	var spr := AnimatedSprite2D.new()
	print("AnimationPlayer.callback_mode_process default = %d (PHYSICS=%d, IDLE=%d, MANUAL=%d)" % [ap.callback_mode_process,
		AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS, AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_IDLE, AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL])
	print("AnimationTree.callback_mode_process default = %d" % at.callback_mode_process)
	print("AnimationTree.advance_expression_base_node default = '%s'" % at.advance_expression_base_node)
	print("Animation.step default = %.6f   length default = %.3f   loop_mode default = %d (NONE=%d LINEAR=%d PINGPONG=%d)" % [an.step, an.length, an.loop_mode, Animation.LOOP_NONE, Animation.LOOP_LINEAR, Animation.LOOP_PINGPONG])
	var t := an.add_track(Animation.TYPE_VALUE)
	print("new value track update mode = %d (CONTINUOUS=%d DISCRETE=%d CAPTURE=%d)" % [an.value_track_get_update_mode(t), Animation.UPDATE_CONTINUOUS, Animation.UPDATE_DISCRETE, Animation.UPDATE_CAPTURE])
	print("Godot 3 names: 'loop' in Animation=%s  'playback_speed' in AnimationPlayer=%s  'speed_scale' in AnimationPlayer=%s  'frames' in AnimatedSprite2D=%s  'sprite_frames'=%s  class AnimatedSprite exists=%s" % [
		"loop" in an, "playback_speed" in ap, "speed_scale" in ap, "frames" in spr, "sprite_frames" in spr, ClassDB.class_exists("AnimatedSprite")])
	print("AnimatedSprite2D has callback_mode_process=%s; AnimationPlayer 'current_animation'=%s; AnimatedSprite2D 'animation'=%s 'current_animation'=%s" % [
		"callback_mode_process" in spr, "current_animation" in ap, "animation" in spr, "current_animation" in spr])
	ap.free(); at.free(); spr.free()
	quit(0)
