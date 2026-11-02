extends SceneTree
## Film tool (not part of the game): a SCRIPTED-INPUT Movie Maker capture of the
## REWIND tint fading in and out. Run WINDOWED on an isolated copy of 2e6946d:
##   godot --path <copy>/godot --resolution 3840x2160 --write-movie <dir>/frame.png --fixed-fps 30 --script res://film_rewind.gd
## Starts a round through the real input path (confirm), waits through the intro,
## then holds rewind for 1.5 s, releases, and holds again briefly. It never sets
## rewind_amount; the game's own driver does. Prints Bolt's value each frame.

var main
var t := 0

func _initialize() -> void:
	call_deferred("run")

func frames(n: int) -> void:
	for i in n:
		await process_frame
		t += 1
		if main and main.bolt and main.bolt.sprite.material:
			print("frame %d state %d rewind_amount %.4f" % [t, main.bolt.state, main.bolt.sprite.material.get_shader_parameter("rewind_amount")])

func tap(action: String) -> void:
	for pressed in [true, false]:
		var ev := InputEventAction.new()
		ev.action = action
		ev.pressed = pressed
		Input.parse_input_event(ev)
		await frames(1)

func run() -> void:
	main = load("res://game/main.tscn").instantiate()
	root.add_child(main)
	await frames(15)
	await tap("confirm")                       # TITLE -> INTRO
	await frames(int(main.INTRO_TIME * 30) + 30)   # through the intro, then 1 s of FIGHT
	print("HOLD rewind at frame %d" % t)
	Input.action_press("rewind")
	await frames(45)                           # 1.5 s held
	print("RELEASE rewind at frame %d" % t)
	Input.action_release("rewind")
	await frames(30)                           # 1.0 s: fade-out (0.30 s) then rest
	print("HOLD rewind at frame %d" % t)
	Input.action_press("rewind")
	await frames(30)
	print("RELEASE rewind at frame %d" % t)
	Input.action_release("rewind")
	await frames(30)
	print("film capture done at frame %d" % t)
	quit()
