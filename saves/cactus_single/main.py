# exp-cactus_single-001 -- mechanics probe
#
# First-ever look at this category. Cactus is NOT a polyculture crop
# (Polyculture.md only lists Grass/Bush/Tree/Carrot) -- it's a
# size/sort cascade mechanic (Cactus.md). This measures the stockpile,
# planting cost, growth-to-harvestable time, and whether measure()'s
# size (0-9) keeps changing after a cactus is fully grown, or is fixed
# once reached.
#
# Not chasing the target -- terminates quickly. Expect "Run Failed".

quick_print("START", "HAY", num_items(Items.Hay), "WOOD", num_items(Items.Wood),
	"CARROT", num_items(Items.Carrot), "WATER", num_items(Items.Water),
	"CACTUS", num_items(Items.Cactus))

quick_print("COST_CACTUS", get_cost(Entities.Cactus))

if get_ground_type() != Grounds.Soil:
	till()
plant(Entities.Cactus)
t_plant = get_tick_count()

h = can_harvest()
while not h:
	h = can_harvest()
t_ripe = get_tick_count()
size_at_ripe = measure()

# Wait a further fixed amount without harvesting -- does size change?
WAIT_TICKS = 2000
t_wait_target = get_tick_count() + WAIT_TICKS
while get_tick_count() < t_wait_target:
	pass
size_after_wait = measure()

WAIT_TICKS_2 = 4000
t_wait_target_2 = get_tick_count() + WAIT_TICKS_2
while get_tick_count() < t_wait_target_2:
	pass
size_after_wait_2 = measure()

quick_print("TILE0", "GROWTH_TICKS", t_ripe - t_plant, "SIZE_AT_RIPE", size_at_ripe,
	"SIZE_AFTER_WAIT_2000", size_after_wait, "SIZE_AFTER_WAIT_6000", size_after_wait_2)

harvest()
quick_print("AFTER_HARVEST", "CACTUS", num_items(Items.Cactus))

# Second tile, planted later, to see if the eventual size after the
# same total extra-wait depends on anything besides elapsed time.
move(East)
if get_ground_type() != Grounds.Soil:
	till()
plant(Entities.Cactus)
t_plant2 = get_tick_count()
h = can_harvest()
while not h:
	h = can_harvest()
t_ripe2 = get_tick_count()
size2_at_ripe = measure()
t_wait_target3 = get_tick_count() + WAIT_TICKS
while get_tick_count() < t_wait_target3:
	pass
size2_after_wait = measure()

quick_print("TILE1", "GROWTH_TICKS", t_ripe2 - t_plant2, "SIZE_AT_RIPE", size2_at_ripe,
	"SIZE_AFTER_WAIT_2000", size2_after_wait)
