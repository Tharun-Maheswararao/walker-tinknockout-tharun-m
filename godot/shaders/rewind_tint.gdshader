shader_type canvas_item;

uniform float rewind_amount : hint_range(0.0, 1.0) = 0.0;
uniform vec4 tint_color : source_color = vec4(0.353, 0.627, 1.0, 1.0);
uniform float tint_strength : hint_range(0.0, 1.0) = 0.5;

void fragment() {
	COLOR.rgb = mix(COLOR.rgb, tint_color.rgb, rewind_amount * tint_strength);
}
