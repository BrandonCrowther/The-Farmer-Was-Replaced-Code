# exp-cactus_single-006 -- finish-and-score (8x8 grid sort + single cascade, insertion sort)
#
# 004's design, with 005's insertion sort in place of bubble sort.
# Cactus is not a polyculture crop (Polyculture.md excludes it) -- it's
# Cactus.md's size/sort cascade: harvesting n simultaneously-cascading,
# fully-grown, sorted cacti yields 32 * n**2 Items.Cactus (002, exact,
# independent of individual cactus size). 32 * 8**2 = 131,072 --
# exactly Cactus_Single's target. So: plant a full 8x8 grid, sort it,
# harvest one corner, done in a single cascade.
#
# Sizes (0-9) are randomly fixed once a cactus is fully grown and never
# converge by waiting (001) -- a real swap()-based sort is required.
# Sorting every row, then every column, of a matrix leaves the rows
# still sorted (classical lemma) -- so one row-sort pass over every row
# followed by one column-sort pass over every column is provably
# sufficient to sort the whole grid in both dimensions at once.
#
# 004 used a full-re-walk bubble sort (early exit per pass, but each
# pass still walks the entire row/column regardless of real inversion
# count -- O(n) per pass for up to n-1 passes). This uses insertion
# sort instead: walk forward once; on finding an out-of-order adjacent
# pair, swap and walk backward correcting until in order, then resume
# forward. Cost is n + inversions, the minimum possible for an
# adjacent-swap sort -- validated exactly at 4x4 in 005 (exact
# 32*16**2=8192 match, 42% fewer sort ticks than 003's bubble sort).
#
# Planting uses a boustrophedon (snake) path so every one of the 63
# non-first tiles needs exactly one move, and the drone ends up
# standing on the very last tile planted -- the only one that still
# needs to finish growing once setup completes.

N = 8
OX = get_pos_x()
OY = get_pos_y()

def move_to(x, y):
	while get_pos_x() < x:
		move(East)
	while get_pos_x() > x:
		move(West)
	while get_pos_y() < y:
		move(North)
	while get_pos_y() > y:
		move(South)

def till_plant():
	if get_ground_type() != Grounds.Soil:
		till()
	plant(Entities.Cactus)

def insertion_row(y, n):
	move_to(OX, y)
	for i in range(1, n):
		move_to(OX + i, y)
		j = i
		cont = True
		while j > 0 and cont:
			a = measure(West)
			b = measure()
			if a > b:
				swap(West)
				move(West)
				j = j - 1
			else:
				cont = False

def insertion_col(x, n):
	move_to(x, OY)
	for i in range(1, n):
		move_to(x, OY + i)
		j = i
		cont = True
		while j > 0 and cont:
			a = measure(South)
			b = measure()
			if a > b:
				swap(South)
				move(South)
				j = j - 1
			else:
				cont = False

till_plant()
going_east = True
for dy in range(N):
	if dy > 0:
		move(North)
		till_plant()
	for i in range(N - 1):
		if going_east:
			move(East)
		else:
			move(West)
		till_plant()
	going_east = not going_east

# Drone is on the last-planted tile -- wait for it here.
h = can_harvest()
while not h:
	h = can_harvest()

for dy in range(N):
	insertion_row(OY + dy, N)
for dx in range(N):
	insertion_col(OX + dx, N)

move_to(OX, OY)
before = num_items(Items.Cactus)
harvest()
gained = num_items(Items.Cactus) - before

quick_print("DONE", "GAINED", gained, "CACTUS", num_items(Items.Cactus), "TICK_FINAL",
	get_tick_count(), "TIME_FINAL", get_time())
