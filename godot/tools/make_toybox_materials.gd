extends SceneTree
## A5: writes the two ShaderMaterials that share painted_tin.gdshader
## (CHANGE-BRIEF A5.5). Written by Claude. Built in code so ResourceSaver
## writes the resource UIDs; none is typed by hand.
##   godot --headless --path godot --script res://tools/make_toybox_materials.gd
## Both bind the same three textures; they differ in two values only. Every
## other uniform is left unset, so the shader's default applies.

const SHADER := "res://shaders/painted_tin.gdshader"
const TEX := "res://assets/textures/metal_plate/metal_plate_%s_1k.png"
const OUT := "res://prop_room/materials/"
const MATERIALS := {
	"toybox_fresh": {"wear_amount": 0.05, "paint_roughness": 0.30},   # "fresh from the shop"
	"toybox_worn": {"wear_amount": 0.55, "paint_roughness": 0.70},    # "a hundred rounds later"
}

func _initialize() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
	var failures := 0
	for name in MATERIALS:
		var m := ShaderMaterial.new()
		m.resource_name = name
		m.shader = load(SHADER)
		m.set_shader_parameter("metal_albedo", load(TEX % "diff"))
		m.set_shader_parameter("metal_normal", load(TEX % "nor_gl"))
		m.set_shader_parameter("metal_rough", load(TEX % "rough"))
		for k in MATERIALS[name]:
			m.set_shader_parameter(k, MATERIALS[name][k])
		var err := ResourceSaver.save(m, OUT + name + ".tres")
		print("saved %s%s.tres (err %d)" % [OUT, name, err])
		if err != OK:
			failures += 1
	quit(failures)
