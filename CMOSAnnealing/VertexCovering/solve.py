from amplify import BinaryPoly, gen_symbols, sum_poly, Solver
from amplify.constraint import greater_equal
from amplify.client import HitachiClient

from secret import get_token
import utils

import time

# 問題サイズ N=2,4,6,8,10,12,14,16 で実験
for N in range(2, 16 + 1, 2):
    # QUBO変数の2次元配列（正方格子グラフに対応）
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
    client.parameters.outputs.energies = False
    client.parameters.outputs.spins = True
    client.parameters.outputs.execution_time = False
    client.parameters.outputs.num_outputs = 1
    client.parameters.temperature_num_steps = 10
    client.parameters.temperature_step_length = 100
    client.parameters.temperature_initial = 100.0
    client.parameters.temperature_target = 0.02

    # ソルバー生成
    solver = Solver(client)

    # 重み変更してアニーリング実行
    w_step = 0.1           # 重み変更幅
    num_steps = 10         # 重み変更回数
    num_execution = 100    # アニーリング実行回数

    print('N, w_a, w_b, optimal_answer_percentage[%], time[s]')
    # 結果出力用ファイルを開く
    f = open('result_{0}.txt'.format(N), 'w')

    for i in range(1, num_steps + 1):
        w_a = i * w_step
        for j in range(1, num_steps + 1):
            w_b = j * w_step
            # 最終的なエネルギー関数
            energy_function = w_a*constraint + w_b*cost_function

            num_optimum = 0      # 最適解が導かれた回数
            sum_exe_time = 0.0   # 実行時間の総和
            num_skip = 0         # RuntimeError でスキップされた回数
            for _ in range(num_execution):
                try:
                    # 通信時間を含む計算実行時間の計測
                    start_time = time.perf_counter()
                    result = solver.solve(energy_function)
                    end_time = time.perf_counter()

                    sum_exe_time += end_time - start_time
                except RuntimeError as e:
                    num_skip += 1
                    print(e)
                    continue
                # 結果出力
                str_spin, result_is_optimum = utils.print_solver_result(N, result)
                #print(str_spin)
                if result_is_optimum:
                    num_optimum += 1
            # 最適回答率
            percentage_of_optimum = (num_optimum / (num_execution - num_skip)) * 100
            # 実行時間
            exe_time = sum_exe_time / (num_execution - num_skip)
            result_str = '{0}, {1}, {2}, {3}, {4}\n'.format(N, w_a, w_b, percentage_of_optimum, exe_time)
            # ログ出力
            print(result_str, end="")
            # ファイル書き込み
            f.write(result_str)
    # 結果出力用ファイルを閉じる
    f.close()

