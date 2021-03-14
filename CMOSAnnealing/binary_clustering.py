import urllib.request
import urllib.parse
import json
import acw
import numpy as np

from sklearn import datasets
from secret import get_token

# トークン設定
access_token = get_token()
headers = {'Authorization': 'Bearer '+ access_token}
url = 'https://annealing-cloud.com/api/v2/solve'

# イジングモデル読み込み
model = np.zeros((1, 5))
file_path = './iris_ising_model.txt'
with open(file_path, mode='r') as f:
	line_list = f.read().split('\n')
	for line in line_list:
		l = np.array([line.split(',')])
		if l.shape[1] == model.shape[1]:
			model = np.append(model, l, axis=0)
model = np.delete(model, 0, 0)
_model = [[0, 0, 0, 0, 0.000000]]
for (x0, y0, x1, y1, p) in model:
	_model.append([int(x0), int(y0), int(x1), int(y1), float(p)])
print('イジングモデル')
print(_model[:10])

# APIに渡すパラメータ
params = {
	"type": 4,
  "num_executions": 10,
  #"model": [[0,0,0,0,1],[0,1,0,1,1]],
  "model": _model,
  "parameters": {
    "temperature_initial": 10.0,
    "temperature_target": 0.01
  },
  "outputs": {
    "averaged_spins": True,
    "averaged_energy": True
  }
}


# API呼び出し
data = urllib.parse.urlencode(params)
data = data.encode('ascii')
req = urllib.request.Request(url, json.dumps(params).encode(), headers, 'POST')

# CMOSアニーリングマシン実行結果受け取り
with urllib.request.urlopen(req) as response:
	json_data = json.loads(response.read())
	#print(json.dumps(json_data, indent=2))
	acw.print_spins(json_data['result']['spins'])






