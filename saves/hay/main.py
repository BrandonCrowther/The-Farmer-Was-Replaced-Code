# exp-hay-050 -- is a global dict actually shared across spawned drones?
#
# If drone B can see writes drone A made to a plain top-level dict, a
# SHARED companion-memory dict (not each drone's own private one) could
# unlock much more of the "neighbor cooperation" effect than currently
# happens by accident (via the physical world state alone).

shared = {}

def writer():
	shared["from_writer"] = 12345
	quick_print("WRITER", "wrote", dict(shared))

def reader():
	# give the writer a moment
	i = 0
	while i < 50000:
		i = i + 1
	quick_print("READER", "sees", dict(shared))

d = spawn_drone(writer)
wait_for(d)
reader()
quick_print("MAIN", "sees", dict(shared))
