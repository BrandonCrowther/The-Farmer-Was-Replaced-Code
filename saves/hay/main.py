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

# exp-hay-077 -- spawn-tree parallelization. 076 fixed the setup-phase
# WALK; this fixes the setup-phase SPAWN. The old loop had one drone
# call spawn_drone() 31 times in a row before it ever started farming
# (measured live, probe: 200 ticks/call flat, 6745 ticks total for the
# real 31-call loop with its overhead -- exp-hay-077/result.md). Every
# one of those ticks is paid again every ~2h-simulated repeat the score
# averages over, same "setup isn't amortized" point 076 made.
#
# Fix: a binary spawn tree. spawn_group(positions) is handed a list of
# base tiles; it keeps positions[0] as ITS OWN tile, splits the rest in
# half, and spawns at most two new drones -- one per half -- each of
# which repeats the same pattern before it starts farming. Depth is
# ceil(log2(32)) = 5, so no drone waits on more than 2 sequential
# spawn_drone() calls per level of the tree it sits at (<=10 calls, ~5
# levels x 2 children), instead of up to 31 sequential calls in the old
# design -- and every level's drones spawn their own children truly
# concurrently with each other (043 confirmed tick rate is identical
# regardless of drone count, i.e. drones really do run in parallel, not
# time-sliced against each other).
def spawn_group(positions):
	my_pos = positions[0]
	rest = positions[1:]
	n = len(rest)
	mid = n // 2
	spawned = []
	if mid > 0:
		d = spawn_drone(spawn_group, rest[:mid])
		if d:
			spawned.append(d)
	if n - mid > 0:
		d = spawn_drone(spawn_group, rest[mid:])
		if d:
			spawned.append(d)
	bx, by = my_pos
	driver(bx, by)
	for d in spawned:
		wait_for(d)

clear()
quick_print("FARM", "world", get_world_size(), "max_drones", max_drones())
rest = ALL_BASES[1:]
n = len(rest)
mid = n // 2
drones = []
if mid > 0:
	d = spawn_drone(spawn_group, rest[:mid])
	if d:
		drones.append(d)
if n - mid > 0:
	d = spawn_drone(spawn_group, rest[mid:])
	if d:
		drones.append(d)
quick_print("SPAWNED_ROOT_CHILDREN", len(drones))
driver(3, 3)
for d in drones:
	wait_for(d)
