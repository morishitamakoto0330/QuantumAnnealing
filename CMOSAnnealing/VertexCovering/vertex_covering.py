def set(N):
    print('N={} の問題を設定します。'.format(N))
    model = []
    # 磁場設定
    model.append([0, 0, 0, 0, 1])
    model.append([0, 1, 0, 1, 1])
    model.append([1, 0, 1, 0, 1])
    model.append([1, 1, 1, 1, 1])
    # 相互作用設定
    model.append([0, 0, 0, 1, 1])
    model.append([0, 0, 1, 0, 1])
    model.append([0, 0, 1, 1, 1])
    return model

