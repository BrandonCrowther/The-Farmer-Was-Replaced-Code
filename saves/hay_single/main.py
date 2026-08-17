import Common

# exp-hay_single-005 -- clustered-probe
#
# 004 derived (arithmetic only) that clustering 2-3 grass tiles close enough
# for their companion balls to overlap heavily should push the solo hit rate
# toward its ~1/3 ceiling faster than a single tile does alone (002 measured
# ~25-30%, close to but not at that ceiling already). This probe builds the
# cluster and measures whether it actually gets there, using the same shared
# `planted` memory dict across all three tiles -- the only change from 002 is
# that the memory is now populated by, and checked against, three tiles'
# worth of visits instead of one.
#
# Three tiles, pairwise wrapped distance 2 (50% ball overlap per 004's
# table): (0,0), (2,0), (0,2).
#
# Still a probe: fixed cycle count, does not chase the 100,000,000 target.
# Expect "Run Failed"; the duration is not a score.

instructions = Common.get_planting_instructions(Entities.Grass)
TILES = [(0, 0), (2, 0), (0, 2)]

for (x, y) in TILES:
	Common.move_to_wrapped(x, y)
	instructions()

planted = {}
CYCLES = 90
hits = 0
misses_afford = 0
misses_satisfied = 0
carrot_seen = 0

for i in range(CYCLES):
	tx, ty = TILES[i % len(TILES)]
	Common.move_to_wrapped(tx, ty)

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
				Common.move_to_wrapped(cx, cy)
				if get_entity_type() != ctype:
					harvest()
					Common.plant_companion(ctype)
				planted[key] = ctype
				Common.move_to_wrapped(tx, ty)
				misses_satisfied = misses_satisfied + 1
			else:
				misses_afford = misses_afford + 1

	before = num_items(Items.Hay)
	harvest()
	gained = num_items(Items.Hay) - before
	quick_print("CYCLE", i, "TILE", (tx, ty), "COMPANION", companion, "HIT", hit,
		"AFFORD", afforded, "GAINED", gained, "TICK", get_tick_count())
	instructions()

quick_print("SUMMARY", "CYCLES", CYCLES, "HITS", hits, "SAT", misses_satisfied,
	"UNAFFORD", misses_afford, "CARROT_SEEN", carrot_seen,
	"WOOD", num_items(Items.Wood), "HAY", num_items(Items.Hay),
	"TICK_FINAL", get_tick_count(), "TIME_FINAL", get_time())
# Deliberately do not loop to the 100_000_000 target -- this is a probe.
