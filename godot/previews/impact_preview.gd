extends Node2D
## Effect A preview, a FIXTURE (CHANGE-BRIEF D.1). Not part of the game.
##   godot --path godot res://previews/impact_preview.tscn --write-movie <abs>/frame.png --fixed-fps 30 --quit-after 60
##
## The arena background and camera exactly as main.gd sets them (main.gd:39-47),
## Bolt frozen in his jab pose at x 170 for scale, and the burst fired at the
## centre of that jab's attack box: (209, 227), over the light castle stretch
## x 192-223. The burst fires at frame 10 and, when `retrigger` is on, a second
## overlapping instance at frame 11 (A-R3). Only these preview instances use a
## fixed seed, so before/after strips are comparable; the effect scene does not.

const EFFECT := preload("res://effects/impact_effect.tscn")
const ART_SCALE := 1.0 / 3.0          # fighter.gd:260
const FEET := Vector2(240, 435)       # fighter.gd:261

@export var trigger_frame := 10
@export var retrigger := true
@export var retrigger_frame := 11
@export var impact_point := Vector2(209, 227)   # Bolt at (170, 292), jab box Rect2(24, -76, 30, 22) (fighter.gd:41, 124-125)
@export var fixed_seed := 6270

var frame := 0

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
	var bolt := Sprite2D.new()
	bolt.texture = load("res://assets/fighters/bolt/jab.png")
	bolt.centered = false
	bolt.offset = -FEET
	bolt.scale = Vector2(ART_SCALE, ART_SCALE)
	bolt.position = Vector2(170, 292)
	add_child(bolt)

func _process(_delta: float) -> void:
	if frame == trigger_frame:
		_fire(0)
	if retrigger and frame == retrigger_frame:
		_fire(1)
	frame += 1

func _fire(i: int) -> void:
	var fx := EFFECT.instantiate()
	fx.position = impact_point
	add_child(fx)
	var left := [fx.get_child_count()]   # an Array, because lambdas capture locals by value
	for e: GPUParticles2D in fx.get_children():
		e.use_fixed_seed = true
		e.seed = fixed_seed + i
		e.finished.connect(func():
			left[0] -= 1
			if left[0] == 0:
				print("preview: burst %d finished at frame %d" % [i + 1, frame])
				fx.queue_free())
		e.restart(true)
	print("preview: burst %d fired at frame %d" % [i + 1, frame])
