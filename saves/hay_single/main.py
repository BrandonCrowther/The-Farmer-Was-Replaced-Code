import Common

# exp-hay_single-002 -- instrumented reactive-companion probe
#
# 001 computed a floor from arithmetic alone and flagged two things that
# arithmetic can't settle: whether the 81,920 multiplied yield transfers here,
# and whether a *solo* drone's own-memory skip rate can approach Hay's
# (44-66%, boosted there by neighbour drones accidentally pre-stocking each
# other's companion tiles -- 021's "contention is cooperation"). hay_single has
# no neighbours, so the skip rate this probe measures is a hard ceiling, not a
# floor to design past.
#
# It also tests a free deduction that didn't need a run: Carrot costs 512 hay
# *and 512 wood*, and nothing in this design ever produces wood (companion
# trees are planted and left standing, never harvested for wood). So Carrot
# should show as permanently unaffordable -- `Common.affordable()` already
# skips it, and this probe checks that assumption rather than trusting it.
#
# This is still a probe: it runs a fixed number of harvest cycles and
# terminates without reaching 100,000,000. Expect "Run Failed"; the duration
# is not a score.

instructions = Common.get_planting_instructions(Entities.Grass)
ax, ay = get_pos_x(), get_pos_y()
instructions()

planted = {}
CYCLES = 60
hits = 0
misses_afford = 0
misses_satisfied = 0
carrot_seen = 0

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
	quick_print("CYCLE", i, "COMPANION", companion, "HIT", hit, "AFFORD", afforded,
		"GAINED", gained, "TICK", get_tick_count())
	instructions()

quick_print("SUMMARY", "CYCLES", CYCLES, "HITS", hits, "SAT", misses_satisfied,
	"UNAFFORD", misses_afford, "CARROT_SEEN", carrot_seen,
	"WOOD", num_items(Items.Wood), "HAY", num_items(Items.Hay),
	"TICK_FINAL", get_tick_count(), "TIME_FINAL", get_time())
# Deliberately do not loop to the 100_000_000 target -- this is a probe.
