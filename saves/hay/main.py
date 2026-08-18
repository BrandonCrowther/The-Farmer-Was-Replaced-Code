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
# 073's spawn pattern (one drone sequentially spawning all 31 others)
# was the same class of issue -- fixed separately in exp-077 (see
# spawn_group() below).
#
# exp-hay-079 -- a code scour for the same class of stray-tick overhead
# 075/076/077 already found, this time inside driver() itself:
# (1) reroll chase: `planted[key] == ctype` did a SECOND tuple-keyed
#     dict lookup (~2 ticks) to re-derive a value that has exactly one
#     write site in this whole file (line ~80, always Entities.Bush) --
#     there is no second value it can ever hold, so the lookup was
#     re-deriving a compile-time constant at runtime. Compare `ctype`
#     to the constant directly instead; this runs on every reroll
#     attempt (avg ~2/harvest per 069's p=1/3 model), so it is the one
#     change here that actually touches the ~871-harvest/drone hot loop
#     rather than the one-time setup phase.
# (2) bush-wall setup: `d2 = wdist(...)` was computed unconditionally
#     even though `d1 <= 3 or d2 <= 3` only needs d2 when d1 already
#     misses (or short-circuits) -- wdist() costs ~11 ticks/call (2
#     subtractions + 2 mods + a min() per axis, +1 to sum), paid on
#     every one of the ~54 candidate positions per drone regardless of
#     whether d1 alone already qualified.
# (3) bush-wall setup: `get_entity_type()` (a 1-tick getter) was called
#     twice per position instead of cached in a local.
# All three are provable from reading the code alone (single write
# site for `planted`'s value; `or`'s short-circuit is a documented
# language rule; a cached getter read is definitionally identical to
# two reads of state nothing between them mutates) -- no new game
# mechanic assumed, unlike 078's rejected territory-partitioning idea.

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
			# exp-hay-079 -- d2 is only needed when d1 already misses (d1<=3
			# is or'd with d2<=3, and or short-circuits) -- but the old code
			# built the args in application order so both wdist() calls
			# (11 ticks each: 2 subs + 2 mods + a min() per axis, +1 to sum)
			# ran on every position regardless. Compute d1 first and skip
			# d2 entirely once it already qualifies.
			near = wdist(c1x, c1y, px, py, size) <= 3
			if not near:
				near = wdist(c2x, c2y, px, py, size) <= 3
			if near:
				Common.move_to_wrapped(px, py)
				# exp-hay-079 -- get_entity_type() is a getter (1 tick);
				# the old code called it twice (once per if) instead of
				# caching the one read it needs.
				et = get_entity_type()
				if et != Entities.Bush:
					if et != None:
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
			# exp-hay-079 -- `planted` has exactly one call site that ever
			# writes to it (the bush-wall setup above) and it always
			# writes Entities.Bush -- there is no second value the dict
			# can ever hold. So "planted[key] == ctype" was a second
			# tuple-keyed dict lookup (~2 ticks) to re-derive a constant;
			# comparing ctype to the constant directly costs 1 tick and
			# needs no second lookup at all.
			if key in planted and ctype == Entities.Bush:
				break
			harvest()
			companion = get_companion()
			rerolls = rerolls + 1

		# exp-hay-081 -- this was the THIRD num_items(Items.Hay)>=TARGET
		# check per iteration (outer `while`'s own condition, the one
		# above guarding harvest()/the reroll chase, and this one), each
		# 3 ticks (if-entry + getter + compare) every single iteration
		# regardless of whether target is anywhere close -- ~2600
		# ticks/drone recurring over 871 harvests. Removed this one,
		# which only guarded the cheap move() call: worst case, a
		# straggler drone that misses the shared target being hit by
		# someone else during its own reroll chase pays one extra
		# 200-tick move before the outer while's own check catches it
		# next iteration -- bounded, one-time, and only possible at all
		# in the last iteration of the whole run. Kept the check above
		# (before harvest()/the reroll chase): that one guards much more
		# expensive work (a full harvest + up to REROLL_LIMIT more), a
		# worse thing to risk overshooting.
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
