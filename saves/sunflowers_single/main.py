# exp-sunflowers_single-003 -- finish-and-score (reroll-to-15, 10-tile round robin)
#
# 001/002's design: harvest() on an unripe entity destroys it for 200
# ticks (Available-Functions.md) rather than requiring
# can_harvest()==True, and petals are fixed and readable immediately
# at plant time -- so a cheap reroll (harvest the just-planted unripe
# sunflower + replant, ~400 ticks/attempt) redraws petals before paying
# the ~17,643-tick growth cost. Reroll every tile to petals=15 (the
# maximum) before letting it grow: since nothing can exceed 15, a
# farm-wide tie for max is permanent, and every harvest gets the 8x
# bonus with zero tracking. 10 tiles is both the mandatory minimum for
# bonus eligibility (Sunflowers.md: needs >=10 standing) and already
# comfortably above the idle-elimination threshold for this growth/
# handling ratio (002: no measurable idle wait at N=10).
#
# Real run: repeats internally until 2 real hours of simulated time
# accumulate (Leaderboard.md) before the completion modal shows.

TARGET = 10000
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
	while p != 15:
		harvest()
		plant(Entities.Sunflower)
		p = measure()

positions = []
for i in range(N):
	positions.append((OX + i % 5, OY + i // 5))

for pos in positions:
	move_to(pos[0], pos[1])
	if get_ground_type() != Grounds.Soil:
		till()
	plant_and_reroll_to_15()

i = 0
while num_items(Items.Power) < TARGET:
	pos = positions[i % N]
	i = i + 1
	move_to(pos[0], pos[1])
	h = can_harvest()
	while not h and num_items(Items.Power) < TARGET:
		h = can_harvest()
	if num_items(Items.Power) >= TARGET:
		break
	harvest()
	if num_items(Items.Power) >= TARGET:
		break
	plant_and_reroll_to_15()

quick_print("DONE", "POWER", num_items(Items.Power), "TICK_FINAL", get_tick_count(),
	"TIME_FINAL", get_time())
