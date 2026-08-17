import Common

# exp-hay_single-007 -- single-tile, long run
#
# 006 found that a companion tile left standing long enough eventually gets
# harvested-and-replanted for real wood when a fresh request names it with a
# different type -- and that unlocked Carrot from ~cycle 22 on, in a 2-tile
# run. 002's single-tile probe only ran 60 cycles and never saw this (WOOD
# stayed 0 throughout). This is the same design as 002, just long enough
# (200 cycles) to see whether the same thing happens with one tile instead
# of two, and what the real steady-state ticks/harvest looks like once it
# does.
#
# Still a probe: fixed cycle count, does not chase 100,000,000. Expect
# "Run Failed"; the duration is not a score.

instructions = Common.get_planting_instructions(Entities.Grass)
ax, ay = get_pos_x(), get_pos_y()
instructions()

planted = {}
CYCLES = 200
hits = 0
misses_afford = 0
misses_satisfied = 0
carrot_seen = 0
carrot_afforded = 0

for i in range(CYCLES):
	while num_items(Items.Water) > 0 and get_water() < 0.999:
		use_item(Items.Water)

	h = can_harvest()
	while not h:
		h = can_harvest()

	companion = get_companion()
	hit = False
	afforded = None
	if companion != None:
		ctype, (cx, cy) = companion
		key = (cx, cy)
		if ctype == Entities.Carrot:
			carrot_seen = carrot_seen + 1
		if key in planted and planted[key] == ctype:
			hit = True
			hits = hits + 1
		else:
			afforded = Common.affordable(ctype)
			if afforded:
				if ctype == Entities.Carrot:
					carrot_afforded = carrot_afforded + 1
				Common.move_to_wrapped(cx, cy)
				if get_entity_type() != ctype:
					harvest()
					Common.plant_companion(ctype)
				planted[key] = ctype
				Common.move_to_wrapped(ax, ay)
				misses_satisfied = misses_satisfied + 1
			else:
				misses_afford = misses_afford + 1

	before = num_items(Items.Hay)
	harvest()
	gained = num_items(Items.Hay) - before
	# Print every 5th cycle plus the first 10, to keep output.txt a
	# manageable size at 200 cycles while still showing the warm-up window
	# and the trend.
	if i < 10 or i % 5 == 0:
		quick_print("CYCLE", i, "COMPANION", companion, "HIT", hit, "AFFORD", afforded,
			"GAINED", gained, "WOOD", num_items(Items.Wood), "TICK", get_tick_count())
	instructions()

quick_print("SUMMARY", "CYCLES", CYCLES, "HITS", hits, "SAT", misses_satisfied,
	"UNAFFORD", misses_afford, "CARROT_SEEN", carrot_seen, "CARROT_AFFORDED", carrot_afforded,
	"WOOD", num_items(Items.Wood), "HAY", num_items(Items.Hay),
	"TICK_FINAL", get_tick_count(), "TIME_FINAL", get_time())
# Deliberately do not loop to the 100_000_000 target -- this is a probe.
