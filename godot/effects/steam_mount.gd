class_name SteamMount
extends Node2D
## Holds Effect B (wind_steam.tscn) on a fighter at the key: the key's position,
## facing and visibility, and its z_index (behind the body), but NOT the key's
## REWIND spin squash (fighter.gd:272-273). Parented to the key itself, every live
## puff narrowed to 15 % width with the spinning key, about eight times a second,
## which read in game as "the steam cut out on rewind" (TUNING.md, Effect B r0).
## Presentation only: it reads the fighter, never writes it, and sets no effect values.

var fighter: Fighter

## Adds a mount to `f` with one instance of `scene` on it; returns the steam.
static func attach(f: Fighter, scene: PackedScene) -> GPUParticles2D:
	var m := SteamMount.new()
	m.name = "SteamMount"
	m.fighter = f
	f.add_child(m)
	var steam: GPUParticles2D = scene.instantiate()
	m.add_child(steam)
	return steam

func _ready() -> void:
	z_index = fighter.key_sprite.z_index
	follow()

## Runs after the fighter's step() each tick: Main (or a fixture) is the parent,
## so its _physics_process, which steps the fighter, runs first.
func _physics_process(_delta: float) -> void:
	follow()

func follow() -> void:
	var key := fighter.key_sprite
	position = key.position
	scale = Vector2(Fighter.ART_SCALE * fighter.facing, Fighter.ART_SCALE)
	visible = key.visible
