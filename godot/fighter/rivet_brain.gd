extends RefCounted
## Rivet's pattern-driven controller (not real AI - that is a next step).
## Fills Rivet's `intent` from simple distance/wind rules so the player can learn
## it: close in, jab-jab-cutlass, back off and rewind when the spring runs low,
## take pop-gun shots from range, sometimes block a visible attack startup.
## Deterministic: no randomness, so scripted tests replay identically.

var me: Fighter
var cooldown := 0.6
var combo := 0
var pop_cd := 1.5   # no cork in the first 1.5 s of a round (found by the test run)
var retreating := false
var block_toggle := false

func think(dt: float) -> void:
	var foe := me.opponent
	var i := {"move": 0, "jab": false, "cutlass": false, "pop": false, "block": false, "rewind": false}
	cooldown -= dt
	pop_cd -= dt
	if foe == null or foe.is_out() or me.is_out():
		me.intent = i
		return
	var dx := foe.position.x - me.position.x
	var dist := absf(dx)
	var toward := int(signf(dx))
	if me.wind < 25.0:
		retreating = true
	if retreating:
		if dist < 170.0 and me.position.x > me.arena_min + 4 and me.position.x < me.arena_max - 4:
			i.move = -toward                     # walks away (turns its back)
		else:
			i.rewind = true
		if me.wind >= 90.0:
			retreating = false
		me.intent = i
		return
	# block a visible attack startup every other time
	if dist < 90.0 and foe.state in [Fighter.S.JAB, Fighter.S.CUTLASS] and foe.state_t < 0.08:
		block_toggle = not block_toggle
		if block_toggle and me.facing == toward:
			i.block = true
			me.intent = i
			return
	if dist > 230.0 and pop_cd <= 0.0 and me.wind > 50.0 and me.facing == toward:
		i.pop = true
		pop_cd = 2.8
	elif dist > 64.0:
		i.move = toward
	elif cooldown <= 0.0:
		if me.facing != toward:
			i.move = toward
		else:
			if combo % 3 == 2:
				i.cutlass = true
			else:
				i.jab = true
			combo += 1
			cooldown = 0.75
	me.intent = i
