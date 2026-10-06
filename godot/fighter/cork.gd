extends Sprite2D
## Cork projectile from the pop-gun. Moves in a straight line; on the first
## overlap with the target's hurtbox it calls receive_hit once and frees itself.

const SPEED := 320.0
const SIZE := Vector2(10, 10)
var owner_fighter: Fighter
var dir := 1
var life := 2.0
var done := false
signal struck(cork: Node2D, blocked: bool)

func step(dt: float) -> void:
	if done:
		return
	position.x += dir * SPEED * dt
	rotation += dir * 12.0 * dt
	life -= dt
	var target := owner_fighter.opponent
	var box := Rect2(position - SIZE / 2, SIZE)
	if target and box.intersects(target.hurtbox()):
		done = true
		var blocked := target.receive_hit(self, Fighter.ATTACKS[Fighter.S.POP].dmg, Fighter.ATTACKS[Fighter.S.POP].push)
		struck.emit(self, blocked)
		queue_free()
	elif life <= 0.0 or position.x < -20 or position.x > 660:
		done = true
		queue_free()
