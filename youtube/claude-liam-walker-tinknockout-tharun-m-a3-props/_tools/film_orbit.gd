# Film tool (not part of the game). Copied into an ISOLATED copy of commit 1d93dcb as
# res://film_orbit.gd and run under Godot Movie Maker:
#   godot --path <copy>/godot --resolution 3840x2160 --write-movie orbit/frame.png --fixed-fps 30 \
#         --script res://film_orbit.gd
# It loads the unchanged prop_room.tscn, holds the scene's own saved Camera3D for HOLD
# frames, then moves that same camera on a circle around the props. It never touches the
# props, the light, the floor or any resource, and it writes nothing back to the project.
extends SceneTree

const HOLD := 120          # 4 s on the saved camera
const ORBIT := 720         # 24 s for one full turn
const CENTRE := Vector3(0.0, 0.9, 0.0)   # the point shot_prop_views.gd's front_wide view looks at
const RADIUS := 5.5        # the saved camera's distance (z = 5.5)
const HEIGHT := 1.6        # the saved camera's height

var cam: Camera3D
var f := 0

func _initialize() -> void:
	var room: Node3D = (load("res://prop_room/prop_room.tscn") as PackedScene).instantiate()
	root.add_child(room)
	cam = room.get_node("Camera3D")
	print("FILM saved camera ", cam.transform)

func _process(_delta: float) -> bool:
	if f >= HOLD:
		var a := TAU * float(f - HOLD) / ORBIT
		var pos := Vector3(RADIUS * sin(a), HEIGHT, RADIUS * cos(a))
		cam.transform = Transform3D(Basis.IDENTITY, pos).looking_at(CENTRE, Vector3.UP)
	f += 1
	return f >= HOLD + ORBIT
