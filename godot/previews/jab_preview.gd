extends Node2D
## Jab preview, a FIXTURE (CHANGE-BRIEF.md §9). Not part of the game. Written by Claude.
## Capture (Tharun runs it: it needs a window), at 60 fps so every phase boundary
## of the 60 fps phase table is a drawn frame:
##   godot --path godot res://previews/jab_preview.tscn --write-movie <abs>/frame.png --fixed-fps 60 --disable-vsync --always-on-top --quit-after 35
##
## The arena background and camera exactly as main.gd sets them (main.gd:42-51), and
## the real Fighter (fighter.gd, with its rig, players and clips) standing at x 207,
## inside the light castle stretch x 192-223 (design/a6/BRIEF-FACTS.md §4), facing
## right, wind full, nobody else on screen. Its intent is SCRIPTED (no keyboard):
## the jab is requested on physics tick 10, so the state becomes JAB on tick 10,
## and at --fixed-fps 60 tick N is capture frame N. The script steps the fighter
## once per physics tick, as main.gd's _simulate does, and prints one log line per
## tick ("frame N ...") so each capture frame can be read beside its state, state_t,
## clip time and rig pose.
##
## Frames to read (CHANGE-BRIEF.md §9): 10 entry, 13 coil peak, 14 last startup,
## 15 active onset, 20 last active, 21 recovery onset, 31 back to IDLE.
##
## For watching, never for captures (after `--`):
##   --loop    re-requests the jab every 45 ticks (0.75 s), wind refilled each time
##   --boxes   draws the hurtbox (green) and the live attack box (red), as F1 does in game
##   --left    stands Bolt facing left at x 433 (mirror check)
##   godot --path godot res://previews/jab_preview.tscn -- --loop [--boxes] [--left]
## Slow motion: add the engine flag --time-scale 0.25 before `--`.

const TRIGGER := 10
const LOOP_TICKS := 45

var bolt: Fighter
var tick := 0
var args := OS.get_cmdline_user_args()
var loop := "--loop" in args
var boxes := "--boxes" in args
var left := "--left" in args
var overlay: Node2D

func _ready() -> void:
	var cam := Camera2D.new()
	cam.position = Vector2(320, 180)          # main.gd:43
	add_child(cam)
	var bg := Sprite2D.new()                  # main.gd:45-51
	bg.centered = false
	bg.z_index = -10
	bg.texture = load("res://assets/env/bowl.png")
	bg.scale = Vector2(640.0 / bg.texture.get_width(), 360.0 / bg.texture.get_height())
	add_child(bg)
	bolt = Fighter.new()
	bolt.skin = "bolt"
	add_child(bolt)
	bolt.reset(433.0 if left else 207.0, -1 if left else 1)
	bolt.position.y = 292.0                   # FLOOR_Y, main.gd:12
	overlay = Node2D.new()
	overlay.z_index = 5
	overlay.draw.connect(_draw_boxes)
	add_child(overlay)
	print("jab_preview: FIXTURE, scripted intent; Bolt at x %d facing %+d; jab requested on tick %d%s" % [bolt.position.x, bolt.facing, TRIGGER, ", looping every %d ticks" % LOOP_TICKS if loop else ""])

func _physics_process(dt: float) -> void:
	var fire := tick == TRIGGER or (loop and tick > TRIGGER and (tick - TRIGGER) % LOOP_TICKS == 0)
	if fire:
		bolt.wind = Fighter.MAX_WIND          # fixture: keep the jab available
	bolt.intent = {"move": 0, "jab": fire, "cutlass": false, "pop": false, "block": false, "rewind": false}
	bolt.step(dt)
	var fa: AnimationPlayer = bolt.fighter_anim
	print("frame %3d  %-5s state_t %.4f  clip %s %.4f  x %6.2f  rot %6.3f  keybob %5.2f  box %s" % [tick,
		Fighter.S.keys()[bolt.state], bolt.state_t,
		"jab_action" if fa.current_animation != &"" else "-         ",
		fa.current_animation_position if fa.current_animation != &"" else 0.0,
		bolt.body_pivot.position.x, bolt.body_pivot.rotation, bolt.key_bob.position.y,
		"LIVE" if bolt.attack_box().has_area() else "-"])
	overlay.queue_redraw()
	tick += 1

func _draw_boxes() -> void:
	if not boxes:
		return
	overlay.draw_rect(bolt.hurtbox(), Color(0.1, 0.9, 0.3), false, 1.0)
	var ab := bolt.attack_box()
	if ab.has_area():
		overlay.draw_rect(ab, Color(1, 0.2, 0.2), false, 1.0)
