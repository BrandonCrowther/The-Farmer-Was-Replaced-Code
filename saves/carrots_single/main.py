# exp-carrots_single-001 -- mechanics-probe
#
# Fresh category, same as hay_single was at the start of tonight. Unlike
# Grass, Carrot costs resources to plant (512 hay + 512 wood per
# Entity-Planting-Costs, already measured indirectly via Hay tonight) --
# and per Polyculture.md, a Carrot plant's own companion preference is
# Grass, Bush, or Tree (never itself), all three of which are FREE to
# plant. That's the opposite asymmetry from hay_single, where the crop was
# free and one companion option (Carrot) was expensive. Measuring fresh
# rather than assuming hay_single's design transfers unchanged.
#
# This probe does not chase the 100,000,000 target -- it terminates after
# a handful of measured cycles. Expect "Run Failed"; the duration is not a
# score.

quick_print("WORLD", get_world_size(), "MAX_DRONES", max_drones())
quick_print("POS", get_pos_x(), get_pos_y())
quick_print("START_CARROT", num_items(Items.Carrot), "START_HAY", num_items(Items.Hay),
	"START_WOOD", num_items(Items.Wood), "START_WATER_TANK", num_items(Items.Water))
quick_print("COST_CARROT", get_cost(Entities.Carrot))
quick_print("COST_BUSH", get_cost(Entities.Bush))
quick_print("COST_TREE", get_cost(Entities.Tree))
quick_print("COST_GRASS", get_cost(Entities.Grass))
quick_print("WATER0", get_water(), "TICK0", get_tick_count(), "TIME0", get_time())

# --- op-cost sanity check ---
t_a = get_tick_count()
move(East)
t_b = get_tick_count()
quick_print("MOVE_TICKS", t_b - t_a)

till()
t_c = get_tick_count()
quick_print("TILL_TICKS", t_c - t_b, "GROUND_AFTER_TILL", get_ground_type())

plant(Entities.Carrot)
t_d = get_tick_count()
quick_print("PLANT_TICKS", t_d - t_c, "PLANTED", get_entity_type() == Entities.Carrot,
	"CARROT_AFTER_PLANT", num_items(Items.Carrot), "HAY_AFTER_PLANT", num_items(Items.Hay),
	"WOOD_AFTER_PLANT", num_items(Items.Wood))

# --- water equilibrium ---
for i in range(5):
	while num_items(Items.Water) > 0 and get_water() < 0.999:
		use_item(Items.Water)
	quick_print("WATER_SAMPLE", i, get_water(), "TANK", num_items(Items.Water), "TICK", get_tick_count())

# --- growth-ticks + companion distribution for Carrot, 5 cycles ---
for i in range(5):
	while get_entity_type() != Entities.Carrot or get_ground_type() != Grounds.Soil:
		if get_ground_type() != Grounds.Soil:
			till()
		if get_entity_type() != Entities.Carrot:
			plant(Entities.Carrot)
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
		N = get_world_size()
		dx = min(abs(cx - get_pos_x()), N - abs(cx - get_pos_x()))
		dy = min(abs(cy - get_pos_y()), N - abs(cy - get_pos_y()))
		dist = dx + dy
	quick_print("GROWTH", i, "TICKS", t_ripe - t_plant, "W_PLANT", w_plant, "W_RIPE", w_ripe,
		"COMPANION", companion, "DIST", dist)
	before = num_items(Items.Carrot)
	harvest()
	quick_print("YIELD_BARE", i, num_items(Items.Carrot) - before, "HAY", num_items(Items.Hay),
		"WOOD", num_items(Items.Wood))

quick_print("DONE", "TICK_FINAL", get_tick_count(), "TIME_FINAL", get_time())
