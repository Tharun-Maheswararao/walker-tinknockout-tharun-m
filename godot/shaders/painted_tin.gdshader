shader_type spatial;

uniform sampler2D metal_albedo : source_color, filter_linear_mipmap, repeat_enable;
uniform sampler2D metal_normal : hint_normal, filter_linear_mipmap, repeat_enable;
uniform sampler2D metal_rough : filter_linear_mipmap, repeat_enable;

group_uniforms paint;
uniform vec4 paint_color : source_color = vec4(0.710, 0.188, 0.165, 1.0);
uniform float paint_roughness : hint_range(0.0, 1.0) = 0.35;
group_uniforms metal;
uniform float wear_amount : hint_range(0.0, 1.0) = 0.1;
uniform float normal_depth : hint_range(0.0, 2.0) = 1.0;
uniform float uv_scale : hint_range(0.5, 8.0) = 2.5;
group_uniforms;

void fragment() {
	vec2 uv = UV * uv_scale;
	vec3 metal = texture(metal_albedo, uv).rgb;
	float rough = texture(metal_rough, uv).r;
	float wear = step(1.0 - wear_amount, rough);
	ALBEDO = mix(paint_color.rgb, metal, wear);
	ROUGHNESS = mix(paint_roughness, rough, wear);
	NORMAL_MAP = texture(metal_normal, uv).rgb;
	NORMAL_MAP_DEPTH = normal_depth;
}
