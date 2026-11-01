shader_type spatial;
render_mode unshaded;

uniform sampler2D grey_as_colour : source_color, filter_nearest;
uniform sampler2D grey_as_data : filter_nearest;

uniform bool use_colour_sampler = true;

void fragment() {
	if (use_colour_sampler) {
		ALBEDO = texture(grey_as_colour, UV).rgb;
	} else {
		ALBEDO = texture(grey_as_data, UV).rgb;
	}
}
