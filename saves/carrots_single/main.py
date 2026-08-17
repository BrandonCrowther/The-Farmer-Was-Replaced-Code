import Common

# exp-carrots_single-007 -- 5-tile reroll pipeline probe
#
# Combines 004's multi-tile pipelining (growth-bound single tile -> hide
# idle time behind other tiles' handling) with 006's reroll-before-walk
# (companion preference is fixed at plant time, so a cheap reroll beats
# a walk-and-service round trip most of the time). 006 measured
# single-tile handling at ~1,571 ticks (idle subtracted) vs 003's
# walk-always ~2,422 -- the idle-elimination crossing point N >=
# growth/handling moves from 004's N~2.23 to N~4.58, so 5 tiles (not 3)
# are needed to fully hide ~7,196-tick growth behind this cheaper
# handling. Tiles are spaced pairwise wrapped distance >=4 (self-
# collision structurally impossible, brute-force confirmed to fit on the
# 8x8 wrapped world -- see 007/hypothesis.md).
#
# Not chasing the target -- terminates after a bounded number of cycles.
# Expect "Run Failed"; the duration is not a score.

TILES = [(0, 0), (0, 4), (2, 2), (2, 6), (4, 0)]
TILE_SET = set(TILES)
REROLL_LIMIT = 5

def own_tile_ready():
	if get_ground_type() != Grounds.Soil:
		till()
	if get_entity_type() != Entities.Carrot:
		plant(Entities.Carrot)

def water_here():
	while num_items(Items.Water) > 0 and get_water() < 0.999:
		use_item(Items.Water)

for t in TILES:
	Common.move_to_wrapped(t[0], t[1])
	own_tile_ready()
	water_here()

# Shared across all 5 tiles -- only one drone ever touches the farm, so
# one authoritative memory dict is correct, same as 006.
planted = {}

CYCLES = 75
harvests = 0
hits_grass = 0
hits_reroll = 0
hits_walk = 0
hits_guard = 0
t_start = get_tick_count()
for i in range(CYCLES):
	tx, ty = TILES[i % len(TILES)]
	t_arrive = get_tick_count()
	Common.move_to_wrapped(tx, ty)
	water_here()

	# Whatever is standing here was planted (and its companion already
	# settled) on the *previous* visit to this tile, a full round-robin
	# lap ago -- it may or may not be ripe yet. Wait if not (this wait is
	# the real, unavoidable idle time this design is trying to shrink by
	# spreading it across other tiles' handling).
	h = can_harvest()
	while not h:
		h = can_harvest()
	t_ripe = get_tick_count()
	before = num_items(Items.Carrot)
	harvest()
	gained = num_items(Items.Carrot) - before
	harvests = harvests + 1

	# BUG FIX (r1 -> r2): the reroll/walk resolution must happen
	# immediately after replanting, in the same visit -- *before* moving
	# on -- exactly like 006's single-tile timing. r1 checked the
	# companion at the *start* of the next visit instead, after the crop
	# had already grown for a full lap; a reroll miss there threw away a
	# full growth cycle's progress (harvest+replant resets growth) instead
	# of costing ~400 ticks at plant time, which is why r1 measured worse
	# than 004's 3-tile champion despite cheaper handling per attempt.
	own_tile_ready()
	t_plant = get_tick_count()
	companion = get_companion()
	rerolls = 0
	walked = False
	while companion != None:
		ctype, pos = companion
		key = pos
		if key in TILE_SET:
			# Should be structurally impossible at pairwise distance >=4
			# vs a <=3 companion range -- guarded defensively, matching
			# 004. Treat as an unsatisfiable draw: reroll it away.
			hits_guard = hits_guard + 1
		elif key in planted:
			if planted[key] == ctype:
				hits_reroll = hits_reroll + 1
				break
		elif ctype == Entities.Grass:
			hits_grass = hits_grass + 1
			break
		if rerolls < REROLL_LIMIT:
			harvest()
			plant(Entities.Carrot)
			companion = get_companion()
			rerolls = rerolls + 1
		else:
			if Common.affordable(ctype):
				Common.move_to_wrapped(pos[0], pos[1])
				if get_entity_type() != ctype:
					harvest()
					Common.plant_companion(ctype)
				planted[key] = ctype
				Common.move_to_wrapped(tx, ty)
				hits_walk = hits_walk + 1
				walked = True
			break
	t_end = get_tick_count()
	if i < 10 or i % 10 == 0:
		quick_print("CYCLE", i, "TILE", (tx, ty), "COMPANION", companion, "GAINED", gained,
			"REROLLS", rerolls, "WALKED", walked, "COMMUTE_AND_WAIT_TICKS", t_ripe - t_arrive,
			"SETTLE_TICKS", t_end - t_plant, "TOTAL_TICKS", t_end - t_arrive)

t_total = get_tick_count() - t_start
quick_print("SUMMARY", "CYCLES", CYCLES, "HARVESTS", harvests, "HITS_GRASS", hits_grass,
	"HITS_REROLL", hits_reroll, "HITS_WALK", hits_walk, "HITS_GUARD", hits_guard,
	"TICKS", t_total, "TICKS_PER_HARVEST", t_total / harvests, "CARROT", num_items(Items.Carrot))
