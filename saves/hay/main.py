import Common

# exp-hay-076 -- fix the setup/spawn phase's movement, not the hot loop.
# User-flagged, both real: (1) the initial long walk from each drone's
# spawn point to its own base tile used Common.move_to() -- the
# UNWRAPPED version -- which always takes the direct path even when the
# wrapped path is much shorter; with drones at 3..28 on a 32-wide farm,
# some assignments are exactly this bad. (2) move_to() also carries a
# leftover `protocol()` parameter (an indirect call, p_noop by default)
# and a num_unlocked(Unlocks.Mazes) check, both evaluated on every move,
# for a maze-avoidance feature this category never uses.
# move_to_wrapped() has neither problem. Switched every Common.move_to()
# call in driver() to Common.move_to_wrapped() -- a strict improvement
# here since Hay never needs maze-aware movement.
#
# Setup-phase cost, not per-harvest -- doesn't show in the single-drone
# smoke-test methodology (068-075), which starts measuring after setup
# completes. Its effect is on real score directly: "repeat until 2h
# simulated time, average the runs" means setup is paid again every
# repeat, not amortized away by one very long run.
#
# 073's spawn pattern (one drone sequentially spawns all 31 others,
# ~6200 ticks of pure spawn latency before the last drone even starts)
# is a separate, real inefficiency flagged in the same review --
# deferred, not fixed here: a tree-spawn redesign needs its own
# correctness validation (every position covered exactly once) that
# doesn't fit safely in the time available for this pass.

TARGET = 2000000000
REROLL_LIMIT = 30
WATER_THRESHOLD = 0.75
entity = Entities.Grass
instructions = Common.get_planting_instructions(entity)

HOLES = [(1, 1), (1, 4), (4, 1), (4, 4)]

ALL_BASES = [(3, 3)]
for i in range(6):
	for j in range(6):
		if i + j != 0:
			if (i, j) not in HOLES:
				ALL_BASES.append((3 + i * 5, 3 + j * 5))

ALL_CROPS = {}
for base in ALL_BASES:
	bx, by = base
	ALL_CROPS[(bx, by)] = True
	ALL_CROPS[(bx + 1, by)] = True

def wdist(ax, ay, bx, by, size):
	dx = min((bx - ax) % size, (ax - bx) % size)
	dy = min((by - ay) % size, (ay - by) % size)
	return dx + dy

def driver(bx, by):
	size = get_world_size()
	c1x, c1y = bx, by
	c2x, c2y = bx + 1, by

	Common.move_to_wrapped(c1x, c1y)
	instructions()
	Common.move_to_wrapped(c2x, c2y)
	instructions()

	planted = {}
	for dx in range(-3, 5):
		for dy in range(-3, 4):
			px = (c1x + dx) % size
			py = (c1y + dy) % size
			if (px, py) in ALL_CROPS:
				continue
			d1 = wdist(c1x, c1y, px, py, size)
			d2 = wdist(c2x, c2y, px, py, size)
			if d1 <= 3 or d2 <= 3:
				Common.move_to_wrapped(px, py)
				if get_entity_type() != Entities.Bush:
					if get_entity_type() != None:
						harvest()
					Common.plant_companion(Entities.Bush)
				planted[(px, py)] = Entities.Bush
	Common.move_to_wrapped(c1x, c1y)

	current_is_c1 = True
	while num_items(Items.Hay) < TARGET:
		while num_items(Items.Water) > 0 and get_water() < WATER_THRESHOLD:
			use_item(Items.Water)
		h = can_harvest()
		while not h and num_items(Items.Hay) < TARGET:
			while num_items(Items.Water) > 0 and get_water() < WATER_THRESHOLD:
				use_item(Items.Water)
			h = can_harvest()
		if num_items(Items.Hay) >= TARGET:
			break
		harvest()

		rerolls = 0
		companion = get_companion()
		while rerolls < REROLL_LIMIT and companion != None:
			ctype, (cx, cy) = companion
			key = (cx, cy)
			if key in planted and planted[key] == ctype:
				break
			harvest()
			companion = get_companion()
			rerolls = rerolls + 1

		if num_items(Items.Hay) >= TARGET:
			break
		if current_is_c1:
			move(East)
		else:
			move(West)
		current_is_c1 = not current_is_c1

clear()
quick_print("FARM", "world", get_world_size(), "max_drones", max_drones())
drones = []
for i in range(6):
	for j in range(6):
		if i + j != 0:
			if (i, j) not in HOLES:
				d = spawn_drone(driver, 3 + i * 5, 3 + j * 5)
				if d:
					drones.append(d)
quick_print("SPAWNED", len(drones) + 1, "of", max_drones())
driver(3, 3)
for d in drones:
	wait_for(d)
