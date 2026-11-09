extends Node2D
## Effect B rewind preview, a FIXTURE for the tuning loop on Tharun's in-game
## observation "the steam cut out as soon as I started rewinding". Not part of
## the game. The D.2 strip (steam_preview.tscn) never rewinds, so it cannot show it.
##   godot --path godot res://previews/steam_rewind_preview.tscn --disable-vsync --write-movie <abs>/frame.png --fixed-fps 30 --quit-after 100
##
## Same background, camera and real Fighter (Bolt, x 314, key over the darkest
## stretch) as steam_preview.tscn. What differs: Bolt runs his real step() from
## frame 10, so the key really spins and squashes in REWIND (fighter.gd:272-273),
## and amount_ratio follows his wind through the game's own mapping,
## main.gd steam_ratio(), on his real wind_changed signal.
##   frame 10: _spend(96) takes wind 100 -> 4 (ratio 0.84), as eight jabs would
##   frame 30: rewind held from here on (intent, as a held S key sets it)
##   then one click per 0.25 s: wind 14 (0.44), 24 (0.04), 34 (0.0), ...
## Only this preview instance uses a fixed seed.
##
## For watching (never for captures): `-- --loop` restarts the run every
## LOOP_FRAMES of real time (counted in 30 fps frames); `--random` drops the seed.
##   godot --path godot res://previews/steam_rewind_preview.tscn -- --loop [--random]

const LOOP_FRAMES := 100
const EFFECT := preload("res://effects/wind_steam.tscn")
const MAIN := preload("res://game/main.gd")   # for steam_ratio(), the game's mapping
const IDLE := {"move": 0, "jab": false, "cutlass": false, "pop": false, "block": false, "rewind": false}

@export var low_wind_frame := 10
@export var rewind_frame := 30
@export var bolt_x := 314.0
@export var fixed_seed := 6271

var frame := 0
var loop := "--loop" in OS.get_cmdline_user_args()
var random := "--random" in OS.get_cmdline_user_args()
var bolt: Fighter
var steam: GPUParticles2D
var running := false
var t := 0.0

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
	bolt = Fighter.new()
	bolt.skin = "bolt"
	bolt.arena_min = 132.0                 # main.gd ARENA
	bolt.arena_max = 500.0
	bolt.position = Vector2(bolt_x, 292)   # FLOOR_Y
	add_child(bolt)
	steam = SteamMount.attach(bolt, EFFECT)   # mounted as in the game (main.gd)
	steam.use_fixed_seed = not random
	steam.seed = fixed_seed
	steam.restart()                         # so the fixed seed applies from the start
	bolt.wind_changed.connect(func(_f, w):
		steam.amount_ratio = MAIN.steam_ratio(w)
		print("preview: frame %d wind %.0f -> amount_ratio %.2f" % [frame, w, steam.amount_ratio]))
	bolt.intent = IDLE.duplicate()

func _physics_process(delta: float) -> void:
	if running:
		bolt.step(delta)

func _process(delta: float) -> void:
	if loop:
		var f := int(t * 30.0)
		t = fmod(t + delta, LOOP_FRAMES / 30.0)
		if f == frame:
			return
		if f < frame:                       # a new cycle: put Bolt back as he started
			running = false
			bolt.reset(bolt_x, 1)
			bolt.intent = IDLE.duplicate()
		frame = f
	if frame == low_wind_frame:
		running = true
		bolt._spend(96.0)                   # wind 100 -> 4 through the fighter's own path
	if frame == rewind_frame:
		var i := IDLE.duplicate()
		i.rewind = true
		bolt.intent = i
		print("preview: rewind held from frame %d" % frame)
	if not loop:
		frame += 1
