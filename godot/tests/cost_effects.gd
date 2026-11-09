extends SceneTree
## A6 Step 7: the headless CPU price of both effects (CHANGE-BRIEF F).
##   ./scripts/run-test.sh cost_effects.gd 60 300
##
## Written for this project from the handout's description: Example 09's cost
## script from the chapter was not available on this machine.
##
## Four cases, each in a fresh scene, WARMUP frames discarded, then FRAMES
## measured at the fixed rate:
##   empty      a bare Node2D: the CONTROL, i.e. what the instrument reads by itself
##   game_off   main.tscn in FIGHT, Rivet frozen, nobody moving, both effects
##              absent: no impact bursts and the two steam emitters freed
##   a_peak     game_off + Effect A held at the brief's peak, 4 bursts alive
##              (A-R3): 4 fresh bursts at the hit point every lifetime (15 ticks)
##   b_heavy    game_off but with both steam emitters kept at amount_ratio 1.0
##              (both fighters at wind 0, B's heaviest state)
## The cases set state directly (they are a benchmark, not a state test). They
## never change an effect, a scene file or gameplay code.
##
## Two clocks per frame:
##   wall   microseconds between consecutive frames (everything the engine did)
##   proc   Performance TIME_PROCESS, the engine's own process-step time
##   phys   Performance TIME_PHYSICS_PROCESS (the game's logic runs in physics)
## A headless run uses a dummy renderer: GPU particles are not simulated or
## drawn, so a GPU effect's number here is only its CPU-side share (node and
## scene work). Its real price is GPU time, measured in the editor's Visual
## Profiler (Use It). Exit code: 0 (a benchmark has no pass/fail), except a
## case that could not be set up.

const WARMUP := 60
const FRAMES := 600
const BURST_EVERY := 15            # 0.25 s lifetime at 60 ticks (A.3)
const PEAK_BURSTS := 4             # A-R3
const HIT := Vector2(339, 227)     # a jab's attack-box centre (state test)

var problems := 0

func _initialize() -> void:
	call_deferred("run")

func stats(xs: Array) -> Dictionary:
	var n := xs.size()
	var mean := 0.0
	for x in xs:
		mean += x
	mean /= n
	var v := 0.0
	for x in xs:
		v += (x - mean) * (x - mean)
	var sd := sqrt(v / maxi(1, n - 1))
	var sorted := xs.duplicate()
	sorted.sort()
	return {"mean": mean, "sd": sd, "median": sorted[n / 2], "p95": sorted[int(n * 0.95)]}

## Measures FRAMES frames; `each` runs at the start of every measured frame.
func measure(name: String, each: Callable) -> Dictionary:
	for i in WARMUP:
		each.call(i)
		await process_frame
	var wall := []
	var proc := []
	var phys := []
	var t0 := Time.get_ticks_usec()
	for i in FRAMES:
		each.call(WARMUP + i)
		await process_frame
		var t1 := Time.get_ticks_usec()
		wall.append((t1 - t0) / 1000.0)
		proc.append(Performance.get_monitor(Performance.TIME_PROCESS) * 1000.0)
		phys.append(Performance.get_monitor(Performance.TIME_PHYSICS_PROCESS) * 1000.0)
		t0 = t1
	var w := stats(wall)
	var p := stats(proc)
	var q := stats(phys)
	print("%-9s wall %.4f ms ± %.4f (median %.4f, p95 %.4f)   proc %.4f ± %.4f   phys %.4f ± %.4f" % [
		name, w.mean, w.sd, w.median, w.p95, p.mean, p.sd, q.mean, q.sd])
	return {"name": name, "wall": w, "proc": p, "phys": q}

class FrozenBrain:
	func think(_dt): pass

func game(keep_steam: bool) -> Node:
	var main = load("res://game/main.tscn").instantiate()
	root.add_child(main)
	for i in 3:
		await process_frame
	main.brain = FrozenBrain.new()
	main._set_round(main.R.INTRO)
	for i in int(main.INTRO_TIME * 60) + 3:
		await physics_frame
	if main.round_state != main.R.FIGHT:
		print("SETUP PROBLEM: round did not reach FIGHT")
		problems += 1
	for f in [main.bolt, main.rivet]:
		for m in f.get_children():
			if m is SteamMount:
				for s in m.get_children():
					if keep_steam:
						(s as GPUParticles2D).amount_ratio = 1.0
					else:
						s.queue_free()
	await process_frame
	return main

func steam_nodes(main) -> Array:
	var out := []
	for f in [main.bolt, main.rivet]:
		for m in f.get_children():
			if m is SteamMount:
				out.append_array(m.get_children())
	return out

func bursts(main) -> Array:
	return main.get_children().filter(func(n): return n.scene_file_path == "res://effects/impact_effect.tscn")

func run() -> void:
	print("cost_effects: WARMUP %d, FRAMES %d, fixed rate from the wrapper; headless (dummy renderer)" % [WARMUP, FRAMES])
	var results := []

	var empty := Node2D.new()
	root.add_child(empty)
	await process_frame
	results.append(await measure("empty", func(_i): pass))
	empty.queue_free()
	await process_frame

	var main = await game(false)
	print("          game_off: steam emitters left %d, bursts %d" % [steam_nodes(main).size(), bursts(main).size()])
	results.append(await measure("game_off", func(_i): pass))

	var alive := []
	results.append(await measure("a_peak", func(i):
		if i % BURST_EVERY == 0:
			for k in PEAK_BURSTS:
				main._spawn_impact(HIT + Vector2(k * 6, 0), false)
		alive.append(bursts(main).size())))
	var most := 0
	var total := 0
	for a in alive:
		most = maxi(most, a)
		total += a
	print("          a_peak: bursts alive per frame, mean %.2f, most %d (brief peak %d)" % [float(total) / alive.size(), most, PEAK_BURSTS])
	if most < PEAK_BURSTS:
		print("SETUP PROBLEM: never reached %d bursts" % PEAK_BURSTS)
		problems += 1
	main.queue_free()
	await process_frame

	main = await game(true)
	var st := steam_nodes(main)
	print("          b_heavy: steam emitters %d, amount_ratio %s, emitting %s" % [st.size(), st.map(func(s): return s.amount_ratio), st.map(func(s): return s.emitting)])
	if st.size() != 2:
		print("SETUP PROBLEM: expected 2 steam emitters")
		problems += 1
	results.append(await measure("b_heavy", func(_i): pass))
	main.queue_free()
	await process_frame

	print("\n-- reading against the control")
	var by := {}
	for r in results:
		by[r.name] = r
	for pair in [["game_off", "empty"], ["a_peak", "game_off"], ["b_heavy", "game_off"]]:
		var a: Dictionary = by[pair[0]]
		var b: Dictionary = by[pair[1]]
		for clock in ["wall", "proc", "phys"]:
			var d: float = a[clock].mean - b[clock].mean
			var spread: float = maxf(a[clock].sd, b[clock].sd)
			var verdict := "differs by more than the spread" if absf(d) > spread else "WITHIN the spread: these two cases read the same"
			print("%-8s - %-8s %s: %+.4f ms (larger spread %.4f): %s" % [pair[0], pair[1], clock, d, spread, verdict])
	print("\ncost_effects done, %d setup problems" % problems)
	quit(problems)
