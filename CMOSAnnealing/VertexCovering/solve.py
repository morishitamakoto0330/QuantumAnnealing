from amplify import BinaryPoly, gen_symbols, sum_poly, Solver
from amplify.constraint import greater_equal
from amplify.client import HitachiClient

from secret import get_token
import utils

# 問題設定（正方格子グラフにおける頂点被覆）
N = 2         # 問題サイズ
q = gen_symbols(BinaryPoly, N, N)

# コスト関数（w1 で調整）
cost_function = sum([sum_poly(q[i]) for i in range(N)])

# 制約（w2 で調整）
constraint_x = sum([greater_equal(q[i][j] + q[i + 1][j], 1) for i in range(N - 1) for j in range(N)])
constraint_y = sum([greater_equal(q[i][j] + q[i][j + 1], 1) for i in range(N) for j in range(N - 1)])
constraint = constraint_x + constraint_y

# クライアント設定
client = HitachiClient()
client.token = get_token()
client.parameters.num_executions = 1
client.parameters.temperature_num_steps = 100
client.parameters.temperature_step_length = 100
client.parameters.temperature_initial = 100.0
client.parameters.temperature_target = 0.02

solver = Solver(client)

# 重み変更して複数回アニーリング
w_init = 1
num = 1
for i in range(num):
    w1 = i * w_init
    for j in range(num):
        w2 = j * w_init
        # 最終的なエネルギー関数
        energy_function = w1*cost_function + w2*constraint
        # 解く
        result = solver.solve(energy_function)
        # 結果出力
        print('(w1, w2)=({0}, {1})'.format(w1, w2))
        print(utils.print_solver_result(N, result))


