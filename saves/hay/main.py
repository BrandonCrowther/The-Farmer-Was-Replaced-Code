import Common

# Leaderboards.Hay succeeds when num_items(Items.Hay) >= TARGET is true *at the
# moment the program ends*. The simulation never stops on its own, so every drone
# has to notice the target and return, and the main drone has to outlive them all.
TARGET = 2000000000

entity = Entities.Grass
instructions = Common.get_planting_instructions(entity)

# Diagnostic. exp-008 was built on reading 007's "can_harvest() False on 94.1% of
# passes" as "the farm is growth-bound", and that misreading cost a 59x
# regression. The statistic is a frequency of arriving early, not a duration
# spent waiting.
#
# get_tick_count() costs 0 ticks, so the real number is free to take: ticks burnt
# inside the busy-wait against ticks for the whole pass. That is the share of the
# run actually spent idle, and it decides whether idle time is worth attacking.
SAMPLES = 25

def driver(x, y):
	Common.move_to(x,y)
	instructions()
	passes = 0
	waited = 0
	total = 0
	while num_items(Items.Hay) < TARGET:
		t0 = get_tick_count()
		while get_water() < 0.75:
			use_item(Items.Water)
		Common.polyculture()
		# Not Common.await_harvest(): that spins forever on a plant that will
		# never ripen, and once the target is hit nothing else is going to move.
		# Checking the target here too is what stops a straggler from hanging
		# the whole run.
		t1 = get_tick_count()
		h = can_harvest()
		while not h and num_items(Items.Hay) < TARGET:
			h = can_harvest()
		t2 = get_tick_count()
		harvest()

		if x == 3 and y == 3 and passes < SAMPLES:
			waited = waited + (t2 - t1)
			total = total + (t2 - t0)
			quick_print("TICKS", passes, "work", t1 - t0, "wait", t2 - t1, "cum_wait", waited, "cum_total", total)
		passes = passes + 1

clear()
drones = []
for i in range(6):
	for j in range(6):
		if i + j != 0:
			d = spawn_drone(driver, 3 + i*5, 3 + j*5)
			# None means the drone cap was hit; there is no handle to wait on.
			if d:
				drones.append(d)
driver(3, 3)
# The run is not over until the program is, and the program is not over while a
# spawned drone is still farming. Reap them before falling off the end.
for d in drones:
	wait_for(d)
