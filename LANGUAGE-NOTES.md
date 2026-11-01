# LANGUAGE-NOTES: the Godot shading language (Assignment 5, Step 4)

*Headings and questions copied from the Assignment 5 handout by Claude. Every answer and every line reference is mine (Tharun), in my own words. The agent only checked that my line references point where I say.*

My three shaders: `godot/shaders/rewind_tint.gdshader`, `godot/shaders/painted_tin.gdshader`, `godot/shaders/hint_experiment.gdshader`.
Generated shader: `godot/shaders/standard_generated.gdshader`, converted in the editor from a StandardMaterial3D with my Metal Plate albedo, normal and roughness textures.

## Part A: line numbers in `standard_generated.gdshader`

| What | Line(s) |
|---|---|
| `shader_type` | Line 3 (shader_type spatial;) |
| `render_mode` | Line 4 (render_mode blend_mix, depth_draw_opaque, cull_back, diffuse_burley, specular_schlick_ggx;) |
| The uniform for the Inspector's albedo colour | Line 6 (uniform vec4 albedo : source_color;) |
| The uniform for the Inspector's normal-map strength | Line 20 (uniform float normal_scale : hint_range(-16.0, 16.0);) |
| The albedo sampler, and its hints | Line 7 (uniform sampler2D texture_albedo : source_color, filter_linear_mipmap, repeat_enable;) |
| The normal-map sampler, and its hints | Line 19 (uniform sampler2D texture_normal : hint_roughness_normal, filter_linear_mipmap, repeat_enable;) |
| The line that writes `ALBEDO` | Line 35 (ALBEDO = albedo.rgb * albedo_tex.rgb;) |
| The line that writes `ROUGHNESS` | Line 43 (ROUGHNESS = roughness_tex * roughness;) |
| The line that writes `NORMAL_MAP` | Line 46 (NORMAL_MAP = texture(texture_normal, base_uv).rgb;) |

## Part B: questions (each answer cites a line of one of my three shaders)

### 1. What does `shader_type` decide? Answer for each type you used, citing the first line of each shader.
shader_type determines the rendering pipeline, available built-in variables, and supported render modes. I used shader_type canvas_item; (godot/shaders/rewind_tint.gdshader:1) for 2D screen/sprite rendering, and shader_type spatial; (godot/shaders/painted_tin.gdshader:1 and godot/shaders/hint_experiment.gdshader:1) for 3D mesh rendering.

### 2. Which processor functions did you write, and when does each run? What would change if you moved your colour line into `vertex()`, and why?
I wrote fragment() (e.g., godot/shaders/rewind_tint.gdshader:7), which runs once per pixel during rasterization. If I moved the colour tinting arithmetic into vertex(), which runs once per mesh vertex, the effect would interpolate linearly across triangle faces rather than operating per-pixel, resulting in blocky or distorted gradients on low-poly meshes.

### 3. Name three built-ins you read and two you wrote. Which of the ones you read are read-only?
Read: My shaders read only two built-ins—COLOR (godot/shaders/rewind_tint.gdshader:8) and UV (godot/shaders/painted_tin.gdshader:17).

Written: COLOR (godot/shaders/rewind_tint.gdshader:8) and ALBEDO (godot/shaders/painted_tin.gdshader:21).

Read-only status: UV is strictly read-only per pixel, whereas COLOR can be both read and written in a canvas_item fragment shader.

### 4. For each hint you used, does it change only the Inspector, or also the value the shader receives? Cite your hint experiment.
Hints like source_color (godot/shaders/hint_experiment.gdshader:4) change both the Inspector UI and the value the shader receives by automatically triggering an sRGB-to-linear conversion upon sampling. As demonstrated in hint_experiment.gdshader, Quad_S with source_color received decoded values (showing 64) while Quad_D without it received raw linear values (showing 137). In contrast, hint_range and group_uniforms change only the Inspector UI.

### 5. Does `hint_range` clamp a value set from code? Cite what you observed.
No, hint_range only constrains the UI slider in the Inspector. As observed in evidence/a5/captures/pixel-samples.txt when passing 2.0 via code to rewind_amount (declared at godot/shaders/rewind_tint.gdshader:3), the pixels became exactly the tint (90, 160, 255), proving the uniform received and processed 2.0 without being clamped.

### 6. Which line of the generated shader makes the albedo sample as colour and the normal map as data, and what is the equivalent line in your textured shader?
In standard_generated.gdshader, line 7 (uniform sampler2D texture_albedo : source_color...) handles colour conversion, and line 19 (uniform sampler2D texture_normal : hint_roughness_normal...) handles normal data. The equivalents in painted_tin.gdshader are line 3 (metal_albedo with source_color) and line 4 (metal_normal with hint_normal).

### 7. Your `fragment()` runs for every pixel at once. Why can't it read what the neighbouring pixel's `fragment()` is computing, and how does game state reach it instead?
GPUs execute fragments in parallel across independent threads with no guaranteed execution order or shared local memory between adjacent threads, preventing direct neighbor reads. Game state reaches the shader instead via uniforms (uniform float..., uniform vec4... in godot/shaders/rewind_tint.gdshader:3-4) set globally from CPU-side GDScript.

### 8. Name two things the Godot shading language provides that plain GLSL does not, or makes you write yourself.
Godot Shading Language automatically handles uniform bindings, texture unit descriptor sets, and built-in pipeline integrations (such as standard material conversions and built-in variables like COLOR referenced in godot/shaders/rewind_tint.gdshader:8) that plain core GLSL requires manual boilerplate code to set up.
