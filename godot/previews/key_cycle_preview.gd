extends Node2D
## Key-cycle preview, a FIXTURE (A7 Use It: the cycle seam, registration and the
## backgrounds; CHANGE-BRIEF.md §3, A-R3). Not part of the game. Written by Claude.
##
## The arena background and camera as main.gd sets them, and the real Fighter (its
## rig, KeyAnimPlayer and wind_key_cycle) held in REWIND for as long as it runs. Its
## intent is SCRIPTED (rewind held from tick 10), and its wind is topped back to 50
## every tick so it never reaches full wind: the key turns without stopping, one
## turn per second, so five wraps take five seconds. In the game a single rewind
## reaches full wind after at most ten clicks (2.5 turns) and the key then holds
## (CHANGE-BRIEF.md §3), which is why the seam is watched here.
##   watch:    godot --path godot res://previews/key_cycle_preview.tscn [-- --dark]
##   strip:    godot --path godot res://previews/key_cycle_preview.tscn --write-movie <abs>/frame.png --fixed-fps 60 --disable-vsync --always-on-top --quit-after 80
##             (rewind starts on frame 10; the key shows cell k from about frame 10 + 7.5 k)
## Options after `--`:
##   --dark    stands Bolt at x 271, over the darkest stretch x 256-287 (default x 207,
##             the lightest stretch x 192-223; design/a6/BRIEF-FACTS.md §4)
##   --zoom    camera zoom 3 on the key, for judging registration by eye
## One log line per tick: frame, state, state_t, the key's frame.

const START := 10

var bolt: Fighter
var tick := 0
var args := OS.get_cmdline_user_args()
var last_frame := -1
var wraps := 0

func _ready() -> void:
	var cam := Camera2D.new()
	cam.position = Vector2(320, 180)          # main.gd:43
	add_child(cam)
	var bg := Sprite2D.new()
	bg.centered = false
	bg.z_index = -10
	bg.texture = load("res://assets/env/bowl.png")
	bg.scale = Vector2(640.0 / bg.texture.get_width(), 360.0 / bg.texture.get_height())
	add_child(bg)
	bolt = Fighter.new()
	bolt.skin = "bolt"
	add_child(bolt)
	bolt.reset(271.0 if "--dark" in args else 207.0, 1)
	bolt.position.y = 292.0
	if "--zoom" in args:
		await get_tree().process_frame
		cam.position = bolt.key_sprite.global_position
		cam.zoom = Vector2(3, 3)
	print("key_cycle_preview: FIXTURE, scripted rewind from tick %d, wind topped to 50 each tick; Bolt at x %d" % [START, bolt.position.x])

func _physics_process(dt: float) -> void:
	if tick >= START:
		bolt.wind = 50.0                      # fixture: never reaches full wind, so the key keeps turning
	bolt.intent = {"move": 0, "jab": false, "cutlass": false, "pop": false, "block": false, "rewind": tick >= START}
	bolt.step(dt)
	var f: int = bolt.key_sprite.frame
	if last_frame == 7 and f == 0:
		wraps += 1
	last_frame = f
	print("frame %3d  %-6s state_t %.4f  key frame %d  wraps %d" % [tick, Fighter.S.keys()[bolt.state], bolt.state_t, f, wraps])
	tick += 1
