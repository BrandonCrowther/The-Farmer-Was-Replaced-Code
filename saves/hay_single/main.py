import Common

# exp-hay_single-010 -- finish-and-score-v2
#
# 008's champion (walk on every companion miss) plus 009's measured
# improvement: the structural hit rate against remembered stock is only
# ~1/3 (004 -- three companion types, one stocked per position), so most
# misses are cheaper to resolve with up to REROLL_LIMIT cheap rerolls
# (harvest the just-planted unripe grass -- "harvesting an entity that
# can't be harvested destroys it", 200 ticks -- then replant, ~400
# ticks/attempt, no travel) than with one real ~1,600-tick walk. Capped, so
# the memory still gets new stock from a real walk often enough to keep
# growing -- pure reroll-forever never establishes anything new.
#
# 009 measured ≈98.75 hay/tick steady state against the champion's ≈55.8,
# projecting roughly 02:47 -- an estimate, not a guarantee; see
# experiments/hay_single/009/result.md and 010/hypothesis.md.

TARGET = 100000000
REROLL_LIMIT = 2
instructions = Common.get_planting_instructions(Entities.Grass)
ax, ay = get_pos_x(), get_pos_y()
instructions()

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
