extends SceneTree
## Film tool (not part of the game): a SCRIPTED-INPUT Movie Maker capture of both A7
## clips in the running game. Run WINDOWED on an isolated copy of a5978c0, at 60 fps
## so every physics tick is a drawn frame (as the jab strips are):
##   godot --path <copy>/godot --resolution 3840x2160 --disable-vsync --always-on-top \
##         --write-movie <dir>/frame.png --fixed-fps 60 --script res://film_a7_play.gd
## It instantiates the unchanged game/main.tscn and goes through the title and intro.
## Bolt is driven only through the real input path (Input.parse_input_event, key
## events, as test_a7_edges.gd does). Rivet is driven by a stand-in brain with a fixed
## plan (the same method as test_a7_edges.gd's ScriptBrain): idle, except one cutlass
## request per interrupt case. Between cases both fighters stand IDLE and their x is
## SET (a SETUP line in the log), as the edge test does; the film labels it.
## Cases (gap = Rivet x - Bolt x; e = the tick Bolt's JAB starts):
##   1 WHIFF      gap 90: the jab (reach 54) misses
##   2 LAND       gap 70: the jab lands on e+5; hitstop holds both fighters 5 ticks
##   3 STARTUP    gap 90: Rivet's cutlass (reach 78, lands on its 9th tick) requested
##                on e+k-9 lands on e+k, k = 3
##   4 ACTIVE     the same, k = 7
##   5 RECOVERY   the same, k = 15
##   6 REWIND     Bolt holds S (wind 40 after five jabs): the key turns, clicks to
##                full wind, then holds; release
## It never writes a clip, a player, the rig or any fighter state other than the SET
## x positions. One log line per physics tick (after both fighters stepped).

const KEY_J_CODE := KEY_J
const KEY_S_CODE := KEY_S

class Driver extends Node:
	var game
	var tick := 0
	var schedule := {}
	func _ready() -> void:
		process_physics_priority = 1000
	func _physics_process(_dt: float) -> void:
		var b = game.bolt
		var r = game.rivet
		var fa: AnimationPlayer = b.fighter_anim
		var ka: AnimationPlayer = b.key_anim
		var c: Vector2 = b.get_global_transform_with_canvas().origin
		print("tick %d frame %d round %d bolt %s t %.4f x %.2f rot %.3f bob %.2f fa %s fa_pos %.4f key %d ka %s wind %.0f hitstop %.3f rivet %s rwind %.0f gap %.1f hp %.0f canvas %.1f %.1f" % [
			tick, Engine.get_process_frames(), game.round_state, Fighter.S.keys()[b.state], b.state_t,
			b.body_pivot.position.x, b.body_pivot.rotation, b.key_bob.position.y,
			String(fa.current_animation) if fa.current_animation != &"" else "-",
			fa.current_animation_position if fa.current_animation != &"" else -1.0,
			b.key_sprite.frame, String(ka.current_animation) if ka.current_animation != &"" else "-",
			b.wind, b.hitstop, Fighter.S.keys()[r.state], r.wind, r.position.x - b.position.x, b.hp, c.x, c.y])
		for ev in schedule.get(tick, []):
			var k := InputEventKey.new()
			k.physical_keycode = ev[0]
			k.pressed = ev[1]
			Input.parse_input_event(k)
		tick += 1

class StandIn:
	var me
	var driver
	var plan := {}
	func think(_dt) -> void:
		var it := {"move": 0, "jab": false, "cutlass": false, "pop": false, "block": false, "rewind": false}
		var p: Dictionary = plan.get(driver.tick, {})
		for k in p:
			it[k] = p[k]
		me.intent = it

var main
var d: Driver
var brain: StandIn

func _initialize() -> void:
	call_deferred("run")

func land(t: int, code: int, down: bool) -> void:
	if not d.schedule.has(t - 1):
		d.schedule[t - 1] = []
	d.schedule[t - 1].append([code, down])

func tap(t: int, code: int) -> void:
	land(t, code, true)
	land(t + 1, code, false)

func run_to(t: int) -> void:
	while d.tick <= t:
		await physics_frame

func setup(bolt_x: float, gap: float, label: String) -> void:
	main.bolt.position.x = bolt_x
	main.rivet.position.x = bolt_x + gap
	print("SETUP tick %d case %s bolt x %.0f rivet x %.0f gap %.0f" % [d.tick, label, bolt_x, bolt_x + gap, gap])

func confirm() -> void:
	for pressed in [true, false]:
		var ev := InputEventAction.new()
		ev.action = "confirm"
		ev.pressed = pressed
		Input.parse_input_event(ev)
		await physics_frame

func run() -> void:
	main = load("res://game/main.tscn").instantiate()
	root.add_child(main)
	await physics_frame
	brain = StandIn.new()
	brain.me = main.rivet
	main.brain = brain
	d = Driver.new()
	d.game = main
	brain.driver = d
	main.add_child(d)
	for i in 20:
		await physics_frame
	await confirm()                                  # TITLE -> INTRO
	while main.round_state != main.R.FIGHT:
		await physics_frame
	print("FIGHT at tick %d" % d.tick)
	await run_to(d.tick + 30)
	var cases := [["1 WHIFF", 90.0, -1], ["2 LAND", 70.0, -1], ["3 STARTUP", 90.0, 3], ["4 ACTIVE", 90.0, 7], ["5 RECOVERY", 90.0, 15]]
	for c in cases:
		setup(300.0, c[1], c[0])
		var e := d.tick + 24
		tap(e, KEY_J_CODE)
		if c[2] >= 0:
			brain.plan[e + c[2] - 9] = {"cutlass": true}
			print("CASE %s: jab on tick %d, cutlass requested on tick %d, hit planned on tick %d (e+%d)" % [c[0], e, e + c[2] - 9, e + c[2], c[2]])
		else:
			print("CASE %s: jab on tick %d" % [c[0], e])
		await run_to(e + 70)
	setup(300.0, 120.0, "6 REWIND")
	var s := d.tick + 20
	land(s, KEY_S_CODE, true)
	land(s + 150, KEY_S_CODE, false)
	print("CASE 6 REWIND: S held from tick %d to %d" % [s, s + 150])
	await run_to(s + 190)
	print("film capture done at tick %d" % d.tick)
	quit()
