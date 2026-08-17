import Common

# exp-hay_single-016 -- two-tile interleaving, ported from Hay(multi)'s
# exp-073 champion. 012's paused "proven ceiling" (011's R=400 reroll
# model) rested on the same stale assumption Hay(multi) corrected in
# exp-066: Grass auto-regrows ("Grass grows automatically on
# grassland", Grass.md) -- an entity property, not specific to Hay's
# world size or drone count. Directly confirmed in this leaderboard's
# own 8x8/single-drone context (exp-016): instructions() after harvest
# costs 7 ticks, not 200, in 6/6 cycles. Real reroll cost is ~207, not
# 400 -- the whole 001-015 asymptote needs re-deriving, and since this
# category is single-drone, the two-tile trick (hide the growth wait
# behind a sibling tile's reroll-chase) needs no macro-layout work at
# all -- just two adjacent tiles, both reachable by the one drone.
#
# Same design as Hay-multi's 073: two tiles at distance 1, every
# position within distance 3 of either pre-seeded once as permanent
# Bush (accept a companion draw the instant it's a memory-matched
# Bush; anything else is cheap to reroll, never worth walking to),
# water threshold 0.75 (growth isn't the bottleneck once hidden), and
# a direct move() for the known single-hop between tiles.

TARGET = 100000000
REROLL_LIMIT = 30
WATER_THRESHOLD = 0.75
entity = Entities.Grass
instructions = Common.get_planting_instructions(entity)

size = get_world_size()
c1x, c1y = get_pos_x(), get_pos_y()
c2x, c2y = (c1x + 1) % size, c1y

def wdist(ax, ay, bx, by):
	dx = min((bx - ax) % size, (ax - bx) % size)
	dy = min((by - ay) % size, (ay - by) % size)
	return dx + dy

Common.move_to(c1x, c1y)
instructions()
Common.move_to(c2x, c2y)
instructions()

planted = {}
for dx in range(-3, 5):
	for dy in range(-3, 4):
		px = (c1x + dx) % size
		py = (c1y + dy) % size
		if (px, py) == (c1x, c1y) or (px, py) == (c2x, c2y):
			continue
		d1 = wdist(c1x, c1y, px, py)
		d2 = wdist(c2x, c2y, px, py)
		if d1 <= 3 or d2 <= 3:
			Common.move_to(px, py)
			if get_entity_type() != Entities.Bush:
				if get_entity_type() != None:
					harvest()
				Common.plant_companion(Entities.Bush)
			planted[(px, py)] = Entities.Bush
Common.move_to(c1x, c1y)

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
	instructions()
	companion = get_companion()
	while rerolls < REROLL_LIMIT and companion != None:
		ctype, (cx, cy) = companion
		key = (cx, cy)
		if key in planted and planted[key] == ctype:
			break
		harvest()
		instructions()
		companion = get_companion()
		rerolls = rerolls + 1

	if num_items(Items.Hay) >= TARGET:
		break
	if current_is_c1:
		move(East)
	else:
		move(West)
	current_is_c1 = not current_is_c1

quick_print("DONE", "HAY", num_items(Items.Hay), "WOOD", num_items(Items.Wood),
	"TICK_FINAL", get_tick_count(), "TIME_FINAL", get_time())
