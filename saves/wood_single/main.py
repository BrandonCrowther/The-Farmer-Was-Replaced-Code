import Common

# exp-wood_single-002 -- finish-and-score (single-tile reroll-before-walk)
#
# Direct adaptation of hay_single's champion (008-013): the companion
# preference is fixed at plant time, so a cheap reroll (harvest +
# replant, ~400 ticks) redraws it far cheaper than a walk-and-service
# round trip, up to REROLL_LIMIT tries before falling back to a real
# walk. A Tree's companion is always Grass, Bush, or Carrot -- never
# Tree itself (Polyculture.md: never the plant's own species) -- so
# this design never plants a second Tree anywhere, sidestepping 001's
# 2.44x neighbor-growth-penalty entirely.
#
# own_tile_ready() plants Entities.Tree directly -- NOT via
# Common.get_planting_instructions(Entities.Tree), which deliberately
# plants Grass instead (a different wood-farming-pattern use case, see
# Common.py's own comment on p_planting_table's Tree entry).
#
# Real run: repeats internally until 2 real hours of simulated time
# accumulate (Leaderboard.md) before the completion modal shows.

TARGET = 500000000
REROLL_LIMIT = 5

def own_tile_ready():
	if get_ground_type() != Grounds.Grassland:
		till()
	if get_entity_type() != Entities.Tree:
		plant(Entities.Tree)

ax, ay = get_pos_x(), get_pos_y()
own_tile_ready()

# What this drone believes it has planted, keyed by companion position --
# only this drone ever touches the farm, so the memory is authoritative.
planted = {}

while num_items(Items.Wood) < TARGET:
	while num_items(Items.Water) > 0 and get_water() < 0.999:
		use_item(Items.Water)

	h = can_harvest()
	while not h and num_items(Items.Wood) < TARGET:
		h = can_harvest()
	if num_items(Items.Wood) >= TARGET:
		break
	harvest()

	if num_items(Items.Wood) >= TARGET:
		break

	own_tile_ready()
	companion = get_companion()
	rerolls = 0
	while companion != None:
		ctype, (cx, cy) = companion
		key = (cx, cy)
		if key in planted and planted[key] == ctype:
			break
		if rerolls < REROLL_LIMIT:
			harvest()
			own_tile_ready()
			companion = get_companion()
			rerolls = rerolls + 1
		else:
			if Common.affordable(ctype):
				Common.move_to_wrapped(cx, cy)
				if get_entity_type() != ctype:
					harvest()
					Common.plant_companion(ctype)
				planted[key] = ctype
				Common.move_to_wrapped(ax, ay)
			break

quick_print("DONE", "WOOD", num_items(Items.Wood), "TICK_FINAL", get_tick_count(),
	"TIME_FINAL", get_time())
