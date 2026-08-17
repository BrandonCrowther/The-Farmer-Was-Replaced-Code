import Common

# exp-carrots_single-008 -- finish-and-score (5-tile reroll pipeline)
#
# 007's design, wired to the real target. 5 tiles round-robin at
# pairwise wrapped distance >=4 (self-collision structurally impossible
# vs a <=3 companion range). Companion resolution is reroll-before-walk
# (006): the preference is fixed at plant time, so harvest+replant
# (~400 ticks) redraws it far cheaper than a walk-and-service round
# trip, up to REROLL_LIMIT tries before falling back to a real walk.
# Resolution happens immediately after planting, in the same visit,
# before moving to the next tile -- growth only starts once the
# companion is already settled (007's r1 bug: checking a lap later lets
# a miss throw away a full growth cycle). Positions this drone has
# walked-and-serviced are remembered and never reverted -- a later draw
# of the same (type, position) is a free hit too, same as Grass always
# is for a position never touched. The setup loop below runs the exact
# same resolution as every later visit, so there is no unresolved
# warm-up plant (007's minor caveat, fixed here).
#
# Real run: repeats internally until 2 real hours of simulated time
# accumulate (Leaderboard.md) before the completion modal shows.

TARGET = 100000000
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

# One authoritative memory dict -- only this drone ever touches the farm.
planted = {}

def settle(tx, ty):
	# Resolve the just-planted companion: free Grass, remembered stock, a
	# cheap reroll, or (after REROLL_LIMIT misses) a real walk-and-service.
	own_tile_ready()
	companion = get_companion()
	rerolls = 0
	while companion != None:
		ctype, pos = companion
		key = pos
		if key in TILE_SET:
			pass
		elif key in planted:
			if planted[key] == ctype:
				break
		elif ctype == Entities.Grass:
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
			break

for t in TILES:
	Common.move_to_wrapped(t[0], t[1])
	water_here()
	settle(t[0], t[1])

i = 0
while num_items(Items.Carrot) < TARGET:
	tx, ty = TILES[i % len(TILES)]
	i = i + 1
	Common.move_to_wrapped(tx, ty)
	water_here()

	h = can_harvest()
	while not h and num_items(Items.Carrot) < TARGET:
		h = can_harvest()
	if num_items(Items.Carrot) >= TARGET:
		break
	harvest()
	if num_items(Items.Carrot) >= TARGET:
		break

	settle(tx, ty)

quick_print("DONE", "CARROT", num_items(Items.Carrot), "TICK_FINAL", get_tick_count(),
	"TIME_FINAL", get_time())
