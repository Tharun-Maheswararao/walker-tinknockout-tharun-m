extends SceneTree
## Scratch check (not part of the repo): screenshots of the title, round intro,
## an idle fight frame and the A3 prop room, under whichever --rendering-method
## the run uses. Output dir comes from the OUT environment variable.

var out := OS.get_environment("OUT")

func _initialize() -> void:
	call_deferred("run")

func frames(n: int) -> void:
	for i in n:
		await physics_frame

func snap(name: String) -> void:
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
	root.get_viewport().get_texture().get_image().save_png(out.path_join(name + ".png"))
	print("shot ", name)

func press(action: String) -> void:
	for p in [true, false]:
		var e := InputEventAction.new()
		e.action = action
		e.pressed = p
		Input.parse_input_event(e)
		await frames(1)

func run() -> void:
	print("renderer: ", RenderingServer.get_current_rendering_method(), " / ", RenderingServer.get_current_rendering_driver_name(), " / ", RenderingServer.get_video_adapter_name())
	var main = (load("res://game/main.tscn") as PackedScene).instantiate()
	root.add_child(main)
	await frames(30)
	await snap("1_title")
	await press("confirm")
	await frames(20)
	await snap("2_intro")
	await frames(120)
	await snap("3_fight_idle")
	main.queue_free()
	await frames(2)
	var room = (load("res://prop_room/prop_room.tscn") as PackedScene).instantiate()
	root.add_child(room)
	await frames(10)
	await snap("4_prop_room")
	quit()
