extends SceneTree
## Effect A state test (CHANGE-BRIEF A.4: A-R1 … A-R5, A-R7, F2).
##   ./scripts/run-test.sh test_impact_effect_state.gd 60
##
## Drives the real game: main.tscn, the real physics loop, and Bolt through the
## real Input path (Input.action_press/release, parsed pause events), as
## test_slice.gd does. Rivet is driven through his `intent`, the path his game
## brain uses, by a stand-in brain (SETUP, like test_slice's FrozenBrain).
## Setup lines may place fighters or reset hp/wind (marked SETUP). The test never
## calls _on_impact or _spawn_impact: bursts are counted as they enter Main's
## tree, and every expected position is recomputed here from the event itself.
##
## Proves: when bursts are created, which scene, where, how many, that they
## overlap, that they free themselves (also while paused). Cannot prove anything
## about how they look or their draw order on screen: a headless run draws nothing.
## Exit code = number of failed checks.

const FULL := "res://effects/impact_effect.tscn"
const BLOCKED := "res://effects/impact_effect_blocked.tscn"
const LIFETIME_FRAMES := 15      # 0.25 s at 60 physics ticks per second (A.3)
const FREE_MARGIN := 30          # frames allowed past the lifetime for `finished` + queue_free

var main
var failures := 0
var checks := 0
var bursts: Array = []           # every burst that entered Main, in order: {node, id, pos, scene, frame}
var corks: Array = []            # [cork, p_at_struck, blocked, frame] per struck
var frame := 0

func _initialize() -> void:
	physics_frame.connect(func(): frame += 1)
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

func live() -> Array:
	return bursts.filter(func(b): return is_instance_valid(b.node) and b.node.is_inside_tree())

## Waits until no burst is alive, at most `cap` frames; returns the frames waited.
func wait_all_freed(cap: int) -> int:
	var n := 0
	while live().size() > 0 and n < cap:
		await frames(1)
		n += 1
	return n

class StandInBrain:
	var me: Fighter
	var block := false
	var pop_in := -1               # frames until one pop press; -1 = never
	func think(_dt):
		var i := {"move": 0, "jab": false, "cutlass": false, "pop": false, "block": block, "rewind": false}
		if pop_in == 0:
			i.pop = true
		if pop_in >= 0:
			pop_in -= 1
		me.intent = i

func _on_child(n: Node) -> void:
	if n.scene_file_path == FULL or n.scene_file_path == BLOCKED:
		# main sets position before add_child, so this is the burst's spawn point
		bursts.append({"node": n, "id": n.get_instance_id(), "pos": (n as Node2D).position, "scene": n.scene_file_path, "frame": frame})
	elif n.get_script() == preload("res://fighter/cork.gd"):
		n.struck.connect(func(c, blocked): corks.append([c, c.position, blocked, frame]))

func fresh() -> StandInBrain:
	if main:
		main.queue_free()
		await frames(2)
	bursts.clear()
	corks.clear()
	main = load("res://game/main.tscn").instantiate()
	main.child_entered_tree.connect(_on_child)
	root.add_child(main)
	await frames(2)
	var brain := StandInBrain.new()      # SETUP: Rivet idles unless a test arms him
	brain.me = main.rivet
	main.brain = brain
	main._set_round(main.R.INTRO)
	await frames(int(main.INTRO_TIME * 60) + 3)
	return brain

func run() -> void:
	await test_none_on_load()
	await test_one_per_jab_hit()
	await test_none_otherwise()
	await test_cork_hit()
	await test_two_inside_one_lifetime()
	await test_blocked_hit()
	await test_pause()
	print("\n%d checks, %d failed" % [checks, failures])
	quit(failures)

# ---------------------------------------------------------------------------
func test_none_on_load() -> void:
	print("== A-R1: scene load")
	await fresh()
	ok(main.round_state == main.R.FIGHT, "round reached FIGHT")
	ok(bursts.size() == 0, "A-R1 no burst from loading main.tscn and starting the round (got %d)" % bursts.size())

func test_one_per_jab_hit() -> void:
	print("== A-R1, A-R2, A-R5: one unblocked burst per jab hit, at the attack box centre")
	await fresh()
	var hits: Array = []                 # [p, blocked]
	main.bolt.hit_landed.connect(func(a, _att, blocked): hits.append([a.attack_box().get_center(), blocked]))
	for i in 6:
		main.bolt.position.x = 300; main.rivet.position.x = 350   # SETUP: in jab range
		main.bolt.wind = 100.0; main.rivet.hp = 100.0
		await tap("jab")
		await frames(30)
	ok(hits.size() == 6, "6 jab presses in range -> 6 hit_landed (got %d)" % hits.size())
	ok(bursts.size() == hits.size(), "A-R1 one burst per hit: %d bursts for %d hits" % [bursts.size(), hits.size()])
	for i in mini(bursts.size(), hits.size()):
		var b: Dictionary = bursts[i]
		ok(b.pos.is_equal_approx(hits[i][0]) and b.scene == FULL and hits[i][1] == false,
			"A-R2/A-R5 burst %d: impact_effect.tscn at the attack box centre %s (got %s, %s)" % [i + 1, hits[i][0], b.pos, b.scene.get_file()])
		ok(is_instance_valid(b.node) == false or b.node.get_parent() == main, "A-R4 burst %d spawned under Main" % (i + 1))
	await wait_all_freed(LIFETIME_FRAMES + FREE_MARGIN)
	ok(live().size() == 0, "F2 all %d bursts freed after their lifetime (live %d)" % [bursts.size(), live().size()])

func test_none_otherwise() -> void:
	print("== A-R1: never otherwise (whiffs, walking, rewinding)")
	await fresh()
	main.bolt.position.x = 150; main.rivet.position.x = 450         # SETUP: far apart
	for i in 3:
		await tap("jab")
		await frames(30)
	await tap("cutlass")
	await frames(45)
	Input.action_press("move_right")
	await frames(20)
	Input.action_release("move_right")
	main.bolt.wind = 40.0                                           # SETUP
	Input.action_press("rewind")
	await frames(60)
	Input.action_release("rewind")
	await frames(10)
	ok(bursts.size() == 0, "A-R1 no burst from whiffed jabs, a whiffed cutlass, walking or rewinding (got %d)" % bursts.size())

func test_cork_hit() -> void:
	print("== A-R2, A-R4: cork hit; the burst outlives the freed cork")
	await fresh()
	main.bolt.position.x = 150; main.rivet.position.x = 450         # SETUP: pop-gun range
	await tap("pop")
	var n := 0
	while corks.is_empty() and n < 120:
		await frames(1)
		n += 1
	ok(corks.size() == 1, "Bolt's cork struck Rivet (struck %d)" % corks.size())
	if corks.size() != 1:
		return
	var cork = corks[0][0]
	var p: Vector2 = corks[0][1]
	ok(bursts.size() == 1, "A-R1 one burst for one cork hit (got %d)" % bursts.size())
	if bursts.size() != 1:
		return
	var b: Node2D = bursts[0].node
	ok(bursts[0].pos.is_equal_approx(p), "A-R2 burst at the cork's position when it struck %s (got %s)" % [p, bursts[0].pos])
	ok(bursts[0].scene == FULL and corks[0][2] == false, "A-R5 unblocked cork -> impact_effect.tscn")
	await frames(2)
	ok(not is_instance_valid(cork), "the cork has freed itself")
	ok(is_instance_valid(b) and b.is_inside_tree() and b.get_parent() == main,
		"A-R4 the burst is still in the tree under Main after the cork is gone")
	var waited := await wait_all_freed(LIFETIME_FRAMES + FREE_MARGIN)
	ok(live().size() == 0, "F2 burst freed itself %d frames later" % (waited + 2))

func test_two_inside_one_lifetime() -> void:
	print("== A-R3: two impacts inside one lifetime overlap")
	var brain := await fresh()
	main.bolt.position.x = 150; main.rivet.position.x = 450         # SETUP: facing each other at range
	brain.pop_in = 6                                                # SETUP: Rivet pops 6 frames after Bolt
	await tap("pop")
	var most := 0
	var both_seen := false
	var n := 0
	while n < 150 and (corks.size() < 2 or live().size() > 0):
		await frames(1)
		n += 1
		var l := live()
		most = maxi(most, l.size())
		if l.size() == 2:
			both_seen = true
	ok(corks.size() == 2, "both corks struck (got %d)" % corks.size())
	ok(bursts.size() == 2, "two impacts -> two bursts (got %d)" % bursts.size())
	if corks.size() == 2:
		var gap: int = corks[1][3] - corks[0][3]
		ok(gap > 0 and gap < LIFETIME_FRAMES, "the second impact came %d frames after the first, inside the %d-frame lifetime" % [gap, LIFETIME_FRAMES])
	ok(both_seen and most == 2, "A-R3 overlap: both bursts alive in the tree at once (most alive %d)" % most)
	if bursts.size() == 2:
		# instance ids recorded at spawn: both nodes are freed by now, and freed objects cannot be compared
		ok(bursts[0].id != bursts[1].id, "A-R3 two distinct instances, not one restarted (ids %d, %d)" % [bursts[0].id, bursts[1].id])
		for i in 2:
			ok(bursts[i].pos.is_equal_approx(corks[i][1]) if corks.size() == 2 else false,
				"A-R2 burst %d at its own cork's position %s (got %s)" % [i + 1, corks[i][1] if corks.size() == 2 else "-", bursts[i].pos])
	ok(live().size() == 0, "F2 both freed afterwards (live %d)" % live().size())

func test_blocked_hit() -> void:
	print("== A-R5: blocked hit -> blocked scene")
	var brain := await fresh()
	main.bolt.position.x = 300; main.rivet.position.x = 350         # SETUP: in jab range, Rivet faces Bolt
	brain.block = true                                              # SETUP: Rivet holds block
	await frames(5)
	ok(main.rivet.state == Fighter.S.BLOCK, "Rivet is blocking")
	var hits: Array = []
	main.bolt.hit_landed.connect(func(a, _att, blocked): hits.append([a.attack_box().get_center(), blocked]))
	await tap("jab")
	await frames(8)
	ok(hits.size() == 1 and hits[0][1] == true, "the jab landed blocked (%s)" % [hits])
	ok(bursts.size() == 1, "one burst for the blocked hit (got %d)" % bursts.size())
	if bursts.size() == 1 and hits.size() == 1:
		ok(bursts[0].scene == BLOCKED, "A-R5 blocked hit -> impact_effect_blocked.tscn (got %s)" % bursts[0].scene.get_file())
		ok(bursts[0].pos.is_equal_approx(hits[0][0]), "A-R2 blocked burst at the attack box centre %s (got %s)" % [hits[0][0], bursts[0].pos])
	await wait_all_freed(LIFETIME_FRAMES + FREE_MARGIN)
	ok(live().size() == 0, "F2 blocked burst freed")

func test_pause() -> void:
	print("== A-R7: pause on the frame after the impact; the burst still finishes")
	await fresh()
	main.bolt.position.x = 300; main.rivet.position.x = 350         # SETUP
	Input.action_press("jab")
	var n := 0
	while bursts.is_empty() and n < 20:
		await frames(1)
		n += 1
	Input.action_release("jab")
	ok(bursts.size() == 1, "jab hit -> one burst")
	if bursts.size() != 1:
		return
	var b: Node2D = bursts[0].node
	await press_event("pause")
	ok(main.paused, "main.paused is set (real pause event)")
	ok(is_instance_valid(b) and b.can_process(), "A-R7 burst still processes while paused (PROCESS_MODE_ALWAYS inherited)")
	var waited := await wait_all_freed(LIFETIME_FRAMES + FREE_MARGIN)
	ok(main.paused and live().size() == 0, "A-R7 burst finished and freed itself while still paused (%d frames)" % waited)
	await press_event("pause")
	ok(not main.paused, "unpaused")
