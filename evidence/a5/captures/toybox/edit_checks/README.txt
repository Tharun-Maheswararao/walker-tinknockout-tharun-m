One shader, two materials: edit checks (2026-11-01)
Edits by Tharun (nano). Captures and measurements by Claude, in windowed
runs of tools/a5_capture_side_by_side.gd (Vulkan Forward+), compared with
0_before_edits.png. A pixel counts as "changed" if its difference is
greater than 8 levels.

1. Shader edit (1_shader_edit.diff): painted_tin.gdshader line 13, the
   uv_scale default 2.5 -> 6.0. Neither material sets uv_scale.
   fresh box: 88 px changed across x 784-888 (finer dents, nearly flat red)
   worn box : 1622 px changed (finer pattern, red specks gone)
   castle   : 0 px
   -> BOTH objects changed. The shader was then restored with git checkout
      (SHA-256 0462a674...).

2. Material edit (2_material_edit.diff): toybox_worn.tres, wear_amount
   0.55 -> 0.2.
   fresh box: unchanged. The only "changes" in its crop are the worn box's
              left edge at x 885-888.
   worn box : 6698 px changed (mostly bare metal -> mostly red paint)
   castle   : 0 px
   -> ONLY the worn object changed.
