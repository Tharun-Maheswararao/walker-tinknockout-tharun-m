extends SceneTree
## A7 Step 6: edge tests for the committing action, jab_action (CHANGE-BRIEF.md §4
## "Edge-input & interrupt outcomes", rule B-R3). Written by Claude.
##   ./scripts/run-test.sh test_a7_edges.gd 60
## Pinned at 60 only: at --fixed-fps 30 input can only arrive on a frame's first
## tick, so a press cannot land on an odd tick (test_a7_pins.gd P5). The test
## checks that each press landed on the intended tick and fails if it did not.
##
## For each phase boundary of the table (startup->active on 5, active->recovery
## on 11, recovery->IDLE on 21), with e the tick JAB starts:
##   E1 a jab press landing one tick before, on and after it (4/5/6, 10/11/12,
##      20/21/22): what the state machine does and what the clip shows;
##   E2 other inputs in each phase (move, block, rewind) are ignored too;
##   E3 an interrupt by a hit landing before, on and after each boundary
##      (4/5/6, 10/11/12, 20/21/22): JAB -> HURT, rig at rest, no clip, that tick;
##   E4 a pause landing on each boundary tick: the clip freezes with state_t,
##      and after it the boundary still falls where the table puts it.
## Input: Bolt through Input.parse_input_event; Rivet through a stand-in brain.
## It proves the state machine and the clip agree at every boundary; it cannot
## show whether the interrupts read well (the Step 7 strip and play do).
## Exit code = number of failed checks.

const F := 60.0
var checks := 0
var failures := 0
var JAB: Animation

func ok(cond: bool, msg: String) -> void:
	checks += 1
	if not cond:
		failures += 1
	print(("PASS  " if cond else "FAIL  ") + msg)

class Driver extends Node:
	var game
	var tick := 0
	var schedule := {}
	var rows: Array = []
	var transitions: Array = []
	func _ready() -> void:
		process_physics_priority = 1000
	func _physics_process(_dt: float) -> void:
		var b = game.bolt
		var fa: AnimationPlayer = b.fighter_anim
		rows.append({"tick": tick, "state": b.state, "t": b.state_t, "x": b.body_pivot.position.x,
			"rot": b.body_pivot.rotation, "bob": b.key_bob.position.y, "fa": String(fa.current_animation),
			"fa_pos": fa.current_animation_position if fa.current_animation != &"" else -1.0,
			"jab": b.intent.jab, "px": b.position.x, "paused": game.paused, "frame": Engine.get_process_frames()})
		for ev in schedule.get(tick, []):
			var k := InputEventKey.new()
			k.physical_keycode = ev[0]
			k.pressed = ev[1]
			Input.parse_input_event(k)
		tick += 1

class ScriptBrain:
	var me
	var driver
	var plan := {}
	func think(_dt) -> void:
		var it := {"move": 0, "jab": false, "cutlass": false, "pop": false, "block": false, "rewind": false}
		var p: Dictionary = plan.get(driver.tick, {})
		for k in p:
			it[k] = p[k]
		me.intent = it

func land(d: Driver, t: int, code: int, down: bool) -> void:
	if not d.schedule.has(t - 1):
		d.schedule[t - 1] = []
	d.schedule[t - 1].append([code, down])

func tap(d: Driver, t: int, code: int) -> void:
	land(d, t, code, true)
	land(d, t + 1, code, false)

func fresh(bolt_x: float, rivet_x: float) -> Array:
	var main = load("res://game/main.tscn").instantiate()
	root.add_child(main)
	await process_frame
	var d := Driver.new()
	var brain := ScriptBrain.new()
	brain.me = main.rivet
	brain.driver = d
	main.brain = brain
	main._set_round(main.R.INTRO)
	while main.round_state != main.R.FIGHT:
		await physics_frame
	main.bolt.position.x = bolt_x     # SETUP
	main.rivet.position.x = rivet_x   # SETUP
	d.game = main
	main.bolt.state_changed.connect(func(_f, o, n): d.transitions.append([d.tick, o, n]))
	main.add_child(d)
	await physics_frame
	return [main, d, brain]

func run_to(d: Driver, t: int) -> void:
	while d.tick <= t:
		await physics_frame

func done(main) -> void:
	main.queue_free()
	await process_frame

func entries(d: Driver, s: int, a: int, b: int) -> Array:
	return d.transitions.filter(func(x): return x[2] == s and x[0] >= a and x[0] <= b).map(func(x): return x[0])

func near(a: float, b: float, eps := 1e-3) -> bool:
	return absf(a - b) < eps

func clip_x(t: float) -> float:
	return JAB.value_track_interpolate(JAB.find_track(NodePath("FacingPivot/BodyPivot:position:x"), Animation.TYPE_VALUE), t)

## The clip shows exactly its own value at state_t on every JAB tick in [a, b].
func clip_in_step(d: Driver, a: int, b: int) -> bool:
	for i in range(a, b + 1):
		var r: Dictionary = d.rows[i]
		if r.state != Fighter.S.JAB:
			continue
		if r.fa != "jab_action" or absf(r.fa_pos - r.t) > 0.5 / F or not near(r.x, clip_x(r.t)):
			return false
	return true

func at_rest(r: Dictionary) -> bool:
	return near(r.x, 0.0) and near(r.rot, 0.0) and near(r.bob, 0.0) and r.fa == ""

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	var S := Fighter.S
	JAB = load("res://animations/jab_action.tres")
	var phase_of := func(k: int) -> String: return "startup" if k <= 4 else ("active" if k <= 10 else ("recovery" if k <= 20 else "after the jab"))

	# --- E1: a second jab press around every boundary ------------------------
	print("-- E1 jab press one tick before, on and after each boundary")
	var r: Array = await fresh(200, 440)
	var main = r[0]
	var d: Driver = r[1]
	var base := 5
	var tpf := 1
	for k in [4, 5, 6, 10, 11, 12, 20, 21, 22]:
		tap(d, base, KEY_J)
		tap(d, base + k, KEY_J)
		await run_to(d, base + 50)
		var e: int = entries(d, S.JAB, base, base + 1)[0] if entries(d, S.JAB, base, base + 1).size() else -1
		var landed := -1
		for i in range(e + 1, e + 30):
			if d.rows[i].jab:
				landed = i
				break
		ok(e == base and landed == e + k, "E1 setup: JAB on e=%d, second press landed on e+%d (want e+%d)" % [e, landed - e, k])
		var jabs := entries(d, S.JAB, base, base + 48)
		if k <= 21:
			ok(jabs == [e] and d.rows[e + 20].state == S.JAB and d.rows[e + 21].state == S.IDLE,
				"E1 press on e+%d (%s, %s boundary %d): lost; one JAB, IDLE on e+21 (JAB entries %s)" % [k, phase_of.call(k), "on" if k in [5, 11, 21] else ("before" if k in [4, 10, 20] else "after"), [5, 11, 21][[4, 5, 6, 10, 11, 12, 20, 21].find(k) / 3], jabs])
			ok(clip_in_step(d, e, e + 20) and at_rest(d.rows[e + 21]), "E1 press on e+%d: jab_action runs uninterrupted at state_t and ends at rest on e+21" % k)
		else:
			ok(jabs == [e, e + 22] and at_rest(d.rows[e + 21]) and d.rows[e + 22].fa == "jab_action" and near(d.rows[e + 22].fa_pos, 0.0, 1e-5),
				"E1 press on e+22 (after the end boundary): a new JAB starts on e+22 with jab_action from 0 (entries %s)" % [jabs])
		tpf = maxi(tpf, d.rows.filter(func(x): return x.frame == d.rows[e].frame).size())
		main.bolt.wind = 100.0   # SETUP between trials
		base += 60
	ok(tpf == 1, "E1 ran with one physics tick per frame, as the edge tests need (got %d)" % tpf)
	# what the clip shows at the boundaries (brief §4, "Clip outcome")
	var e1 := 5
	ok(near(d.rows[e1 + 4].x, -1.0) and near(d.rows[e1 + 5].x, 14.0) and near(d.rows[e1 + 6].x, 14.0), "E1 clip: coil eases out to -1 px on e+4, full extension +14 on e+5 and e+6")
	ok(near(d.rows[e1 + 10].x, 14.0) and near(d.rows[e1 + 11].x, 8.0) and d.rows[e1 + 12].x < 8.0, "E1 clip: holds +14 on e+10, retracts to +8 on e+11, eases back on e+12 (%.2f)" % d.rows[e1 + 12].x)
	ok(near(d.rows[e1 + 20].x, clip_x(20.0 / F)) and at_rest(d.rows[e1 + 21]), "E1 clip: e+20 at %.2f px, rest on e+21" % d.rows[e1 + 20].x)
	await done(main)

	# --- E2: other inputs in each phase --------------------------------------
	print("\n-- E2 move, block and rewind inputs in each phase are ignored")
	r = await fresh(200, 440); main = r[0]; d = r[1]
	var e := 5
	tap(d, e, KEY_J)
	land(d, e + 2, KEY_D, true); land(d, e + 4, KEY_D, false)     # startup: move
	land(d, e + 5, KEY_I, true); land(d, e + 9, KEY_I, false)     # active: block
	land(d, e + 11, KEY_S, true); land(d, e + 18, KEY_S, false)   # recovery: rewind
	await run_to(d, e + 30)
	ok(d.rows.slice(e, e + 21).all(func(x): return x.state == S.JAB) and d.rows[e + 21].state == S.IDLE, "E2 move in startup, block in active, rewind in recovery: JAB runs its 21 ticks, IDLE on e+21")
	ok(near(d.rows[e + 5].px, d.rows[e].px), "E2 the move input did not move Bolt during the jab (x %.1f -> %.1f)" % [d.rows[e].px, d.rows[e + 5].px])
	ok(clip_in_step(d, e, e + 20), "E2 jab_action stays at state_t throughout")
	await done(main)

	# --- E3: a hit around every boundary --------------------------------------
	print("\n-- E3 a hit landing one tick before, on and after each boundary")
	for k in [4, 5, 6, 10, 11, 12, 20, 21, 22]:
		# Gap 90: Bolt's jab (reach 54) whiffs, Rivet's cutlass (reach 78) lands on its 9th tick.
		r = await fresh(300, 390); main = r[0]; d = r[1]
		e = 20
		tap(d, e, KEY_J)
		r[2].plan[e + k - 9] = {"cutlass": true}
		await run_to(d, e + k + 12)
		var h: Array = entries(d, S.HURT, e, e + k + 10)
		var before: int = d.rows[e + k - 1].state
		var hit_ok: bool = h.size() == 1 and h[0] == e + k
		if k <= 20:
			ok(hit_ok and before == S.JAB, "E3 hit on e+%d (%s): JAB -> HURT that tick (HURT on %s)" % [k, phase_of.call(k), h.map(func(x): return "e+%d" % (x - e))])
		elif k == 21:
			# Bolt steps before Rivet (main.gd:181-182): on e+21 his jab ends first
			# (JAB -> IDLE), then Rivet's cutlass lands (IDLE -> HURT), in one tick.
			var on21 := d.transitions.filter(func(x): return x[0] == e + 21).map(func(x): return [x[1], x[2]])
			ok(hit_ok and on21 == [[S.JAB, S.IDLE], [S.IDLE, S.HURT]], "E3 hit on e+21 (on the end boundary): the jab ends, then the hit lands, both on e+21 (transitions that tick %s)" % [on21.map(func(x): return "%s>%s" % [Fighter.S.keys()[x[0]], Fighter.S.keys()[x[1]]])])
		else:
			ok(hit_ok and before == S.IDLE, "E3 hit on e+%d (%s): IDLE -> HURT that tick, the jab already over (HURT on %s)" % [k, phase_of.call(k), h.map(func(x): return "e+%d" % (x - e))])
		ok(at_rest(d.rows[e + k]) and d.rows.slice(e + k, e + k + 6).all(func(x): return at_rest(x)), "E3 hit on e+%d: no clip and the rig at rest from the hit tick through the hitstop" % k)
		if k <= 20:
			ok(clip_in_step(d, e, e + k - 1), "E3 hit on e+%d: until then jab_action was at state_t" % k)
		await done(main)

	# --- E4: a pause landing on each boundary ---------------------------------
	print("\n-- E4 pause landing on each boundary tick")
	for k in [5, 11, 21]:
		r = await fresh(200, 440); main = r[0]; d = r[1]
		e = 5
		tap(d, e, KEY_J)
		tap(d, e + k, KEY_P)
		tap(d, e + k + 8, KEY_P)
		await run_to(d, e + 50)
		var pr := d.rows.filter(func(x): return x.paused)
		var frozen := pr.size() == 8 and pr.all(func(x): return near(x.t, pr[0].t, 1e-6) and near(x.x, pr[0].x, 1e-6))
		ok(frozen and near(pr[0].t, (k - 1) / F), "E4 pause on e+%d: 8 paused ticks frozen at state_t %.4f (the e+%d pose)" % [k, pr[0].t if pr.size() else -1.0, k - 1])
		var live := d.rows.filter(func(x): return x.state == S.JAB and not x.paused)
		ok(live.size() == 21, "E4 pause on e+%d: the jab still runs 21 unpaused ticks (got %d)" % [k, live.size()])
		var first_active := live.filter(func(x): return x.t >= 0.07)
		ok(first_active.size() and near(first_active[0].t, 5.0 / F) and near(first_active[0].x, 14.0), "E4 pause on e+%d: active still opens at state_t 5/60 with the +14 pose" % k)
		ok(clip_in_step(d, e, d.rows.size() - 1), "E4 pause on e+%d: jab_action at state_t on every JAB tick, paused or not" % k)
		await done(main)

	print("\n%d checks, %d failed" % [checks, failures])
	quit(failures)
