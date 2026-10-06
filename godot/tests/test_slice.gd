extends SceneTree
## Automated checks for the Tin Knockout asset slice.
##   godot --headless --path godot --script res://tests/test_slice.gd
##
## Input goes through the REAL input path (Input.action_press/release); the
## player controller reads the same Input singleton a keyboard drives. Setup
## lines may place fighters or set a starting wind/hp (marked SETUP); assertions
## only read results. Exit code = number of failed checks.
##
## Covers CHANGE-BRIEF predictions F2 (hit sound once per attack), F5 (rewind
## clicks once per quarter-turn, not per frame), the event-to-sound map, the
## music behaviour on low wind / pause / KO, and "sound never decides state"
## (a muted run and an unmuted run end in the identical game state).

var main
var failures := 0
var checks := 0

func _initialize() -> void:
	call_deferred("run")

func ok(cond: bool, what: String) -> void:
	checks += 1
	if not cond:
		failures += 1
	print(("PASS  " if cond else "FAIL  ") + what)

func frames(n: int) -> void:
	for i in n:
		await physics_frame

func tap(action: String, hold := 1) -> void:
	Input.action_press(action)
	await frames(hold)
	Input.action_release(action)
	await frames(1)

## Event-driven actions (pause, mute, rematch) are sent as real parsed input events.
func press_event(action: String) -> void:
	for pressed in [true, false]:
		var ev := InputEventAction.new()
		ev.action = action
		ev.pressed = pressed
		Input.parse_input_event(ev)
		await frames(1)

func fresh(brain_on := false) -> void:
	if main:
		main.queue_free()
		await frames(2)
	main = load("res://game/main.tscn").instantiate()
	root.add_child(main)
	await frames(2)
	if not brain_on:
		main.brain = FrozenBrain.new()   # SETUP: freeze Rivet BEFORE the fight starts
	main._set_round(main.R.INTRO)
	await frames(int(main.INTRO_TIME * 60) + 3)

class FrozenBrain:
	func think(_dt): pass

func run() -> void:
	await test_jab_once_per_hit()
	await test_held_jab_is_one_attack()
	await test_cutlass_once_per_hit()
	await test_popgun_once_per_press()
	await test_rewind_clicks()
	await test_empty_once()
	await test_bell_and_ko_music()
	await test_low_wind_and_pause_music()
	await test_facing_follows_input()
	await test_mute_does_not_change_game()
	print("\n%d checks, %d failed" % [checks, failures])
	quit(failures)

# ---------------------------------------------------------------------------
func test_jab_once_per_hit() -> void:
	await fresh()
	main.bolt.position.x = 300; main.rivet.position.x = 350   # SETUP: in jab range
	var hits := [0]
	main.bolt.hit_landed.connect(func(_a, attack, _b): if attack == "jab": hits[0] += 1)
	for i in 8:
		await tap("jab")
		await frames(30)
		main.bolt.wind = 100.0; main.rivet.hp = 100.0         # SETUP: keep the test about sound counts
		main.bolt.position.x = 300; main.rivet.position.x = 350
	ok(hits[0] == 8, "F2 jab: 8 presses in range -> 8 hits (got %d)" % hits[0])
	ok(main.sfx.counts["jab"] == hits[0], "F2 jab: one SFX-JAB per hit (sfx %d, hits %d)" % [main.sfx.counts["jab"], hits[0]])

func test_held_jab_is_one_attack() -> void:
	await fresh()
	main.bolt.position.x = 300; main.rivet.position.x = 350
	Input.action_press("jab")
	await frames(90)                                            # held for 1.5 s
	Input.action_release("jab")
	await frames(5)
	ok(main.sfx.counts["jab"] == 1, "held J for 1.5 s -> exactly 1 jab sound (got %d)" % main.sfx.counts["jab"])

func test_cutlass_once_per_hit() -> void:
	await fresh()
	var hits := [0]
	main.bolt.hit_landed.connect(func(_a, attack, _b): if attack == "cutlass": hits[0] += 1)
	for i in 5:
		main.bolt.position.x = 300; main.rivet.position.x = 360   # SETUP: cutlass range
		main.bolt.wind = 100.0; main.rivet.hp = 100.0
		await tap("cutlass")
		await frames(45)
	ok(hits[0] == 5, "F2 cutlass: 5 swings in range -> 5 hits (got %d)" % hits[0])
	ok(main.sfx.counts["cutlass"] == hits[0], "F2 cutlass: one SFX-CUTLASS per hit (sfx %d)" % main.sfx.counts["cutlass"])

func test_popgun_once_per_press() -> void:
	await fresh()
	main.bolt.position.x = 120; main.rivet.position.x = 520
	Input.action_press("pop")
	await frames(60)
	Input.action_release("pop")
	await frames(90)
	ok(main.sfx.counts["pop"] == 1, "pop-gun held 1 s -> 1 shot, 1 SFX-POP (got %d)" % main.sfx.counts["pop"])
	ok(main.rivet.hp < 100.0, "cork travelled and hit Rivet (hp %.1f)" % main.rivet.hp)

func test_rewind_clicks() -> void:
	await fresh()
	main.bolt.wind = 40.0                                       # SETUP
	Input.action_press("rewind")
	await frames(120)                                           # 2.0 s at 360 deg/s = 8 quarter-turns possible
	var during: int = main.sfx.counts["rewind"]
	await frames(60)                                            # keep holding after full
	Input.action_release("rewind")
	await frames(2)
	ok(during == 6, "F5 rewind 2 s from 40 wind -> 6 clicks (one per 10 wind), not one per frame (got %d)" % during)
	ok(main.sfx.counts["rewind"] == 6, "F5 no clicks once the spring is full (got %d)" % main.sfx.counts["rewind"])
	ok(is_equal_approx(main.bolt.wind, 100.0), "wind refilled to 100 (got %.1f)" % main.bolt.wind)

func test_empty_once() -> void:
	await fresh()
	main.bolt.position.x = 120; main.rivet.position.x = 520
	main.bolt.wind = 8.0                                        # SETUP: one jab empties the spring
	await tap("jab")
	await frames(30)
	ok(main.bolt.state == Fighter.S.EMPTY, "jab with 8 wind -> EMPTY state (state %d)" % main.bolt.state)
	await frames(60)                                            # stays empty ~1.6 s
	ok(main.sfx.counts["empty"] == 1, "SFX-EMPTY once on entering EMPTY, not repeated while stalled (got %d)" % main.sfx.counts["empty"])

func test_bell_and_ko_music() -> void:
	await fresh()
	ok(main.sfx.counts["bell"] == 1, "bell once at round start (got %d)" % main.sfx.counts["bell"])
	ok(main.music.playing and main.music.stream != null and main.music.stream.loop, "music loop playing during the fight (stream loaded, loop on)")
	main.bolt.position.x = 300; main.rivet.position.x = 350
	main.rivet.hp = 5.0                                         # SETUP: next jab is the KO
	await tap("jab")
	await frames(20)
	ok(main.round_state == main.R.KO, "jab at 5 hp -> KO round state")
	ok(main.sfx.counts["bell"] == 2, "bell once more at KO (got %d)" % main.sfx.counts["bell"])
	ok(not main.music.playing, "music stopped on KO")
	await frames(60)
	ok(main.sfx.counts["bell"] == 2, "no repeated KO bell while KO screen stays up (got %d)" % main.sfx.counts["bell"])

func test_low_wind_and_pause_music() -> void:
	await fresh()
	main.bolt.position.x = 120; main.rivet.position.x = 520
	main.bolt.wind = 30.0                                       # SETUP
	await tap("jab")                                            # 30 - 12 = 18 < 25
	await frames(50)
	ok(main.music.low and main.music.pitch_scale < 0.9, "spring < 25%% -> music slowed (pitch %.2f)" % main.music.pitch_scale)
	var x0: float = main.bolt.position.x
	await press_event("pause")
	Input.action_press("move_right")
	await frames(30)
	Input.action_release("move_right")
	var bus := AudioServer.get_bus_index(&"Music")
	ok(main.paused and AudioServer.is_bus_effect_enabled(bus, 0), "pause -> Music bus low-pass on")
	ok(is_equal_approx(main.bolt.position.x, x0), "pause -> fighters frozen")
	await press_event("pause")
	ok(not AudioServer.is_bus_effect_enabled(bus, 0), "unpause -> low-pass off")

func test_facing_follows_input() -> void:
	await fresh()
	Input.action_press("move_left")
	await frames(10)
	Input.action_release("move_left")
	await frames(2)
	ok(main.bolt.facing == -1 and main.bolt.sprite.scale.x < 0.0, "walking left flips Bolt's sprite (runtime flip)")
	Input.action_press("move_right")
	await frames(10)
	Input.action_release("move_right")
	await frames(2)
	ok(main.bolt.facing == 1 and main.bolt.sprite.scale.x > 0.0, "walking right faces right again")

## The same scripted fight, muted and unmuted, must end identically.
func scripted_fight(muted: bool) -> Array:
	await fresh(true)
	AudioServer.set_bus_mute(AudioServer.get_bus_index(&"Music"), muted)
	AudioServer.set_bus_mute(AudioServer.get_bus_index(&"SFX"), muted)
	var plan := [["move_right", 40], ["jab", 1], ["", 20], ["jab", 1], ["", 20], ["cutlass", 1], ["", 40],
		["move_left", 50], ["rewind", 70], ["move_right", 30], ["jab", 1], ["", 25], ["pop", 1], ["", 60]]
	for step in plan:
		if step[0] == "":
			await frames(step[1])
		else:
			await tap(step[0], step[1])
	var s := [snappedf(main.bolt.hp, 0.01), snappedf(main.rivet.hp, 0.01), snappedf(main.bolt.wind, 0.01),
		snappedf(main.rivet.wind, 0.01), snappedf(main.bolt.position.x, 0.01), snappedf(main.rivet.position.x, 0.01), main.round_state]
	AudioServer.set_bus_mute(AudioServer.get_bus_index(&"Music"), false)
	AudioServer.set_bus_mute(AudioServer.get_bus_index(&"SFX"), false)
	return s

func test_mute_does_not_change_game() -> void:
	var a: Array = await scripted_fight(false)
	var b: Array = await scripted_fight(true)
	print("      unmuted end state ", a)
	print("      muted   end state ", b)
	ok(a == b, "sound never decides state: muted run == unmuted run")
