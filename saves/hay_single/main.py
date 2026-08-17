import Common

# exp-hay_single-009 -- reroll-before-walk probe
#
# The champion (008) walks to satisfy every companion miss, at ~1,600 ticks
# a trip, and the structural hit rate is only ~1/3 (three possible companion
# types, one stocked at a time per position -- 004's ceiling argument, now
# with Carrot back in the type pool since 006/007 showed wood stops being
# scarce). A miss doesn't have to mean "walk": `harvest()` destroys an
# unripe plant for 200 ticks (Available-Functions.md), so replanting our own
# tile rerolls its (type, position) request for ~400 ticks (harvest the
# unripe grass + replant) without moving at all. If that reroll lands on a
# position/type combo already in memory, it's a hit for free; if not, try
# again, capped, then fall back to the champion's walk-and-establish (which
# also grows the memory for next time -- pure reroll-forever would never
# stock anything new and could loop indefinitely).
#
# Expected value (P(hit)=1/3 per attempt, 2 rerolls capped, then walk
# ~1,600): ~918 ticks average per miss, vs. the champion's flat ~1,600 --
# see 009's hypothesis for the arithmetic. This probe measures whether that
# holds, and whether the reroll traffic slows memory coverage enough to
# matter.
#
# Still a probe: fixed cycle count, does not chase 100,000,000.

instructions = Common.get_planting_instructions(Entities.Grass)
ax, ay = get_pos_x(), get_pos_y()
instructions()

planted = {}
CYCLES = 200
REROLL_LIMIT = 2
hits_initial = 0
hits_reroll = 0
walks = 0
unafford = 0
rerolls_total = 0

for i in range(CYCLES):
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
	outcome = "none"
	rerolls = 0
	while companion != None:
		ctype, (cx, cy) = companion
		key = (cx, cy)
		if key in planted and planted[key] == ctype:
			outcome = "hit"
			if rerolls == 0:
				hits_initial = hits_initial + 1
			else:
				hits_reroll = hits_reroll + 1
			break
		if rerolls < REROLL_LIMIT:
			harvest()
			instructions()
			companion = get_companion()
			rerolls = rerolls + 1
			rerolls_total = rerolls_total + 1
		else:
			if Common.affordable(ctype):
				Common.move_to_wrapped(cx, cy)
				if get_entity_type() != ctype:
					harvest()
					Common.plant_companion(ctype)
				planted[key] = ctype
				Common.move_to_wrapped(ax, ay)
				outcome = "walk"
				walks = walks + 1
			else:
				outcome = "unafford"
				unafford = unafford + 1
			break

	quick_print("CYCLE", i, "GAINED", gained, "OUTCOME", outcome, "REROLLS", rerolls,
		"WOOD", num_items(Items.Wood), "TICK", get_tick_count())

quick_print("SUMMARY", "CYCLES", CYCLES, "HITS_INITIAL", hits_initial, "HITS_REROLL", hits_reroll,
	"WALKS", walks, "UNAFFORD", unafford, "REROLLS_TOTAL", rerolls_total,
	"WOOD", num_items(Items.Wood), "HAY", num_items(Items.Hay),
	"TICK_FINAL", get_tick_count(), "TIME_FINAL", get_time())
# Deliberately do not loop to the 100_000_000 target -- this is a probe.
