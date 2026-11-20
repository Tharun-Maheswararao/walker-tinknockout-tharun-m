extends SceneTree
## A7 Step 4: read-back for the rig clip jab_action (CHANGE-BRIEF.md §4, rule
## B-R1). Written by Claude for Tharun's review.
##   ./scripts/run-test.sh test_jab_action_readback.gd 60
##
## What it reads:
##   1. the clip resource godot/animations/jab_action.tres: LOOP_NONE, step one
##      frame period at 60 fps, length 21 frames, no Godot 3 names;
##   2. each of its three tracks: value track, path, linear interpolation,
##      continuous updates (update mode is asked only of value tracks), keys at
##      frames 0, 3, 5, 10, 11, 21 (compared within half a frame, never ==),
##      the brief's values and the brief's transitions;
##   3. every track resolves to a real node and property (the handout's
##      track_problems, branching on track type) on a FIXTURE built to the
##      brief's hierarchy; the game has no such nodes until Step 5;
##   4. the clip played on that fixture (MANUAL, seek to each frame): the pose
##      at every phase boundary, the hold through the active window, the
##      spacing the brief's easing asks for, and the rest pose at the end;
##   5. facing: with FacingPivot.scale.x = -1 the lunge goes to -x (Rivet's
##      forward), with +1 to +x.
## It proves the clip is structured as the brief says. It cannot show whether
## the jab reads (a frame strip and play do), or that the game plays it on
## JAB in step with state_t (Step 5).
## Exit code = number of failed checks.

const CLIP := "res://animations/jab_action.tres"
const FPS := 60.0                          # CHANGE-BRIEF §4
const LENGTH_FRAMES := 21
const KEY_FRAMES := [0, 3, 5, 10, 11, 21]  # every phase boundary (0, 5, 11, 21) plus the coil peak and the end of the hold
const TRANS := [0.5, 2.0, 1.0, 1.0, 0.5, 1.0]
const TRACKS := {
	"FacingPivot/BodyPivot:position:x": [0.0, -6.0, 14.0, 14.0, 8.0, 0.0],
	"FacingPivot/BodyPivot:rotation": [0.0, -0.10, 0.12, 0.12, 0.05, 0.0],
	"FacingPivot/BodyPivot/KeyMount/KeyBob:position:y": [0.0, 2.0, -2.0, -2.0, -1.0, 0.0],
}

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

func near(a: float, b: float, eps := 1e-4) -> bool:
	return absf(a - b) < eps

## Fixture to the brief's hierarchy (CHANGE-BRIEF §1): Fighter/FacingPivot/
## BodyPivot/{sprite, KeyMount/KeyBob/key_sprite}, FighterAnimPlayer under Fighter.
func fixture(clip: Animation, facing: float) -> Dictionary:
	var fighter := Node2D.new()
	fighter.name = "Fighter"
	fighter.position = Vector2(300, 292)
	var fp := Node2D.new(); fp.name = "FacingPivot"; fp.scale = Vector2(facing, 1)
	var bp := Node2D.new(); bp.name = "BodyPivot"
	var spr := Sprite2D.new(); spr.name = "sprite"
	var km := Node2D.new(); km.name = "KeyMount"
	var kb := Node2D.new(); kb.name = "KeyBob"
	var ks := Sprite2D.new(); ks.name = "key_sprite"
	fighter.add_child(fp); fp.add_child(bp); bp.add_child(spr); bp.add_child(km); km.add_child(kb); kb.add_child(ks)
	var player := AnimationPlayer.new()
	player.name = "FighterAnimPlayer"
	fighter.add_child(player)
	root.add_child(fighter)
	var lib := AnimationLibrary.new()
	lib.add_animation("jab_action", clip)
	player.add_animation_library("", lib)
	player.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	return {"fighter": fighter, "body": bp, "bob": kb, "player": player}

func pose_at(f: Dictionary, frame: float) -> Array:
	f.player.seek(frame / FPS, true)
	return [f.body.position.x, f.body.rotation, f.bob.position.y]

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
	ok(clip.loop_mode == Animation.LOOP_NONE, "loop_mode is Animation.LOOP_NONE: the jab commits once (got %d)" % clip.loop_mode)
	ok(is_equal_approx(clip.step, 1.0 / FPS) or absf(clip.step - 1.0 / FPS) < 1e-6, "step is one frame period at 60 fps, 1/60 s (got %.7f)" % clip.step)
	ok(absf(clip.length - LENGTH_FRAMES / FPS) < tol, "length is 21 frames = 0.35 s (got %.7f)" % clip.length)
	var text := FileAccess.get_file_as_string(CLIP)
	ok(["loop = ", "playback_speed", "\nloop="].all(func(s): return not (s in text)), "no Godot 3 names (loop =, playback_speed) in the resource text")
	ok(clip.get_track_count() == TRACKS.size(), "%d tracks (got %d)" % [TRACKS.size(), clip.get_track_count()])

	# --- 2. each track --------------------------------------------------------
	print("\n-- 2. tracks")
	var found := {}
	for t in clip.get_track_count():
		var path := String(clip.track_get_path(t))
		found[path] = true
		ok(TRACKS.has(path), "track %d path %s is one the brief names" % [t, path])
		if not TRACKS.has(path):
			continue
		ok(clip.track_get_type(t) == Animation.TYPE_VALUE, "%s: value track" % path)
		if clip.track_get_type(t) == Animation.TYPE_VALUE:   # update mode exists only on value tracks
			ok(clip.value_track_get_update_mode(t) == Animation.UPDATE_CONTINUOUS, "%s: continuous updates (a transform moves between keys)" % path)
		ok(clip.track_get_interpolation_type(t) == Animation.INTERPOLATION_LINEAR, "%s: linear interpolation, shaped by each key's transition" % path)
		var n := clip.track_get_key_count(t)
		ok(n == KEY_FRAMES.size(), "%s: %d keys (got %d)" % [path, KEY_FRAMES.size(), n])
		var want_vals: Array = TRACKS[path]
		for k in mini(n, KEY_FRAMES.size()):
			var kt := clip.track_get_key_time(t, k)
			var kv: float = clip.track_get_key_value(t, k)
			var tr := clip.track_get_key_transition(t, k)
			ok(absf(kt - KEY_FRAMES[k] / FPS) < tol and near(kv, want_vals[k]) and near(tr, TRANS[k]),
				"%s key %d: frame %d (time %.7f), value %.3f, transition %.1f" % [path.get_file(), k, KEY_FRAMES[k], kt, kv, tr])
	ok(found.size() == TRACKS.size() and TRACKS.keys().all(func(p): return found.has(p)), "every track the brief names is present")
	for b in [0, 5, 11, 21]:
		ok(KEY_FRAMES.has(b), "a key sits on phase boundary frame %d" % b)

	# --- 3. tracks resolve (fixture) -------------------------------------------
	print("\n-- 3. track resolution on a FIXTURE built to the brief's hierarchy")
	var f := fixture(clip, 1.0)
	f.player.play("jab_action")
	var probs := track_problems(f.player)
	ok(probs.is_empty(), "track_problems finds nothing: every track names a real node and property %s" % [probs])

	# --- 4. played: poses, hold, spacing, rest ----------------------------------
	print("\n-- 4. played on the fixture (MANUAL, seek to each frame)")
	var poses := []
	for fr in LENGTH_FRAMES + 1:
		poses.append(pose_at(f, fr))
	print("frame  x       rot     keybob_y")
	for fr in poses.size():
		print("%5d  %6.2f  %6.3f  %6.2f" % [fr, poses[fr][0], poses[fr][1], poses[fr][2]])
	for i in KEY_FRAMES.size():
		var fr: int = KEY_FRAMES[i]
		var want := [TRACKS.values()[0][i], TRACKS.values()[1][i], TRACKS.values()[2][i]]
		ok(near(poses[fr][0], want[0], 1e-3) and near(poses[fr][1], want[1], 1e-3) and near(poses[fr][2], want[2], 1e-3),
			"pose at frame %d is (%.2f, %.3f, %.2f) as the brief keys it" % [fr, want[0], want[1], want[2]])
	var hold := true
	for fr in range(5, 11):
		hold = hold and near(poses[fr][0], 14.0, 1e-3) and near(poses[fr][1], 0.12, 1e-3)
	ok(hold, "the extension holds at +14 px, +0.12 rad on every active frame 5..10")
	ok(poses[1][0] - poses[0][0] < poses[3][0] - poses[2][0], "startup 0->3 eases out: the first frame moves furthest back (%.2f vs %.2f)" % [poses[1][0] - poses[0][0], poses[3][0] - poses[2][0]])
	ok(poses[4][0] - poses[3][0] < poses[5][0] - poses[4][0], "3->5 eases in: it accelerates into the active frame (%.2f then %.2f px)" % [poses[4][0] - poses[3][0], poses[5][0] - poses[4][0]])
	ok(poses[11][0] - poses[12][0] > poses[20][0] - poses[21][0], "recovery 11->21 eases out: it settles (first step %.2f px, last %.2f px)" % [poses[11][0] - poses[12][0], poses[20][0] - poses[21][0]])
	f.player.seek(LENGTH_FRAMES / FPS, true)
	f.player.advance(0.5)
	ok(near(f.body.position.x, 0.0) and near(f.body.rotation, 0.0) and near(f.bob.position.y, 0.0), "after the end the rig stays at rest: LOOP_NONE does not wrap into the coil")
	f.fighter.queue_free()

	# --- 5. facing --------------------------------------------------------------
	print("\n-- 5. facing comes from FacingPivot, not the clip")
	for facing in [1.0, -1.0]:
		var g := fixture(clip, facing)
		g.player.play("jab_action")
		g.player.seek(5.0 / FPS, true)
		var dx: float = g.body.global_position.x - g.fighter.global_position.x
		ok(near(dx, 14.0 * facing, 1e-3), "facing %+d: at active onset the body is %+.1f px from the feet (forward)" % [int(facing), dx])
		g.fighter.queue_free()

	print("\n%d checks, %d failed" % [checks, failures])
	quit(failures)
