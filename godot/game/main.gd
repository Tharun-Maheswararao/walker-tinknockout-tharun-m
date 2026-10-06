extends Node2D
## Tin Knockout asset slice: one round, Bolt (player) vs Rivet (pattern opponent)
## at the bottom of an empty goldfish bowl.
##
## Round flow: TITLE -> INTRO ("ROUND 1") -> FIGHT (bell) -> KO (bell, music
## stops) -> R / Enter -> INTRO again. Pause (Esc/P) freezes the fight and
## muffles the music. M / N mute music / effects separately.

signal round_changed(state: int)

enum R { TITLE, INTRO, FIGHT, KO }
const FLOOR_Y := 292.0     # sand floor of ENV-BOWL (80% of frame height)
const ARENA := Vector2(132, 500)  # inside the bowl's glass
const INTRO_TIME := 1.3
const LOW_WIND := 25.0

var round_state: int = R.TITLE
var round_t := 0.0
var paused := false
var show_boxes := false
var winner: Fighter

var bolt: Fighter
var rivet: Fighter
var brain
var corks: Array = []
var sfx
var music
var hud
var cam: Camera2D
var bg: Sprite2D
var shake := 0.0
var roll := 0.0
var sparks: Array = []   # [pos, t]
var fx: Node2D           # drawn above the fighters

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	cam = Camera2D.new()
	cam.position = Vector2(320, 180)
	add_child(cam)
	bg = Sprite2D.new()
	bg.centered = false
	bg.z_index = -10
	if ResourceLoader.exists("res://assets/env/bowl.png"):
		bg.texture = load("res://assets/env/bowl.png")
		bg.scale = Vector2(640.0 / bg.texture.get_width(), 360.0 / bg.texture.get_height())
	add_child(bg)

	bolt = Fighter.new()
	bolt.skin = "bolt"
	rivet = Fighter.new()
	rivet.skin = "rivet"
	for f in [bolt, rivet]:
		f.position.y = FLOOR_Y
		f.arena_min = ARENA.x
		f.arena_max = ARENA.y
		f.spawn_cork = _spawn_cork
		add_child(f)
		f.hit_landed.connect(_on_hit)
	bolt.opponent = rivet
	rivet.opponent = bolt
	brain = preload("res://fighter/rivet_brain.gd").new()
	brain.me = rivet

	sfx = preload("res://audio/sfx.gd").new()
	add_child(sfx)
	sfx.watch(bolt)
	sfx.watch(rivet)
	round_changed.connect(func(s):
		if s == R.FIGHT or s == R.KO:
			sfx.play("bell"))
	music = preload("res://audio/music.gd").new()
	add_child(music)
	bolt.wind_changed.connect(func(_f, w):
		if round_state == R.FIGHT:
			music.set_low_wind(w < LOW_WIND))

	fx = Node2D.new()
	fx.z_index = 5
	add_child(fx)
	fx.draw.connect(_draw_fx)
	hud = preload("res://ui/hud.gd").new()
	hud.game = self
	add_child(hud)
	_reset_fighters()
	_set_round(R.TITLE)
	music.title()

func _reset_fighters() -> void:
	for c in corks:
		if is_instance_valid(c):
			c.queue_free()
	corks.clear()
	bolt.reset(200, 1)
	rivet.reset(440, -1)
	if brain and brain.get("pop_cd") != null:
		brain.pop_cd = 1.5
	winner = null

func _set_round(s: int) -> void:
	round_state = s
	round_t = 0.0
	round_changed.emit(s)

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("mute_music"):
		var b := AudioServer.get_bus_index(&"Music")
		AudioServer.set_bus_mute(b, not AudioServer.is_bus_mute(b))
	elif event.is_action_pressed("mute_sfx"):
		var b := AudioServer.get_bus_index(&"SFX")
		AudioServer.set_bus_mute(b, not AudioServer.is_bus_mute(b))
	elif event.is_action_pressed("debug_boxes"):
		show_boxes = not show_boxes
	elif event.is_action_pressed("pause") and round_state == R.FIGHT:
		paused = not paused
		music.set_paused(paused)
	elif round_state == R.TITLE and event.is_action_pressed("confirm"):
		_set_round(R.INTRO)
	elif round_state == R.KO and (event.is_action_pressed("rematch") or event.is_action_pressed("confirm")):
		_reset_fighters()
		_set_round(R.INTRO)

func _physics_process(dt: float) -> void:
	round_t += dt
	match round_state:
		R.INTRO:
			for f in [bolt, rivet]:
				f.intent = {"move": 0, "jab": false, "cutlass": false, "pop": false, "block": false, "rewind": false}
			if round_t >= INTRO_TIME:
				_set_round(R.FIGHT)
				music.fight_start()
		R.FIGHT:
			if not paused:
				_read_player()
				brain.think(dt)
				_simulate(dt)
				if bolt.is_out() or rivet.is_out():
					winner = rivet if bolt.is_out() else bolt
					winner.win()
					music.knockout()
					roll = 0.45
					_set_round(R.KO)
		R.KO:
			bolt.intent = {"move": 0, "jab": false, "cutlass": false, "pop": false, "block": false, "rewind": false}
			_simulate(dt)
	_effects(dt)
	hud.redraw()
	fx.queue_redraw()

func _read_player() -> void:
	bolt.intent = {
		"move": int(Input.get_axis("move_left", "move_right")),
		"jab": Input.is_action_just_pressed("jab"),
		"cutlass": Input.is_action_just_pressed("cutlass"),
		"pop": Input.is_action_just_pressed("pop"),
		"block": Input.is_action_pressed("block"),
		"rewind": Input.is_action_pressed("rewind"),
	}

func _simulate(dt: float) -> void:
	bolt.step(dt)
	rivet.step(dt)
	# tin bodies don't pass through each other
	var gap := rivet.position.x - bolt.position.x
	var min_gap := 44.0
	if absf(gap) < min_gap:
		var side := signf(gap) if gap != 0.0 else 1.0
		var fix := (min_gap - absf(gap)) / 2.0
		bolt.position.x -= side * fix
		rivet.position.x += side * fix
	for c in corks.duplicate():
		if is_instance_valid(c):
			c.step(dt)
		else:
			corks.erase(c)

func _spawn_cork(f: Fighter) -> void:
	var c := Sprite2D.new()
	c.set_script(preload("res://fighter/cork.gd"))
	c.owner_fighter = f
	c.dir = f.facing
	var pa: Dictionary = f.anchors.get("pop", {})
	var m: Array = pa.get("muzzle", [60, -64])
	c.position = f.position + Vector2(m[0] * f.facing, m[1])
	if ResourceLoader.exists("res://assets/props/cork.png"):
		c.texture = load("res://assets/props/cork.png")
		c.scale = Vector2.ONE * (14.0 / c.texture.get_width())
	add_child(c)
	sfx.watch_cork(c)
	c.struck.connect(func(cork, _blocked): _on_impact(cork.position))
	corks.append(c)

func _on_hit(attacker: Fighter, _attack: String, _blocked: bool) -> void:
	var box := attacker.attack_box()
	_on_impact(box.get_center() if box.has_area() else attacker.opponent.position + Vector2(0, -70))

func _on_impact(p: Vector2) -> void:
	sparks.append([p, 0.14])
	shake = 0.15
	if bolt.state == Fighter.S.HURT and bolt.stun >= Fighter.KNOCKDOWN_TIME:
		roll = 0.45   # knockdown: Dutch-angle camera roll (storyboard panel 5)

func _effects(dt: float) -> void:
	shake = maxf(0.0, shake - dt)
	roll = maxf(0.0, roll - dt)
	cam.offset = Vector2(randf_range(-3, 3), randf_range(-3, 3)) if shake > 0.0 else Vector2.ZERO
	cam.rotation = deg_to_rad(5.0) * (roll / 0.45) if roll > 0.0 else 0.0
	for s in sparks:
		s[1] -= dt
	sparks = sparks.filter(func(s): return s[1] > 0.0)

func _draw_fx() -> void:
	for s in sparks:
		var k: float = s[1] / 0.14
		var pts := PackedVector2Array()
		for i in 16:
			var r := (14.0 if i % 2 == 0 else 6.0) * (1.4 - k * 0.4)
			pts.append(s[0] + Vector2.from_angle(i * TAU / 16.0) * r)
		fx.draw_colored_polygon(pts, Color(1, 0.95, 0.6, k))
	if show_boxes:
		for f in [bolt, rivet]:
			fx.draw_rect(f.hurtbox(), Color(0.1, 0.9, 0.3), false, 1.0)
			var ab: Rect2 = f.attack_box()
			if ab.has_area():
				fx.draw_rect(ab, Color(1, 0.2, 0.2), false, 1.0)
		for c in corks:
			if is_instance_valid(c):
				fx.draw_rect(Rect2(c.position - Vector2(5, 5), Vector2(10, 10)), Color(1, 0.2, 0.2), false, 1.0)
