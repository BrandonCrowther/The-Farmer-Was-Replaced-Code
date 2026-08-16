import Common

# MECHANICS PROBE — not an optimisation, and not expected to score.
#
# Too much of this category's reasoning rests on numbers that were inferred from
# whole-run times rather than measured. The polyculture multiplier of "67x" comes
# from a rate ratio in 011 that conflates the multiplier with everything else that
# changed; "walk time ~= growth time" is a story fitted to 016's regression;
# companion range and water starvation come from the wiki and arithmetic. Three
# rejections rest on those numbers.
#
# quick_print costs 0 ticks, so all of it can simply be looked at.
#
# ONE drone, deliberately. num_items(Items.Hay) is global, so with 32 drones
# harvesting concurrently the delta across our own harvest is contaminated by
# everyone else's. With a single drone the delta is exactly our own yield.
#
# The run will not reach 2e9 hay and will be reported as failed. That is expected
# — the telemetry is the point, not the score.
SAMPLES = 40

entity = Entities.Grass
instructions = Common.get_planting_instructions(entity)

clear()
Common.move_to(3, 3)
instructions()

p = 0
while p < SAMPLES:
	# Alternate: satisfy the companion on even passes, skip it on odd ones. The
	# difference between the two yields *is* the multiplier, measured directly
	# rather than inferred from a run time.
	satisfy = p % 2 == 0

	companion = get_companion()
	if companion == None:
		quick_print("COMP", p, "none")
	else:
		ct, (px, py) = companion
		dx = px - get_pos_x()
		dy = py - get_pos_y()
		# Verifies the "within 3 moves" claim, and shows whether any request is
		# far enough to imply the position was given across the wrap.
		quick_print("COMP", p, ct, "dx", dx, "dy", dy, "l1", abs(dx) + abs(dy))
		if satisfy:
			Common.move_to(px, py)
			if get_entity_type() != ct:
				harvest()
				Common.plant_companion(ct)
			Common.move_to(3, 3)

	# Growth: ticks spent waiting for our own grass to ripen, with no companion
	# walk in the way on odd passes. This is the number 016 guessed at.
	t0 = get_tick_count()
	h = can_harvest()
	while not h:
		h = can_harvest()
	t1 = get_tick_count()

	before = num_items(Items.Hay)
	harvest()
	after = num_items(Items.Hay)
	quick_print("YIELD", p, "satisfied", satisfy, "hay", after - before,
		"growticks", t1 - t0, "water", get_water(), "tanks", num_items(Items.Water))
	p = p + 1

quick_print("PROBE_DONE", p)
