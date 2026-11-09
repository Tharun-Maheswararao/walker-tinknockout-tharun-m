extends Node
## A6 Use It: F10 toggles vsync for the FPS comparison of the GPU price
## (handout "The GPU price"; CHANGE-BRIEF C allows a vsync debug key, F10-F12).
## Debug builds only; reads the raw key, adds no input action, and changes no
## project setting. Prints the new mode so the run's log records it.
## (F9 is A5's capture key, game/debug_capture.gd.) Written by Claude.

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_F10:
		var off := DisplayServer.window_get_vsync_mode() == DisplayServer.VSYNC_DISABLED
		DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_ENABLED if off else DisplayServer.VSYNC_DISABLED)
		print("debug_vsync: vsync %s (F10)" % ("ON" if off else "OFF"))
