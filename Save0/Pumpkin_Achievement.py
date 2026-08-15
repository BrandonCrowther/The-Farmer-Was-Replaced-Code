import Common

entity = Entities.Pumpkin
instructions = Common.get_planting_instructions(entity)

def force_grow_pumpkin():
	gee = get_entity_type()
	if gee == None:
		return True
	if gee == Entities.Pumpkin and can_harvest():
		return True
	plant(Entities.Pumpkin)
	use_item(Items.Fertilizer)
	use_item(Items.Weird_Substance)
	use_item(Items.Weird_Substance)
	return force_grow_pumpkin()
	
def driver(x, y):
	Common.move_to(x,y)	
	if x != get_world_size() - 1:
		spawn_drone(driver, x + 1, 0)
	while True:
		protocol(x, y)

def protocol(x,y):
	first_pumpkin = -1
	# First pass - plant normally
	for i in range(get_world_size()):
		instructions()
		if i == 0:
			first_pumpkin = measure()
		while get_water() < 0.75:
			use_item(Items.Water)
		move(North)
		
	# Second pass, replant and Fertilizer
	for i in range(get_world_size()):
		force_grow_pumpkin()
		
		if i == 0:
			first_pumpkin = measure()
			
		# Once finished, check to see if
		# our drone's first pumpkin is the winner
		if get_pos_y() == get_world_size() - 1:
			m = measure()
			while m != None:
				m = measure()
				if m == first_pumpkin:
					harvest()
		move(North)


clear()
driver(0, 0)