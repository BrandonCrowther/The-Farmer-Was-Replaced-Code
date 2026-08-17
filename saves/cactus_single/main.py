# exp-cactus_single-004 -- finish-and-score (8x8 grid sort + single cascade)
#
# 001/002/003's design, at full scale. Cactus is not a polyculture crop
# (Polyculture.md excludes it) -- it's Cactus.md's size/sort cascade:
# harvesting n simultaneously-cascading, fully-grown, sorted cacti
# yields 32 * n**2 Items.Cactus (002, exact, independent of individual
# cactus size). 32 * 8**2 = 32 * 64 = 131,072 -- exactly Cactus_Single's
# target (Leaderboard.md). So: plant a full 8x8 grid, sort it, harvest
# one corner, done in a single cascade.
#
# Sizes (0-9) are randomly fixed once a cactus is fully grown and never
# converge by waiting (001) -- a real swap()-based sort is required.
# Sorting every row, then every column, of a matrix leaves the rows
# still sorted (classical lemma) -- so one row-bubble-sort pass over
# every row followed by one column-bubble-sort pass over every column
# is provably sufficient to sort the whole grid in both dimensions at
# once (Cactus.md's sorted-order condition, applied grid-wide).
# Validated exactly at 4x4 scale in 003 (8192 = 32*16**2, first try).
# Early exit added to each bubble pass here: stop once a pass makes
# zero swaps, since much of the naive worst-case pass count does no
# real work once the row/column is already sorted.
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

def bubble_row(y, n):
	for p in range(n - 1):
		move_to(OX, y)
		swapped = False
		for i in range(n - 1):
			a = measure()
			b = measure(East)
			if a > b:
				swap(East)
				swapped = True
			move(East)
		if not swapped:
			break

def bubble_col(x, n):
	for p in range(n - 1):
		move_to(x, OY)
		swapped = False
		for i in range(n - 1):
			a = measure()
			b = measure(North)
			if a > b:
				swap(North)
				swapped = True
			move(North)
		if not swapped:
			break

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
	bubble_row(OY + dy, N)
for dx in range(N):
	bubble_col(OX + dx, N)

move_to(OX, OY)
before = num_items(Items.Cactus)
harvest()
gained = num_items(Items.Cactus) - before

quick_print("DONE", "GAINED", gained, "CACTUS", num_items(Items.Cactus), "TICK_FINAL",
	get_tick_count(), "TIME_FINAL", get_time())
