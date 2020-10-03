from pyqubo import Array, Constraint, Placeholder, solve_qubo

###################
# Problem Setting #
###################

N = 3    # feature point
K = 2    # class
d = [
	[0, 1, 4],
	[0, 0, 3],
	[0, 0, 0],
]

# binary variable
q = Array.create("q", shape=(N, K), vartype="BINARY")

# energy function
H_p = Constraint(sum([ -q[i][0]*q[i][1] + (q[i][0] + q[i][1])/2 for i in range(N) ]), "penalty")
H_distance = sum([ d[i][j]*q[i][k]*q[j][k] for i in range(N) for j in range(i+1, N) for k in range(K) ])
H = H_distance + Placeholder("penalty")*H_p

model = H.compile()

feed_dict = {"penalty": -20.0}
qubo, offset = model.to_qubo(feed_dict=feed_dict)
ising = model.to_ising(feed_dict=feed_dict)

print(ising)

raw_solution = solve_qubo(qubo)

decoded_solution, broken, energy = model.decode_solution(raw_solution, vartype="BINARY", feed_dict=feed_dict)

print(decoded_solution)



