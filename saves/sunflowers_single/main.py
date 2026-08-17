# exp-sunflowers_single-002 -- reroll-to-15 + 10-tile round robin validation
#
# 001 found harvest() on an unripe entity destroys it for 200 ticks
# (Available-Functions.md) rather than requiring can_harvest()==True,
# and petals are fixed and readable immediately at plant time -- so a
# cheap reroll (harvest the just-planted unripe sunflower + replant,
# ~400 ticks/attempt) can redraw petals before paying the ~17,643-tick
# growth cost. Reroll every tile to petals=15 (the maximum) before
# letting it grow: since nothing can exceed 15, a farm-wide tie for max
# is permanent, and every harvest gets the 8x bonus with zero tracking.
#
# Not chasing the target -- terminates after a bounded number of cycles.
# Expect "Run Failed"; the duration is not a score.

N = 10
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

def plant_and_reroll_to_15():
	plant(Entities.Sunflower)
	p = measure()
	attempts = 1
	while p != 15:
		harvest()
		plant(Entities.Sunflower)
		p = measure()
		attempts = attempts + 1
	return attempts

positions = []
for i in range(N):
	positions.append((OX + i % 5, OY + i // 5))

for pos in positions:
	move_to(pos[0], pos[1])
	if get_ground_type() != Grounds.Soil:
		till()
	plant_and_reroll_to_15()

CYCLES = 30
total_gain = 0
total_rerolls = 0
harvests = 0
t_start = get_tick_count()
for c in range(CYCLES):
	pos = positions[c % N]
	move_to(pos[0], pos[1])
	h = can_harvest()
	while not h:
		h = can_harvest()
	before = num_items(Items.Power)
	harvest()
	gain = num_items(Items.Power) - before
	total_gain = total_gain + gain
	harvests = harvests + 1
	r = plant_and_reroll_to_15()
	total_rerolls = total_rerolls + r
	if c < 10 or c % 5 == 0:
		quick_print("CYCLE", c, "GAIN", gain, "REROLLS", r)

t_total = get_tick_count() - t_start
quick_print("SUMMARY", "HARVESTS", harvests, "TOTAL_GAIN", total_gain, "AVG_REROLLS",
	total_rerolls / harvests, "TICKS", t_total, "TICKS_PER_HARVEST", t_total / harvests)
