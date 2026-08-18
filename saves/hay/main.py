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
# the spawn-tree helpers below).
#
# exp-hay-079 -- a code scour for the same class of stray-tick overhead
# 075/076/077 already found, this time inside driver() itself:
# (1) reroll chase: `planted[key] == ctype` did a SECOND tuple-keyed
#     dict lookup (~2 ticks) to re-derive a value that has exactly one
#     write site in this whole file, always Entities.Bush -- there is
#     no second value it can ever hold, so the lookup was re-deriving a
#     compile-time constant at runtime. Compare `ctype` to the constant
#     directly instead; this runs on every reroll attempt (avg ~2/
#     harvest per 069's p=1/3 model), so it is the one change here that
#     actually touches the ~871-harvest/drone hot loop rather than the
#     one-time setup phase.
# (2) bush-wall setup: `d2 = wdist(...)` was computed unconditionally
#     even though `d1 <= 3 or d2 <= 3` only needs d2 when d1 already
#     misses (or short-circuits) -- wdist() costs ~11 ticks/call (2
#     subtractions + 2 mods + a min() per axis, +1 to sum), paid on
#     every one of the ~54 candidate positions per drone regardless of
#     whether d1 alone already qualified.
# (3) bush-wall setup: `get_entity_type()` (a 1-tick getter) was called
#     twice per position instead of cached in a local.
#
# exp-hay-081 -- removed a third, redundant num_items(Items.Hay)>=TARGET
# check per hot-loop iteration that only guarded the cheap move() call.
#
# exp-hay-082 -- reordered the water-check `and` so its usually-False
# operand (get_water() < WATER_THRESHOLD) is checked first, letting the
# `and` short-circuit past num_items() on the ~98% of iterations that
# don't need a top-up.
#
# exp-hay-084 -- reroll chase: bind `ctype, pos = companion` directly
# instead of destructuring cx,cy and rebuilding an identical tuple; and
# check `ctype == Entities.Bush` before `pos in planted` so `and` skips
# the dict lookup on the 2/3 of attempts that aren't even a Bush.
#
# exp-hay-085 -- setup phase: build `pos = (px, py)` once and reuse it
# for both the ALL_CROPS check and the planted-dict write, instead of
# two fresh tuple literals.
#
# exp-hay-086 -- shared bush-wall territory partitioning.
#
# User-raised: every drone independently walks and companion-plants its
# *entire* ~54-position candidate window, even though 079/080's own
# analysis (and a direct offline replication of this file's near-check
# logic, see the session's scratch notes) shows 204 of the 960 total
# per-drone candidate visits across the whole farm are pairwise
# redundant -- two adjacent drones each walking to and planting the
# same shared tile. 078 tried a version of this idea and was rejected:
# it had no execution-order guarantee, so a drone's hot loop could ask
# for a companion on a tile a neighbor hadn't planted yet and silently
# lose the multiplier -- a race, not a partition.
#
# Fix here is a genuine partition plus a genuine barrier, not a trust
# shortcut:
#   1. Ownership is decided once, offline (not at runtime -- see below),
#      by a directional, wraparound-aware tie-break: for any position
#      reachable by exactly two bases, the base to its East owns it (or
#      North, for a same-x pair), using `(ax - bx) % size <= size // 2`
#      to stay well-defined across the world's wraparound seam too. No
#      position in this farm's layout is ever reachable by 3+ bases
#      (confirmed by direct enumeration), so this tie-break fully
#      resolves every position to exactly one owner. OWNED_OFFSETS below
#      is that resolution, as (dx, dy) offsets relative to each base's
#      own (bx, by), in ALL_BASES order.
#   2. A drone plants ONLY its own OWNED_OFFSETS positions during setup
#      -- roughly 3/4 of what it walked before, the other ~1/4 now
#      planted once by whichever neighbor owns it instead of twice.
#   3. Two full, sequential spawn trees enforce the barrier a runtime
#      trust shortcut can't provide: `setup_group` spawns and joins
#      ALL 32 drones doing ONLY their owned planting (root's own
#      `wait_for` loop, by construction, cannot return until every
#      single one of them -- including any owner of any position ANY
#      drone will later read -- has finished planting). Only after that
#      full join does a SECOND, fresh spawn tree (`hotloop_group`) start
#      anyone's hot loop. Every drone's hot loop still builds its own
#      *full* candidate-window `planted` dict exactly as before (084/
#      085's logic, unchanged) -- it just never re-walks to verify,
#      because the barrier already guarantees every position in that
#      window is Bush by the time any hot loop can possibly run.
#
# Why OWNED_OFFSETS is a hardcoded literal and not computed at runtime:
# an early version of this experiment built the ownership map with a
# nested loop + dict, live, and measured (probe, see scratch notes)
# 68,447 ticks for the naive version and an analytically-estimated
# still-substantial cost even for a stripped-down dict-only rebuild --
# a one-time, unavoidable cost eating directly into the walk savings
# this experiment exists to capture, on EVERY repeat the score averages
# over. But the ownership result is a fixed property of this farm's
# fixed layout (32 fixed bases, fixed HOLES, fixed spacing) -- it never
# changes between runs, so there is no reason to ever pay to compute it
# live at all. Per Operation-Costs.md, list/dict LITERALS cost only
# "N + cost of each item" (cheap); it's *building* one via a loop of
# .append() calls that's expensive. OWNED_OFFSETS is generated once
# offline (script in the session's scratch notes) and verified there:
# every offset is a real candidate of its own base (subset check),
# zero positions double-owned across all 32 bases, and the full union
# covers exactly 756 unique positions -- an exact match to this farm's
# real total bush-wall coverage, confirming nothing is dropped.

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

# Hand-derived and verified offline -- see the exp-086 header comment
# above for the tie-break rule and the verification checks. Index N
# here corresponds to ALL_BASES[N] (same construction order, checked
# by hand against this file's own ALL_BASES loop).
OWNED_OFFSETS = [
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(1,-3),(1,-2),(1,-1),(1,1),(2,-2),(2,-1),(2,1),(2,2)],  # base 0 (3, 3)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(1,-3),(1,-2),(1,-1),(1,1),(2,-2),(2,-1),(2,0),(2,1),(2,2),(3,-1),(3,0),(3,1),(4,0)],  # base 1 (3, 8)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(1,-3),(1,-2),(1,-1),(1,1),(2,-2),(2,-1),(2,1),(2,2)],  # base 2 (3, 13)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(1,-3),(1,-2),(1,-1),(1,1),(2,-2),(2,-1),(2,1),(2,2)],  # base 3 (3, 18)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(1,-3),(1,-2),(1,-1),(1,1),(2,-2),(2,-1),(2,0),(2,1),(2,2),(3,-1),(3,0),(3,1),(4,0)],  # base 4 (3, 23)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(0,2),(0,3),(1,-3),(1,-2),(1,-1),(1,1),(1,2),(1,3),(2,-2),(2,-1),(2,1),(2,2)],  # base 5 (3, 28)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(0,2),(0,3),(1,-3),(1,-2),(1,-1),(1,1),(1,2),(1,3),(2,-2),(2,-1),(2,1),(2,2)],  # base 6 (8, 3)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(1,-3),(1,-2),(1,-1),(1,1),(2,-2),(2,-1),(2,1),(2,2)],  # base 7 (8, 13)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(0,2),(0,3),(1,-3),(1,-2),(1,-1),(1,1),(1,2),(1,3),(2,-2),(2,-1),(2,1),(2,2)],  # base 8 (8, 18)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(0,2),(0,3),(1,-3),(1,-2),(1,-1),(1,1),(1,2),(1,3),(2,-2),(2,-1),(2,1),(2,2)],  # base 9 (8, 28)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(1,-3),(1,-2),(1,-1),(1,1),(2,-2),(2,-1),(2,1),(2,2)],  # base 10 (13, 3)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(1,-3),(1,-2),(1,-1),(1,1),(2,-2),(2,-1),(2,1),(2,2)],  # base 11 (13, 8)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(1,-3),(1,-2),(1,-1),(1,1),(2,-2),(2,-1),(2,1),(2,2)],  # base 12 (13, 13)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(1,-3),(1,-2),(1,-1),(1,1),(2,-2),(2,-1),(2,1),(2,2)],  # base 13 (13, 18)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(1,-3),(1,-2),(1,-1),(1,1),(2,-2),(2,-1),(2,1),(2,2)],  # base 14 (13, 23)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(0,2),(0,3),(1,-3),(1,-2),(1,-1),(1,1),(1,2),(1,3),(2,-2),(2,-1),(2,1),(2,2)],  # base 15 (13, 28)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(1,-3),(1,-2),(1,-1),(1,1),(2,-2),(2,-1),(2,1),(2,2)],  # base 16 (18, 3)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(1,-3),(1,-2),(1,-1),(1,1),(2,-2),(2,-1),(2,0),(2,1),(2,2),(3,-1),(3,0),(3,1),(4,0)],  # base 17 (18, 8)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(1,-3),(1,-2),(1,-1),(1,1),(2,-2),(2,-1),(2,1),(2,2)],  # base 18 (18, 13)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(1,-3),(1,-2),(1,-1),(1,1),(2,-2),(2,-1),(2,1),(2,2)],  # base 19 (18, 18)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(1,-3),(1,-2),(1,-1),(1,1),(2,-2),(2,-1),(2,0),(2,1),(2,2),(3,-1),(3,0),(3,1),(4,0)],  # base 20 (18, 23)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(0,2),(0,3),(1,-3),(1,-2),(1,-1),(1,1),(1,2),(1,3),(2,-2),(2,-1),(2,1),(2,2)],  # base 21 (18, 28)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(0,2),(0,3),(1,-3),(1,-2),(1,-1),(1,1),(1,2),(1,3),(2,-2),(2,-1),(2,1),(2,2)],  # base 22 (23, 3)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(1,-3),(1,-2),(1,-1),(1,1),(2,-2),(2,-1),(2,1),(2,2)],  # base 23 (23, 13)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(0,2),(0,3),(1,-3),(1,-2),(1,-1),(1,1),(1,2),(1,3),(2,-2),(2,-1),(2,1),(2,2)],  # base 24 (23, 18)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(0,2),(0,3),(1,-3),(1,-2),(1,-1),(1,1),(1,2),(1,3),(2,-2),(2,-1),(2,1),(2,2)],  # base 25 (23, 28)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(1,-3),(1,-2),(1,-1),(1,1),(2,-2),(2,-1),(2,0),(2,1),(2,2),(3,-1),(3,0),(3,1)],  # base 26 (28, 3)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(1,-3),(1,-2),(1,-1),(1,1),(2,-2),(2,-1),(2,0),(2,1),(2,2),(3,-1),(3,0),(3,1)],  # base 27 (28, 8)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(1,-3),(1,-2),(1,-1),(1,1),(2,-2),(2,-1),(2,0),(2,1),(2,2),(3,-1),(3,0),(3,1)],  # base 28 (28, 13)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(1,-3),(1,-2),(1,-1),(1,1),(2,-2),(2,-1),(2,0),(2,1),(2,2),(3,-1),(3,0),(3,1)],  # base 29 (28, 18)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(1,-3),(1,-2),(1,-1),(1,1),(2,-2),(2,-1),(2,0),(2,1),(2,2),(3,-1),(3,0),(3,1)],  # base 30 (28, 23)
	[(-3,0),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-3),(0,-2),(0,-1),(0,1),(0,2),(0,3),(1,-3),(1,-2),(1,-1),(1,1),(1,2),(1,3),(2,-2),(2,-1),(2,0),(2,1),(2,2),(3,-1),(3,0),(3,1)],  # base 31 (28, 28)
]

def wdist(ax, ay, bx, by, size):
	dx = min((bx - ax) % size, (ax - bx) % size)
	dy = min((by - ay) % size, (ay - by) % size)
	return dx + dy

# Phase 1 (setup-only): plant ONLY this base's owned positions, plus
# its own two Grass tiles. Never touches the hot loop or `planted`.
def setup_only(idx):
	bx, by = ALL_BASES[idx]
	size = get_world_size()
	c1x, c1y = bx, by
	c2x, c2y = bx + 1, by

	Common.move_to_wrapped(c1x, c1y)
	instructions()
	Common.move_to_wrapped(c2x, c2y)
	instructions()

	for offset in OWNED_OFFSETS[idx]:
		odx, ody = offset
		px = (bx + odx) % size
		py = (by + ody) % size
		Common.move_to_wrapped(px, py)
		et = get_entity_type()
		if et != Entities.Bush:
			if et != None:
				harvest()
			Common.plant_companion(Entities.Bush)

# Phase 2 (hot loop): identical to 085's driver(), except the setup
# walk/plant loop is gone -- `planted` is still built from this base's
# FULL candidate window (own positions plus shared ones a neighbor may
# own), exactly as before, but every one of those positions is
# guaranteed already Bush by construction (Phase 1 fully joined before
# any Phase 2 drone could start), so no per-position walk or
# get_entity_type()/plant_companion() call is needed here at all.
def driver(idx):
	bx, by = ALL_BASES[idx]
	size = get_world_size()
	c1x, c1y = bx, by
	c2x, c2y = bx + 1, by

	planted = {}
	for dx in range(-3, 5):
		for dy in range(-3, 4):
			px = (c1x + dx) % size
			py = (c1y + dy) % size
			pos = (px, py)
			if pos in ALL_CROPS:
				continue
			near = wdist(c1x, c1y, px, py, size) <= 3
			if not near:
				near = wdist(c2x, c2y, px, py, size) <= 3
			if near:
				planted[pos] = Entities.Bush
	Common.move_to_wrapped(c1x, c1y)

	current_is_c1 = True
	while num_items(Items.Hay) < TARGET:
		while get_water() < WATER_THRESHOLD and num_items(Items.Water) > 0:
			use_item(Items.Water)
		h = can_harvest()
		while not h and num_items(Items.Hay) < TARGET:
			while get_water() < WATER_THRESHOLD and num_items(Items.Water) > 0:
				use_item(Items.Water)
			h = can_harvest()
		if num_items(Items.Hay) >= TARGET:
			break
		harvest()

		rerolls = 0
		companion = get_companion()
		while rerolls < REROLL_LIMIT and companion != None:
			ctype, pos = companion
			if ctype == Entities.Bush and pos in planted:
				break
			harvest()
			companion = get_companion()
			rerolls = rerolls + 1

		if current_is_c1:
			move(East)
		else:
			move(West)
		current_is_c1 = not current_is_c1

# Binary spawn tree over a list of ALL_BASES indices (not positions --
# 086 threads the index itself through, since both setup_only() and
# driver() need it to look up OWNED_OFFSETS/ALL_BASES). Same shape as
# 077's spawn_group(), used twice: once for the setup-only tree, once
# for the fresh hot-loop tree.
def setup_group(indices):
	my_idx = indices[0]
	rest = indices[1:]
	n = len(rest)
	mid = n // 2
	spawned = []
	if mid > 0:
		d = spawn_drone(setup_group, rest[:mid])
		if d:
			spawned.append(d)
	if n - mid > 0:
		d = spawn_drone(setup_group, rest[mid:])
		if d:
			spawned.append(d)
	setup_only(my_idx)
	for d in spawned:
		wait_for(d)

def hotloop_group(indices):
	my_idx = indices[0]
	rest = indices[1:]
	n = len(rest)
	mid = n // 2
	spawned = []
	if mid > 0:
		d = spawn_drone(hotloop_group, rest[:mid])
		if d:
			spawned.append(d)
	if n - mid > 0:
		d = spawn_drone(hotloop_group, rest[mid:])
		if d:
			spawned.append(d)
	driver(my_idx)
	for d in spawned:
		wait_for(d)

clear()
quick_print("FARM", "world", get_world_size(), "max_drones", max_drones())

ALL_INDICES = []
for i in range(len(ALL_BASES)):
	ALL_INDICES.append(i)

rest = ALL_INDICES[1:]
n = len(rest)
mid = n // 2

# Phase 1: setup only. Root's own wait_for loop cannot return until
# EVERY drone in the tree (root included) has finished its own owned
# planting -- the barrier that makes Phase 2's trust-without-walking
# safe.
setup_drones = []
if mid > 0:
	d = spawn_drone(setup_group, rest[:mid])
	if d:
		setup_drones.append(d)
if n - mid > 0:
	d = spawn_drone(setup_group, rest[mid:])
	if d:
		setup_drones.append(d)
setup_only(0)
for d in setup_drones:
	wait_for(d)
quick_print("PHASE1_DONE", "tick", get_tick_count())

# Phase 2: a completely fresh spawn tree for the hot loop. Every one of
# these drones' own driver() call moves to its own c1 first, same as
# before -- unaffected by wherever this fresh spawn chain happens to
# place it.
hotloop_drones = []
if mid > 0:
	d = spawn_drone(hotloop_group, rest[:mid])
	if d:
		hotloop_drones.append(d)
if n - mid > 0:
	d = spawn_drone(hotloop_group, rest[mid:])
	if d:
		hotloop_drones.append(d)
driver(0)
for d in hotloop_drones:
	wait_for(d)
