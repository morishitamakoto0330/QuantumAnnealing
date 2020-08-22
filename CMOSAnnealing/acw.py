def print_spins(spins):
	print_string = ""
	y_prev = 0
	for exec_index, spin in enumerate(spins):
		#print("{0}回目の実行時のスピン".format(exec_index + 1))
		print_string += "\n\n{0}回目の実行時のスピン\n".format(exec_index + 1)
		for x,y,p in spin:
			if y != y_prev:
				print_string += "\n"
			#print("({0}, {1}) = {2}".format(x, y, p))
			print_string += "{0:>5}".format(p)

			y_prev = y

	print(print_string)
	return





