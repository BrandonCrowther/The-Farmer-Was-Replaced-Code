import Common

# exp-hay_single-012 -- reroll-limit-5
#
# 010's champion (walk on every companion miss, after up to REROLL_LIMIT
# cheap rerolls -- see 010's comment for the full rationale). 011 fit an
# exact probability model to real data (R=400 reroll, W=1,600 walk, p=1/3
# hit chance) and it reproduces 008's real 55.8 hay/tick at K=0 almost
# exactly. The model predicts diminishing but real further gains raising
# REROLL_LIMIT past 2: K=2 -> 62.13, K=5 -> 66.33, K=7 -> 67.39 hay/tick.
# This tests K=5, the point past which 011 found returns thin out sharply.

TARGET = 100000000
REROLL_LIMIT = 5
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
