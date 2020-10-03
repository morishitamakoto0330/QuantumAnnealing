import random
import math
import numpy as np
import matplotlib.pyplot as plt

from pyqubo import Array, Constraint, Placeholder, solve_qubo

def get_class(solution):
	class_list = []
	s = solution['q']

	for i in range(len(s)):
		if s[i][0] == 0:
			class_list.append(1)
		elif s[i][0] == 1:
			class_list.append(2)
		else:
			class_list.append(0)

	return class_list

###################
# Problem Setting #
###################

N = 10   # feature point
K = 2    # class
d = []   # distance

# get random points
MAX = 100
MIN = 0
points = [ random.randint(MIN, MAX) for i in range(N) ]
points = list(dict.fromkeys(points))
N = len(points)

# calc distance
for i in range(N-1):
	_d = []
	for j in range(i+1, N):
		_d.append(abs(points[i] - points[j]))
	d.append(_d)

# binary variable
q = Array.create("q", shape=(N, K), vartype="BINARY")

# energy function
H_p = Constraint(sum([ -q[i][0]*q[i][1] + (q[i][0] + q[i][1])/2 for i in range(N) ]), "penalty")
H_distance = sum([ d[i][j]*q[i][k]*q[j][k] for i in range(N-1) for j in range(N-i-1) for k in range(K) ])
H = H_distance + Placeholder("penalty")*H_p

model = H.compile()

feed_dict = {"penalty": -20.0}
qubo, offset = model.to_qubo(feed_dict=feed_dict)
ising = model.to_ising(feed_dict=feed_dict)

# print(ising)

raw_solution = solve_qubo(qubo)

decoded_solution, broken, energy = model.decode_solution(raw_solution, vartype="BINARY", feed_dict=feed_dict)

print("N={0}".format(N))
print(decoded_solution)

class_list = get_class(decoded_solution)

print(class_list)

plt.scatter(points, [0]*N, c="red")
plt.grid()
plt.show()









