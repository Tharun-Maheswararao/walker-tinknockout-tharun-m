extends SceneTree
## A7 Step 5: structure and state test for the two clips and their one authority
## (CHANGE-BRIEF.md §1, §5-7; rules A-R1..A-R4, B-R1..B-R3). Written by Claude.
##   ./scripts/run-test.sh test_a7_structure.gd 60      (also 30)
##
## Part A reads the STRUCTURE of the real fighters in main.tscn against the
## brief and the clip resources: the named rig and its parentage, both players
## MANUAL with root_node at the fighter, every clip name the code requests
## present in its player, track_problems() empty on the real nodes (this closes
## the fixture limit of the two read-backs), the key's sheet and slicing, no
## AnimationTree or AnimatedSprite2D, and the one-authority rule in the source.
## Part B drives the STATE MACHINE through the real game loop with real key
## events (Input.parse_input_event; Rivet through a stand-in brain) and reads
## the current clip with current_animation, as the AnimationPlayer route uses:
## the clip each state plays, clip position = state_t, the pose equal to the
## clip's own value at state_t (so no second writer touched it), the freezes,
## the rest snap on a hit, the key cycle and its full-wind hold, and facing.
## Every check is anchored on the tick an action actually started, so it holds
## at 60 and 30 fps (see test_a7_pins.gd for why).
## It cannot show whether the motion reads, the seam over five wraps by eye,
## registration, the backgrounds, or that the key draws behind the body: those
## are frame strips and play (CHANGE-BRIEF.md §8).
## Exit code = number of failed checks.

const JAB_PATHS := ["FacingPivot/BodyPivot:position:x", "FacingPivot/BodyPivot:rotation", "FacingPivot/BodyPivot/KeyMount/KeyBob:position:y"]
const KEY_PATH := "FacingPivot/BodyPivot/KeyMount/KeyBob/key_sprite:frame"

var checks := 0
var failures := 0

func ok(cond: bool, msg: String) -> void:
	checks += 1
	if not cond:
		failures += 1
	print(("PASS  " if cond else "FAIL  ") + msg)

## The handout's check: every track resolves to a real node, and to a real
## property, bone or blend shape where the track names one.
static func track_problems(player: AnimationPlayer) -> Array[String]:
	var problems: Array[String] = []
	var root := player.get_node_or_null(player.root_node)
	if root == null:
		problems.append("root_node %s resolves to nothing" % player.root_node)
		return problems
	for clip_name in player.get_animation_list():
		var clip := player.get_animation(clip_name)
		for t in clip.get_track_count():
			var path := clip.track_get_path(t)
			var node := root.get_node_or_null(NodePath(path.get_concatenated_names()))
			if node == null:
				problems.append("%s track %d: no node at %s" % [clip_name, t, path])
				continue
			if path.get_subname_count() == 0:
				continue
			var sub := path.get_subname(0)
			match clip.track_get_type(t):
				Animation.TYPE_POSITION_3D, Animation.TYPE_ROTATION_3D, Animation.TYPE_SCALE_3D:
					var skeleton := node as Skeleton3D
					if skeleton == null or skeleton.find_bone(sub) == -1:
						problems.append("%s track %d: no bone %s on %s" % [clip_name, t, sub, node.name])
				Animation.TYPE_BLEND_SHAPE:
					var mesh := node as MeshInstance3D
					if mesh == null or mesh.find_blend_shape_by_name(sub) == -1:
						problems.append("%s track %d: no blend shape %s on %s" % [clip_name, t, sub, node.name])
				_:
					if not (sub in node):
						problems.append("%s track %d: %s has no property %s" % [clip_name, t, node.name, sub])
	return problems

class Driver extends Node:
	var game
	var tick := 0
	var schedule := {}
	var rows: Array = []
	var transitions: Array = []
	func _ready() -> void:
		process_physics_priority = 1000   # after main
	func snap(f) -> Dictionary:
		var fa: AnimationPlayer = f.fighter_anim
		var ka: AnimationPlayer = f.key_anim
		return {"state": f.state, "t": f.state_t, "wind": f.wind,
			"fa": String(fa.current_animation), "fa_pos": fa.current_animation_position if fa.current_animation != &"" else -1.0,
			"ka": String(ka.current_animation), "ka_pos": ka.current_animation_position if ka.current_animation != &"" else -1.0,
			"x": f.body_pivot.position.x, "rot": f.body_pivot.rotation, "bob": f.key_bob.position.y, "frame": f.key_sprite.frame,
			"face": f.facing_pivot.scale.x, "facing": f.facing, "sx": f.sprite.scale.x,
			"key_shown": f.key_sprite.is_visible_in_tree(), "gx": f.body_pivot.global_position.x - f.global_position.x}
	func _physics_process(_dt: float) -> void:
		rows.append({"tick": tick, "b": snap(game.bolt), "r": snap(game.rivet), "paused": game.paused,
			"jab": game.bolt.intent.jab, "frame": Engine.get_process_frames()})
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

func first_entry(d: Driver, s: int, a: int) -> int:
	for x in d.transitions:
		if x[2] == s and x[0] >= a:
			return x[0]
	return -1

func near(a: float, b: float, eps := 1e-3) -> bool:
	return absf(a - b) < eps

## The jab clip's own value on each of its tracks at time t.
func jab_at(clip: Animation, t: float) -> Array:
	var out := []
	for p in JAB_PATHS:
		out.append(clip.value_track_interpolate(clip.find_track(NodePath(p), Animation.TYPE_VALUE), t))
	return out

func at_rest(s: Dictionary) -> bool:
	return near(s.x, 0.0) and near(s.rot, 0.0) and near(s.bob, 0.0)

func source_of(path: String, fn: String) -> String:
	var text := FileAccess.get_file_as_string(path)
	var a := text.find("func %s(" % fn)
	if a < 0:
		return ""
	var b := text.find("\nfunc ", a + 1)
	return text.substr(a, (b if b > 0 else text.length()) - a)

func gd_files(dir: String, out: Array) -> void:
	for f in DirAccess.get_files_at(dir):
		if f.ends_with(".gd"):
			out.append(dir.path_join(f))
	for sub in DirAccess.get_directories_at(dir):
		if sub not in ["tests", ".godot", "addons"]:
			gd_files(dir.path_join(sub), out)

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	var S := Fighter.S
	var JAB: Animation = load("res://animations/jab_action.tres")
	var tol := 0.5 / 60.0

	# ===================== A. structure of the real fighters ======================
	print("-- A. structure (real Bolt and Rivet in main.tscn)")
	var main = load("res://game/main.tscn").instantiate()
	root.add_child(main)
	await process_frame
	for f in [main.bolt, main.rivet]:
		var who: String = f.skin
		var want := {"FacingPivot": "Node2D", "FacingPivot/BodyPivot": "Node2D", "FacingPivot/BodyPivot/sprite": "Sprite2D",
			"FacingPivot/BodyPivot/KeyMount": "Node2D", "FacingPivot/BodyPivot/KeyMount/KeyBob": "Node2D",
			"FacingPivot/BodyPivot/KeyMount/KeyBob/key_sprite": "Sprite2D", "weapon": "Sprite2D",
			"FighterAnimPlayer": "AnimationPlayer", "KeyAnimPlayer": "AnimationPlayer"}
		var missing := []
		for p in want:
			var n: Node = f.get_node_or_null(p)
			if n == null or n.get_class() != want[p]:
				missing.append(p)
		ok(missing.is_empty(), "%s: every named node of the brief's rig, with its parentage and class (missing or wrong: %s)" % [who, missing])
		ok(f.body_pivot == f.get_node_or_null("FacingPivot/BodyPivot") and f.key_bob == f.get_node_or_null("FacingPivot/BodyPivot/KeyMount/KeyBob")
			and f.key_sprite == f.get_node_or_null("FacingPivot/BodyPivot/KeyMount/KeyBob/key_sprite") and f.sprite == f.get_node_or_null("FacingPivot/BodyPivot/sprite"),
			"%s: the script's rig variables are those named nodes" % who)
		for pl in [f.fighter_anim, f.key_anim]:
			ok(pl.callback_mode_process == AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL, "%s %s: callback_mode_process MANUAL (got %d)" % [who, pl.name, pl.callback_mode_process])
			ok(pl.get_node_or_null(pl.root_node) == f, "%s %s: root_node %s resolves to the fighter" % [who, pl.name, pl.root_node])
		ok(f.fighter_anim.get_animation_list() == PackedStringArray([Fighter.JAB_CLIP]) and f.fighter_anim.has_animation(Fighter.JAB_CLIP)
			and f.fighter_anim.get_animation(Fighter.JAB_CLIP).resource_path == "res://animations/jab_action.tres",
			"%s: FighterAnimPlayer holds exactly the clip the code requests, %s, from its resource" % [who, Fighter.JAB_CLIP])
		ok(f.key_anim.get_animation_list() == PackedStringArray([Fighter.KEY_CLIP]) and f.key_anim.has_animation(Fighter.KEY_CLIP)
			and f.key_anim.get_animation(Fighter.KEY_CLIP).resource_path == "res://animations/wind_key_cycle.tres",
			"%s: KeyAnimPlayer holds exactly the clip the code requests, %s, from its resource" % [who, Fighter.KEY_CLIP])
		var probs: Array = track_problems(f.fighter_anim) + track_problems(f.key_anim)
		ok(probs.is_empty(), "%s: track_problems finds nothing on the REAL rig %s" % [who, probs])
		ok(f.key_sprite.texture != null and f.key_sprite.texture.resource_path == "res://assets/props/key-%s-sheet.png" % who
			and f.key_sprite.hframes == 8 and f.key_sprite.vframes == 1, "%s: key_sprite shows key-%s-sheet.png sliced 8 x 1" % [who, who])
		ok(f.find_children("*", "AnimationTree", true, false).is_empty() and f.find_children("*", "AnimatedSprite2D", true, false).is_empty(),
			"%s: no AnimationTree and no AnimatedSprite2D (brief §5-6)" % who)
		ok(String(f.fighter_anim.current_animation) == "" and at_rest(d_snap(f)) and f.key_sprite.frame == 0, "%s: at load, no clip playing, rig at rest, key on frame 0" % who)
	await done(main)

	print("\n-- A. one authority, from the source (every assignment to a rig node, by function)")
	var files := []
	gd_files("res://", files)
	var writes := []   # [file, line, function, target]
	var rx := RegEx.create_from_string("\\b(facing_pivot|body_pivot|key_mount|key_bob|key_sprite)\\.([a-z_.]+)\\s*=[^=]")
	for p in files:
		var lines := FileAccess.get_file_as_string(p).split("\n")
		var fn := ""
		for i in lines.size():
			if lines[i].begins_with("func "):
				fn = lines[i].get_slice("(", 0).trim_prefix("func ")
			var m := rx.search(lines[i])
			if m != null:
				writes.append([p.trim_prefix("res://"), i + 1, fn, m.get_string(1) + "." + m.get_string(2)])
	var shown := writes.map(func(w): return "%s:%d %s %s" % w)
	print("rig writes found: %s" % [shown])
	ok(writes.all(func(w): return w[0] == "fighter/fighter.gd"), "no script outside fighter.gd writes a rig node")
	var per_tick := writes.filter(func(w): return w[2] not in ["_ready", "_load_art"])
	ok(per_tick.all(func(w): return w[2] == "_apply_pose" and w[3] in ["facing_pivot.scale", "key_mount.position", "key_mount.visible"]),
		"after setup, the only code writes to the rig are _apply_pose's FacingPivot.scale and KeyMount.position/visible (got %s)" % [per_tick.map(func(w): return "%s %s" % [w[2], w[3]])])
	ok(writes.all(func(w): return not (w[3].begins_with("body_pivot.") or w[3].begins_with("key_bob.")) or w[3].ends_with(".name")),
		"BodyPivot and KeyBob are never written by code (only named at setup): FighterAnimPlayer is their one writer")
	ok(writes.all(func(w): return w[3] != "key_sprite.frame"), "key_sprite.frame is never written by code: KeyAnimPlayer is its one writer")
	var sync_src := source_of("res://fighter/fighter.gd", "_sync_clips")
	ok(sync_src != "" and rx.search(sync_src) == null, "_sync_clips assigns to no rig node; it only moves the two players")

	# ===================== B. the state machine, real input ======================
	print("\n-- B1. jab whiff: jab_action only in JAB, at state_t, pose = the clip's value")
	var r: Array = await fresh(200, 440)
	main = r[0]
	var d: Driver = r[1]
	tap(d, 5, KEY_J)
	await run_to(d, 40)
	var e := first_entry(d, S.JAB, 0)
	var ok_pos := true
	var ok_pose := true
	var worst := 0.0
	for i in range(e, e + 21):
		var b: Dictionary = d.rows[i].b
		ok_pos = ok_pos and b.fa == "jab_action" and absf(b.fa_pos - b.t) < tol
		var want: Array = jab_at(JAB, b.t)
		worst = maxf(worst, maxf(absf(b.x - want[0]), maxf(absf(b.rot - want[1]), absf(b.bob - want[2]))))
		ok_pose = ok_pose and near(b.x, want[0]) and near(b.rot, want[1]) and near(b.bob, want[2])
	ok(ok_pos, "B-R2 jab_action plays on every JAB tick e..e+20 with position = state_t (within half a frame)")
	ok(ok_pose, "one authority: on every JAB tick BodyPivot x, rotation and KeyBob y equal the clip's own value at state_t (largest gap %.5f)" % worst)
	ok(d.rows[e - 1].b.fa == "" and at_rest(d.rows[e - 1].b), "before the jab: no clip, rig at rest")
	ok(d.rows[e + 21].b.state == S.IDLE and d.rows[e + 21].b.fa == "" and at_rest(d.rows[e + 21].b), "IDLE on e+21: no clip, rig back at rest")
	ok(d.rows.slice(e, e + 21).all(func(x): return x.b.ka == "" and x.b.frame == 0), "during the jab the key holds frame 0 with no key clip")
	await done(main)

	print("\n-- B2. jab lands: the clip freezes with state_t through hitstop")
	r = await fresh(390, 440); main = r[0]; d = r[1]
	tap(d, 5, KEY_J)
	await run_to(d, 45)
	e = first_entry(d, S.JAB, 0)
	var held := true
	for i in range(e + 6, e + 11):
		held = held and near(d.rows[i].b.fa_pos, d.rows[e + 5].b.fa_pos, 1e-5) and near(d.rows[i].b.x, 14.0)
	ok(held, "B-R2 clip position and pose frozen on e+6..e+10 (hitstop), at %.4f s and +14 px" % d.rows[e + 5].b.fa_pos)
	ok(d.rows[e + 11].b.fa_pos > d.rows[e + 10].b.fa_pos, "the clip moves again on e+11")
	ok(d.rows[e + 26].b.state == S.IDLE and at_rest(d.rows[e + 26].b), "IDLE on e+26 with the rig at rest")
	ok(d.rows[e + 5].r.state == S.HURT and at_rest(d.rows[e + 5].r) and d.rows[e + 5].r.fa == "", "Rivet, hit, shows no clip and a resting rig")
	await done(main)

	print("\n-- B3. pause mid-jab")
	r = await fresh(200, 440); main = r[0]; d = r[1]
	tap(d, 5, KEY_J)
	tap(d, 8, KEY_P)
	tap(d, 18, KEY_P)
	await run_to(d, 50)
	var pr := d.rows.filter(func(x): return x.paused)
	ok(pr.size() == 10 and pr.all(func(x): return x.b.fa == "jab_action" and near(x.b.fa_pos, pr[0].b.fa_pos, 1e-5) and near(x.b.x, pr[0].b.x, 1e-5)),
		"B-R2 paused 10 ticks: clip position and pose frozen at %.4f s (%d paused ticks)" % [pr[0].b.fa_pos if pr.size() else -1.0, pr.size()])
	await done(main)

	print("\n-- B4. hit in each phase: the rig snaps to rest on the tick the hit lands")
	for k in [2, 7, 15]:
		r = await fresh(300, 390); main = r[0]; d = r[1]
		tap(d, 20, KEY_J)
		r[2].plan[20 + k - 9] = {"cutlass": true}
		await run_to(d, 50)
		e = first_entry(d, S.JAB, 0)
		var h := first_entry(d, S.HURT, e)
		var phase := "startup" if h - e <= 4 else ("active" if h - e <= 10 else "recovery")
		ok(h > e and d.rows[h - 1].b.fa == "jab_action" and d.rows[h].b.fa == "" and at_rest(d.rows[h].b),
			"B-R3 %s (hit on e+%d): jab_action on e+%d, then no clip and rest pose on the hit tick itself (x %.2f)" % [phase, h - e, h - e - 1, d.rows[h].b.x])
		ok(d.rows.slice(h, h + 6).all(func(x): return at_rest(x.b)), "B-R3 %s: the rig stays at rest through the hitstop that follows" % phase)
		await done(main)
	r = await fresh(300, 390); main = r[0]; d = r[1]
	main.bolt.hp = 5.0   # SETUP
	tap(d, 20, KEY_J)
	r[2].plan[18] = {"cutlass": true}
	await run_to(d, 40)
	var ko := first_entry(d, S.KO, 0)
	ok(ko > 0 and at_rest(d.rows[ko].b) and d.rows[ko].b.fa == "", "B-R3 KO: no clip and the rig at rest on the KO tick")
	# KeyMount.visible is written by _apply_pose, which the hitstop after the hit skips
	# (fighter.gd step), so the key hides on the first unfrozen tick, as key_sprite.visible
	# did before A7.
	var hid := -1
	for i in range(ko, d.rows.size()):
		if not d.rows[i].b.key_shown:
			hid = i
			break
	print("KO on tick %d; key first hidden on tick %d (hitstop %d ticks)" % [ko, hid, hid - ko])
	ok(hid > ko and hid - ko <= 6 and d.rows.slice(hid).all(func(x): return not x.b.key_shown), "B-R5 KO: the key is hidden from the first tick after the hitstop (KO+%d) and stays hidden" % (hid - ko))
	await done(main)

	print("\n-- B5. rewind: the key cycle at state_t, held at full wind, frame 0 after")
	r = await fresh(200, 440); main = r[0]; d = r[1]
	main.bolt.wind = 40.0   # SETUP: 6 clicks to full, 90 ticks = 1.5 turns
	land(d, 5, KEY_S, true)
	land(d, 150, KEY_S, false)
	await run_to(d, 160)
	var rw := first_entry(d, S.REWIND, 0)
	var full := -1
	for i in range(rw, d.rows.size()):
		if near(d.rows[i].b.wind, 100.0):
			full = i
			break
	var turn_ok := true
	for i in range(rw, full + 1):
		var b: Dictionary = d.rows[i].b
		turn_ok = turn_ok and b.ka == "wind_key_cycle" and absf(b.ka_pos - fposmod(b.t, 1.0)) < tol and b.frame == int(floor(fposmod(b.t, 1.0) * 8.0 + 1e-4)) % 8
	ok(turn_ok, "A-R3 r..full (ticks %d..%d): wind_key_cycle at state_t mod 1 s, frame = floor(8 x that)" % [rw, full])
	var hold_frame: int = d.rows[full].b.frame
	var out := first_entry(d, S.IDLE, rw)
	ok(d.rows.slice(full, out).all(func(x): return x.b.frame == hold_frame), "A-R3 at full wind the key holds frame %d until release (ticks %d..%d)" % [hold_frame, full, out - 1])
	ok(d.rows.slice(rw, out).all(func(x): return x.b.fa == "" and at_rest(x.b)), "during REWIND no jab clip and the rig at rest")
	ok(d.rows[out].b.frame == 0 and d.rows[out].b.ka == "", "A-R3 release: IDLE on tick %d with the key back on frame 0 and no key clip" % out)
	await done(main)
	r = await fresh(200, 440); main = r[0]; d = r[1]
	land(d, 5, KEY_S, true)
	land(d, 40, KEY_S, false)
	await run_to(d, 45)
	rw = first_entry(d, S.REWIND, 0)
	ok(rw > 0 and d.rows.slice(rw, rw + 30).all(func(x): return x.b.frame == 0 and x.b.ka == ""), "A-R3 REWIND entered at full wind: the key never turns (frame 0, no clip)")
	await done(main)

	print("\n-- B6. facing lives on FacingPivot")
	r = await fresh(300, 440); main = r[0]; d = r[1]
	land(d, 5, KEY_A, true)
	land(d, 15, KEY_A, false)
	r[2].plan[30] = {"jab": true}   # Rivet jabs (whiff: gap 140)
	await run_to(d, 60)
	var left: Dictionary = d.rows[14].b
	ok(left.facing == -1 and left.face == -1.0 and left.sx > 0.0, "walking left: facing -1, FacingPivot.scale.x -1, sprite.scale.x stays positive (%.3f)" % left.sx)
	var re := -1
	for i in d.rows.size():
		if d.rows[i].r.state == S.JAB:
			re = i
			break
	ok(re > 0 and d.rows[re + 5].r.face == -1.0 and near(d.rows[re + 5].r.gx, -14.0), "Rivet's jab goes forward for him: body %.1f px from his feet at active onset (want -14)" % (d.rows[re + 5].r.gx if re > 0 else 0.0))
	await done(main)

	print("\n%d checks, %d failed" % [checks, failures])
	quit(failures)

func d_snap(f) -> Dictionary:
	return {"x": f.body_pivot.position.x, "rot": f.body_pivot.rotation, "bob": f.key_bob.position.y}
