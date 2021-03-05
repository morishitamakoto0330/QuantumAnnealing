import math, random, copy
import numpy as np

def getRandomDistance(N):
	min_number = 0
	max_number = 10
	points = [[random.randint(min_number, max_number), random.randint(min_number, max_number)] for i in range(N)]

	distance = []
	tmp = 0.0

	for i in range(N - 1):
		_distance = []
		for j in range(i + 1, N):
			_distance.append(math.sqrt(math.pow(points[i][0] - points[j][0], 2) + math.pow(points[i][1] - points[j][1], 2)))
		distance.append(_distance)

	return distance

def print_spins(spins):
	# get index
	x_max = -1
	y_max = -1
	for spin in spins:
		for x,y,p in spin:
			if x > x_max:
				x_max = x
			if y > y_max:
				y_max = y
	# spins -> spin list dim=(exe_time, x, y)
	spin_list = [[0]*(x_max + 1) for i in range(y_max + 1)]
	spins_list = [copy.deepcopy(spin_list) for i in range(len(spins))]
	for i, spin in enumerate(spins):
		for x,y,p in spin:
			spins_list[i][x][y] = p
	# spin list -> string
	print_string = ''
	for i, s1 in enumerate(spins_list):
		print_string += '\n\n{0}回目の実行時のスピン\n'.format(i + 1)
		for x, s2 in enumerate(s1):
			for y, p in enumerate(s2):
				print_string += '{0:>5}'.format(p)
			print_string += '\n'
	print(print_string)

	return

def createClusteringIsingModel(N, distance):
	# constant value for constraint
	M = 1
	C = 30
	CHAIN = -30
	# set full connection model
	model = [[0,0,0,0,0]]

	##################################################
	# set magnetic field and chaining
	##################################################
	x = y = 0
	x_prev = y_prev = 0
	# left side
	for i in range(int((N + 1)/2)):
		for j in range(N - 1):
			x = N - 2 + i - j
			y = i + j
			if y > N - 2:
				y = N - 1 - y%(N - 2)
			# magnetic field
			model.append([x, y, x, y, M])
			# chain
			if j != 0:
				model.append([x_prev, y_prev, x, y, CHAIN])
			x_prev = x
			y_prev = y
	# right side
	for i in range(int((N + 1)/2)):
		for j in range(N - 1):
			x = N - 1 - i + j
			y = i + j
			if y > N - 2:
				y = N - 1 - y%(N - 2)
			# magnetic field
			model.append([x, y, x, y, M])
			# chain
			if j != 0:
				model.append([x_prev, y_prev, x, y, CHAIN])
			x_prev = x
			y_prev = y
	
	##################################################
	# set constraint for representing clusters
	##################################################
	model.append([N - 2, 0, N - 1, 0, C])
	for i in range(1, int(N/2)):
		model.append([N - 2, i*2 - 1, N - 1, i*2 - 1, C])

	##################################################
	# set distance constraint 
	##################################################
	for i in range(int(N/2) - 1):
		x = i*2
		y = N - 2
		_x = 2*N - 3 - x
		_y = y
		for j in range(int(N/2) - 1 - i):
			model.append([x, y, x + 1, y, int(distance[i][j])])
			model.append([_x, _y, _x - 1, _y, int(distance[i][j])])
			x += 1
			y -= 1
			_x -= 1
			_y -= 1
	

	# delete duplication
	_model = list(set(map(tuple, model)))

	return _model

def getClusteringSample():
	# constant value for constraint
	M = 1
	C = 3
	CHAIN = -3
	# set magnetic field
	model_mag = [
		#sigma 1a
		[0,1,0,1,M],
		[1,0,1,0,M],
		#sigma 1b
		[3,1,3,1,M],
		[2,0,2,0,M],
		#sigma 2a
		[1,1,1,1,M],
		#sigma 2b
		[2,1,2,1,M],
		#sigma 3a
		[1,2,1,2,M],
		#sigma 3b
		[2,2,2,2,M],
	]
	# set interaction
	model_int = [
		#sigma 1a
		[0,1,1,0,CHAIN],
		#sigma 1b
		[3,1,2,0,CHAIN],
		# distance=√13=3.61
		[0,1,1,1,3.61],
		[0,1,1,2,3.61],
		[2,1,3,1,3.61],
		[2,2,3,1,3.61],
		# distance=√2=1.41
		[1,1,1,2,1.41],
		[2,1,2,2,1.41],
		# constraint
		[1,0,2,0,C],
		[1,1,2,1,C],
		[1,2,2,2,C],
	]

	model = model_mag + model_int
	return model

'''
	model_mag = [
		# sigma 1a
		[0,4,0,4,M],
		[1,3,1,3,M],
		[2,2,2,2,M],
		[3,1,3,1,M],
		[4,0,4,0,M],
		# sigma 1b
		[0,5,0,5,M],
		[1,6,1,6,M],
		[2,7,2,7,M],
		[3,8,3,8,M],
		[4,9,4,9,M],
		# sigma 2a
		[1,5,1,5,M],
		[2,4,2,4,M],
		[3,3,3,3,M],
		[4,2,4,2,M],
		[4,1,4,1,M],
		# sigma 2b
		[1,4,1,4,M],
		[2,5,2,5,M],
		[3,6,3,6,M],
		[4,7,4,7,M],
		[4,8,4,8,M],
		# sigma 3a
		[2,6,2,6,M],
		[3,5,3,5,M],
		[4,4,4,4,M],
		[4,3,4,3,M],
		[3,2,3,2,M],
		# sigma 3b
		[2,3,2,3,M],
		[3,4,3,4,M],
		[4,5,4,5,M],
		[4,6,4,6,M],
		[3,7,3,7,M],
	]
	
	# set interaction
	model_int = [
		# sigma 1a
		[0,4,1,3,CHAIN],
		[1,3,2,2,CHAIN],
		[2,2,3,1,CHAIN],
		[3,1,4,0,CHAIN],
		# sigma 1b
		[0,5,1,6,CHAIN],
		[1,6,2,7,CHAIN],
		[2,7,3,8,CHAIN],
		[3,8,4,9,CHAIN],
		# sigma 2a
		[1,5,2,4,CHAIN],
		[2,4,3,3,CHAIN],
		[3,3,4,2,CHAIN],
		[4,2,5,1,CHAIN],
		# sigma 2b
		[1,4,2,5,CHAIN],
		[2,5,3,6,CHAIN],
		[3,6,4,7,CHAIN],
		[4,7,4,8,CHAIN],
		# sigma 3a
		[2,6,3,5,CHAIN],
		[3,5,4,4,CHAIN],
		[4,4,4,3,CHAIN],
		[4,3,3,2,CHAIN],
		# sigma 3b
		[2,3,3,4,CHAIN],
		[3,4,4,5,CHAIN],
		[4,5,4,6,CHAIN],
		[4,6,3,7,CHAIN],
		# distance=√13=3.61
		[3,1,3,2,3.61],
		[4,0,4,1,3.61],
		[3,7,3,8,3.61],
		[4,8,4,9,3.61],
		# distance=√2=1.41
		[4,2,4,3,1.41],
		[4,6,4,7,1.41],
		# constraint
		[0,4,0,5,C],
		[1,4,1,5,C],
		[3,4,3,5,C],
	]
'''
'''
	# set magnetic field
	model_mag = [
		# sigma 1a
		[0,6,0,6,1],
		[1,5,1,5,1],
		[2,4,2,4,1],
		[3,3,3,3,1],
		[4,2,4,2,1],
		[5,1,5,1,1],
		[6,0,6,0,1],
		# sigma 1b
		[0,7,0,7,1],
		[1,8,1,8,1],
		[2,9,2,9,1],
		[3,10,3,10,1],
		[4,11,4,11,1],
		[5,12,5,12,1],
		[6,13,6,13,1],
		# sigma 2a
		[1,7,1,7,1],
		[2,6,2,6,1],
		[3,5,3,5,1],
		[4,4,4,4,1],
		[5,3,5,3,1],
		[6,2,6,2,1],
		[6,1,6,1,1],
		# sigma 2b
		[1,6,1,6,1],
		[2,7,2,7,1],
		[3,8,3,8,1],
		[4,9,4,9,1],
		[5,10,5,10,1],
		[6,11,6,11,1],
		[6,12,6,12,1],
		# sigma 3a
		[2,8,2,8,1],
		[3,7,3,7,1],
		[4,6,4,6,1],
		[5,5,5,5,1],
		[6,4,6,4,1],
		[6,3,6,3,1],
		[5,2,5,2,1],
		# sigma 3b
		[2,5,2,5,1],
		[3,6,3,6,1],
		[4,7,4,7,1],
		[5,8,5,8,1],
		[6,9,6,9,1],
		[6,10,6,10,1],
		[5,11,5,11,1],
		# sigma 4a
		[3,9,3,9,1],
		[4,8,4,8,1],
		[5,7,5,7,1],
		[6,6,6,6,1],
		[6,5,6,5,1],
		[5,4,5,4,1],
		[4,3,4,3,1],
		# sigma 4b
		[3,4,3,4,1],
		[4,5,4,5,1],
		[5,6,5,6,1],
		[6,7,6,7,1],
		[6,8,6,8,1],
		[5,9,5,9,1],
		[4,10,4,10,1],
	]
	# set interaction
	model_int = [
		# sigma 1a
		[0,6,1,5,-3],
		[1,5,2,4,-3],
		[2,4,3,3,-3],
		[3,3,4,2,-3],
		[4,2,5,1,-3],
		[5,1,6,0,-3],
		# sigma 1b
		[0,7,1,8,-3],
		[1,8,2,9,-3],
		[2,9,3,10,-3],
		[3,10,4,11,-3],
		[4,11,5,12,-3],
		[5,12,6,13,-3],
		# sigma 2a
		[1,7,2,6,-3],
		[2,6,3,5,-3],
		[3,5,4,4,-3],
		[4,4,5,3,-3],
		[5,3,6,2,-3],
		[6,2,6,1,-3],
		# sigma 2b
		[1,6,2,7,-3],
		[2,7,3,8,-3],
		[3,8,4,9,-3],
		[4,9,5,10,-3],
		[5,10,6,11,-3],
		[6,11,6,12,-3],
		# sigma 3a
		[2,8,3,7,-3],
		[3,7,4,6,-3],
		[4,6,5,5,-3],
		[5,5,6,4,-3],
		[6,4,6,3,-3],
		[6,3,5,2,-3],
		# sigma 3b
		[2,5,3,6,-3],
		[3,6,4,7,-3],
		[4,7,5,8,-3],
		[5,8,6,9,-3],
		[6,9,6,10,-3],
		[6,10,5,11,-3],
		# sigma 4a
		[3,9,4,8,-3],
		[4,8,5,7,-3],
		[5,7,6,6,-3],
		[6,6,6,5,-3],
		[6,5,5,4,-3],
		[5,4,4,3,-3],
		# sigma 4b
		[3,4,4,5,-3],
		[4,5,5,6,-3],
		[5,6,6,7,-3],
		[6,7,7,8,-3],
		[6,8,5,9,-3],
		[5,9,4,10,-3],
		# distance=1
		[6,0,6,1,1],
		[6,2,6,3,1],
		[6,4,6,5,1],
		[6,8,6,9,1],
		[6,10,6,11,1],
		[6,12,6,13,1],
		# distance=2
		[5,1,5,2,2],
		[5,3,5,4,2],
		[5,9,5,10,2],
		[5,11,5,12,2],
		# distance=3
		[4,2,4,3,3],
		[4,10,4,11,3],
		# constraint
		[0,6,0,7,C],
		[1,6,1,7,C],
		[3,6,3,7,C],
		[5,6,5,7,C],
	]
'''




