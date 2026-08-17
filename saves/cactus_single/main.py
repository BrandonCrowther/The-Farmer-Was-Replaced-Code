# exp-cactus_single-003 -- 4x4 grid sort + full cascade harvest
#
# Validates the intended design before spending ticks on the full 8x8:
# plant a grid, sort it via row-then-column adjacent-swap bubble sort
# (sorting columns of a row-sorted matrix leaves the rows sorted -- a
# classical lemma, so one row pass + one column pass suffices, no
# shearsort/snake needed), harvest one corner, expect the whole grid to
# cascade for 32 * n**2 (002: yield formula, independent of individual
# cactus size).
#
# Not chasing the target -- terminates after this one cascade. Expect
# "Run Failed"; the duration is not a score, but is measured to project
# the full 8x8 driver's cost.

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

def bubble_row(y, n):
	for p in range(n - 1):
		move_to(OX, y)
		for i in range(n - 1):
			a = measure()
			b = measure(East)
			if a > b:
				swap(East)
			move(East)

def bubble_col(x, n):
	for p in range(n - 1):
		move_to(x, OY)
		for i in range(n - 1):
			a = measure()
			b = measure(North)
			if a > b:
				swap(North)
			move(North)

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
	bubble_row(OY + dy, N)
for dx in range(N):
	bubble_col(OX + dx, N)
t_sort_end = get_tick_count()

move_to(OX, OY)
before = num_items(Items.Cactus)
harvest()
gained = num_items(Items.Cactus) - before
t_end = get_tick_count()

quick_print("SETUP_TICKS", t_setup_end - t_setup_start, "GROWTH_WAIT_TICKS", t_grown - t_setup_end,
	"SORT_TICKS", t_sort_end - t_sort_start, "GAINED", gained, "TOTAL_TICKS", t_end - t_setup_start)
