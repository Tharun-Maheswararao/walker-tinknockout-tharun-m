extends SceneTree
## Film tool (not part of the game): a SCRIPTED-INPUT Movie Maker capture of both
## A6 effects in the running game. Run WINDOWED on an isolated copy of c844ab2:
##   godot --path <copy>/godot --resolution 3840x2160 --disable-vsync --always-on-top \
##         --write-movie <dir>/frame.png --fixed-fps 30 --script res://film_play.gd
## It instantiates the unchanged game/main.tscn and drives Bolt only through the real
## input path (Input.parse_input_event / Input.action_press). Rivet is the game's own
## brain. It never touches an effect, its values or amount_ratio; the game does.
## Sequence: confirm; wait until Rivet is within reach; tap jab every time Bolt is
## back to IDLE, until 8 jabs have started (each costs 12 wind: 100 -> 4, so Effect B
## turns on); wait 1 s; pause 1 s; unpause; hold rewind 1.5 s; release; wait 1.2 s.
## Prints one line per movie frame: Bolt/Rivet state, Bolt wind, both steam
## amount_ratios, live bursts (normal / blocked), key scale.x, paused.

var main
var t := 0
var jabs := 0
var seen := {}

func _initialize() -> void:
	call_deferred("run")

func steam(f) -> GPUParticles2D:
	var m = f.get_node_or_null("SteamMount")
	return m.get_child(0) if m and m.get_child_count() > 0 else null

func bursts() -> Array:
	var n := 0
	var b := 0
	for c in main.get_children():
		var p: String = c.scene_file_path
		if p.ends_with("impact_effect.tscn"):
			n += 1
		elif p.ends_with("impact_effect_blocked.tscn"):
			b += 1
		if p.contains("impact_effect") and not seen.has(c.get_instance_id()):
			seen[c.get_instance_id()] = true
			print("SPAWN frame %d %s at (%.0f, %.0f)" % [t, p.get_file(), c.position.x, c.position.y])
	return [n, b]

func frames(n: int) -> void:
	for i in n:
		await process_frame
		t += 1
		if main and main.bolt and main.rivet:
			var bb := bursts()
			var sb := steam(main.bolt)
			var sr := steam(main.rivet)
			print("frame %d bolt %d rivet %d wind %.1f ratio %.2f rivet_ratio %.2f bursts %d blocked %d keyx %.3f paused %s gap %.0f" % [
				t, main.bolt.state, main.rivet.state, main.bolt.wind,
				sb.amount_ratio if sb else -1.0, sr.amount_ratio if sr else -1.0,
				bb[0], bb[1], main.bolt.key_sprite.scale.x, main.paused,
				main.rivet.position.x - main.bolt.position.x])

func tap(action: String) -> void:
	for pressed in [true, false]:
		var ev := InputEventAction.new()
		ev.action = action
		ev.pressed = pressed
		Input.parse_input_event(ev)
		await frames(1)

func run() -> void:
	main = load("res://game/main.tscn").instantiate()
	root.add_child(main)
	await frames(15)
	await tap("confirm")                              # TITLE -> INTRO
	await frames(int(main.INTRO_TIME * 30) + 6)
	var guard := 0
	while absf(main.rivet.position.x - main.bolt.position.x) > 78.0 and guard < 150:
		await frames(1)
		guard += 1
	print("JABS start at frame %d" % t)
	guard = 0
	while jabs < 8 and guard < 400:
		if main.bolt.state == 0:                       # Fighter.S.IDLE
			print("JAB %d pressed at frame %d" % [jabs + 1, t])
			await tap("jab")
			if main.bolt.state == 2:                   # Fighter.S.JAB
				jabs += 1
			guard += 2
		else:
			await frames(1)
			guard += 1
	await frames(30)
	print("PAUSE at frame %d" % t)
	await tap("pause")
	await frames(29)
	print("UNPAUSE at frame %d" % t)
	await tap("pause")
	await frames(10)
	print("HOLD rewind at frame %d" % t)
	Input.action_press("rewind")
	await frames(45)
	print("RELEASE rewind at frame %d" % t)
	Input.action_release("rewind")
	await frames(36)
	print("film capture done at frame %d" % t)
	quit()
