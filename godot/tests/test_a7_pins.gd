extends SceneTree
## A7 Step 2: behaviour pins. They record what the game does BEFORE any clip
## exists, and must still pass after A7 (CHANGE-BRIEF.md §7: no timing,
## transition or input change). Written by Claude for Tharun's review.
##   ./scripts/run-test.sh test_a7_pins.gd 60      (pinned mode; also passes at 30)
##
## How it drives the game:
##   - the real main.tscn, real round flow (INTRO -> FIGHT), real physics loop;
##   - Bolt's input is real key events through Input.parse_input_event (physical
##     keycodes, as godot/game/controls.gd binds them). Godot buffers parsed
##     events and flushes them once per drawn frame, before that frame's physics
##     ticks. At --fixed-fps 60 (one tick per frame) an event parsed during tick
##     T-1 reaches the game on tick T. At 30 (two ticks per frame) it can only
##     arrive on the first tick of a frame, so it may land one tick later
##     (measured 2026-11-19). Every check below is therefore anchored on the tick
##     an action ACTUALLY started and the tick each press ACTUALLY landed
##     (Bolt's intent), never on the scheduled tick;
##   - Rivet has no player input; a scripted stand-in brain sets his intent
##     (the same seam rivet_brain.gd uses, main.gd:155);
##   - a logger node runs after main each physics tick (priority 1000) and
##     records Bolt's state, state_t, attack box, hitstop, wind, intent and pause.
## SETUP lines place fighters or set wind/hp between trials; assertions only
## read results. It reads behaviour only (state, timing, boxes, wind): no node
## names or clips, so the A7 presentation change cannot move these numbers.
## Exit code = number of failed checks.

var checks := 0
var failures := 0

func ok(cond: bool, msg: String) -> void:
	checks += 1
	if not cond:
		failures += 1
	print(("PASS  " if cond else "FAIL  ") + msg)

class Driver extends Node:
	var game
	var tick := 0
	var schedule := {}        # tick -> [[keycode, pressed], ...], parsed DURING that tick
	var rows: Array = []
	var transitions: Array = []   # Bolt: [tick, old, new]
	var hits: Array = []          # [tick, attacker skin, attack, blocked]
	var verbose := false
	func _ready() -> void:
		process_physics_priority = 1000   # after main (priority 0)
	func _physics_process(_dt: float) -> void:
		var b = game.bolt
		var row := {"tick": tick, "state": b.state, "t": b.state_t, "box": b.attack_box().has_area(),
			"hitstop": b.hitstop, "wind": b.wind, "hp": b.hp, "rstate": game.rivet.state, "paused": game.paused,
			"jab": b.intent.jab, "rewind": b.intent.rewind, "frame": Engine.get_process_frames()}
		rows.append(row)
		if verbose:
			print("P1 tick %3d  %-8s t=%.4f box=%s wind=%5.1f paused=%s" % [tick, Fighter.S.keys()[b.state], b.state_t,
				"LIVE" if row.box else "-", b.wind, game.paused])
		for ev in schedule.get(tick, []):
			var k := InputEventKey.new()
			k.physical_keycode = ev[0]
			k.pressed = ev[1]
			Input.parse_input_event(k)
		tick += 1

class ScriptBrain:
	var me
	var driver
	var plan := {}            # tick -> intent overrides for Rivet on that tick
	func think(_dt) -> void:
		var it := {"move": 0, "jab": false, "cutlass": false, "pop": false, "block": false, "rewind": false}
		var p: Dictionary = plan.get(driver.tick, {})
		for k in p:
			it[k] = p[k]
		me.intent = it

## Schedules a key change for tick t (at 30 fps it may land on t+1).
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
	for f in [main.bolt, main.rivet]:
		f.hit_landed.connect(func(a, atk, bl): d.hits.append([d.tick, a.skin, atk, bl]))
	main.add_child(d)
	await physics_frame
	return [main, d, brain]

func run_to(d: Driver, t: int) -> void:
	while d.tick <= t:
		await physics_frame

func done(main) -> void:
	main.queue_free()
	await process_frame

func live_ticks(d: Driver, a: int, b: int) -> Array:
	var out := []
	for r in d.rows.slice(a, b + 1):
		if r.box:
			out.append(r.tick)
	return out

func entries(d: Driver, s: int, a: int, b: int) -> Array:
	return d.transitions.filter(func(x): return x[2] == s and x[0] >= a and x[0] <= b).map(func(x): return x[0])

func first_entry(d: Driver, s: int, a: int) -> int:
	var e := entries(d, s, a, 1 << 30)
	return e[0] if e.size() else -1

## First tick at or after a on which Bolt's intent[key] is true (the press landed).
func landed(d: Driver, key: String, a: int) -> int:
	for r in d.rows.slice(a):
		if r[key]:
			return r.tick
	return -1

func sname(s: int) -> String:
	return Fighter.S.keys()[s] if s >= 0 else "-"

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	print("test_a7_pins: physics %d ticks/s" % Engine.physics_ticks_per_second)
	var S := Fighter.S

	# --- P1: one scripted run, every transition in order -----------------
	print("\n-- P1 scripted run: walk, jab, cutlass, block, rewind")
	var r: Array = await fresh(200, 440)
	var main = r[0]
	var d: Driver = r[1]
	d.verbose = true
	land(d, 3, KEY_D, true);  land(d, 23, KEY_D, false)
	tap(d, 30, KEY_J)
	tap(d, 60, KEY_K)
	land(d, 100, KEY_I, true); land(d, 110, KEY_I, false)
	land(d, 120, KEY_S, true); land(d, 140, KEY_S, false)
	await run_to(d, 150)
	d.verbose = false
	var want := [[S.IDLE, S.WALK], [S.WALK, S.IDLE], [S.IDLE, S.JAB], [S.JAB, S.IDLE], [S.IDLE, S.CUTLASS],
		[S.CUTLASS, S.IDLE], [S.IDLE, S.BLOCK], [S.BLOCK, S.IDLE], [S.IDLE, S.REWIND], [S.REWIND, S.IDLE]]
	var got: Array = d.transitions.map(func(x): return [x[1], x[2]])
	print("P1 transition ticks: %s" % [d.transitions.map(func(x): return "%d %s->%s" % [x[0], sname(x[1]), sname(x[2])])])
	ok(got == want, "P1 order IDLE>WALK>IDLE>JAB>IDLE>CUTLASS>IDLE>BLOCK>IDLE>REWIND>IDLE (got %s)" % [got.map(func(x): return sname(x[1]))])
	if d.transitions.size() == want.size():
		var tt: Array = d.transitions.map(func(x): return x[0])
		var dur := [tt[1] - tt[0], tt[3] - tt[2], tt[5] - tt[4], tt[7] - tt[6], tt[9] - tt[8]]
		ok(dur[1] == 21, "P1 JAB lasts 21 ticks (got %d)" % dur[1])
		ok(dur[2] == 34, "P1 CUTLASS lasts 34 ticks (got %d)" % dur[2])
		ok(dur[0] == 20 and dur[3] == 10 and dur[4] == 20, "P1 WALK, BLOCK and REWIND last as long as their keys are held: 20, 10, 20 (got %s)" % [[dur[0], dur[3], dur[4]]])
	else:
		ok(false, "P1 durations (transition count wrong)")
	await done(main)

	# --- P2: jab, whiff ---------------------------------------------------
	print("\n-- P2 jab whiff (phase ticks)")
	r = await fresh(200, 440); main = r[0]; d = r[1]
	tap(d, 5, KEY_J)
	await run_to(d, 40)
	var e := first_entry(d, S.JAB, 0)
	print("P2 JAB entered on tick %d" % e)
	ok(e >= 0 and is_zero_approx(d.rows[e].t), "P2 JAB entry tick has state_t 0 (got %.4f)" % (d.rows[e].t if e >= 0 else -1.0))
	ok(live_ticks(d, e, e + 25) == range(e + 5, e + 11), "P2 box live on e+5..e+10, 6 ticks (got %s, e=%d)" % [live_ticks(d, e, e + 25), e])
	ok(d.rows[e + 4].t < 0.07 and d.rows[e + 5].t >= 0.07, "P2 startup ends on e+4 (state_t %.4f < 0.07), active opens on e+5 (%.4f)" % [d.rows[e + 4].t, d.rows[e + 5].t])
	ok(d.rows[e + 20].state == S.JAB and d.rows[e + 21].state == S.IDLE, "P2 last JAB tick e+20, IDLE on e+21 (21 ticks, 0.35 s)")
	ok(is_equal_approx(d.rows[e - 1].wind - d.rows[e].wind, 12.0), "P2 jab costs 12 wind on entry (%.1f -> %.1f)" % [d.rows[e - 1].wind, d.rows[e].wind])
	ok(landed(d, "jab", 0) == e, "P2 JAB starts on the tick the press lands (press %d, JAB %d)" % [landed(d, "jab", 0), e])
	await done(main)

	# --- P3: cutlass, whiff ----------------------------------------------
	print("\n-- P3 cutlass whiff (phase ticks)")
	r = await fresh(200, 440); main = r[0]; d = r[1]
	tap(d, 5, KEY_K)
	await run_to(d, 50)
	e = first_entry(d, S.CUTLASS, 0)
	ok(live_ticks(d, e, e + 38) == range(e + 9, e + 16), "P3 box live on e+9..e+15, 7 ticks (got %s, e=%d)" % [live_ticks(d, e, e + 38), e])
	ok(d.rows[e + 33].state == S.CUTLASS and d.rows[e + 34].state == S.IDLE, "P3 last CUTLASS tick e+33, IDLE on e+34 (34 ticks)")
	await done(main)

	# --- P4: jab lands on an idle Rivet: the active window and hitstop ----
	print("\n-- P4 jab lands (the gameplay fact the clip is read against)")
	r = await fresh(390, 440); main = r[0]; d = r[1]
	tap(d, 5, KEY_J)
	await run_to(d, 50)
	e = first_entry(d, S.JAB, 0)
	var bh := d.hits.filter(func(h): return h[1] == "bolt")
	ok(bh.size() == 1 and bh[0][0] == e + 5 and bh[0][2] == "jab" and not bh[0][3], "P4 one unblocked jab hit, on e+5, the first active tick (got %s, e=%d)" % [bh, e])
	var frozen := true
	for i in range(e + 6, e + 11):
		frozen = frozen and is_equal_approx(d.rows[i].t, d.rows[e + 5].t) and d.rows[i].state == S.JAB
	ok(frozen, "P4 hitstop: state_t frozen at %.4f on e+6..e+10 (5 ticks)" % d.rows[e + 5].t)
	ok(is_equal_approx(d.rows[e + 11].t, d.rows[e + 5].t + 1.0 / 60.0), "P4 state_t moves again on e+11 (%.4f)" % d.rows[e + 11].t)
	ok(d.rows[e + 25].state == S.JAB and d.rows[e + 26].state == S.IDLE, "P4 IDLE on e+26: a landed jab lasts 5 ticks longer than a whiff")
	ok(d.rows[e + 5].rstate == S.HURT, "P4 Rivet HURT on e+5")
	var r_idle := -1
	for i in range(e + 5, d.rows.size()):
		if d.rows[i].rstate == S.IDLE:
			r_idle = i
			break
	# Bolt steps before Rivet (main.gd:181-182): Bolt's hit sets Rivet's hitstop inside
	# Bolt's step, and Rivet's own step that same tick already spends the first hitstop
	# tick. So the defender is frozen on e+5..e+9, the attacker on e+6..e+10.
	ok(r_idle == e + 29, "P4 Rivet HURT -> IDLE on e+29: frozen e+5..e+9 (his step follows Bolt's), then 20 ticks (0.32 s) (got e+%d)" % (r_idle - e))
	await done(main)

	# --- P5: a second jab press near each phase boundary ------------------
	print("\n-- P5 second jab press before, on and after each boundary (no buffering)")
	r = await fresh(200, 440); main = r[0]; d = r[1]
	var base := 5
	var offsets := []
	for k in [4, 5, 6, 10, 11, 12, 20, 21, 22]:
		tap(d, base, KEY_J)
		tap(d, base + k, KEY_J)
		await run_to(d, base + 50)
		e = first_entry(d, S.JAB, base)
		var lk := landed(d, "jab", e + 1) - e      # where the second press really landed
		offsets.append(lk)
		var jabs := entries(d, S.JAB, base, base + 48)
		if lk <= 21:
			ok(jabs == [e], "P5 press landing on e+%d (scheduled e+%d) is lost: one JAB only (got %s, e=%d)" % [lk, k, jabs, e])
		else:
			ok(jabs == [e, e + lk], "P5 press landing on e+%d (scheduled e+%d): a new JAB starts that tick (got %s, e=%d)" % [lk, k, jabs, e])
		main.bolt.wind = 100.0   # SETUP between trials
		base += 60
	print("P5 second presses landed on e+%s" % [offsets])
	# How many physics ticks each drawn frame runs (1 at --fixed-fps 60, 2 at 30).
	var per_frame := {}
	for x in d.rows:
		per_frame[x.frame] = per_frame.get(x.frame, 0) + 1
	var tpf: int = per_frame.values().max()
	if tpf == 1:
		ok(offsets == [4, 5, 6, 10, 11, 12, 20, 21, 22], "P5 one tick per frame: every press landed where scheduled, incl. e+21 (lost) and e+22 (accepted) (landed %s)" % [offsets])
	else:
		ok(offsets.all(func(o): return o % tpf == 0), "P5 %d ticks per frame: input only arrives on a frame's first tick, so every press landed on an even offset from the jab (landed %s)" % [tpf, offsets])
	await done(main)

	# --- P6: Bolt hit in each phase of his jab ----------------------------
	print("\n-- P6 hit interrupts in startup, active and recovery")
	for k in [2, 7, 15]:
		# Gap 90: Bolt's jab (reach 54) whiffs, Rivet's cutlass (reach 78) lands.
		r = await fresh(300, 390); main = r[0]; d = r[1]
		var brain = r[2]
		tap(d, 20, KEY_J)
		brain.plan[20 + k - 9] = {"cutlass": true}   # Rivet's first active tick: tick 20+k
		await run_to(d, 60)
		e = first_entry(d, S.JAB, 0)
		var h := first_entry(d, S.HURT, e)
		var hk := h - e
		var phase := "startup" if hk <= 4 else ("active" if hk <= 10 else "recovery")
		var meant: String = {2: "startup", 7: "active", 15: "recovery"}[k]
		ok(h > e and d.rows[h - 1].state == S.JAB and d.rows[h].state == S.HURT, "P6 hit on e+%d (%s): JAB -> HURT that tick (got %s -> %s)" % [hk, phase, sname(d.rows[h - 1].state), sname(d.rows[h].state)])
		ok(phase == meant, "P6 the hit fell in %s as intended (e+%d)" % [meant, hk])
		ok(entries(d, S.IDLE, e, h).is_empty(), "P6 %s: the jab never reached its own end" % phase)
		ok(is_equal_approx(d.rows[h - 1].hp - d.rows[h].hp, 13.0), "P6 %s: Bolt takes the cutlass's 13 damage" % phase)
		await done(main)
	# KO interrupt
	r = await fresh(300, 390); main = r[0]; d = r[1]
	main.bolt.hp = 5.0   # SETUP
	tap(d, 20, KEY_J)
	r[2].plan[20 + 7 - 9] = {"cutlass": true}
	await run_to(d, 40)
	e = first_entry(d, S.JAB, 0)
	var ko := first_entry(d, S.KO, e)
	ok(ko > e and d.rows[ko - 1].state == S.JAB and ko - e >= 5 and ko - e <= 10, "P6 hit with hp 5 during active: JAB -> KO (on e+%d)" % (ko - e))
	await done(main)

	# --- P7: pause during the jab ------------------------------------------
	print("\n-- P7 pause mid-jab")
	r = await fresh(200, 440); main = r[0]; d = r[1]
	tap(d, 5, KEY_J)
	tap(d, 8, KEY_P)
	tap(d, 18, KEY_P)
	await run_to(d, 60)
	var paused_rows := d.rows.filter(func(x): return x.paused)
	var still := paused_rows.all(func(x): return x.state == S.JAB and is_equal_approx(x.t, paused_rows[0].t))
	ok(paused_rows.size() == 10 and still, "P7 paused for 10 ticks with JAB's state_t frozen at %.4f (paused ticks %d)" % [paused_rows[0].t if paused_rows.size() else -1.0, paused_rows.size()])
	var jab_live := d.rows.filter(func(x): return x.state == S.JAB and not x.paused).size()
	ok(jab_live == 21, "P7 the jab still runs 21 unpaused ticks (got %d)" % jab_live)
	await done(main)

	# --- P8: rewind clicks ---------------------------------------------------
	print("\n-- P8 rewind: a click every 15 ticks, none at full wind")
	r = await fresh(200, 440); main = r[0]; d = r[1]
	main.bolt.wind = 40.0   # SETUP
	land(d, 5, KEY_S, true)
	land(d, 140, KEY_S, false)
	await run_to(d, 150)
	var rw := first_entry(d, S.REWIND, 0)
	var clicks := []
	for i in range(1, d.rows.size()):
		if d.rows[i].wind > d.rows[i - 1].wind:
			clicks.append(d.rows[i].tick - rw)
	ok(rw >= 0 and landed(d, "rewind", 0) == rw, "P8 REWIND starts on the tick the key lands (tick %d)" % rw)
	ok(clicks == [15, 30, 45, 60, 75, 90], "P8 clicks on r+15, 30, 45, 60, 75, 90: 40 -> 100 (got r+%s)" % [clicks])
	ok(d.rows[rw + 125].state == S.REWIND and is_equal_approx(d.rows[rw + 125].wind, 100.0), "P8 still REWIND at full wind with no more clicks (r+125)")
	var out := first_entry(d, S.IDLE, rw)
	ok(out > rw and not d.rows[out].rewind and d.rows[out - 1].rewind, "P8 IDLE on the tick the release lands (tick %d)" % out)
	await done(main)

	# --- P9: EMPTY ------------------------------------------------------------
	print("\n-- P9 walking to 0 wind: EMPTY, then IDLE")
	r = await fresh(200, 440); main = r[0]; d = r[1]
	main.bolt.wind = 1.0   # SETUP: 20 ticks of walking (3 wind/s)
	land(d, 5, KEY_D, true)
	await run_to(d, 140)
	var z: Array = entries(d, S.EMPTY, 0, 140)
	var back: Array = entries(d, S.IDLE, 6, 140)
	ok(z.size() == 1, "P9 one EMPTY entry (got %s)" % [z])
	# 96 x (1/60) added one tick at a time sums to just under 1.60, so the check
	# state_t >= 1.60 (fighter.gd:150) first passes on the 97th tick.
	ok(z.size() == 1 and back.size() >= 1 and back[0] - z[0] == 97, "P9 EMPTY lasts 97 ticks: 1.60 s plus one tick of float accumulation (got %s)" % [str(back[0] - z[0]) if z.size() and back.size() else "none"])
	await done(main)

	print("\n%d checks, %d failed" % [checks, failures])
	quit(failures)
