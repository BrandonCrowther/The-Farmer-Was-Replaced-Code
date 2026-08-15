import Common

entity = Entities.Sunflower
instructions = Common.get_planting_instructions(entity)

def driver(x,y):
	Common.move_to(x,y)
	while True:
		while get_water() < 0.75:
			use_item(Items.Water)
		if can_harvest():
			harvest()
		instructions()
		move(North)

clear()
for x in range(1, 32):
	spawn_drone(driver, x, 0)
driver(0, 0)