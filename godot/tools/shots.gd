extends SceneTree
## In-engine screenshots for TEST-REPORT (character states vs sheet, storyboard
## panels vs slice). Runs WINDOWED (needs rendering):
##   godot --path godot --script res://tools/shots.gd
## Gameplay is driven through the real input path. Rivet is frozen and a few
## shots place the fighters first (marked POSED) so one state can be framed;
## those are labelled "posed" in TEST-REPORT, not presented as free play.

const OUT := "res://../evidence/screens/"
var main

func _initialize() -> void:
	call_deferred("run")

func frames(n: int) -> void:
	for i in n:
		await physics_frame

func snap(name: String, show_boxes := false) -> void:
	main.show_boxes = show_boxes
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
	var img := root.get_viewport().get_texture().get_image()
	img.save_png(ProjectSettings.globalize_path(OUT) + name + ".png")
	print("shot ", name)

func ev(action: String) -> void:
	for p in [true, false]:
		var e := InputEventAction.new()
		e.action = action
		e.pressed = p
		Input.parse_input_event(e)
		await frames(1)

class Frozen:
	func think(_dt): pass

func run() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
	main = load("res://game/main.tscn").instantiate()
	root.add_child(main)
	await frames(5)
	await snap("01-title")
	main.brain = Frozen.new()
	await ev("confirm")
	await frames(20)
	await snap("02-round-intro")
	await frames(70)
	await snap("02b-fight-idle")
	await snap("02c-fight-idle-boxes", true)
	# walk (POSED start, real input)
	Input.action_press("move_right"); await frames(12); await snap("state-walk-right"); Input.action_release("move_right")
	Input.action_press("move_left"); await frames(8); await snap("state-walk-left-flipped"); Input.action_release("move_left")
	await frames(5)
	main.bolt.position.x = 300; main.rivet.position.x = 350   # POSED
	Input.action_press("jab"); await frames(1); Input.action_release("jab"); await frames(6)
	await snap("03-jab-hit")
	await snap("03b-jab-hit-boxes", true)
	await frames(30)
	main.bolt.position.x = 290; main.rivet.position.x = 352; main.bolt.facing = 1
	Input.action_press("cutlass"); await frames(1); Input.action_release("cutlass"); await frames(10)
	await snap("state-cutlass")
	await snap("state-cutlass-boxes", true)
	await frames(40)
	main.bolt.position.x = 160; main.rivet.position.x = 470; main.bolt.wind = 100
	Input.action_press("pop"); await frames(1); Input.action_release("pop"); await frames(14)
	await snap("06b-popgun-cork")
	await frames(60)
	Input.action_press("block"); await frames(4); await snap("state-block"); Input.action_release("block")
	await frames(3)
	main.bolt.wind = 30
	Input.action_press("rewind"); await frames(20); await snap("04-rewind"); await frames(30); Input.action_release("rewind")
	await frames(3)
	main.bolt.wind = 5; main.bolt.position.x = 200; main.rivet.position.x = 440   # POSED: one jab empties it
	Input.action_press("jab"); await frames(1); Input.action_release("jab"); await frames(26)
	await snap("05-spring-empty")
	main.rivet.position.x = main.bolt.position.x + 60; main.rivet.facing = -1
	main.rivet.intent = {"move": 0, "jab": false, "cutlass": true, "pop": false, "block": false, "rewind": false}
	await frames(1)
	main.rivet.intent = {"move": 0, "jab": false, "cutlass": false, "pop": false, "block": false, "rewind": false}
	await frames(14)
	await snap("05b-knockdown-hurt")
	await frames(90)
	await ev("pause"); await frames(3); await snap("pause"); await ev("pause")
	main.bolt.position.x = 300; main.rivet.position.x = 350; main.rivet.hp = 4; main.bolt.facing = 1
	main.bolt.state = Fighter.S.IDLE; main.bolt.wind = 100
	Input.action_press("jab"); await frames(1); Input.action_release("jab"); await frames(40)
	await snap("07-knockout-win")
	main._reset_fighters(); main._set_round(main.R.FIGHT)
	main.bolt.hp = 4; main.bolt.position.x = 300; main.rivet.position.x = 350
	main.rivet.intent = {"move": 0, "jab": true, "cutlass": false, "pop": false, "block": false, "rewind": false}
	await frames(1)
	main.rivet.intent = {"move": 0, "jab": false, "cutlass": false, "pop": false, "block": false, "rewind": false}
	await frames(40)
	await snap("07b-knockout-lose")
	quit()
