import copy
import numpy as np
from sklearn import datasets
from matplotlib import pyplot as plt

def my_plt(x):
	plt.scatter(x[:,0], x[:,1])
	plt.grid()
	plt.show()

# 2クラス分類用のデータ準備
dataset = datasets.load_iris()
_x, _y = dataset.data, dataset.target

mask = np.bitwise_or(_y == 0, _y == 1)
x = _x[mask][:, 2:]
y = _y[mask]


print('準備したデータ')
print(x[:10])

# 重複削除
x_unique = copy.deepcopy(x)
delete_list = []
for i in range(len(x)):
	xi = x[i]
	for j in range(i + 1, len(x)):
		xj = x[j]
		if xi[0] == xj[0] and xi[1] == xj[1]:
			delete_list.append(j)
d_list = sorted(set(delete_list), reverse=True)
for delete_index in d_list:
	x_unique = np.delete(x_unique, delete_index, 0)

print('重複削除したデータ')
print(x_unique[:10])

# 距離計算
distance = np.zeros((len(x_unique), len(x_unique)))
for i, (x0, x1) in enumerate(x_unique):
	for j, (_x0, _x1) in enumerate(x_unique):
		_distance = np.sqrt(np.power(x0 - _x0, 2) + np.power(x1 - _x1, 2))
		distance[i][j] = _distance


# (x0, x1)のうち，x0の要素で昇順ソート
x_sorted = np.zeros((1,3))
index_list = np.array(range(len(x_unique)))
index_list = index_list.reshape((len(x_unique), 1))
x = np.append(copy.deepcopy(x_unique), index_list, axis=1)
while(x.any()):
	index = np.argmin(x[:,0])
	x_add = np.array([x[index]])
	x_sorted = np.append(x_sorted, x_add, axis=0)
	x = np.delete(x, index, 0)
x_sorted = np.delete(x_sorted, 0, 0)

print('x0の要素で昇順ソート')
print(x_sorted[:10])
#print(my_plt(x_sorted))

# 特徴点リスト x の要素それぞれにキンググラフ上の座標割り当て
x_mapped = copy.deepcopy(x_sorted)
for index, (x0, _, _) in enumerate(x_sorted):
	y_graph = 0
	for i in range(0, index):
		(x0_prev, _, _) = x_sorted[i]
		if x0 == x0_prev:
			y_graph += 1
	[_x0, _, num] = x_mapped[index]
	x_mapped[index] = [_x0, y_graph, num]

print('座標割り当て その1')
print(x_mapped[:10])
#print(my_plt(x_mapped))

# (x0, x1)のうち，x1の要素で昇順ソート
x_sorted = np.zeros((1,3))
x = copy.deepcopy(x_mapped)
while(x.any()):
	index = np.argmin(x[:,1])
	x_add = np.array([x[index]])
	x_sorted = np.append(x_sorted, x_add, axis=0)
	x = np.delete(x, index, 0)
x_sorted = np.delete(x_sorted, 0, 0)

print('x1の要素で昇順ソート')
print(x_sorted[:10])
#print(my_plt(x_sorted))

# 特徴点リスト x の要素それぞれにキンググラフ上の座標割り当て
x_mapped = copy.deepcopy(x_sorted)
for index, (_, x1, _) in enumerate(x_sorted):
	x_graph = 0
	for i in range(0, index):
		(_, x1_prev, _) = x_sorted[i]
		if x1 == x1_prev:
			x_graph += 1
	[_, _x1, num] = x_mapped[index]
	x_mapped[index] = [x_graph, _x1, num]

print('座標割り当て その2')
print(x_mapped[:10])
print(my_plt(x_mapped))




