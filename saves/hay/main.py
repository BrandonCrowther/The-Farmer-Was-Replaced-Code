import Common

# exp-hay-043 -- tick-rate-check
#
# 041 measured Hay's real growth-to-ripe time at ~1,183 ticks -- nearly 3x
# hay_single's directly-measured ~404 ticks, for the same crop (Grass) at
# similar water levels. That gap is too large to explain by water alone
# (linear 1x-5x, and both categories run near the top of that range). If
# the *tick rate* (ticks per simulated second) is lower with 32 concurrent
# drones than solo -- e.g. a shared "Power"/compute budget divided among
# active drones -- that would explain the gap directly, and would also
# reframe 039's leader-implied ~441-ticks/harvest figure: the leader might
# not be doing fewer ticks of *work* per harvest, but running at a higher
# tick rate from using fewer concurrent drones.
#
# Measures get_time()/get_tick_count() deltas over an identical, fixed
# sequence of operations, first solo (no other drones spawned), then again
# with all 31 others spawned and farming normally. A leaderboard run does
# NOT end when the main entry function returns -- it stays "running" while
# any spawned drone is still executing, even unreaped (learned the hard
# way: an earlier version of this probe spawned drones in an unbounded
# `while True` and the run never ended on its own; Shift+F5 does not stop
# a leaderboard run either, confirming docs/LOOP.md's own warning -- a
# relaunch was the only way out). So each spawned drone here does a small,
# *bounded* number of cycles and returns, and they are reaped with
# wait_for() before the script ends. Expect "Run Failed" (target not
# reached); the duration is not a score.

clear()

def measure(label):
	t0 = get_time()
	k0 = get_tick_count()
	for i in range(20):
		move(East)
		move(West)
	t1 = get_time()
	k1 = get_tick_count()
	dk = k1 - k0
	dt = t1 - t0
	rate = -1
	if dt > 0:
		rate = dk / dt
	quick_print(label, "DTICK", dk, "DTIME", dt, "RATE", rate)

quick_print("FARM", "world", get_world_size(), "max_drones", max_drones())
measure("SOLO")

entity = Entities.Grass
instructions = Common.get_planting_instructions(entity)

def driver(x, y):
	Common.move_to(x, y)
	instructions()
	planted = {}
	for i in range(5):
		while num_items(Items.Water) > 0 and get_water() < 0.75:
			use_item(Items.Water)
		Common.polyculture_mapped(planted)
		h = can_harvest()
		while not h:
			h = can_harvest()
		harvest()
		instructions()

HOLES = [(1, 1), (1, 4), (4, 1), (4, 4)]
drones = []
for i in range(6):
	for j in range(6):
		if i + j != 0:
			if (i, j) not in HOLES:
				d = spawn_drone(driver, 3 + i * 5, 3 + j * 5)
				if d:
					drones.append(d)
quick_print("SPAWNED", len(drones) + 1, "of", max_drones())
measure("SWARM32")
for d in drones:
	wait_for(d)
