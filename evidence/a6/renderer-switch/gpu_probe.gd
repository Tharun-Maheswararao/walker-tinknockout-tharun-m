extends SceneTree
## Scratch probe (not in the repo): does this driver report GPU render time?
## Uses the viewport render-time measurement, which reads GPU timestamps.

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	print("driver: ", RenderingServer.get_current_rendering_driver_name(), " | method: ", RenderingServer.get_current_rendering_method(), " | adapter: ", RenderingServer.get_video_adapter_name())
	root.add_child((load("res://game/main.tscn") as PackedScene).instantiate())
	var vp := root.get_viewport_rid()
	RenderingServer.viewport_set_measure_render_time(vp, true)
	var samples := []
	for i in 180:
		await process_frame
		if i >= 60:
			samples.append([RenderingServer.viewport_get_measured_render_time_cpu(vp), RenderingServer.viewport_get_measured_render_time_gpu(vp)])
	var cpu := 0.0
	var gpu := 0.0
	var gpu_max := 0.0
	for s in samples:
		cpu += s[0]
		gpu += s[1]
		gpu_max = maxf(gpu_max, s[1])
	print("120 frames: mean cpu ", snappedf(cpu / samples.size(), 0.0001), " ms | mean gpu ", snappedf(gpu / samples.size(), 0.0001), " ms | max gpu ", snappedf(gpu_max, 0.0001), " ms")
	quit()
