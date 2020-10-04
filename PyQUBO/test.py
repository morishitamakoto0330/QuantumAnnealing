import random
import math
import numpy as np
import matplotlib.pyplot as plt

from pyqubo import Array, Constraint, Placeholder, solve_qubo

def get_class(solution):
	class_list = []
	s = solution['q']

	for i in range(len(s)):
		if s[i][0] == 0 and s[i][1] == 1:
			class_list.append(1)
		elif s[i][0] == 1 and s[i][1] == 0:
			class_list.append(2)
		else:
			class_list.append(0)

	return class_list

###################
# Problem Setting #
###################
N = 3   # feature point
K = 2    # class
d = []   # distance

# get random points
MAX = 300
MIN = 0
points = []

while True:
	points = [ random.randint(MIN, MAX) for i in range(N) ]
	points = sorted(list(dict.fromkeys(points)))
	if len(points) == N:
		break

# calc distance
for i in range(N):
	_d = []
	for j in range(N):
		_d.append(abs(points[i] - points[j]))
	d.append(_d)
'''
N = 3
K = 2
points = [0, 1, 4]
d = [
	[0, 1, 4],
	[0, 0, 3],
	[0, 0, 0],
]
'''

# binary variable
q = Array.create("q", shape=(N, K), vartype="BINARY")

# energy function
H_p = Constraint(sum([ -q[i][0]*q[i][1] + (q[i][0] + q[i][1])/2 for i in range(N) ]), "penalty")
H_distance = sum([ d[i][j]*q[i][k]*q[j][k] for i in range(N) for j in range(i+1, N) for k in range(K) ])
H = H_distance + Placeholder("penalty")*H_p

model = H.compile()

c_i = -1.0

while True:
	feed_dict = {"penalty": c_i}

	qubo, offset = model.to_qubo(feed_dict=feed_dict)
	ising = model.to_ising(feed_dict=feed_dict)
	raw_solution = solve_qubo(qubo)
	decoded_solution, broken, energy = model.decode_solution(raw_solution, vartype="BINARY", feed_dict=feed_dict)

	class_list = get_class(decoded_solution)

	print(class_list)

	if 0 not in class_list:
		break

	c_i = c_i - 1.0

feed_dict = {"penalty": c_i}

print("c_i={0}".format(c_i))

qubo, offset = model.to_qubo(feed_dict=feed_dict)
linear, ising, offset= model.to_ising(feed_dict=feed_dict)

print("qubo=")
print(qubo)
print("ising=")
print(ising)
print("offset=")
print(offset)

raw_solution = solve_qubo(qubo)
decoded_solution, broken, energy = model.decode_solution(raw_solution, vartype="BINARY", feed_dict=feed_dict)

print("N={0}".format(N))
print(decoded_solution)

class_list = get_class(decoded_solution)

print("class_list=")
print(class_list)
print("points=")
print(points)
print("distance=")
print(d)

for i, x in enumerate(points):
	color = ""
	if class_list[i] == 1:
		color = "blue"
	elif class_list[i] == 2:
		color = "red"
	else:
		color = "black"
	plt.scatter([x], [0], c=color)

plt.grid()
plt.show()









