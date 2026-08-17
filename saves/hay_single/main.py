# exp-hay_single-001 -- mechanics-probe
#
# No `import Common` here: this probe calls only builtin API functions, and
# hay_single (like every other _single category) has no Common.py yet — none
# of the seven _single categories do. One will be added, byte-identical to the
# nine main-category copies, when a driver actually needs it (queued as 002).
#
# Nothing about hay_single has ever been measured: it is a fresh category (8x8
# farm, 1 drone, target 100_000_000 hay). Before designing a multi-tile layout
# around a "minimum floor" of hay squares, this probe measures the numbers that
# floor depends on, directly, at 0 ticks a print -- rather than reusing the
# Hay (32-drone, larger world) category's figures, which were taken under
# different water economics (one drone's water supply serving one tile here,
# not one drone's supply contending with 31 neighbours).
#
# This probe does NOT try to reach the 100_000_000 target. It terminates on its
# own after a fixed number of measured cycles. Expect the modal to say "Run
# Failed" -- that is correct for a probe and the duration must not be recorded
# as a score (see docs/LOOP.md).
#
# Falsifier for the design this feeds: if growth ticks (G) turn out to be
# small relative to a companion-satisfying handling pass, a single hay tile
# with a walked companion is already schedulable and no multi-tile floor is
# needed at all. If G is large relative to a handling pass, the floor N_min =
# ceil(G / handling_ticks_per_other_tile) is real and the design has to hit it.

quick_print("WORLD", get_world_size(), "MAX_DRONES", max_drones())
quick_print("POS", get_pos_x(), get_pos_y())
quick_print("COST_CARROT", get_cost(Entities.Carrot))
quick_print("COST_BUSH", get_cost(Entities.Bush))
quick_print("COST_TREE", get_cost(Entities.Tree))
quick_print("COST_GRASS", get_cost(Entities.Grass))
quick_print("WATER0", get_water(), "TICK0", get_tick_count(), "TIME0", get_time())

# --- op-cost sanity check: confirm the wiki's 200-ticks-a-success figure holds
# here (it should -- it's a global constant -- but it's free to check once).
t_a = get_tick_count()
move(East)
t_b = get_tick_count()
quick_print("MOVE_TICKS", t_b - t_a)

till()
t_c = get_tick_count()
quick_print("TILL_TICKS", t_c - t_b)

plant(Entities.Grass)
t_d = get_tick_count()
quick_print("PLANT_TICKS", t_d - t_c)

# --- water equilibrium: how high does a single tile's water climb when this
# drone is the only thing drawing from the tank and the only thing draining it?
for i in range(5):
	while num_items(Items.Water) > 0 and get_water() < 0.999:
		use_item(Items.Water)
	quick_print("WATER_SAMPLE", i, get_water(), "TANK", num_items(Items.Water), "TICK", get_tick_count())

# --- growth-ticks distribution, at whatever water this tile actually holds.
# Five cycles: plant, water once to the equilibrium loop above already primed
# the tile, wait for can_harvest(), record ticks and water at ripeness, harvest,
# replant. Also record the companion request each cycle -- type and distance --
# since that is the other half of the handling-pass cost.
for i in range(5):
	while get_entity_type() != Entities.Grass or get_ground_type() != Grounds.Grassland:
		if get_ground_type() != Grounds.Grassland:
			till()
		if get_entity_type() != Entities.Grass:
			plant(Entities.Grass)
	t_plant = get_tick_count()
	w_plant = get_water()
	h = can_harvest()
	while not h:
		h = can_harvest()
	t_ripe = get_tick_count()
	w_ripe = get_water()
	companion = get_companion()
	dist = -1
	if companion != None:
		ctype, (cx, cy) = companion
		dist = abs(cx - get_pos_x()) + abs(cy - get_pos_y())
	quick_print("GROWTH", i, "TICKS", t_ripe - t_plant, "W_PLANT", w_plant, "W_RIPE", w_ripe,
		"COMPANION", companion, "DIST", dist)
	harvest()
	quick_print("YIELD_BARE", i, num_items(Items.Hay))

quick_print("DONE", "TICK_FINAL", get_tick_count(), "TIME_FINAL", get_time())
# Deliberately do not loop to the 100_000_000 target -- this is a probe.
