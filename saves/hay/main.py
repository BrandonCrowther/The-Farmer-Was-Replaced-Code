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

# exp-hay-088 -- offset + row-stagger base grid (see 088's own comment
# history for the original reasoning: every drone spawns at (0,0), so
# walk-in is wdist((0,0), base), and the old offset(3,3)/spacing(5,5)
# grid centered its footprint on the farthest point from the origin).
#
# exp-hay-090 -- 088's own stagger search was incomplete: it only tried
# staggering the X coordinate per alternating row. A fair search that
# also tries staggering Y per alternating column finds the true
# optimum for this domino shape is better than what 088 found --
# 336 total walk-in / 19 max vs 088's 384/21 (-12.5%/-9.5%), same
# horizontal-domino shape, zero new geometric risk. (A diagonal domino
# shape was also checked and does not beat this: identical scan/window
# cost to horizontal, but a worse achievable walk-in optimum -- see
# experiments/hay/090/hypothesis.md.) Re-verified exhaustively: 32
# unique positions, 64 unique crop tiles, global minimum cross-base
# crop distance still exactly 4 (this session's measured safe floor,
# same margin as 088, not tighter), uniform 30-position windows.
X_OFFSET = 23
Y_OFFSET = 22
X_SPACING = 3
Y_SPACING = 4
COL_STAGGER = 2

ALL_BASES = [(X_OFFSET, Y_OFFSET)]
for i in range(6):
	for j in range(6):
		if i + j != 0:
			if (i, j) not in HOLES:
				bx = X_OFFSET + i * X_SPACING
				by = Y_OFFSET + j * Y_SPACING
				if i % 2 == 1:
					by = by + COL_STAGGER
				ALL_BASES.append((bx % 32, by % 32))

# exp-hay-091 -- ALL_CROPS (every base's own two crop tiles) existed
# only to filter the setup scan's raster-order window down to the 30
# candidate positions. SCAN_ORDER now encodes that filtering offline,
# so nothing reads ALL_CROPS anymore -- building it live was pure
# wasted setup-phase work once the scan stopped needing it.

def wdist(ax, ay, bx, by, size):
	dx = min((bx - ax) % size, (ax - bx) % size)
	dy = min((by - ay) % size, (ay - by) % size)
	return dx + dy

# exp-hay-091 -- the setup-phase candidate-window scan (30 tiles,
# translation-invariant -- same relative shape for every base) was
# always walked in raster order (dx outer, dy inner), computing near()
# at runtime. Nobody had ever asked whether raster order minimizes the
# total WALKING DISTANCE between consecutive tiles -- it doesn't.
# Offline TSP-style search (greedy nearest-neighbor + 2-opt + or-opt,
# 30 seeds, experiments/hay/091/hypothesis.md) found a visiting order
# with total path cost 36 tiles (c1 -> ... -> c1) vs raster's 62 -- a
# 42% cut in pure movement distance, sanity-checked against a
# minimum-spanning-tree lower bound (30) to confirm it's close to
# optimal, not a lucky first find. Live-calibrated against the real
# champion before committing: measured move-only cost is a flat 12,482
# ticks/drone across all 32 drones, matching the raster model (12,400)
# almost exactly -- the reordered model's 7,200-tick prediction is
# equally trustworthy. Hardcoded as a static, offline-verified list
# (same "never compute it live" pattern as ALL_BASES/OWNED_OFFSETS) --
# exactly the same 30-position SET as the raster scan (verified:
# set(SCAN_ORDER) == the raster-order set, no position added or
# dropped), so the near()/ALL_CROPS runtime checks are no longer
# needed at all -- the list already encodes them.
SCAN_ORDER = [(-1, 0), (-2, 0), (-3, 0), (-2, -1), (-1, -1), (-1, -2),
	(0, -2), (0, -3), (1, -3), (1, -2), (2, -2), (2, -1), (2, 0), (2, 1),
	(2, 2), (1, 2), (1, 3), (0, 3), (0, 2), (-1, 2), (-1, 1), (-2, 1),
	(0, 1), (1, 1), (3, 1), (3, 0), (4, 0), (3, -1), (1, -1), (0, -1)]

def driver(bx, by):
	size = get_world_size()
	c1x, c1y = bx, by
	c2x, c2y = bx + 1, by

	Common.move_to_wrapped(c1x, c1y)
	instructions()
	Common.move_to_wrapped(c2x, c2y)
	instructions()

	planted = {}
	# exp-hay-091 -- iterate the precomputed distance-minimizing order
	# directly. No near()/ALL_CROPS check needed -- SCAN_ORDER already
	# is exactly the 30-position set those checks used to filter down
	# to, in an order chosen to minimize total move_to_wrapped() cost
	# between consecutive tiles.
	for offset in SCAN_ORDER:
		odx, ody = offset
		px = (c1x + odx) % size
		py = (c1y + ody) % size
		pos = (px, py)
		Common.move_to_wrapped(px, py)
		# exp-hay-079 -- get_entity_type() is a getter (1 tick); the old
		# code called it twice (once per if) instead of caching the one
		# read it needs.
		et = get_entity_type()
		if et != Entities.Bush:
			if et != None:
				harvest()
			Common.plant_companion(Entities.Bush)
		planted[pos] = Entities.Bush
	Common.move_to_wrapped(c1x, c1y)

	current_is_c1 = True
	while num_items(Items.Hay) < TARGET:
		# exp-hay-082 -- `num_items(Items.Water) > 0` is checked first in
		# the original ordering, but water is genuinely fine here (046/047:
		# real water sits 0.8-1.0), so that operand is almost always True
		# and `and` never short-circuits on it -- both getters pay every
		# iteration. get_water() < WATER_THRESHOLD is the operand that's
		# usually False (072 measured only 16/871 cycles actually needing
		# a top-up), so putting IT first lets `and` short-circuit and skip
		# num_items() entirely on the ~98% of iterations that don't need
		# water -- same two getters, same safety guarantee (num_items is
		# still checked before any use_item() call happens), just
		# reordered for the case that's actually common.
		while get_water() < WATER_THRESHOLD and num_items(Items.Water) > 0:
			use_item(Items.Water)
		h = can_harvest()
		while not h and num_items(Items.Hay) < TARGET:
			# exp-hay-082 -- same reorder as above, for the same reason.
			while get_water() < WATER_THRESHOLD and num_items(Items.Water) > 0:
				use_item(Items.Water)
			h = can_harvest()
		if num_items(Items.Hay) >= TARGET:
			break
		harvest()

		rerolls = 0
		companion = get_companion()
		while rerolls < REROLL_LIMIT and companion != None:
			# exp-hay-079 -- `planted` has exactly one call site that ever
			# writes to it (the bush-wall setup above) and it always
			# writes Entities.Bush -- there is no second value the dict
			# can ever hold. So "planted[key] == ctype" was a second
			# tuple-keyed dict lookup (~2 ticks) to re-derive a constant;
			# comparing ctype to the constant directly costs 1 tick and
			# needs no second lookup at all.
			#
			# exp-hay-084 -- two more in the same spot, missed in 079:
			# (1) `cx, cy = companion[1]` was unpacked only to be
			# immediately repacked into `key = (cx, cy)` -- an identical
			# tuple to the one already sitting inside `companion`, and
			# cx/cy are never used for anything else. Bind the position
			# directly (`ctype, pos = companion`) instead of destructuring
			# and rebuilding it -- free unpack either way, but this skips
			# the 1-tick tuple-literal rebuild entirely.
			# (2) the `and` was ordered so its almost-always-True operand
			# (`key in planted` -- coverage is nearly total) went first,
			# so `and` almost never short-circuited: both operands paid
			# on nearly every attempt. `ctype == Entities.Bush` is False
			# 2/3 of the time (uniform 1/3 draw, 069) -- checking it first
			# lets `and` skip the tuple-keyed dict lookup (~2 ticks) on
			# 2/3 of attempts, the same reorder-for-short-circuit trick
			# 082 used for the water check.
			ctype, pos = companion
			if ctype == Entities.Bush and pos in planted:
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
# exp-hay-088 -- root's own base is ALL_BASES[0] (X_OFFSET, Y_OFFSET),
# not the old hardcoded (3, 3).
root_bx, root_by = ALL_BASES[0]
driver(root_bx, root_by)
for d in drones:
	wait_for(d)
