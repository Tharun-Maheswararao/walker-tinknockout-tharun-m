extends SceneTree
## A5 hint experiment (CHANGE-BRIEF A5.4): builds the two materials and the
## scene that shows them. Written by Claude; the shader is Tharun's.
##   godot --headless --path godot --script res://tools/make_hint_scene.gd
## Both materials bind the SAME 3x1 grey PNG to both samplers. Only the bool
## differs, so the only variable is which sampler (source_color or not) writes
## ALBEDO. Environment values use Godot's named constants, not typed integers.

const SHADER := "res://shaders/hint_experiment.gdshader"
const PNG := "res://assets/textures/hint/hint_greys_3x1.png"
const DIR := "res://hint_experiment/"

func _initialize() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(DIR))
	var tex: Texture2D = load(PNG)
	var mats := {}
	for use_colour in [true, false]:
		var name := "hint_source_color" if use_colour else "hint_data"
		var m := ShaderMaterial.new()
		m.resource_name = name
		m.shader = load(SHADER)
		m.set_shader_parameter("grey_as_colour", tex)
		m.set_shader_parameter("grey_as_data", tex)
		m.set_shader_parameter("use_colour_sampler", use_colour)
		ResourceSaver.save(m, DIR + name + ".tres")
		mats[use_colour] = load(DIR + name + ".tres")

	var scene := Node3D.new()
	scene.name = "HintExperiment"

	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.1, 0.1, 0.1)
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR   # Linear tonemap ...
	env.tonemap_exposure = 1.0                           # ... at exposure 1.0
	env.glow_enabled = false
	env.fog_enabled = false
	env.volumetric_fog_enabled = false
	env.adjustment_enabled = false
	var we := WorldEnvironment.new()
	we.name = "WorldEnvironment"
	we.environment = env
	_add(scene, we)

	var cam := Camera3D.new()
	cam.name = "Camera3D"
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = 2.6                                       # both 3x1 quads fit vertically
	cam.position = Vector3(0, 0, 5)
	cam.current = true
	_add(scene, cam)

	# Quad S (top): source_color sampler. Quad D (bottom): data sampler.
	for q in [["Quad_S_source_color", true, 0.6], ["Quad_D_data", false, -0.6]]:
		var mi := MeshInstance3D.new()
		mi.name = q[0]
		var quad := QuadMesh.new()
		quad.size = Vector2(3, 1)                        # one 1x1 band per texel
		mi.mesh = quad
		mi.material_override = mats[q[1]]
		mi.position = Vector3(0, q[2], 0)
		_add(scene, mi)

	var ps := PackedScene.new()
	var err := ps.pack(scene)
	err = err if err != OK else ResourceSaver.save(ps, DIR + "hint_experiment.tscn")
	print("tonemap_mode %d (TONE_MAPPER_LINEAR = %d), exposure %.1f; saved %shint_experiment.tscn (err %d)" % [env.tonemap_mode, Environment.TONE_MAPPER_LINEAR, env.tonemap_exposure, DIR, err])
	scene.free()
	quit(err)

func _add(parent: Node, child: Node) -> void:
	parent.add_child(child)
	child.owner = parent
