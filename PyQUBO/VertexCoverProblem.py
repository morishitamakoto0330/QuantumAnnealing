from pyqubo import Array, Constraint, Placeholder, solve_qubo

# Problem Setting
N = 6
vertices = list(range(N))
edges = [
	(0, 1),
	(0, 4),
	(0, 5),
	(1, 2),
	(1, 3),
	(3, 4),
	(4, 5),
]

# binary variable
x = Array.create("x", shape=N, vartype="BINARY")

# energy function (QUBO)
H_cover = Constraint(sum((1 - x[u])*(1 - x[v]) for (u, v) in edges), "cover")
H_vertices = sum(x)
H = H_vertices + Placeholder("cover")*H_cover

model = H.compile()

feed_dict = {"cover": 1.0}
qubo, offset = model.to_qubo(feed_dict=feed_dict)

# search answer using SA
raw_solution = solve_qubo(qubo)

# decode answer
decoded_solution, broken, energy = model.decode_solution(raw_solution, vartype="BINARY", feed_dict=feed_dict)

# disp answer
print(decoded_solution)



