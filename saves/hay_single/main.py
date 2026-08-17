import Common

# exp-hay_single-006 -- clustered-v2, distance 4
#
# 005 found that distance-2 clustering self-collides: a farm tile's own
# coordinates can be named as *another* farm tile's companion target and get
# silently overwritten (self-healing but costly). That's only possible when
# tiles sit inside each other's companion range (wrapped distance <= 3).
# Distance 4 is outside that range -- by the triangle inequality, no
# companion target of tile A (always within 3 of A) can equal tile B's
# position (4 from A) -- while still keeping 41.7% ball overlap (004's
# table) for whatever coverage-sharing benefit clustering has.
#
# A same-tile guard is included anyway, defensively and cheaply (a 2-item
# set lookup), so a spacing mistake fails safe instead of silently
# corrupting the farm again.
#
# Still a probe: fixed cycle count, does not chase 100,000,000. Expect
# "Run Failed"; the duration is not a score.

instructions = Common.get_planting_instructions(Entities.Grass)
TILES = [(0, 0), (4, 0)]
TILE_SET = set(TILES)

for (x, y) in TILES:
	Common.move_to_wrapped(x, y)
	instructions()

planted = {}
CYCLES = 90
hits = 0
misses_afford = 0
misses_satisfied = 0
misses_selfguard = 0
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
		if key in TILE_SET:
			misses_selfguard = misses_selfguard + 1
		elif key in planted and planted[key] == ctype:
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
	"UNAFFORD", misses_afford, "SELFGUARD", misses_selfguard, "CARROT_SEEN", carrot_seen,
	"WOOD", num_items(Items.Wood), "HAY", num_items(Items.Hay),
	"TICK_FINAL", get_tick_count(), "TIME_FINAL", get_time())
# Deliberately do not loop to the 100_000_000 target -- this is a probe.
