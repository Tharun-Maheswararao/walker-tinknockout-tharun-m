class_name Fighter
extends Node2D
## One tin wind-up fighter (Bolt or Rivet).
##
## Gameplay only: state machine, spring (wind), health, hitboxes. It never plays
## or queries audio. Everything a sound or effect needs is EMITTED as a signal,
## and audio/sfx.gd listens. Muting or deleting the audio nodes cannot change
## what happens here (TEST-REPORT: "muted run == unmuted run").
##
## A controller (player input or rivet_brain.gd) writes `intent` every physics
## frame. Positions are the fighter's FEET; +x is the facing direction.

signal state_changed(fighter: Fighter, old_state: int, new_state: int)
signal hit_landed(attacker: Fighter, attack: String, blocked: bool)
signal projectile_fired(fighter: Fighter)
signal rewind_tick(fighter: Fighter)
signal wind_changed(fighter: Fighter, wind: float)

enum S { IDLE, WALK, JAB, CUTLASS, POP, BLOCK, REWIND, HURT, EMPTY, KO, WIN }
const POSE := {
	S.IDLE: "idle", S.WALK: "walk", S.JAB: "jab", S.CUTLASS: "cutlass", S.POP: "pop",
	S.BLOCK: "block", S.REWIND: "rewind", S.HURT: "hurt", S.EMPTY: "empty", S.KO: "ko", S.WIN: "win",
}

# ---- tuning (one place; TEST-REPORT quotes these) ----
const MAX_HP := 100.0
const MAX_WIND := 100.0
const SPEED := 110.0              # px/s walking
const WALK_DRAIN := 3.0           # wind/s while walking: even moving unwinds the spring
const CRANK_DEG_PER_S := 360.0    # rewind speed
const WIND_PER_CLICK := 10.0      # one ratchet click = one quarter-turn = 10 wind
const HURT_TIME := 0.32
const KNOCKDOWN_TIME := 0.80      # hit while rewinding or empty
const EMPTY_TIME := 1.60          # stalled, defenceless
const VULNERABLE_MULT := 1.5
const BLOCK_CHIP := 0.2
const HITSTOP := 0.07
const HURTBOX := Vector2(50, 106) # CHARACTER-SHEET: bottom-centred on the feet

## Attack table. Times in seconds; box = hitbox relative to the feet, facing right.
const ATTACKS := {
	S.JAB: {"name": "jab", "cost": 12.0, "startup": 0.07, "active": 0.10, "recovery": 0.18, "dmg": 7.0, "box": Rect2(24, -76, 30, 22), "push": 40.0},
	S.CUTLASS: {"name": "cutlass", "cost": 22.0, "startup": 0.14, "active": 0.12, "recovery": 0.30, "dmg": 13.0, "box": Rect2(20, -98, 58, 40), "push": 70.0},
	S.POP: {"name": "pop", "cost": 30.0, "startup": 0.10, "active": 0.0, "recovery": 0.35, "dmg": 10.0, "push": 50.0},
}

@export var skin := "bolt"
var hp := MAX_HP
var wind := MAX_WIND
var state: int = S.IDLE
var state_t := 0.0
var facing := 1
var opponent: Fighter
var arena_min := 40.0
var arena_max := 600.0
var intent := {"move": 0, "jab": false, "cutlass": false, "pop": false, "block": false, "rewind": false}
var has_hit := false              # the current attack instance already connected
var crank_deg := 0.0
var hitstop := 0.0
var stun := 0.0
var push_v := 0.0
var spawn_cork: Callable          # set by main: func(fighter) -> spawns projectile

var sprite: Sprite2D
var key_sprite: Sprite2D
var weapon: Sprite2D
var textures := {}
var anchors := {}
var key_spin := 0.0

func _ready() -> void:
	sprite = Sprite2D.new()
	sprite.centered = false   # offset = -FEET puts the feet on the node origin (was double-shifted when centred)
	add_child(sprite)
	key_sprite = Sprite2D.new()
	key_sprite.z_index = -1   # behind the body, as on the toy
	add_child(key_sprite)
	weapon = Sprite2D.new()
	weapon.centered = false
	add_child(weapon)
	_load_art()
	_apply_pose()

func _load_art() -> void:
	var base := "res://assets/fighters/%s/" % skin
	for st in POSE:
		var p: String = base + POSE[st] + ".png"
		if ResourceLoader.exists(p):
			textures[st] = load(p)
	var f := FileAccess.open("res://assets/fighters/anchors.json", FileAccess.READ)
	if f:
		anchors = JSON.parse_string(f.get_as_text())
	var kp := "res://assets/props/key-%s.png" % skin
	if ResourceLoader.exists(kp):
		key_sprite.texture = load(kp)

func reset(x: float, face: int) -> void:
	position.x = x
	facing = face
	hp = MAX_HP
	wind = MAX_WIND
	has_hit = false
	crank_deg = 0.0
	hitstop = 0.0
	push_v = 0.0
	_enter(S.IDLE)
	wind_changed.emit(self, wind)

func is_out() -> bool:
	return state == S.KO

func hurtbox() -> Rect2:
	if state == S.KO:
		return Rect2()
	return Rect2(position.x - HURTBOX.x / 2, position.y - HURTBOX.y, HURTBOX.x, HURTBOX.y)

func attack_box() -> Rect2:
	if not ATTACKS.has(state) or not ATTACKS[state].has("box"):
		return Rect2()
	var a: Dictionary = ATTACKS[state]
	if state_t < a.startup or state_t >= a.startup + a.active:
		return Rect2()
	var b: Rect2 = a.box
	var x := position.x + (b.position.x if facing > 0 else -b.position.x - b.size.x)
	return Rect2(x, position.y + b.position.y, b.size.x, b.size.y)

# ------------------------------------------------------------------ simulation
func step(dt: float) -> void:
	if hitstop > 0.0:
		hitstop -= dt
		return
	state_t += dt
	if push_v != 0.0:
		position.x += push_v * dt
		push_v = move_toward(push_v, 0.0, 400.0 * dt)
	match state:
		S.IDLE, S.WALK:
			_neutral(dt)
		S.JAB, S.CUTLASS, S.POP:
			_attack(dt)
		S.BLOCK:
			if not intent.block:
				_enter(S.IDLE)
		S.REWIND:
			_rewind(dt)
		S.HURT:
			if state_t >= stun:
				_enter(S.IDLE)   # never back into EMPTY: that chained into an unescapable stun-lock (film dry run)
		S.EMPTY:
			if state_t >= EMPTY_TIME:
				_enter(S.IDLE)
		S.KO, S.WIN:
			pass
	position.x = clampf(position.x, arena_min, arena_max)
	_apply_pose()

func _neutral(dt: float) -> void:
	if intent.rewind:
		_enter(S.REWIND)
		return
	if intent.block:
		_enter(S.BLOCK)
		return
	for st in [S.JAB, S.CUTLASS, S.POP]:
		if intent[ATTACKS[st].name] and wind > 0.0:
			_spend(ATTACKS[st].cost)
			_enter(st)
			return
	var mv: int = intent.move
	if mv != 0 and wind <= 0.0:
		mv = 0                 # a run-down toy can't walk: at 0 wind the only option is to rewind
	if mv != 0:
		facing = mv            # orientation follows input (left art = runtime flip)
		position.x += mv * SPEED * dt
		_spend(WALK_DRAIN * dt)
		if wind <= 0.0:
			_enter(S.EMPTY)
			return
		if state != S.WALK:
			_enter(S.WALK)
	elif state != S.IDLE:
		_enter(S.IDLE)

func _attack(_dt: float) -> void:
	var a: Dictionary = ATTACKS[state]
	if state == S.POP:
		if not has_hit and state_t >= a.startup:
			has_hit = true      # here: "has fired", one cork per press
			projectile_fired.emit(self)
			if spawn_cork.is_valid():
				spawn_cork.call(self)
	elif not has_hit and opponent:
		var box := attack_box()
		if box.has_area() and box.intersects(opponent.hurtbox()):
			has_hit = true       # first overlapping frame only: one hit per swing (F2)
			var blocked := opponent.receive_hit(self, a.dmg, a.push)
			hit_landed.emit(self, a.name, blocked)
			hitstop = HITSTOP
	if state_t >= a.startup + a.active + a.recovery:
		_enter(S.EMPTY if wind <= 0.0 else S.IDLE)

func _rewind(dt: float) -> void:
	if not intent.rewind:
		_enter(S.IDLE)
		return
	if wind >= MAX_WIND:
		return                  # full: the key stops turning, no more clicks
	crank_deg += CRANK_DEG_PER_S * dt
	while crank_deg >= 90.0 and wind < MAX_WIND:
		crank_deg -= 90.0
		wind = minf(MAX_WIND, wind + WIND_PER_CLICK)
		wind_changed.emit(self, wind)
		rewind_tick.emit(self)
	key_spin = crank_deg

## Called by the attacker (melee) or a cork. Returns true if blocked.
func receive_hit(attacker: Node2D, dmg: float, push: float) -> bool:
	if state == S.KO or state == S.WIN:
		return false
	var from := signf(attacker.position.x - position.x)
	if from == 0.0:
		from = -facing
	var blocked := state == S.BLOCK and int(from) == facing
	if blocked:
		hp -= dmg * BLOCK_CHIP
		push_v = -from * push * 0.5
	else:
		var vulnerable := state == S.REWIND or state == S.EMPTY
		hp -= dmg * (VULNERABLE_MULT if vulnerable else 1.0)
		stun = KNOCKDOWN_TIME if vulnerable else HURT_TIME
		push_v = -from * push * (1.6 if vulnerable else 1.0)
		_enter(S.HURT)
	hitstop = HITSTOP
	if hp <= 0.0:
		hp = 0.0
		_enter(S.KO)
	return blocked

func win() -> void:
	_enter(S.WIN)

func _spend(amount: float) -> void:
	wind = maxf(0.0, wind - amount)
	wind_changed.emit(self, wind)

func _enter(s: int) -> void:
	var old := state
	state = s
	state_t = 0.0
	if ATTACKS.has(s):
		has_hit = false
	if s == S.REWIND:
		crank_deg = 0.0
	if old != s:
		state_changed.emit(self, old, s)   # edge-triggered: same-state re-entry never emits

# ------------------------------------------------------------------ presentation
## where the hand holds each weapon, in the weapon texture's pixels (hilt / grip)
const GRIP := {"cutlass": Vector2(-12, -38), "popgun": Vector2(-26, -58)}
const ART_SCALE := 1.0 / 3.0   # sprites are stored at 3x game size (Bolt = 336 px)
const FEET := Vector2(240, 435) # feet anchor inside every 480x450 sprite canvas

func _apply_pose() -> void:
	if textures.has(state):
		sprite.texture = textures[state]
	sprite.scale = Vector2(ART_SCALE * facing, ART_SCALE)
	sprite.offset = -FEET
	var pa: Dictionary = anchors.get(POSE[state], {})
	var k: Array = pa.get("key", [-42, -50])
	key_sprite.position = Vector2(k[0] * facing, k[1])
	# a key spinning about the body axis, seen in profile, looks like it narrows and widens
	var spin := cos(deg_to_rad(key_spin * 2.0)) if state == S.REWIND else 1.0
	key_sprite.scale = Vector2(ART_SCALE * facing * maxf(0.15, absf(spin)), ART_SCALE)
	key_sprite.visible = key_sprite.texture != null and state != S.KO
	var wname := ""
	if state == S.CUTLASS:
		wname = "cutlass"
	elif state == S.POP:
		wname = "popgun"
	weapon.visible = wname != ""
	if weapon.visible:
		var wp := "res://assets/props/%s.png" % wname
		if ResourceLoader.exists(wp):
			weapon.texture = load(wp)
		var h: Array = pa.get("hand", [30, -60])
		weapon.position = Vector2(h[0] * facing, h[1])
		weapon.offset = GRIP[wname]
		weapon.scale = Vector2(ART_SCALE * facing, ART_SCALE)
		weapon.rotation = deg_to_rad(pa.get("weapon_deg", 0.0)) * facing
