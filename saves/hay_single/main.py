import Common

# exp-hay_single-014 -- adjacent-tiles-reroll-guard probe
#
# 013 closed the single-tile companion-servicing paradigm at a *proven*
# ceiling (~1,200 ticks/harvest, ~68.3 hay/tick, matching 012's real
# ~68.7). The arithmetic says a second tile can only add commute overhead
# for a single serial drone, since growth was never the bottleneck (001)
# and the service-cost floor doesn't improve with more tiles (011). But
# that arithmetic was never checked against reroll-before-walk *combined*
# with multi-tile -- 005/006 tested multi-tile before reroll-before-walk
# existed. This is the one untested combination: two ADJACENT tiles
# (distance 1, cheapest possible commute -- ~200 ticks each way) sharing
# one memory dict, with a same-tile guard (013's fix for 005's bug) instead
# of distance-based avoidance, using the full REROLL_LIMIT=5 champion logic
# on each.
#
# Falsifier stated up front: model predicts ≈1,400 ticks/harvest (worse
# than single-tile's ≈1,200) even at this cheapest-possible commute. If the
# real measurement beats single-tile anyway, the model is missing
# something real (it has undershot reality twice already tonight, on 010
# and 012) and this becomes a real lever. If not, multi-tile is closed for
# real, under the best-case configuration, not just the ones tried before
# reroll-before-walk existed.
#
# Still a probe: fixed cycle count, does not chase 100,000,000.

instructions = Common.get_planting_instructions(Entities.Grass)
TILES = [(0, 0), (0, 1)]
TILE_SET = set(TILES)
REROLL_LIMIT = 5

for (x, y) in TILES:
	Common.move_to_wrapped(x, y)
	instructions()

planted = {}
CYCLES = 150
hits = 0
walks = 0
selfguard = 0
unafford = 0

for i in range(CYCLES):
	tx, ty = TILES[i % len(TILES)]
	Common.move_to_wrapped(tx, ty)

	while num_items(Items.Water) > 0 and get_water() < 0.999:
		use_item(Items.Water)

	h = can_harvest()
	while not h:
		h = can_harvest()

	before = num_items(Items.Hay)
	harvest()
	gained = num_items(Items.Hay) - before

	instructions()
	companion = get_companion()
	rerolls = 0
	outcome = "none"
	while companion != None:
		ctype, (cx, cy) = companion
		key = (cx, cy)
		if key in TILE_SET:
			# Can't satisfy a request that names our own other farm tile --
			# same guard as 013's distance-4 fix, here needed for real since
			# adjacency puts both tiles inside each other's companion range.
			selfguard = selfguard + 1
			if rerolls < REROLL_LIMIT:
				harvest()
				instructions()
				companion = get_companion()
				rerolls = rerolls + 1
				continue
			else:
				outcome = "selfguard-exhausted"
				break
		if key in planted and planted[key] == ctype:
			outcome = "hit"
			hits = hits + 1
			break
		if rerolls < REROLL_LIMIT:
			harvest()
			instructions()
			companion = get_companion()
			rerolls = rerolls + 1
		else:
			if Common.affordable(ctype):
				Common.move_to_wrapped(cx, cy)
				if get_entity_type() != ctype:
					harvest()
					Common.plant_companion(ctype)
				planted[key] = ctype
				Common.move_to_wrapped(tx, ty)
				outcome = "walk"
				walks = walks + 1
			else:
				outcome = "unafford"
				unafford = unafford + 1
			break

	quick_print("CYCLE", i, "TILE", (tx, ty), "GAINED", gained, "OUTCOME", outcome,
		"REROLLS", rerolls, "TICK", get_tick_count())

quick_print("SUMMARY", "CYCLES", CYCLES, "HITS", hits, "WALKS", walks,
	"SELFGUARD", selfguard, "UNAFFORD", unafford,
	"WOOD", num_items(Items.Wood), "HAY", num_items(Items.Hay),
	"TICK_FINAL", get_tick_count(), "TIME_FINAL", get_time())
# Deliberately do not loop to the 100_000_000 target -- this is a probe.
