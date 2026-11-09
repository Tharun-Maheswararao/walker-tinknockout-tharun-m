extends Node2D
## A6 Use It: GPU-price FIXTURE. Not part of the game. Run it from the editor
## (open godot/previews/gpu_price.tscn, press F6 "Run Current Scene") and read
## Debugger -> Visual Profiler for each case. Windowed only: a headless run
## draws nothing.
##
## It runs the real game scene (main.tscn) in FIGHT with Rivet frozen and nobody
## moving, so the only thing that changes between cases is the effects:
##   0  OFF (dormant): no bursts; both steam emitters at amount_ratio 0, as the
##      game ships at wind 100
##   1  Effect A at its peak: 4 fresh impact bursts every 0.25 s lifetime
##      (CHANGE-BRIEF A-R3, peak 4 bursts / 96 particles), through main.gd's own
##      _spawn_impact; steam dormant
##   2  Effect B at its heaviest: both steam emitters held at amount_ratio 1.0
##      (both fighters at wind 0, 50 particles); no bursts
##   9  steam REMOVED (one-way; restart the scene to undo): the true zero for
##      Effect B, in case a dormant emitter still costs GPU time
##   F10 toggles vsync (game/debug_vsync.gd) for the FPS comparison
## The label shows the case, live bursts, steam ratios, FPS and vsync. Keys 0-9
## are not used by the game (game/controls.gd). Written by Claude.

const MAIN := preload("res://game/main.tscn")
const BURST_EVERY := 15            # physics ticks: the 0.25 s lifetime at 60 Hz
const PEAK_BURSTS := 4
const HIT := Vector2(320, 227)     # between the fighters, at jab height

var main
var mode := 0
var tick := 0
var label: Label
var steam_removed := false

class FrozenBrain:
	func think(_dt): pass

func _ready() -> void:
	main = MAIN.instantiate()
	add_child(main)
	await get_tree().process_frame
	main.brain = FrozenBrain.new()
	main._set_round(main.R.INTRO)      # the round's own intro; FIGHT follows after 1.3 s
	var layer := CanvasLayer.new()
	layer.layer = 100
	add_child(layer)
	label = Label.new()
	label.position = Vector2(8, 40)
	label.add_theme_font_size_override("font_size", 12)
	label.add_theme_color_override("font_color", Color.WHITE)
	label.add_theme_color_override("font_outline_color", Color.BLACK)
	label.add_theme_constant_override("outline_size", 4)
	layer.add_child(label)
	print("gpu_price: fixture ready; keys 0 off, 1 A peak, 2 B heaviest, 9 remove steam, F10 vsync")

func steams() -> Array:
	var out := []
	for f in [main.bolt, main.rivet]:
		for m in f.get_children():
			if m is SteamMount:
				out.append_array(m.get_children())
	return out

func bursts() -> int:
	return main.get_children().filter(func(n): return n.scene_file_path == "res://effects/impact_effect.tscn").size()

func _unhandled_input(event: InputEvent) -> void:
	if not (event is InputEventKey and event.pressed and not event.echo):
		return
	match event.keycode:
		KEY_0: set_mode(0)
		KEY_1: set_mode(1)
		KEY_2: set_mode(2)
		KEY_9:
			for s in steams():
				s.queue_free()
			steam_removed = true
			set_mode(0)

func set_mode(m: int) -> void:
	mode = m
	tick = 0
	for s in steams():
		s.amount_ratio = 1.0 if mode == 2 else 0.0
	print("gpu_price: case %d" % mode)

func _physics_process(_delta: float) -> void:
	if main == null or main.round_state != main.R.FIGHT:
		return
	if mode == 1 and tick % BURST_EVERY == 0:
		for k in PEAK_BURSTS:
			main._spawn_impact(HIT + Vector2((k - 1.5) * 12.0, 0), false)
	if mode == 2:
		for s in steams():
			s.amount_ratio = 1.0
	tick += 1

func _process(_delta: float) -> void:
	if label == null or main == null:
		return
	var names := {0: "0 OFF (effects dormant)", 1: "1 Effect A peak: 4 bursts", 2: "2 Effect B heaviest: ratio 1.0 x2"}
	var ratios := steams().map(func(s): return "%.2f" % s.amount_ratio)
	label.text = "GPU-PRICE FIXTURE   case %s%s\nbursts alive %d   steam %s\nFPS %d   vsync %s   (keys 0/1/2/9, F10)" % [
		names[mode], "  [steam removed]" if steam_removed else "", bursts(),
		"removed" if steam_removed else ", ".join(ratios), Engine.get_frames_per_second(),
		"OFF" if DisplayServer.window_get_vsync_mode() == DisplayServer.VSYNC_DISABLED else "ON"]
