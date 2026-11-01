extends SceneTree
var frames := 0
var phys := 0
var t := 0.0
func _initialize() -> void:
	print("driver=", RenderingServer.get_current_rendering_driver_name(), " method=", RenderingServer.get_current_rendering_method())
	var sh := Shader.new()
	sh.code = "shader_type canvas_item;\nuniform float amt : hint_range(0.0, 1.0) = 0.25;\nuniform vec4 tint : source_color = vec4(0.2, 0.4, 0.6, 1.0);\nvoid fragment() { COLOR.rgb = mix(COLOR.rgb, tint.rgb, amt); }"
	var ul := sh.get_shader_uniform_list()
	print("uniform list: ", ul.map(func(u): return "%s type=%d hint=%d hint_string=%s" % [u.name, u.type, u.hint, u.hint_string]))
	print("RS default amt=", RenderingServer.shader_get_parameter_default(sh.get_rid(), "amt"), " tint=", RenderingServer.shader_get_parameter_default(sh.get_rid(), "tint"))
	var broken := Shader.new()
	broken.code = "shader_type canvas_item;\nuniform float amt : hint_range(0.0, 1.0) = 0.25\nvoid fragment() { }"
	print("broken shader (missing semicolon) uniform list: ", broken.get_shader_uniform_list())
	var m := ShaderMaterial.new()
	m.shader = sh
	print("material get before set: ", m.get_shader_parameter("amt"))
	m.set_shader_parameter("amt", 2.0)
	print("set 2.0 (hint_range 0..1) -> readback ", m.get_shader_parameter("amt"))
	m.set_shader_parameter("not_declared", 0.7)
	print("undeclared name -> readback ", m.get_shader_parameter("not_declared"))
	var dup := m.duplicate() as ShaderMaterial
	print("duplicate shares shader: ", dup.shader == m.shader, " separate material: ", dup != m)
	process_frame.connect(func(): frames += 1)
	physics_frame.connect(func(): phys += 1)
func _process(delta: float) -> bool:
	t += delta
	if frames >= 288:
		print("fixed-fps run: frames=", frames, " physics ticks=", phys, " game time=%.4f" % t, " last delta=%.6f" % delta, " physics_ticks_per_second=", Engine.physics_ticks_per_second)
		return true
	return false
