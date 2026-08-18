import Common

# exp-wood_single-004 -- full redesign, applying Hay's proven playbook
# (069 full pre-seeding + 070 growth-hiding interleaving) to Tree/Wood
# for the first time, now that 003/004's simulate()-based measurements
# have the real numbers this needs:
#
# - Tree has NO Grass-style auto-regrow exception (003): harvesting an
#   unripe Tree yields 0 wood and destroys it, reverting to Grassland's
#   natural Grass. tree_ready() correctly recovers (plant() works fine
#   over auto-grown Grass -- it only fails over an intentionally
#   planted entity), but each reroll attempt genuinely costs a real
#   harvest+plant pair (~400 ticks), not Grass's ~207-cost shortcut.
# - Tree's real growth time at water~1, sustained (004): **4,412
#   ticks**, not 001's 34,718 -- that figure was almost certainly an
#   unwatered (water~0) measurement, the same mistake Hay's own 019
#   made before 037 corrected it 6.7x. 4,412 is now the same order of
#   magnitude as one tile's own servicing cost, not 8x it -- meaning
#   interleaving across enough tiles can fully hide it, the way it did
#   for Hay.
# - Tree's real, confirmed constraint (001): growth doubles for every
#   tree directly N/E/S/W of another (2.44x for one neighbor) --
#   *cardinal* only, diagonal is free. Hay's exact adjacent-tile offset
#   (+1,0) would trigger this; used a diagonal line instead
#   ((0,0),(1,1),(2,2),(3,3) relative to spawn), pairwise verified
#   non-cardinal offline before writing this.
#
# Sizing: per-visit servicing (harvest 200 + replant 200 + reroll chase
# avg ~3 attempts x 400 = ~1200 + move 200) ~= 1800 ticks. Needs
# (N-1) x ~1800 >= 4412 to fully hide growth -> N>=3.45 -> N=4 tiles,
# each visit's away-time (~5400) comfortably exceeding the 4,412-tick
# growth requirement.
#
# Companion mechanic is otherwise identical to Hay's: uniform 1/3 draw
# over the plant's non-self companion types (for Tree: Grass, Bush,
# Carrot), so the same "pre-seed everything as one free type (Bush),
# accept on a memory-matched draw, reroll otherwise, REROLL_LIMIT high
# enough that exhaustion is negligible ((2/3)^30~=5e-6)" design applies
# unchanged -- see Hay's exp-069/hay_single's exp-017 for the full
# reasoning trail this reuses verbatim. Water kept topped at ~0.999,
# matching the exact condition the 4,412-tick growth figure was
# measured under -- not yet re-tuned the way Hay's 072 later did, to
# avoid stacking an unverified assumption onto an already large change.

TARGET = 500000000
REROLL_LIMIT = 30

def tree_ready():
	if get_ground_type() != Grounds.Grassland:
		till()
	if get_entity_type() != Entities.Tree:
		plant(Entities.Tree)

size = get_world_size()
ax, ay = get_pos_x(), get_pos_y()
BASES = []
for i in range(4):
	bx = (ax + i) % size
	by = (ay + i) % size
	b = (bx, by)
	BASES.append(b)
BASE_SET = {}
for b in BASES:
	BASE_SET[b] = True

def wdist(px, py, qx, qy):
	dx = min((qx - px) % size, (px - qx) % size)
	dy = min((qy - py) % size, (py - qy) % size)
	return dx + dy

for b in BASES:
	Common.move_to_wrapped(b[0], b[1])
	tree_ready()

planted = {}
for dx in range(-3, 7):
	for dy in range(-3, 7):
		px = (ax + dx) % size
		py = (ay + dy) % size
		if (px, py) in BASE_SET:
			continue
		near = False
		for b in BASES:
			if wdist(b[0], b[1], px, py) <= 3:
				near = True
				break
		if near:
			Common.move_to_wrapped(px, py)
			et = get_entity_type()
			if et != Entities.Bush:
				if et != None:
					harvest()
				Common.plant_companion(Entities.Bush)
			planted[(px, py)] = Entities.Bush

Common.move_to_wrapped(BASES[0][0], BASES[0][1])

current = 0
while num_items(Items.Wood) < TARGET:
	while get_water() < 0.999 and num_items(Items.Water) > 0:
		use_item(Items.Water)
	h = can_harvest()
	while not h and num_items(Items.Wood) < TARGET:
		while get_water() < 0.999 and num_items(Items.Water) > 0:
			use_item(Items.Water)
		h = can_harvest()
	if num_items(Items.Wood) >= TARGET:
		break
	harvest()
	tree_ready()

	rerolls = 0
	companion = get_companion()
	while rerolls < REROLL_LIMIT and companion != None:
		ctype, (cx, cy) = companion
		key = (cx, cy)
		if key in planted and ctype == Entities.Bush:
			break
		harvest()
		tree_ready()
		companion = get_companion()
		rerolls = rerolls + 1

	current = (current + 1) % 4
	nb = BASES[current]
	Common.move_to_wrapped(nb[0], nb[1])

quick_print("DONE", "WOOD", num_items(Items.Wood), "TICK_FINAL", get_tick_count(),
	"TIME_FINAL", get_time())
