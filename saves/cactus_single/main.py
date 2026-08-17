# exp-cactus_single-005 -- insertion-sort validation (4x4)
#
# 004's bubble sort walks the entire row/column on every pass regardless
# of real inversion count -- O(n) work per pass for up to n-1 passes.
# Insertion sort via adjacent swaps (walk forward once; on an inversion,
# swap and walk backward correcting until in order, then resume forward)
# costs n + inversions instead -- the minimum possible for an
# adjacent-swap sort. Validated here at 4x4 before committing to 8x8.
#
# Not chasing the target -- terminates after this one cascade. Expect
# "Run Failed"; the duration is not a score, but is measured against
# 003's bubble-sort baseline (34,852 ticks for this same 4x4 grid).

quick_print("WORLD_SIZE", get_world_size())

N = 4
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

t_setup_start = get_tick_count()
for dy in range(N):
	for dx in range(N):
		move_to(OX + dx, OY + dy)
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Cactus)
t_setup_end = get_tick_count()

# Drone is on the last-planted tile (started growing last -- wait here).
h = can_harvest()
while not h:
	h = can_harvest()
t_grown = get_tick_count()

t_sort_start = get_tick_count()
for dy in range(N):
	insertion_row(OY + dy, N)
for dx in range(N):
	insertion_col(OX + dx, N)
t_sort_end = get_tick_count()

move_to(OX, OY)
before = num_items(Items.Cactus)
harvest()
gained = num_items(Items.Cactus) - before
t_end = get_tick_count()

quick_print("SETUP_TICKS", t_setup_end - t_setup_start, "GROWTH_WAIT_TICKS", t_grown - t_setup_end,
	"SORT_TICKS", t_sort_end - t_sort_start, "GAINED", gained, "TOTAL_TICKS", t_end - t_setup_start)
