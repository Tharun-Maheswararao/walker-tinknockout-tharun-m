extends SceneTree
## A7 Step 3: read-back for the sprite clip wind_key_cycle (CHANGE-BRIEF.md
## §1-3, rules A-R1 and A-R2). Written by Claude for Tharun's review.
##   ./scripts/run-test.sh test_wind_key_cycle_readback.gd 60
##
## What it reads:
##   1. the clip resource godot/animations/wind_key_cycle.tres: loop mode, step,
##      length, one discrete value track keying `frame`, its path, 8 keys at
##      k/8 s (compared with a tolerance of half a frame period, never ==),
##      values 0..7, every value inside the sheet, the seam, no Godot 3 names;
##   2. both sheets: they load, are 672x60 = 8 x 1 cells of 84x60, and the 90
##      and 270 degree cells keep at least 0.15 x 84 px of key (A-R1);
##   3. the track resolves to a real node and property (the handout's
##      track_problems) on a FIXTURE built to the brief's hierarchy,
##      Fighter/FacingPivot/BodyPivot/KeyMount/KeyBob/key_sprite, with the
##      player as a direct child of Fighter (root_node ".."). The game has no
##      such nodes until Step 5; the structure test then checks the real fighter;
##   4. played headless in MANUAL mode for 5 s: frame order 0..7 repeating and
##      each frame held one 8 fps step (7 or 8 physics ticks), including frame 0
##      after the wrap.
## It proves the clip is structured as the brief says. It cannot show whether
## the turn reads, or that the game plays it in REWIND (Step 5).
## Exit code = number of failed checks.

const CLIP := "res://animations/wind_key_cycle.tres"
const PATH := "FacingPivot/BodyPivot/KeyMount/KeyBob/key_sprite:frame"
const FPS := 8.0                      # CHANGE-BRIEF §3
const FRAMES := 8
const CELL := Vector2i(84, 60)        # CHANGE-BRIEF §2
const HFRAMES := 8
const VFRAMES := 1
const MIN_W := 0.15

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

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	# --- 1. the clip resource -------------------------------------------------
	print("-- 1. %s" % CLIP)
	var clip := ResourceLoader.load(CLIP, "", ResourceLoader.CACHE_MODE_IGNORE) as Animation
	ok(clip != null, "clip loads as an Animation")
	if clip == null:
		print("\n%d checks, %d failed" % [checks, failures])
		quit(failures)
		return
	var tol := 0.5 / FPS
	ok(clip.loop_mode == Animation.LOOP_LINEAR, "loop_mode is Animation.LOOP_LINEAR (got %d)" % clip.loop_mode)
	ok(is_equal_approx(clip.step, 1.0 / FPS), "step is one frame period, 1/8 s (got %.6f)" % clip.step)
	ok(absf(clip.length - FRAMES / FPS) < tol, "length is 8 frames = 1.0 s (got %.6f)" % clip.length)
	var text := FileAccess.get_file_as_string(CLIP)
	var g3 := ["loop = ", "playback_speed", "\nloop="]
	ok(g3.all(func(s): return not (s in text)), "no Godot 3 names (loop =, playback_speed) in the resource text")
	ok(clip.get_track_count() == 1, "one track (got %d)" % clip.get_track_count())
	var t := 0
	ok(clip.track_get_type(t) == Animation.TYPE_VALUE, "track 0 is a value track")
	ok(String(clip.track_get_path(t)) == PATH, "track 0 path is %s (got %s)" % [PATH, clip.track_get_path(t)])
	if clip.track_get_type(t) == Animation.TYPE_VALUE:   # update mode exists only on value tracks
		ok(clip.value_track_get_update_mode(t) == Animation.UPDATE_DISCRETE, "track 0 uses discrete updates (got %d)" % clip.value_track_get_update_mode(t))
	var n := clip.track_get_key_count(t)
	ok(n == FRAMES, "8 keys (got %d)" % n)
	var times_ok := true
	var values := []
	for k in n:
		var kt := clip.track_get_key_time(t, k)
		times_ok = times_ok and absf(kt - k / FPS) < tol
		values.append(clip.track_get_key_value(t, k))
	ok(times_ok, "key k sits at k/8 s within half a frame (%s)" % [range(n).map(func(k): return "%.4f" % clip.track_get_key_time(t, k))])
	ok(values == range(FRAMES), "key values are frames 0..7 in order (got %s)" % [values])
	ok(values.all(func(v): return v >= 0 and v < HFRAMES * VFRAMES), "every frame key is inside the sheet: 0 <= frame < hframes x vframes = %d" % (HFRAMES * VFRAMES))
	if n > 0:
		var last := clip.track_get_key_time(t, n - 1)
		ok(absf((clip.length - last) - 1.0 / FPS) < tol, "seam: the gap from the last key (%.4f) to length (%.4f) is one key interval, 1/8 s" % [last, clip.length])
		ok(clip.track_find_key(t, clip.length, Animation.FIND_MODE_APPROX) == -1, "seam: no key at t = length")
		ok(values[0] != values[n - 1], "seam: no duplicate across the wrap (first %s, last %s)" % [values[0], values[n - 1]])

	# --- 2. the sheets --------------------------------------------------------
	print("\n-- 2. sheets")
	for skin in ["bolt", "rivet"]:
		var p := "res://assets/props/key-%s-sheet.png" % skin
		var tex := ResourceLoader.load(p, "", ResourceLoader.CACHE_MODE_IGNORE) as Texture2D
		ok(tex != null and tex.get_width() == CELL.x * HFRAMES and tex.get_height() == CELL.y * VFRAMES,
			"%s loads, %dx%d = %d x %d cells of %dx%d" % [p, CELL.x * HFRAMES, CELL.y * VFRAMES, HFRAMES, VFRAMES, CELL.x, CELL.y])
		var img := Image.load_from_file(ProjectSettings.globalize_path(p))
		for k in [2, 6]:
			var used := img.get_region(Rect2i(k * CELL.x, 0, CELL.x, CELL.y)).get_used_rect()
			ok(used.size.x >= MIN_W * CELL.x, "%s cell %d (%d deg) keeps %d px of key, at least 0.15 x 84 = %.1f" % [skin, k, k * 45, used.size.x, MIN_W * CELL.x])

	# --- 3. the track resolves (fixture to the brief's hierarchy) -------------
	print("\n-- 3. track resolution on a FIXTURE built to the brief's hierarchy")
	var fighter := Node2D.new()
	fighter.name = "Fighter"
	var parent: Node = fighter
	for nm in ["FacingPivot", "BodyPivot", "KeyMount", "KeyBob"]:
		var nd := Node2D.new()
		nd.name = nm
		parent.add_child(nd)
		parent = nd
	var key := Sprite2D.new()
	key.name = "key_sprite"
	key.texture = load("res://assets/props/key-bolt-sheet.png")
	key.hframes = HFRAMES
	key.vframes = VFRAMES
	parent.add_child(key)
	var player := AnimationPlayer.new()
	player.name = "KeyAnimPlayer"
	fighter.add_child(player)
	root.add_child(fighter)
	var lib := AnimationLibrary.new()
	lib.add_animation("wind_key_cycle", clip)
	player.add_animation_library("", lib)
	var probs := track_problems(player)
	ok(probs.is_empty(), "track_problems finds nothing: the track names a real node and property %s" % [probs])

	# --- 4. played headless ----------------------------------------------------
	print("\n-- 4. played headless, MANUAL mode, 300 physics ticks (5 s)")
	player.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	player.play("wind_key_cycle")
	player.advance(0.0)
	var seen := [key.frame]
	var holds := []
	var run := 1
	for i in 300:
		player.advance(1.0 / 60.0)
		if key.frame == seen[-1]:
			run += 1
		else:
			holds.append(run)
			run = 1
			seen.append(key.frame)
	var want := []
	for i in seen.size():
		want.append(i % FRAMES)
	ok(seen == want, "frames change 0,1,..,7,0,1,.. in order across the wraps (%d changes)" % (seen.size() - 1))
	ok(seen.size() >= 5 * FRAMES, "at least 5 full turns seen (%d frames shown)" % seen.size())
	ok(holds.all(func(h): return h == 7 or h == 8), "every frame, frame 0 after each wrap included, is held one 8 fps step: 7 or 8 ticks (holds %s)" % [holds])

	print("\n%d checks, %d failed" % [checks, failures])
	quit(failures)
