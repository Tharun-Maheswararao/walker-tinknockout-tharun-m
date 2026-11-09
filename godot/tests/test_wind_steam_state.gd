extends SceneTree
## Effect B state test (CHANGE-BRIEF B.4: B-R1 … B-R6, B.1 one per fighter, F5).
##   ./scripts/run-test.sh test_wind_steam_state.gd 60
##
## Drives the real game: main.tscn, the real physics loop, and Bolt through the
## real Input path (Input.action_press/release, parsed pause and rematch events),
## as test_slice.gd does. Wind moves only through real jabs (12 each,
## fighter.gd:42) and real rewinding (+10 per click). Rivet is frozen by a
## stand-in brain (SETUP, like test_slice's FrozenBrain). Setup lines only place
## fighters or set hp (marked SETUP). The test never calls steam_ratio() and never
## sets amount_ratio; it finds each fighter's steam under key_sprite and reads it.
##
## Proves: which amount_ratio the wiring sets for each wind value reached in
## play; that amount never changes; per-fighter independence; pause, KO hiding
## and the rematch reset. Cannot prove how the steam looks, whether it fades
## smoothly, or what a hidden emitter shows when it reappears: a headless run
## draws nothing. Exit code = number of failed checks.

const STEAM := "res://effects/wind_steam.tscn"

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

func press_event(action: String) -> void:
	for pressed in [true, false]:
		var ev := InputEventAction.new()
		ev.action = action
		ev.pressed = pressed
		Input.parse_input_event(ev)
		await frames(1)

class FrozenBrain:
	func think(_dt): pass

func steam_of(f: Fighter) -> GPUParticles2D:
	for c in f.key_sprite.get_children():
		if c.scene_file_path == STEAM:
			return c
	return null

func jab() -> void:
	await tap("jab")
	await frames(30)          # jab is 0.35 s; it whiffs at this range, so no hitstop

func run() -> void:
	print("== B-R6: scene load")
	main = load("res://game/main.tscn").instantiate()
	root.add_child(main)
	await frames(2)
	var bs := steam_of(main.bolt)
	var rs := steam_of(main.rivet)
	ok(bs != null and rs != null, "each fighter has one wind_steam under its key_sprite (B.3, one per fighter)")
	if bs == null or rs == null:
		print("\n%d checks, %d failed" % [checks, failures])
		quit(failures)
		return
	ok(bs.amount_ratio == 0.0 and rs.amount_ratio == 0.0, "B-R6 amount_ratio 0 on load (Bolt %.2f, Rivet %.2f)" % [bs.amount_ratio, rs.amount_ratio])
	ok(bs.emitting and rs.emitting and bs.amount == 25 and rs.amount == 25, "emitting on, amount 25 on load")
	main.brain = FrozenBrain.new()                                  # SETUP: Rivet idles
	main._set_round(main.R.INTRO)
	await frames(int(main.INTRO_TIME * 60) + 3)
	ok(main.round_state == main.R.FIGHT, "round reached FIGHT")
	ok(bs.amount_ratio == 0.0 and rs.amount_ratio == 0.0, "B-R6 amount_ratio still 0 at round start, wind 100")

	print("== B-R1, B-R3: real jabs drain Bolt's wind")
	main.bolt.position.x = 150; main.rivet.position.x = 450         # SETUP: out of range, jabs whiff
	for i in 6:
		await jab()
	ok(is_equal_approx(main.bolt.wind, 28.0), "6 jabs: wind 100 -> 28 (got %.1f)" % main.bolt.wind)
	ok(bs.amount_ratio == 0.0, "B-R1 still dormant at wind 28 >= 25 (ratio %.3f)" % bs.amount_ratio)
	await jab()
	ok(is_equal_approx(main.bolt.wind, 16.0), "7th jab: wind 16 (got %.1f)" % main.bolt.wind)
	ok(bs.amount_ratio > 0.0, "B-R1 active once wind drops below 25 (ratio %.3f)" % bs.amount_ratio)
	ok(is_equal_approx(bs.amount_ratio, 0.36), "B-R3 ratio 0.36 at wind 16 (got %.3f)" % bs.amount_ratio)
	ok(bs.amount == 25, "B-R3 amount still 25 at wind 16 (got %d)" % bs.amount)
	await jab()
	ok(is_equal_approx(main.bolt.wind, 4.0), "8th jab: wind 4 (got %.1f)" % main.bolt.wind)
	ok(is_equal_approx(bs.amount_ratio, 0.84), "B-R3 ratio 0.84 at wind 4 (got %.3f)" % bs.amount_ratio)
	ok(bs.amount == 25, "B-R3 amount still 25 at wind 4: the code changes amount_ratio, not amount (got %d)" % bs.amount)
	ok(rs.amount_ratio == 0.0 and is_equal_approx(main.rivet.wind, 100.0),
		"one per fighter: Rivet's ratio stays 0 at his wind 100 while Bolt's rises (Rivet %.2f)" % rs.amount_ratio)

	print("== B-R4: pause holds the steam as it is")
	await press_event("pause")
	ok(main.paused, "main.paused set (real pause event)")
	Input.action_press("move_right")
	await frames(20)
	Input.action_release("move_right")
	await tap("jab")
	await frames(10)
	ok(is_equal_approx(main.bolt.wind, 4.0), "wind unchanged while paused (got %.1f)" % main.bolt.wind)
	ok(is_equal_approx(bs.amount_ratio, 0.84) and bs.emitting and is_equal_approx(bs.speed_scale, 1.0),
		"B-R4 ratio 0.84, emitting, speed_scale 1 while paused (ratio %.3f, speed %.2f)" % [bs.amount_ratio, bs.speed_scale])
	ok(bs.can_process(), "B-R4 steam still processes while paused (PROCESS_MODE_ALWAYS inherited)")
	await press_event("pause")
	ok(not main.paused, "unpaused")

	print("== F5, B-R2: real rewinding raises the wind back past 25")
	var at24 := -1.0
	var n := 0
	Input.action_press("rewind")
	while main.bolt.wind < 34.0 and n < 120:
		await frames(1)
		n += 1
		if is_equal_approx(main.bolt.wind, 24.0) and at24 < 0.0:
			at24 = bs.amount_ratio
	Input.action_release("rewind")
	await frames(2)
	ok(is_equal_approx(at24, 0.04), "ratio 0.04 at wind 24 (got %.3f)" % at24)
	ok(is_equal_approx(bs.amount * at24, 1.0), "F5 at wind 24, amount x amount_ratio = %.2f: the first whole particle" % (bs.amount * at24))
	ok(is_equal_approx(main.bolt.wind, 34.0), "3 clicks: wind 34 (got %.1f)" % main.bolt.wind)
	ok(bs.amount_ratio == 0.0, "B-R2 ratio back to 0 above 25 (got %.3f)" % bs.amount_ratio)
	ok(bs.emitting, "B-R2 emitting stays true, so live puffs finish their lives")
	ok(bs.amount == 25, "amount still 25 after rewinding")

	print("== B-R5: KO hides the steam with the key")
	main.bolt.position.x = 300; main.rivet.position.x = 350         # SETUP: in jab range
	main.rivet.hp = 5.0                                             # SETUP: the next jab is the KO
	await tap("jab")
	await frames(20)
	ok(main.rivet.state == Fighter.S.KO and main.round_state == main.R.KO, "jab at 5 hp -> Rivet KO")
	ok(not main.rivet.key_sprite.visible, "Rivet's key_sprite hidden on KO (fighter.gd:274)")
	ok(not rs.is_visible_in_tree(), "B-R5 Rivet's steam is not visible in the tree")
	ok(main.bolt.key_sprite.visible and bs.is_visible_in_tree(), "Bolt's key and steam still visible")

	print("== B-R6: rematch resets both")
	ok(bs.amount_ratio > 0.0, "before the rematch Bolt's ratio is above 0 (wind %.1f, ratio %.3f)" % [main.bolt.wind, bs.amount_ratio])
	await press_event("rematch")
	await frames(2)
	ok(main.round_state == main.R.INTRO, "rematch (real event) -> INTRO")
	ok(bs.amount_ratio == 0.0 and rs.amount_ratio == 0.0,
		"B-R6 both ratios 0 after reset() announces wind 100 (Bolt %.2f, Rivet %.2f)" % [bs.amount_ratio, rs.amount_ratio])
	ok(steam_of(main.bolt) == bs and steam_of(main.rivet) == rs, "the same two steam nodes: none added on rematch")

	print("\n%d checks, %d failed" % [checks, failures])
	quit(failures)
