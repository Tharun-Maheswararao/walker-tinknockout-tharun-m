extends AudioStreamPlayer
## MUS-WALTZ behaviour (CONCEPT audio direction / CHANGE-BRIEF section 3):
## title = quiet, fight = full, Bolt's spring < 25 % = slows + drops in pitch,
## pause = muffled (low-pass) + quieter, KO = stops dead. Driven by game state,
## never the other way round.

const TITLE_DB := -14.0
const FIGHT_DB := 0.0
const LOW_WIND_PITCH := 0.85
var low := false
var tween: Tween
var music_bus := AudioServer.get_bus_index(&"Music")

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	bus = &"Music"
	if ResourceLoader.exists("res://assets/music/waltz.ogg"):
		stream = load("res://assets/music/waltz.ogg")
		stream.loop = true   # the file IS the loop (cut at a bar boundary by tools/edit/cut_loop.py)

func title() -> void:
	volume_db = TITLE_DB
	pitch_scale = 1.0
	if stream and not playing:
		play()

func fight_start() -> void:
	low = false
	pitch_scale = 1.0
	volume_db = FIGHT_DB
	if stream:
		play(0.0)

func set_low_wind(is_low: bool) -> void:
	if is_low == low:
		return
	low = is_low
	if tween:
		tween.kill()
	tween = create_tween()
	tween.tween_property(self, "pitch_scale", LOW_WIND_PITCH if low else 1.0, 0.6)

func set_paused(p: bool) -> void:
	AudioServer.set_bus_effect_enabled(music_bus, 0, p)
	volume_db = FIGHT_DB - 10.0 if p else FIGHT_DB

func knockout() -> void:
	if tween:
		tween.kill()
	stop()
