import Common

entity = Entities.Grass
instructions = Common.get_planting_instructions(entity)

def driver(x, y):
	Common.move_to(x,y)
	instructions()
	while True:
		while get_water() < 0.75:
			use_item(Items.Water)
		Common.polyculture()
		Common.await_harvest()
		harvest()

clear()
for i in range(6):
	for j in range(6):
		if i + j != 0:
			spawn_drone(driver, 3 + i*5, 3 + j*5)
driver(3, 3)