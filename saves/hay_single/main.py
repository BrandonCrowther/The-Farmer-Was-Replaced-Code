import Common

# exp-hay_single-017 -- ports Hay(multi)'s exp-075/076/079/081/082
# stray-tick fixes verbatim (exp-016 only ported the macro two-tile
# design from Hay-multi's exp-073, not the later micro-optimizations
# built on top of it). This category is single-drone, so none of
# 077/078/080's spawn-tree/territory-partitioning material applies (no
# multi-drone setup latency, no cross-drone territory question) -- just
# the fixes that apply within one drone's own driver:
#
# (075) instructions() is a no-op guard-checked plant() call; Grass
# auto-regrows after harvest() with no replant needed (Grass.md: "grows
# automatically on grassland"). The old code here called it twice per
# reroll cycle (once before the loop, once every iteration) -- pure
# waste, worse than Hay-multi's original since it wasn't fixed here yet.
# (076) Common.move_to() -> Common.move_to_wrapped() for the initial
# placement walk -- shorter path on the wrap, no leftover
# protocol()/Unlocks.Mazes overhead move_to() always pays.
# (079) reroll chase's `planted[key] == ctype` was a second tuple-keyed
# dict lookup re-deriving a value with exactly one write site (always
# Entities.Bush) -- compare `ctype` to the constant directly. Bush-wall
# setup's `d2 = wdist(...)` ran unconditionally even though `d1<=3 or
# d2<=3` only needs d2 when d1 misses -- short-circuit. get_entity_type()
# was called twice per position -- cached in a local.
# (081) of the hot loop's three num_items(Items.Hay)>=TARGET checks per
# iteration, drop the one guarding only the cheap move() call, keep the
# one guarding the expensive harvest+reroll chase.
# (082) water-check `num_items(Items.Water) > 0 and get_water() <
# WATER_THRESHOLD` reordered so the usually-False operand
# (get_water()<THRESHOLD) is checked first, letting `and` short-circuit
# past num_items() on the common no-op path.

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

Common.move_to_wrapped(c1x, c1y)
instructions()
Common.move_to_wrapped(c2x, c2y)
instructions()

planted = {}
for dx in range(-3, 5):
	for dy in range(-3, 4):
		px = (c1x + dx) % size
		py = (c1y + dy) % size
		if (px, py) == (c1x, c1y) or (px, py) == (c2x, c2y):
			continue
		near = wdist(c1x, c1y, px, py) <= 3
		if not near:
			near = wdist(c2x, c2y, px, py) <= 3
		if near:
			Common.move_to_wrapped(px, py)
			et = get_entity_type()
			if et != Entities.Bush:
				if et != None:
					harvest()
				Common.plant_companion(Entities.Bush)
			planted[(px, py)] = Entities.Bush
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
		ctype, (cx, cy) = companion
		key = (cx, cy)
		if key in planted and ctype == Entities.Bush:
			break
		harvest()
		companion = get_companion()
		rerolls = rerolls + 1

	if current_is_c1:
		move(East)
	else:
		move(West)
	current_is_c1 = not current_is_c1

quick_print("DONE", "HAY", num_items(Items.Hay), "WOOD", num_items(Items.Wood),
	"TICK_FINAL", get_tick_count(), "TIME_FINAL", get_time())
