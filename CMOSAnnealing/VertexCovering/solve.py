import urllib.request
import urllib.parse
import json

import vertex_covering as vc
from secret import get_token

# トークン設定
access_token = get_token()
headers = {'Authorization': 'Bearer '+ access_token}
url = 'https://annealing-cloud.com/api/v2/solve'

# 頂点被覆問題の設定
N = 2
model = vc.set(N)

# APIに渡すパラメータ
params = {
	"type": 4,
  "num_executions": 1,
  "model": model,
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
	print(json.dumps(json_data, indent=2))



