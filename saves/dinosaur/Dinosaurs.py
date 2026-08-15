def movef(dir):
	if not can_move(dir):
		return True
	move(dir)
	return False

def cycle():
	ws = get_world_size()
	change_hat(Hats.Brown_Hat)
	change_hat(Hats.Dinosaur_Hat)
	while True:
		# Loop north
		while get_pos_y() < ws - 1:
			if movef(North):
				return True
		if get_pos_x() != ws - 1:
			if movef(East):
				return True
		
		# Loop south to y = 1
		while get_pos_y() > 1:
			if movef(South):
				return True
		if get_pos_x() != ws - 1:
			if movef(East):
				return True
		# If we're at the end, go down
		# then travel west back to the start
		if(get_pos_x() == ws - 1 and get_pos_y() == 1):
			if movef(South):
				return True
			while get_pos_x() != 0:
				if movef(West):
					return True