import Common

entity = Entities.Tree
instructions = Common.get_planting_instructions(entity)

def driver(x,y):
	Common.move_to(x,y)
	while True:
		Common.await_harvest()
		while get_water() < 0.5:
			use_item(Items.Water)
		harvest()
		instructions()
		loop = False
		while loop == False:
			harvest()
			plant(entity)
			plant_type, (px, py) = get_companion()
			if plant_type == Entities.Grass:
				if abs(x - px) + abs(y - py) != 2:
					loop = True
		move(North)
		move(North)


clear()
for x in range(1, get_world_size()):
	spawn_drone(driver, x, x % 2)
driver(0, 0)