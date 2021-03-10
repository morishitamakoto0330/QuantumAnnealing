import urllib.request
import urllib.parse
import json
import acw

from sklearn import datasets
from secret import get_token

access_token = get_token()
headers = {'Authorization': 'Bearer '+ access_token}
url = 'https://annealing-cloud.com/api/v2/solve'

dataset = datasets.load_iris()
_x, _y = dataset.data, dataset.target
mask = np.bitwise_or(_y == 0, _y == 1)
x = _x[mask][:, 2:]
y = _y[mask]


params = {
	"type": 4,
  "num_executions": 10,
#  "model": [[0,0,0,0,1],[1,1,1,1,1],[1,0,1,0,1],[0,0,1,0,100],[0,0,1,1,-100]],
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


data = urllib.parse.urlencode(params)
data = data.encode('ascii')
req = urllib.request.Request(url, json.dumps(params).encode(), headers, 'POST')

with urllib.request.urlopen(req) as response:
	json_data = json.loads(response.read())
	print(json.dumps(json_data, indent=2))
	acw.print_spins(json_data['result']['spins'])






