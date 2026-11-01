extends SceneTree
## A5 Use It: a SCRIPTED-INPUT capture run (label it as such). Written by Claude.
## Run WINDOWED, not headless, so the real renderer draws:
##   godot --path godot --script res://tools/a5_capture_run.gd
## Starts a round through the real input path (confirm, then holding rewind),
## waits until Bolt's tint is at 1.0 in the rewind pose, then presses F9 so
## game/debug_capture.gd saves the four controlled-value captures.

var main

func _initialize() -> void:
	call_deferred("run")

func physics_frames(n: int) -> void:
	for i in n:
		await physics_frame

func tap(action: String) -> void:
	for pressed in [true, false]:
		var ev := InputEventAction.new()
		ev.action = action
		ev.pressed = pressed
		Input.parse_input_event(ev)
		await physics_frames(1)

func run() -> void:
	main = load("res://game/main.tscn").instantiate()
	root.add_child(main)
	await physics_frames(5)
	await tap("confirm")                                   # TITLE -> INTRO
	await physics_frames(int(main.INTRO_TIME * 60) + 5)    # INTRO -> FIGHT
	Input.action_press("rewind")                           # hold Rewind (S)
	for i in 120:
		await physics_frame
		if main.bolt.state == Fighter.S.REWIND and main.bolt.sprite.material.get_shader_parameter("rewind_amount") == 1.0:
			break
	var f9 := InputEventKey.new()
	f9.keycode = KEY_F9
	f9.pressed = true
	Input.parse_input_event(f9)                            # debug_capture.gd: 4 captures
	for i in 30:
		await process_frame
	Input.action_release("rewind")
	print("capture run done")
	quit()
