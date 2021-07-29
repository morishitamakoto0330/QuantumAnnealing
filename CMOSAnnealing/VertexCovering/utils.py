def print_solver_result(N, result):
    d = {}
    l = [0]*(N*N)
    print_str = ''
    # 出力結果を辞書型として保存
    for s in result:
        d = dict(s.values)
    # 出力を整形
    for key, value in d.items():
        l[key] = value
    # リストを文字列に変換
    print_str = str(l)
    return print_str


