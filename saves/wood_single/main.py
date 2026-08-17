import Common

# exp-wood_single-001 -- mechanics probe
#
# Tree is a polyculture crop (Polyculture.md), free to plant
# (Entity-Planting-Costs.md). This measures growth ticks (isolated vs
# with an adjacent tree, per Entities.md's neighbor-slowdown warning),
# base and multiplied Wood yield.
#
# Not chasing the target -- terminates quickly. Expect "Run Failed".

quick_print("START", "HAY", num_items(Items.Hay), "WOOD", num_items(Items.Wood),
	"CARROT", num_items(Items.Carrot))
quick_print("COST_TREE", get_cost(Entities.Tree))

OX = get_pos_x()
OY = get_pos_y()

def move_to(x, y):
	while get_pos_x() < x:
		move(East)
	while get_pos_x() > x:
		move(West)
	while get_pos_y() < y:
		move(North)
	while get_pos_y() > y:
		move(South)

# Tile A: isolated tree, harvested with no companion satisfied -- base yield.
if get_ground_type() != Grounds.Grassland:
	till()
plant(Entities.Tree)
t_plant = get_tick_count()
h = can_harvest()
while not h:
	h = can_harvest()
t_ripe_isolated = get_tick_count()
before = num_items(Items.Wood)
harvest()
base_gain = num_items(Items.Wood) - before

quick_print("TILE_A_ISOLATED", "GROWTH_TICKS", t_ripe_isolated - t_plant, "BASE_GAIN", base_gain)

# Tile B + C: two adjacent trees, measure growth ticks for one with a
# neighbor also growing, to quantify the slowdown Entities.md warns about.
move_to(OX + 2, OY)
if get_ground_type() != Grounds.Grassland:
	till()
plant(Entities.Tree)
move(East)
if get_ground_type() != Grounds.Grassland:
	till()
plant(Entities.Tree)
t_plant_bc = get_tick_count()
h = can_harvest()
while not h:
	h = can_harvest()
t_ripe_c = get_tick_count()

quick_print("TILE_C_NEIGHBOR", "GROWTH_TICKS", t_ripe_c - t_plant_bc)

# Tile D: companion-satisfied tree, multiplied yield.
move_to(OX + 4, OY)
if get_ground_type() != Grounds.Grassland:
	till()
plant(Entities.Tree)
companion = get_companion()
if companion != None:
	ctype, pos = companion
	if Common.affordable(ctype):
		move_to(pos[0], pos[1])
		if get_entity_type() != ctype:
			harvest()
			Common.plant_companion(ctype)
		move_to(OX + 4, OY)

h = can_harvest()
while not h:
	h = can_harvest()
before2 = num_items(Items.Wood)
harvest()
mult_gain = num_items(Items.Wood) - before2

quick_print("TILE_D_MULTIPLIED", "COMPANION", companion, "GAIN", mult_gain, "RATIO",
	mult_gain / base_gain)
