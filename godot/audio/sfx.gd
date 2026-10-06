extends Node
## Event sounds. LISTENS to gameplay signals and plays one sound per event.
## Gameplay never calls this node. `counts` records every trigger (also while
## muted) so tests can assert exactly one sound per event (CHANGE-BRIEF F2, F5).

const FILES := {
	"bell": "res://assets/sfx/bell.ogg",
	"jab": "res://assets/sfx/jab.ogg",
	"cutlass": "res://assets/sfx/cutlass.ogg",
	"pop": "res://assets/sfx/pop.ogg",
	"rewind": "res://assets/sfx/rewind.ogg",
	"empty": "res://assets/sfx/empty.ogg",
}
var players := {}
var counts := {}
var log: Array = []   # [frame, name] - test evidence

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	for n in FILES:
		counts[n] = 0
		var p := AudioStreamPlayer.new()
		p.bus = &"SFX"
		p.max_polyphony = 4
		if ResourceLoader.exists(FILES[n]):
			p.stream = load(FILES[n])
		add_child(p)
		players[n] = p

func watch(f: Fighter) -> void:
	f.hit_landed.connect(func(_a, attack, blocked): play(attack if attack != "pop" else "jab", 0.8 if blocked else 1.0))
	f.projectile_fired.connect(func(_f): play("pop"))
	f.rewind_tick.connect(func(_f): play("rewind", 1.0 + 0.04 * (_f.wind / 100.0)))
	f.state_changed.connect(func(_f, _old, new_state):
		if new_state == Fighter.S.EMPTY:
			play("empty"))

func watch_cork(c: Node) -> void:
	c.struck.connect(func(_c, blocked): play("jab", 1.25 if not blocked else 1.0))

func play(n: String, pitch := 1.0) -> void:
	counts[n] += 1
	log.append([Engine.get_physics_frames(), n])
	var p: AudioStreamPlayer = players[n]
	if p.stream:
		p.pitch_scale = pitch
		p.play()
