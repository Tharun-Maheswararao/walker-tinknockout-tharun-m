extends Node
## Registers the slice's input actions at startup (keyboard + gamepad) so the
## bindings live in one readable place instead of serialized project.godot events.

const KEYS := {
	"move_left": [KEY_A, KEY_LEFT],
	"move_right": [KEY_D, KEY_RIGHT],
	"jab": [KEY_J],
	"cutlass": [KEY_K],
	"pop": [KEY_L],
	"block": [KEY_I, KEY_UP],
	"rewind": [KEY_S, KEY_DOWN],
	"pause": [KEY_ESCAPE, KEY_P],
	"confirm": [KEY_ENTER, KEY_SPACE],
	"rematch": [KEY_R],
	"mute_music": [KEY_M],
	"mute_sfx": [KEY_N],
	"debug_boxes": [KEY_F1],
}
const PADS := {
	"jab": [JOY_BUTTON_X], "cutlass": [JOY_BUTTON_Y], "pop": [JOY_BUTTON_B],
	"block": [JOY_BUTTON_RIGHT_SHOULDER], "rewind": [JOY_BUTTON_LEFT_SHOULDER],
	"pause": [JOY_BUTTON_START], "confirm": [JOY_BUTTON_A], "rematch": [JOY_BUTTON_BACK],
	"move_left": [JOY_BUTTON_DPAD_LEFT], "move_right": [JOY_BUTTON_DPAD_RIGHT],
}

func _ready() -> void:
	for action in KEYS:
		if not InputMap.has_action(action):
			InputMap.add_action(action)
		for k in KEYS[action]:
			var ev := InputEventKey.new()
			ev.physical_keycode = k
			InputMap.action_add_event(action, ev)
		for b in PADS.get(action, []):
			var jb := InputEventJoypadButton.new()
			jb.button_index = b
			InputMap.action_add_event(action, jb)
