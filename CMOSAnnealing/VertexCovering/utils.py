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
    # 総量子ビットの半分のスピンが1になっているか
    print_str += str(N*N/2 == count_one)
    return print_str


