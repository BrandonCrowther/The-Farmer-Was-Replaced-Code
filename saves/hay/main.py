# exp-hay-056 -- clean, isolated growth-floor measurement
#
# Single drone, no spawns, no companion servicing, water maintained at
# max throughout. Ground truth for the growth floor, independent of
# any modeling assumption about Plant-growth.md's units.

if get_ground_type() != Grounds.Grassland:
	till()

for trial in range(5):
	while num_items(Items.Water) > 0 and get_water() < 0.999:
		use_item(Items.Water)
	water_at_plant = get_water()
	t0 = get_tick_count()
	plant(Entities.Grass)
	t_plant = get_tick_count()
	h = can_harvest()
	while not h:
		while num_items(Items.Water) > 0 and get_water() < 0.999:
			use_item(Items.Water)
		h = can_harvest()
	t_ripe = get_tick_count()
	before = num_items(Items.Hay)
	harvest()
	after = num_items(Items.Hay)
	quick_print("TRIAL", trial, "WATER_AT_PLANT", water_at_plant, "PLANT_TICKS", t_plant - t0,
		"GROWTH_TICKS", t_ripe - t_plant, "GAINED", after - before)
