import Common

# Leaderboards.Hay succeeds when num_items(Items.Hay) >= TARGET is true *at the
# moment the program ends*. The simulation never stops on its own, so every drone
# has to notice the target and return, and the main drone has to outlive them all.
TARGET = 2000000000

entity = Entities.Grass
instructions = Common.get_planting_instructions(entity)

def driver(x, y):
	Common.move_to(x,y)
	instructions()
	while num_items(Items.Hay) < TARGET:
		while get_water() < 0.75:
			use_item(Items.Water)
		# Common.polyculture() deliberately not called.
		#
		# 010 established the trade this run exists to price. The companion
		# preference rerolls every pass (007's samples for one drone: Carrot,
		# Carrot, Tree, Carrot, Bush), so the walk cannot be amortised — it costs
		# ~800 ticks of movement, bought fresh every pass. Against that, a pass
		# with no companion trip is roughly 200 ticks: the harvest alone.
		#
		# So polyculture must be worth about 5x to break even. It may be worth far
		# more — the multiplier starts at 5x and doubles per upgrade, and a
		# resource leaderboard starts with everything unlocked — in which case
		# this run loses badly, and that is the answer.
		#
		# 008 looked like this experiment but was not: it removed polyculture
		# *and* added a 25-tile circuit, so its 59x regression cannot be
		# attributed to either one. This changes exactly one thing.
		# Not Common.await_harvest(): that spins forever on a plant that will
		# never ripen, and once the target is hit nothing else is going to move.
		# Checking the target here too is what stops a straggler from hanging
		# the whole run.
		h = can_harvest()
		while not h and num_items(Items.Hay) < TARGET:
			h = can_harvest()
		harvest()

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
