extends Node
## REWIND tint driver (CHANGE-BRIEF A5.2): gives one fighter's body sprite its
## own ShaderMaterial and fades `rewind_amount` from the fighter's state.
##
## Read-only: it reads `fighter.state` and `game.paused` and never writes game
## state. move_toward from the current value gives R3 (extend) and R5 (fade out
## from where it is); `delta` is scaled game time (R4a).

const FADE_IN := 0.15
const FADE_OUT := 0.30

var fighter: Fighter
var game
var material: ShaderMaterial
var amount := 0.0

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_PAUSABLE   # main is ALWAYS; freeze on tree pause (R4b)
	material = ShaderMaterial.new()             # one per fighter (R6)
	material.shader = preload("res://shaders/rewind_tint.gdshader")
	fighter.sprite.material = material
	material.set_shader_parameter("rewind_amount", amount)

func _process(delta: float) -> void:
	if game.paused:
		return                                  # the fight is frozen, so is the tint (R4c)
	var target := 1.0 if fighter.state == Fighter.S.REWIND else 0.0
	var rate := 1.0 / (FADE_IN if target > amount else FADE_OUT)
	amount = move_toward(amount, target, rate * delta)
	material.set_shader_parameter("rewind_amount", amount)
