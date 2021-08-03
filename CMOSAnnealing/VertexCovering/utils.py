def is_optimum(N, l):
    isOptimum = True
    # スピンの並びが交互に0, 1, 0, 1, ...となっているかどうかの判定
    for i in range(N):
        spin_prev = -1
        for j in range(N):
            spin = l[i*N + j]
            if spin_prev == spin:
                isOptimum = False
                break
            spin_prev = spin
    return isOptimum

def print_solver_result(N, result):
    d = {}
    l = [0]*(N*N)
    count_one = 0
    print_str = ''
    # 出力結果を辞書型として保存
    for s in result:
        d = dict(s.values)
    # 出力を整形
    for key, value in d.items():
        l[key] = value
        if value == 1:
            count_one += 1
    # リストを文字列に変換
    print_str += '---------------\n'
    print_str += '最終スピン状態=\n'
    for i in range(N):
        for j in range(N):
            print_str += str(l[i*N + j])
        print_str += '\n'
    print_str += '---------------\n'
    return print_str, is_optimum(N, l)


