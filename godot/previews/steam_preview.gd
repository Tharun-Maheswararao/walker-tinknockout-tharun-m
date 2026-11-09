extends Node2D
## Effect B preview, a FIXTURE (CHANGE-BRIEF D.2). Not part of the game.
##   godot --path godot res://previews/steam_preview.tscn --write-movie <abs>/frame.png --fixed-fps 30 --quit-after 80
##
## The arena background and camera exactly as main.gd sets them, and a real
## Fighter (Bolt, idle, facing right) so the steam rides his actual key_sprite:
## the game's 1/3 scale, z_index -1 and key anchor. Bolt stands at x 314, which
## puts the key (anchor x -42.6, anchors.json "idle") at x 271, the middle of
## the darkest background stretch, x 256-287 (design/a6/BRIEF-FACTS.md §4).
## The condition starts at frame 10 (amount_ratio 1.0, as at wind 0) and ends at
## frame 50 (amount_ratio 0.0; emitting stays true, B-R2). Only this preview
## instance uses a fixed seed; the effect scene does not.
##
## For watching (never for captures): `-- --loop` repeats the on/off schedule
## every LOOP_FRAMES, counted in 30 fps frames of real time (2.67 s per cycle at
## any display rate); adding `--random` drops the fixed seed.
##   godot --path godot res://previews/steam_preview.tscn -- --loop [--random]

const LOOP_FRAMES := 80
const EFFECT := preload("res://effects/wind_steam.tscn")

@export var start_frame := 10
@export var stop_frame := 50
@export var bolt_x := 314.0
@export var fixed_seed := 6271

var frame := 0
var loop := "--loop" in OS.get_cmdline_user_args()
var random := "--random" in OS.get_cmdline_user_args()
var steam: GPUParticles2D

func _ready() -> void:
	var cam := Camera2D.new()
	cam.position = Vector2(320, 180)
	add_child(cam)
	var bg := Sprite2D.new()
	bg.centered = false
	bg.z_index = -10
	bg.texture = load("res://assets/env/bowl.png")
	bg.scale = Vector2(640.0 / bg.texture.get_width(), 360.0 / bg.texture.get_height())
	add_child(bg)
	var bolt := Fighter.new()
	bolt.skin = "bolt"
	bolt.position = Vector2(bolt_x, 292)   # FLOOR_Y, main.gd:12
	add_child(bolt)                        # _ready loads the art and applies the idle pose
	steam = EFFECT.instantiate()
	steam.use_fixed_seed = not random
	steam.seed = fixed_seed
	bolt.key_sprite.add_child(steam)
	print("preview: key_sprite at %s, scale %s; steam amount_ratio %.2f" % [bolt.key_sprite.global_position, bolt.key_sprite.scale, steam.amount_ratio])

var t := 0.0

func _process(delta: float) -> void:
	if loop:
		# a window runs at the display rate (about 120 fps here), not 30, so the
		# watching loop counts 30 fps frames of real time; captures (--fixed-fps 30)
		# keep counting rendered frames
		var f := int(t * 30.0)
		t = fmod(t + delta, LOOP_FRAMES / 30.0)
		if f == frame:
			return
		frame = f
	if frame == start_frame:
		steam.amount_ratio = 1.0
		print("preview: condition on (amount_ratio 1.0) at frame %d" % frame)
	if frame == stop_frame:
		steam.amount_ratio = 0.0
		print("preview: condition off (amount_ratio 0.0, emitting %s) at frame %d" % [steam.emitting, frame])
	if not loop:
		frame += 1
