import Common

# exp-hay_single-015 -- bush-blanket-quad probe
#
# Tests the user's proposal literally: 4 grass tiles clustered together,
# with the *entire rest of the 8x8 board* pre-planted with Bush before the
# main loop starts, so every companion request that names Bush is
# satisfied wherever it points -- no per-position memory, no walk, ever;
# just reroll (uncapped) until the draw is Bush.
#
# Stated prediction, before running: mathematically this hinges on the
# same p=1/3 type-match probability as the existing design's steady state
# (011's proof), so per-harvest cost should converge to the same ~1,200
# ticks (own-tile 400 + reroll-to-Bush average 800) once the one-time
# ~36,000-tick blanket setup is paid off -- plus whatever commute the 4
# tiles need between them. If real numbers land meaningfully below that,
# the model is missing something and this is a genuine new lever, not just
# a restatement of the existing ceiling.
#
# Still a probe: fixed cycle count, does not chase 100,000,000.

TILES = [(3, 3), (4, 3), (3, 4), (4, 4)]
TILE_SET = set(TILES)
instructions = Common.get_planting_instructions(Entities.Grass)
bush = Common.get_planting_instructions(Entities.Bush)

t0 = get_tick_count()
N = get_world_size()
for x in range(N):
	for y in range(N):
		if (x, y) not in TILE_SET:
			Common.move_to_wrapped(x, y)
			bush()
setup_ticks = get_tick_count() - t0

for (x, y) in TILES:
	Common.move_to_wrapped(x, y)
	instructions()

CYCLES = 300
rerolls_total = 0
for i in range(CYCLES):
	tx, ty = TILES[i % len(TILES)]
	Common.move_to_wrapped(tx, ty)

	while num_items(Items.Water) > 0 and get_water() < 0.999:
		use_item(Items.Water)

	h = can_harvest()
	while not h:
		h = can_harvest()

	harvest()

	instructions()
	companion = get_companion()
	rerolls = 0
	while companion != None and (companion[0] != Entities.Bush or companion[1] in TILE_SET):
		# The second condition guards against a false positive: if the draw
		# is Bush but names one of our *other* 3 hay tiles (which hold
		# Grass, not Bush, since those are excluded from the blanket), it
		# is not actually satisfied there -- same hazard 005 found, applied
		# to a type-only check instead of a position-lookup check.
		harvest()
		instructions()
		companion = get_companion()
		rerolls = rerolls + 1
		rerolls_total = rerolls_total + 1
	# companion is now Bush at a genuinely blanketed position (or None) --
	# the whole board except our 4 tiles is already Bush, so nothing
	# further to do; move on to the next tile.

	if i < 10 or i % 50 == 0:
		quick_print("CYCLE", i, "TILE", (tx, ty), "REROLLS", rerolls, "TICK", get_tick_count())

quick_print("SUMMARY", "SETUP_TICKS", setup_ticks, "CYCLES", CYCLES, "REROLLS_TOTAL", rerolls_total,
	"HAY", num_items(Items.Hay), "TICK_FINAL", get_tick_count(), "TIME_FINAL", get_time())
# Deliberately do not loop to the 100_000_000 target -- this is a probe.
