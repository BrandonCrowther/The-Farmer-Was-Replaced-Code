import Common

# exp-hay_single-008 -- finish-and-score
#
# hay_single's first real driver. Design settled by 001-007
# (experiments/hay_single/queue.md has the full trail): single tile,
# reactive skip-and-remember companion servicing, no dedicated wood
# investment -- wood accumulates for free from ordinary companion churn
# (harvesting a now-mature standing Bush/Tree on a type mismatch) and
# Carrot stops being a structural loss once it does (measured from ~cycle
# 15-25 in 007). Measured steady-state throughput was ~49.9 hay/tick,
# projecting ~05:30 -- about 2.4x off the leader's 02:17.995, not a record,
# but the best design found after four independent multi-tile/lever
# rejections (001, 003, 005, 006).
#
# Multi-tile is closed (001: no idle time to hide; 005: self-collision at
# useful overlap distances; 006: a commute tax at safe distances that beats
# any sharing benefit) -- this driver deliberately stays single-tile.

TARGET = 100000000
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
	if companion != None:
		ctype, (cx, cy) = companion
		key = (cx, cy)
		if key in planted and planted[key] == ctype:
			pass
		elif Common.affordable(ctype):
			Common.move_to_wrapped(cx, cy)
			if get_entity_type() != ctype:
				harvest()
				Common.plant_companion(ctype)
			planted[key] = ctype
			Common.move_to_wrapped(ax, ay)

quick_print("DONE", "HAY", num_items(Items.Hay), "WOOD", num_items(Items.Wood),
	"TICK_FINAL", get_tick_count(), "TIME_FINAL", get_time())
