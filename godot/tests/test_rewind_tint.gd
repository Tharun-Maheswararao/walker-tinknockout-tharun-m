extends SceneTree
## Automated checks for the A5 REWIND tint (CHANGE-BRIEF A5.2, rules R1-R6).
##   scripts/run-test.sh test_rewind_tint.gd <30|60|144>
##
## State is driven through the REAL game loop and input path: rewind is held
## with Input.action_press, pause is a parsed input event, Rivet acts only
## through a brain's think() (the hook rivet_brain.gd uses). The driver's update
## is never called. A Sampler node with process_priority 1000 reads each
## material's `rewind_amount` after every other _process() in the frame.
##
## Headless limits (CLAUDE.md, evidence/a5/headless-facts.txt): nothing is drawn
## and a parameter readback only proves what the driver set, not what the GPU
## shows. Shader defaults are read from the .gdshader text.
## Exit code = number of failed checks.

const SHADER_PATH := "res://shaders/rewind_tint.gdshader"
const FADE_IN := 0.15
const FADE_OUT := 0.30
const EPS := 1e-4

var main
var sampler: Sampler
var failures := 0
var checks := 0
var period := 1.0 / 60.0   # one frame at --fixed-fps, read from the command line

func _initialize() -> void:
	call_deferred("run")

func ok(cond: bool, what: String) -> void:
	checks += 1
	if not cond:
		failures += 1
	print(("PASS  " if cond else "FAIL  ") + what)

## Reads both materials after every other _process() (priority 1000), and keeps
## sampling while the tree is paused.
class Sampler extends Node:
	var game
	var t := 0.0
	var samples: Array = []
	func _ready() -> void:
		process_priority = 1000
		process_mode = Node.PROCESS_MODE_ALWAYS
	func _process(delta: float) -> void:
		t += delta
		if game == null or not is_instance_valid(game) or not game.is_inside_tree():
			return
		samples.append({"t": t, "dt": delta,
			"b": game.bolt.sprite.material.get_shader_parameter("rewind_amount"),
			"r": game.rivet.sprite.material.get_shader_parameter("rewind_amount"),
			"bs": game.bolt.state, "rs": game.rivet.state, "gp": game.paused})

class FrozenBrain:
	func think(_dt): pass

## Rivet acts only through intent, like rivet_brain.gd: one jab tick, or held rewind.
class ScriptedBrain:
	var me: Fighter
	var jabs := 0
	var rewind := false
	func think(_dt):
		me.intent = {"move": 0, "jab": jabs > 0, "cutlass": false, "pop": false, "block": false, "rewind": rewind}
		jabs = maxi(0, jabs - 1)

func physics_frames(n: int) -> void:
	for i in n:
		await physics_frame

func frames(n: int) -> void:
	for i in n:
		await process_frame

## Waits (process frames) until cond(last sample) holds. Returns false on timeout.
func until(cond: Callable, max_frames := 2000) -> bool:
	for i in max_frames:
		await process_frame
		if sampler.samples.size() > 0 and cond.call(sampler.samples[-1]):
			return true
	return false

func press_event(action: String) -> void:
	for pressed in [true, false]:
		var ev := InputEventAction.new()
		ev.action = action
		ev.pressed = pressed
		Input.parse_input_event(ev)
		await physics_frames(1)

func fresh(brain = null) -> void:
	Input.action_release("rewind")
	if main:
		main.queue_free()
		await physics_frames(2)
	main = load("res://game/main.tscn").instantiate()
	root.add_child(main)
	await physics_frames(2)
	if brain == null:
		brain = FrozenBrain.new()
	if brain is ScriptedBrain:
		brain.me = main.rivet
	main.brain = brain                  # SETUP: replace Rivet's brain BEFORE the fight starts
	main._set_round(main.R.INTRO)
	await physics_frames(int(main.INTRO_TIME * 60) + 3)
	sampler.game = main
	await frames(2)

## Index of the first sample at or after `from` matching cond, or -1.
func find(from: int, cond: Callable) -> int:
	for i in range(from, sampler.samples.size()):
		if cond.call(sampler.samples[i]):
			return i
	return -1

func max_dt(a: int, b: int) -> float:
	var m := 0.0
	for i in range(a, b + 1):
		m = maxf(m, sampler.samples[i].dt)
	return m

## R1: across [a, b] Bolt's value only rises on REWIND frames and only falls off them.
func direction_follows_state(a: int, b: int, key := "b", state_key := "bs") -> bool:
	for i in range(maxi(a, 1), b + 1):
		var s: Dictionary = sampler.samples[i]
		var prev: float = sampler.samples[i - 1][key]
		if s[key] > prev and s[state_key] != Fighter.S.REWIND:
			return false
		if s[key] < prev and s[state_key] == Fighter.S.REWIND:
			return false
	return true

func all_equal(a: int, b: int, key: String, value: float) -> bool:
	for i in range(a, b + 1):
		if sampler.samples[i][key] != value:
			return false
	return true

func run() -> void:
	var args := OS.get_cmdline_args()
	var k := args.find("--fixed-fps")
	if k >= 0 and k + 1 < args.size():
		period = 1.0 / float(args[k + 1])
	print("frame period %.6f s (%d fps)" % [period, roundi(1.0 / period)])
	sampler = Sampler.new()
	root.add_child(sampler)
	await test_shader_contract()
	await test_materials_and_rest()
	await test_fade_in_and_out()
	await test_retrigger_extends()
	await test_release_mid_fade_in()
	await test_hit_mid_fade_in()
	await test_time_scale()
	await test_tree_pause()
	await test_game_pause()
	await test_rivet_alone()
	Input.action_release("rewind")
	print("\n%d checks, %d failed" % [checks, failures])
	quit(failures)

# ---------------------------------------------------------------------------
## A5.2 uniform table: names and types from the engine, defaults and hints from the text.
func test_shader_contract() -> void:
	var shader: Shader = load(SHADER_PATH)
	var list := shader.get_shader_uniform_list()
	var by_name := {}
	for u in list:
		by_name[u.name] = u
	print("      uniforms: ", list.map(func(u): return "%s type=%d" % [u.name, u.type]))
	ok(list.size() == 3, "shader parsed: exactly 3 uniforms listed (got %d)" % list.size())
	ok(by_name.has("rewind_amount") and by_name.rewind_amount.type == TYPE_FLOAT, "rewind_amount is a float (type 3)")
	ok(by_name.has("tint_color") and by_name.tint_color.type == TYPE_COLOR, "tint_color is vec4 : source_color (type 20)")
	ok(by_name.has("tint_strength") and by_name.tint_strength.type == TYPE_FLOAT, "tint_strength is a float (type 3)")

	var src := FileAccess.get_file_as_string(SHADER_PATH)
	var re := RegEx.new()
	re.compile("uniform\\s+float\\s+rewind_amount\\s*:\\s*hint_range\\(\\s*([-\\d.]+)\\s*,\\s*([-\\d.]+)\\s*\\)\\s*=\\s*([-\\d.]+)\\s*;")
	var m := re.search(src)
	ok(m != null and float(m.get_string(1)) == 0.0 and float(m.get_string(2)) == 1.0 and float(m.get_string(3)) == 0.0,
		"source: rewind_amount hint_range(0.0, 1.0) = 0.0")
	re.compile("uniform\\s+float\\s+tint_strength\\s*:\\s*hint_range\\(\\s*([-\\d.]+)\\s*,\\s*([-\\d.]+)\\s*\\)\\s*=\\s*([-\\d.]+)\\s*;")
	m = re.search(src)
	ok(m != null and float(m.get_string(1)) == 0.0 and float(m.get_string(2)) == 1.0 and float(m.get_string(3)) == 0.5,
		"source: tint_strength hint_range(0.0, 1.0) = 0.5")
	re.compile("uniform\\s+vec4\\s+tint_color\\s*:\\s*source_color\\s*=\\s*vec4\\(([^)]*)\\)\\s*;")
	m = re.search(src)
	var c := PackedFloat64Array()
	if m:
		for part in m.get_string(1).split(","):
			c.append(float(part.strip_edges()))
	ok(c == PackedFloat64Array([0.353, 0.627, 1.0, 1.0]), "source: tint_color = vec4(0.353, 0.627, 1.0, 1.0) (got %s)" % [c])

## R6 wiring and R1 at rest; only the two body sprites carry a material.
func test_materials_and_rest() -> void:
	await fresh()
	var bm = main.bolt.sprite.material
	var rm = main.rivet.sprite.material
	ok(bm is ShaderMaterial and bm.shader.resource_path == SHADER_PATH, "R6 Bolt's body sprite has a ShaderMaterial with rewind_tint.gdshader")
	ok(rm is ShaderMaterial and rm.shader.resource_path == SHADER_PATH, "R6 Rivet's body sprite has a ShaderMaterial with rewind_tint.gdshader")
	ok(bm != rm, "R6 Bolt and Rivet have different material objects")
	ok(bm.shader == rm.shader, "R6 ... using the same shader resource")
	var others_clean := true
	for f in [main.bolt, main.rivet]:
		if f.key_sprite.material != null or f.weapon.material != null:
			others_clean = false
	ok(others_clean and main.bg.material == null, "scope: key, weapon and background sprites have no material")
	ok(bm.get_shader_parameter("tint_color") == null and bm.get_shader_parameter("tint_strength") == null,
		"tint_color / tint_strength not set from code (shader defaults apply)")
	await frames(10)
	var s: Dictionary = sampler.samples[-1]
	ok(s.b == 0.0 and s.r == 0.0, "R1 at rest outside REWIND: both values exactly 0.0 (Bolt %s, Rivet %s)" % [s.b, s.r])

## R1 + R2: hold rewind, fade in 0.15 s; release, fade out 0.30 s.
func test_fade_in_and_out() -> void:
	await fresh()
	var a := sampler.samples.size()
	Input.action_press("rewind")
	ok(await until(func(s): return s.b == 1.0), "R1 holding rewind: Bolt's value reaches 1.0")
	var b := sampler.samples.size() - 1
	var first := find(a, func(s): return s.b > 0.0)
	var t_press: float = sampler.samples[a - 1].t
	var delay: float = sampler.samples[first].t - t_press
	print("      fade START delay (reported, not asserted): %.4f s = %d frame(s) from the press to the first non-zero frame" % [delay, first - a + 1])
	var dur: float = sampler.samples[b].t - sampler.samples[first - 1].t
	var tol := max_dt(first, b) + EPS
	ok(absf(dur - FADE_IN) <= tol, "R2 fade-in 0 -> 1 takes %.4f s game time (want 0.15 +/- %.4f)" % [dur, tol])
	ok(direction_follows_state(a, b), "R1 value only rises while state == REWIND, never drops during the fade-in")
	await frames(roundi(0.2 / period))
	var held := sampler.samples.size() - 1
	ok(all_equal(b, held, "b", 1.0), "R1 value stays exactly 1.0 while REWIND is held")

	var c := sampler.samples.size()
	Input.action_release("rewind")
	ok(await until(func(s): return s.b == 0.0), "R1 released: Bolt's value returns to 0.0")
	var d := sampler.samples.size() - 1
	var move := find(c, func(s): return s.b < 1.0)
	dur = sampler.samples[d].t - sampler.samples[move - 1].t
	tol = max_dt(move, d) + EPS
	ok(absf(dur - FADE_OUT) <= tol, "R2 fade-out 1 -> 0 takes %.4f s game time (want 0.30 +/- %.4f)" % [dur, tol])
	ok(direction_follows_state(c, d), "R1 value only falls once state != REWIND, never rises during the fade-out")
	await frames(10)
	ok(sampler.samples[-1].b == 0.0, "R1 value is exactly 0.0 at rest after the fade-out")
	ok(all_equal(a, sampler.samples.size() - 1, "r", 0.0), "R6 Rivet's value stayed 0.0 throughout Bolt's rewind")

## R3: re-press mid fade-out: extend from the current value, never drop.
func test_retrigger_extends() -> void:
	await fresh()
	Input.action_press("rewind")
	await until(func(s): return s.b == 1.0)
	Input.action_release("rewind")
	await until(func(s): return s.b <= 0.5)
	var a := sampler.samples.size()
	Input.action_press("rewind")
	ok(await until(func(s): return s.b == 1.0), "R3 re-pressed mid fade-out: value reaches 1.0")
	var b := sampler.samples.size() - 1
	var e := find(a, func(s): return s.bs == Fighter.S.REWIND)
	var v: float = sampler.samples[e - 1].b
	var no_drop := true
	for i in range(e, b + 1):
		if sampler.samples[i].b < sampler.samples[i - 1].b:
			no_drop = false
	ok(v > 0.0 and v < 1.0, "R3 re-entry happened mid fade-out (value %.4f when REWIND began again)" % v)
	ok(no_drop, "R3 no frame-to-frame drop from the first REWIND frame on (no restart from 0)")
	var dur: float = sampler.samples[b].t - sampler.samples[e - 1].t
	var want := (1.0 - v) * FADE_IN
	var tol := max_dt(e, b) + EPS
	ok(absf(dur - want) <= tol, "R3 reaches 1.0 after %.4f s (want (1 - %.4f) x 0.15 = %.4f +/- %.4f)" % [dur, v, want, tol])
	Input.action_release("rewind")
	await until(func(s): return s.b == 0.0)

## Shared R5 checks: REWIND ended at sample e; value falls from where it was.
func check_fade_from(a: int, label: String) -> void:
	ok(await until(func(s): return s.b == 0.0), "R5 %s: value returns to 0.0" % label)
	var b := sampler.samples.size() - 1
	var e := find(a, func(s): return s.bs != Fighter.S.REWIND)
	var v: float = sampler.samples[e - 1].b
	var never_above := true
	var never_rises := true
	for i in range(e, b + 1):
		never_above = never_above and sampler.samples[i].b <= v
		never_rises = never_rises and sampler.samples[i].b <= sampler.samples[i - 1].b
	var first_step: float = v - sampler.samples[e].b
	ok(v > 0.0 and v < 1.0, "R5 %s: REWIND ended mid fade-in (value %.4f)" % [label, v])
	ok(never_above and never_rises, "R5 %s: value never rises above %.4f after REWIND ends" % [label, v])
	ok(first_step <= sampler.samples[e].dt / FADE_OUT + EPS, "R5 %s: no snap, first step down %.4f <= dt/0.30" % [label, first_step])
	var dur: float = sampler.samples[b].t - sampler.samples[e - 1].t
	var want := v * FADE_OUT
	var tol := max_dt(e, b) + EPS
	ok(absf(dur - want) <= tol, "R5 %s: fades out in %.4f s (want %.4f x 0.30 = %.4f +/- %.4f)" % [label, dur, v, want, tol])

## R5: key released during the fade-in.
func test_release_mid_fade_in() -> void:
	await fresh()
	Input.action_press("rewind")
	await until(func(s): return s.b >= 0.5)
	var a := sampler.samples.size()
	Input.action_release("rewind")
	await check_fade_from(a, "release")

## R5: a hit during the fade-in (fighter.gd:232, REWIND -> HURT).
func test_hit_mid_fade_in() -> void:
	var brain := ScriptedBrain.new()
	await fresh(brain)
	main.bolt.position.x = 300; main.rivet.position.x = 350   # SETUP: Rivet's jab reaches Bolt
	Input.action_press("rewind")
	await until(func(s): return s.bs == Fighter.S.REWIND)
	var a := sampler.samples.size()
	brain.jabs = 1                                              # Rivet presses jab for one tick
	await until(func(s): return s.bs != Fighter.S.REWIND, 120)
	Input.action_release("rewind")                              # so HURT returns to IDLE, not REWIND
	var e := find(a, func(s): return s.bs != Fighter.S.REWIND)
	ok(e >= 0 and sampler.samples[e].bs == Fighter.S.HURT, "R5 hit: Rivet's jab moved Bolt from REWIND to HURT (state %d)" % (sampler.samples[e].bs if e >= 0 else -1))
	await check_fade_from(a, "hit")

## R4a: Engine.time_scale 0.5 -> 0.15 s of game time, 0.30 s of real frames.
func test_time_scale() -> void:
	await fresh()
	Engine.time_scale = 0.5
	var a := sampler.samples.size()
	Input.action_press("rewind")
	var reached: bool = await until(func(s): return s.b == 1.0)
	var b := sampler.samples.size() - 1
	var first := find(a, func(s): return s.b > 0.0)
	var dur: float = sampler.samples[b].t - sampler.samples[first - 1].t
	var n := b - first + 1
	var real := n * period
	var tol := max_dt(first, b) + EPS
	ok(reached and absf(dur - FADE_IN) <= tol, "R4a time_scale 0.5: fade-in %.4f s game time (want 0.15 +/- %.4f)" % [dur, tol])
	ok(absf(real - FADE_IN / 0.5) <= period + EPS, "R4a time_scale 0.5: %d frames = %.4f s real time (want 0.30 +/- %.4f)" % [n, real, period])
	Input.action_release("rewind")
	await until(func(s): return s.b == 0.0)
	Engine.time_scale = 1.0

## R4b: tree paused mid fade-in (the game never does this): value holds.
func test_tree_pause() -> void:
	await fresh()
	Input.action_press("rewind")
	await until(func(s): return s.b >= 0.3)
	paused = true                                               # SETUP: SceneTree.paused
	await frames(1)
	var a := sampler.samples.size() - 1
	var v: float = sampler.samples[a].b
	await frames(10)
	var b := sampler.samples.size() - 1
	ok(v < 1.0 and all_equal(a, b, "b", v), "R4b tree paused: value held at %.4f for %d frames" % [v, b - a])
	paused = false
	await frames(1)
	var step: float = sampler.samples[-1].b - v
	ok(step > 0.0 and step <= sampler.samples[-1].dt / FADE_IN + EPS, "R4b unpaused: resumes from %.4f (first step +%.4f)" % [v, step])
	Input.action_release("rewind")
	await until(func(s): return s.b == 0.0)

## R4c: the game's own pause (P, real input event) mid fade-in: value holds.
func test_game_pause() -> void:
	await fresh()
	var start := sampler.samples.size()
	Input.action_press("rewind")
	await until(func(s): return s.b >= 0.3)
	await press_event("pause")
	ok(main.paused, "R4c pause event set main.paused")
	await frames(10)
	var a := find(start, func(s): return s.gp)
	var v: float = sampler.samples[a].b
	var b := sampler.samples.size() - 1
	ok(v < 1.0 and all_equal(a, b, "b", v), "R4c main.paused: value held at %.4f for %d frames" % [v, b - a])
	await press_event("pause")
	ok(not main.paused, "R4c second pause event cleared main.paused")
	var u := find(b, func(s): return not s.gp)
	await until(func(s): return s.b == 1.0)
	var step: float = sampler.samples[u].b - v
	ok(step >= 0.0 and step <= sampler.samples[u].dt / FADE_IN + EPS, "R4c unpaused: resumes from %.4f (first step +%.4f)" % [v, step])
	Input.action_release("rewind")
	await until(func(s): return s.b == 0.0)

## R6 the other way round: Rivet rewinds, Bolt's value stays 0.0.
func test_rivet_alone() -> void:
	var brain := ScriptedBrain.new()
	await fresh(brain)
	var a := sampler.samples.size()
	brain.rewind = true
	ok(await until(func(s): return s.r == 1.0), "R6 Rivet rewinding: Rivet's value reaches 1.0")
	ok(direction_follows_state(a, sampler.samples.size() - 1, "r", "rs"), "R1 Rivet's value only rises while Rivet is in REWIND")
	brain.rewind = false
	ok(await until(func(s): return s.r == 0.0), "R6 Rivet released: Rivet's value returns to 0.0")
	ok(all_equal(a, sampler.samples.size() - 1, "b", 0.0), "R6 Bolt's value stayed 0.0 throughout Rivet's rewind")
