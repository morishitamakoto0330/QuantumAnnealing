from amplify import BinaryPoly, gen_symbols, sum_poly, Solver
from amplify.constraint import greater_equal
from amplify.client import HitachiClient

from secret import get_token
import utils

# 問題設定（正方格子グラフにおける頂点被覆）
N = 2         # 問題サイズ
q = gen_symbols(BinaryPoly, N, N)

# コスト関数（w_b で調整）
cost_function = sum([sum_poly(q[i]) for i in range(N)])

# 制約（w_a で調整）
constraint_x = sum([greater_equal(q[i][j] + q[i + 1][j], 1) for i in range(N - 1) for j in range(N)])
constraint_y = sum([greater_equal(q[i][j] + q[i][j + 1], 1) for i in range(N) for j in range(N - 1)])
constraint = constraint_x + constraint_y

# クライアント設定
client = HitachiClient()
client.token = get_token()
client.parameters.num_executions = 1
client.parameters.temperature_num_steps = 10
client.parameters.temperature_step_length = 100
client.parameters.temperature_initial = 100.0
client.parameters.temperature_target = 0.02

solver = Solver(client)

# 重み変更してアニーリング実行
w_step = 0.1         # 重み変更幅
num_steps = 10       # 重み変更回数
num_execution = 100  # アニーリング実行回数

print('N, w_a, w_b, 最適回答率[%]')
# 結果出力用ファイルを開く
f = open('result.txt', 'w')

for i in range(1, num_steps + 1):
    w_a = i * w_step
    for j in range(1, num_steps + 1):
        w_b = j * w_step
        # 最終的なエネルギー関数
        energy_function = w_a*constraint + w_b*cost_function

        num_optimum = 0      # 最適解が導かれた回数
        for _ in range(num_execution):
            # 解く
            result = solver.solve(energy_function)
            # 結果出力
            _, result_is_optimum = utils.print_solver_result(N, result)
            if result_is_optimum:
                num_optimum += 1
        percentage_of_optimum = (num_optimum / num_execution) * 100
        result_str = '{0}, {1}, {2}, {3}'.format(N, w_a, w_b, percentage_of_optimum)
        # ログ出力
        print(result_str)
        # ファイル書き込み
        f.write(result_str)
# 結果出力用ファイルを閉じる
f.close()

