extends CanvasLayer
## Code-drawn HUD (not a generated asset): health bars, spring dials, round text,
## pause and mute indicators. On its own CanvasLayer so camera shake/roll does not
## move it. Every state the player must know is VISIBLE here or in the pose, so
## the slice reads with sound off (pillar "Read the fight at a glance").

var game
var pane := Node2D.new()
var font: Font = ThemeDB.fallback_font

func _ready() -> void:
	layer = 10
	add_child(pane)
	pane.draw.connect(_draw_hud)

func redraw() -> void:
	pane.queue_redraw()

func _bar(x: float, w: float, frac: float, col: Color, right: bool) -> void:
	pane.draw_rect(Rect2(x - 2, 12, w + 4, 16), Color(0.05, 0.05, 0.07, 0.85))
	var fw := w * clampf(frac, 0.0, 1.0)
	pane.draw_rect(Rect2(x + (w - fw if right else 0.0), 14, fw, 12), col)

func _dial(c: Vector2, frac: float, label: String) -> void:
	var low := frac < 0.25
	pane.draw_circle(c, 17, Color(0.12, 0.09, 0.05, 0.9))
	pane.draw_arc(c, 17, 0, TAU, 32, Color("#C9962B"), 3.0)
	pane.draw_arc(c, 12, -PI / 2, -PI / 2 + TAU * frac, 32, Color("#ff5a4a") if low else Color("#E8C35A"), 5.0)
	var a := -PI / 2 + TAU * frac
	pane.draw_line(c, c + Vector2.from_angle(a) * 11, Color.WHITE, 2.0)
	pane.draw_string(font, c + Vector2(-22, 30), label, HORIZONTAL_ALIGNMENT_CENTER, 44, 9, Color(1, 1, 1, 0.85))

func _center(text: String, y: float, size: int, col := Color("#ffd27a")) -> void:
	pane.draw_string_outline(font, Vector2(0, y), text, HORIZONTAL_ALIGNMENT_CENTER, 640, size, 6, Color(0, 0, 0, 0.8))
	pane.draw_string(font, Vector2(0, y), text, HORIZONTAL_ALIGNMENT_CENTER, 640, size, col)

func _draw_hud() -> void:
	if game == null:
		return
	var b: Fighter = game.bolt
	var r: Fighter = game.rivet
	if game.round_state == game.R.TITLE:
		pane.draw_rect(Rect2(0, 0, 640, 360), Color(0, 0, 0, 0.45))
		_center("TIN KNOCKOUT", 130, 44)
		_center("tin toys fight after closing time", 160, 13, Color.WHITE)
		_center("ENTER to start", 210, 16, Color.WHITE)
		_center("A/D move   J jab   K cutlass   L pop-gun   I block   S rewind (hold)", 300, 11, Color(1, 1, 1, 0.8))
		_center("Esc pause   M music   N effects   F1 hitboxes", 318, 11, Color(1, 1, 1, 0.8))
		_mutes()
		return
	_bar(16, 220, b.hp / Fighter.MAX_HP, Color("#E8C35A"), false)
	_bar(404, 220, r.hp / Fighter.MAX_HP, Color("#D9A066"), true)
	pane.draw_string(font, Vector2(16, 42), "BOLT", HORIZONTAL_ALIGNMENT_LEFT, -1, 11, Color.WHITE)
	pane.draw_string(font, Vector2(584, 42), "RIVET", HORIZONTAL_ALIGNMENT_RIGHT, 40, 11, Color.WHITE)
	_dial(Vector2(36, 66), b.wind / Fighter.MAX_WIND, "SPRING")
	_dial(Vector2(604, 66), r.wind / Fighter.MAX_WIND, "SPRING")
	for f in [b, r]:
		var tag := ""
		match f.state:
			Fighter.S.EMPTY: tag = "EMPTY!"
			Fighter.S.REWIND: tag = "rewinding" if f.wind < Fighter.MAX_WIND else "FULL"
			Fighter.S.BLOCK: tag = "block"
		if tag != "":
			var col := Color("#ff6a5a") if tag == "EMPTY!" else Color(1, 1, 1, 0.9)
			pane.draw_string_outline(font, Vector2(f.position.x - 50, f.position.y - 128), tag, HORIZONTAL_ALIGNMENT_CENTER, 100, 13, 4, Color(0, 0, 0, 0.8))
			pane.draw_string(font, Vector2(f.position.x - 50, f.position.y - 128), tag, HORIZONTAL_ALIGNMENT_CENTER, 100, 13, col)
	match game.round_state:
		game.R.INTRO:
			_center("ROUND 1", 150, 36)
		game.R.FIGHT:
			if game.round_t < 0.6:
				_center("FIGHT!", 150, 36)
			if game.paused:
				pane.draw_rect(Rect2(0, 0, 640, 360), Color(0, 0.05, 0.12, 0.55))
				_center("PAUSED", 160, 36, Color.WHITE)
				_center("Esc to resume", 186, 13, Color.WHITE)
		game.R.KO:
			_center("K.O.", 140, 56)
			_center(("BOLT" if game.winner == b else "RIVET") + " WINS", 172, 18, Color.WHITE)
			_center("R - rematch", 198, 13, Color.WHITE)
	_mutes()

func _mutes() -> void:
	var y := 352.0
	if AudioServer.is_bus_mute(AudioServer.get_bus_index(&"Music")):
		pane.draw_string(font, Vector2(8, y), "MUSIC OFF (M)", HORIZONTAL_ALIGNMENT_LEFT, -1, 10, Color(1, 1, 1, 0.8))
	if AudioServer.is_bus_mute(AudioServer.get_bus_index(&"SFX")):
		pane.draw_string(font, Vector2(110, y), "EFFECTS OFF (N)", HORIZONTAL_ALIGNMENT_LEFT, -1, 10, Color(1, 1, 1, 0.8))
