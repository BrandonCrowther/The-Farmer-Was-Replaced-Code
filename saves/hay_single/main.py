import Common

# exp-hay_single-011 -- champion-tick-profile
#
# Same logic as 010's champion (see its comment for the reroll-before-walk
# rationale), unchanged, plus a periodic tick/hay print every 50 harvests.
# 010 undershot 009's 200-cycle probe projection because 200 cycles warms
# its own small set of companion positions up faster than a real
# ~1,221-harvest run does. This measures the *actual* full-run trajectory
# instead of extrapolating from a short probe -- quick_print costs 0 ticks
# (Timing.md), so printing every 50 harvests is free and this run scores
# exactly like 010 while also producing the profile.

TARGET = 100000000
REROLL_LIMIT = 2
instructions = Common.get_planting_instructions(Entities.Grass)
ax, ay = get_pos_x(), get_pos_y()
instructions()
harvests = 0

# What this drone believes it has planted, keyed by companion position --
# see Common.polyculture_mapped. Only this drone ever touches the farm, so
# the memory is authoritative, not just a hint.
planted = {}

while num_items(Items.Hay) < TARGET:
	# Water while there is water to use, not until an unreachable level --
	# see Hay's saves/hay/main.py for why the equivalent unbounded condition
	# spins on failed use_item calls.
	while num_items(Items.Water) > 0 and get_water() < 0.999:
		use_item(Items.Water)

	h = can_harvest()
	while not h and num_items(Items.Hay) < TARGET:
		h = can_harvest()
	if num_items(Items.Hay) >= TARGET:
		break
	harvest()
	harvests = harvests + 1
	if harvests % 50 == 0:
		quick_print("PROFILE", harvests, get_tick_count(), num_items(Items.Hay))

	if num_items(Items.Hay) >= TARGET:
		break

	instructions()
	companion = get_companion()
	rerolls = 0
	while companion != None:
		ctype, (cx, cy) = companion
		key = (cx, cy)
		if key in planted and planted[key] == ctype:
			break
		if rerolls < REROLL_LIMIT:
			# Cheap: destroy the unripe grass we just planted and try again,
			# hoping the fresh (type, position) draw already matches stock.
			harvest()
			instructions()
			companion = get_companion()
			rerolls = rerolls + 1
		else:
			# Fall back to a real walk -- this is also how new stock gets
			# established for future rerolls to find.
			if Common.affordable(ctype):
				Common.move_to_wrapped(cx, cy)
				if get_entity_type() != ctype:
					harvest()
					Common.plant_companion(ctype)
				planted[key] = ctype
				Common.move_to_wrapped(ax, ay)
			break

quick_print("DONE", "HAY", num_items(Items.Hay), "WOOD", num_items(Items.Wood),
	"TICK_FINAL", get_tick_count(), "TIME_FINAL", get_time())
