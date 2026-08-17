# exp-sunflowers_single-001 -- mechanics probe
#
# First-ever look at this category. Sunflowers.md: harvesting the
# max-petal sunflower (petals 7-15, fixed at plant time, measurable
# pre-maturity) while >=10 stand on the farm gives 8x power; harvesting
# a non-max one "wastes" the bonus for the next harvest too. This
# measures the stockpile, planting cost, growth time, base yield, and
# the real bonus yield.
#
# Not chasing the target -- terminates quickly. Expect "Run Failed".

quick_print("START", "HAY", num_items(Items.Hay), "WOOD", num_items(Items.Wood),
	"CARROT", num_items(Items.Carrot), "POWER", num_items(Items.Power))
quick_print("COST_SUNFLOWER", get_cost(Entities.Sunflower))

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

# Tile 0: lone sunflower, harvested with <10 on the farm -- base yield.
if get_ground_type() != Grounds.Soil:
	till()
plant(Entities.Sunflower)
t_plant = get_tick_count()
petals_pre = measure()
h = can_harvest()
while not h:
	h = can_harvest()
t_ripe = get_tick_count()
petals_ripe = measure()

before = num_items(Items.Power)
harvest()
base_gain = num_items(Items.Power) - before

quick_print("TILE0", "GROWTH_TICKS", t_ripe - t_plant, "PETALS_PRE", petals_pre,
	"PETALS_RIPE", petals_ripe, "BASE_GAIN", base_gain)

# Plant 10 more, find the true max-petal one, harvest it for the bonus.
petals = {}
for i in range(10):
	move_to(OX + (i % 5), OY + 1 + i // 5)
	if get_ground_type() != Grounds.Soil:
		till()
	plant(Entities.Sunflower)
	petals[(get_pos_x(), get_pos_y())] = measure()

for pos in petals:
	move_to(pos[0], pos[1])
	h = can_harvest()
	while not h:
		h = can_harvest()

best_pos = None
best_petals = -1
for pos in petals:
	if petals[pos] > best_petals:
		best_petals = petals[pos]
		best_pos = pos

move_to(best_pos[0], best_pos[1])
before2 = num_items(Items.Power)
harvest()
bonus_gain = num_items(Items.Power) - before2

quick_print("BONUS", "BEST_PETALS", best_petals, "GAIN", bonus_gain, "RATIO",
	bonus_gain / base_gain)
