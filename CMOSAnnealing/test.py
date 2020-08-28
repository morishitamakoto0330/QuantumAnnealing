import urllib.request
import urllib.parse
import json

access_token = '046eaee43c3a068433eb6a1c89a9c8fc'
headers = {'Authorization': 'Bearer '+ access_token}
#url = 'https://annealing-cloud.com/api/v1/solve'
url = 'https://annealing-cloud.com/api/v2/solve'



# Web API version 1
'''
params = {
  "num_executions": 5,
  "model": [
    [0,0,0,0,1],
    [0,1,0,2,-1],
    [1,0,1,1,1],
    [1,1,1,2,1],
    [2,0,2,1,1],
    [2,1,2,2,1],
    [0,0,1,0,1],
    [1,0,2,0,1],
    [0,1,1,1,-1]
  ],
  "parameters": {
    "temperature_initial": 30.0,
    "temperature_target": 0.0000001
  },
  "outputs": {
    "averaged_spins": True,
    "averaged_energy": True
  }
}
'''

# Web API version 2
params = {
	"type": 3,
  "num_executions": 5,
  "model": [
    [0,0,0,0,4],
    [0,1,0,2,-1],
    [1,0,1,1,1],
    [1,1,1,2,1],
    [2,0,2,1,1],
    [2,1,2,2,1],
    [0,0,1,0,1],
    [1,0,2,0,1],
    [0,1,1,1,-1]
  ],
  "parameters": {
    "temperature_initial": 30.0,
    "temperature_target": 0.0000001
  },
  "outputs": {
    "averaged_spins": True,
    "averaged_energy": True
  }
}







data = urllib.parse.urlencode(params)




headers = {'Authorization': 'Bearer '+ access_token}



data = urllib.parse.urlencode(params)
data = data.encode('ascii')
req = urllib.request.Request(url, json.dumps(params).encode(), headers, 'POST')

with urllib.request.urlopen(req) as response:
	json_data = json.loads(response.read())
	print(json.dumps(json_data, indent=2))






