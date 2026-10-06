extends SceneTree
## Records real gameplay for the Brutalist film with Godot's Movie Maker, so every
## frame (and the game's own mixed audio) is genuine engine output.
##
## INPUT INTEGRITY: this driver presses keys only through Input.action_press /
## action_release (held actions) and parsed InputEventAction (Enter / Esc / M / N),
## the same paths a keyboard drives. It OBSERVES positions, wind and states to
## decide what to press (a scripted player, labelled "SCRIPTED INPUT" in the film)
## but never sets position, velocity, state, hp or wind, and never disables a
## check. Rivet is driven by its normal pattern brain. Every input edge is logged
## to <clip>-inputs.jsonl; the run exits non-zero if the clip's expected events
## did not happen.
##
##   godot --path godot --resolution 3840x2160 --write-movie OUT.avi --fixed-fps 30 \
##         --script res://tools/capture_film.gd -- <clip> [log_dir]
## Clips: fight (title -> bell -> full round to KO), muted (same policy, M+N pressed:
## readability without sound), dry-run is the same script under --headless.

var main
var clip := "fight"
var log_dir := "res://../evidence/film/"
var lines: Array = []
var held := {}
var t := 0
var greedy_done := false
var phase := "approach"

func _initialize() -> void:
	var a := OS.get_cmdline_user_args()
	if a.size() > 0:
		clip = a[0]
	if a.size() > 1:
		log_dir = a[1]
	call_deferred("run")

func note(kind: String, what: String) -> void:
	lines.append(JSON.stringify({"frame": t, "t": snappedf(t / 60.0, 0.001), "kind": kind, "input": what}))

func hold(action: String, on: bool) -> void:
	if held.get(action, false) == on:
		return
	held[action] = on
	if on:
		Input.action_press(action)
	else:
		Input.action_release(action)
	note("press" if on else "release", action)

func tap_event(action: String) -> void:
	for p in [true, false]:
		var e := InputEventAction.new()
		e.action = action
		e.pressed = p
		Input.parse_input_event(e)
		await physics_frame
		t += 1
	note("event", action)

func release_all() -> void:
	for k in held.keys():
		hold(k, false)

func tap(action: String) -> void:
	hold(action, true)
	await physics_frame
	t += 1
	hold(action, false)

func run() -> void:
	main = load("res://game/main.tscn").instantiate()
	root.add_child(main)
	for i in 50:              # title screen visible ~0.8 s
		await physics_frame
		t += 1
	if clip == "muted":
		await tap_event("mute_music")
		await tap_event("mute_sfx")
	await tap_event("confirm")
	var limit := 60 * 75      # a round must finish within 75 s
	while main.round_state != main.R.KO and t < limit:
		await policy()
	release_all()
	for i in 120:             # hold on the KO screen 2 s (bell rings, music has stopped)
		await physics_frame
		t += 1
	var c: Dictionary = main.sfx.counts
	var ok: bool = main.round_state == main.R.KO and c.bell >= 2 and c.jab > 0 and c.cutlass > 0 and c.pop > 0 and c.rewind > 0 and c.empty > 0
	var summary := {"clip": clip, "frames": t, "seconds": snappedf(t / 60.0, 0.01), "winner": main.winner.skin if main.winner else "",
		"sfx_counts": c, "bolt_hp": main.bolt.hp, "rivet_hp": main.rivet.hp, "expected_events_ok": ok}
	lines.append(JSON.stringify({"summary": summary}))
	var dir := ProjectSettings.globalize_path(log_dir)
	DirAccess.make_dir_recursive_absolute(dir)
	var f := FileAccess.open(dir.path_join(clip + "-inputs.jsonl"), FileAccess.WRITE)
	f.store_string("\n".join(lines) + "\n")
	print(JSON.stringify(summary))
	quit(0 if ok else 3)

## A scripted player in storyboard order: (A) close in and trade jab/cutlass,
## (B) back off and fire one pop-gun shot, (C) get greedy and jab until the spring
## is EMPTY (panel 5), (D) retreat and rewind (panel 6), (E) fight on to the KO.
## It reads positions/wind/state (what the screen shows) and presses keys; it
## never writes game state.
var attacks := 0
var popped := false

func wait(n: int) -> void:
	for i in n:
		await physics_frame
		t += 1

func policy() -> void:
	var b: Fighter = main.bolt
	var r: Fighter = main.rivet
	if main.round_state != main.R.FIGHT or b.state in [Fighter.S.HURT, Fighter.S.EMPTY, Fighter.S.KO]:
		release_all()
		await wait(1)
		return
	var dx := r.position.x - b.position.x
	var dist := absf(dx)
	var toward := "move_right" if dx > 0 else "move_left"
	var away := "move_left" if dx > 0 else "move_right"
	match phase:
		"approach":
			if attacks >= 4:
				phase = "popgun"
		"popgun":
			if popped:
				phase = "greedy"
		"greedy":
			if greedy_done:
				phase = "recover"
		"recover":
			if b.wind >= 95.0:
				phase = "fight"
	if phase == "popgun":
		if dist < 170.0 and b.position.x > b.arena_min + 4 and b.position.x < b.arena_max - 4:
			hold(away, true); hold(toward, false)
			await wait(1)
			return
		release_all()
		await tap(toward)                  # turn to face Rivet
		await wait(4)
		var before: int = main.sfx.counts.pop
		await tap("pop")
		await wait(10)
		popped = main.sfx.counts.pop > before   # observe: did a cork actually fire? retry if not
		await wait(20)
		return
	if phase == "greedy" and dist <= 64.0:
		release_all()
		while b.wind > 0.0 and b.state != Fighter.S.HURT and main.round_state == main.R.FIGHT:
			await tap("jab")
			await wait(22)
		greedy_done = true
		return
	if phase == "recover" or (phase == "fight" and (b.wind < 30.0 or (b.state == Fighter.S.REWIND and b.wind < 95.0))):
		if b.wind > 12.0 and dist < 150.0 and b.state != Fighter.S.REWIND and b.position.x > b.arena_min + 6 and b.position.x < b.arena_max - 6:
			hold("rewind", false); hold(away, true); hold(toward, false)   # back off while there is wind to walk
		else:
			hold(away, false); hold(toward, false); hold("rewind", true)
		await wait(1)
		return
	hold("rewind", false)
	if dist > 62.0:
		hold(toward, true); hold(away, false)
		await wait(1)
		return
	hold(toward, false); hold(away, false)
	if b.facing != int(signf(dx)):
		await tap(toward)
		return
	if phase == "fight" and r.state in [Fighter.S.JAB, Fighter.S.CUTLASS] and r.state_t < 0.05:
		hold("block", true)
		await wait(14)
		hold("block", false)
		return
	await tap("cutlass" if attacks % 3 == 2 else "jab")
	attacks += 1
	await wait(16)
