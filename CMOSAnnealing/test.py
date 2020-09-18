import urllib.request
import urllib.parse
import json
import acw

N = 8
'''
distance = acw.getRandomDistance(int(N/2))

with open("distance.txt", mode="w") as f:
	for _d in distance:
		for d in _d:
			f.write(str(int(d)))
			f.write(" ")
		f.write("\n")
'''

'''
distance = [
	[1,3],
	[2],
]
'''

distance = [
	[2,12,14],
	[10,12],
	[2],
]

'''
distance = [
	[2,4,5,10,12,14],
	[2,3,8,10,12],
	[1,6,8,10],
	[3,5,7],
	[2,4],
	[2],
]
'''

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

'''
# Web API version 2
params = {
	"type": 3,
  "num_executions": 5,
  "model": [
    [0,0,0,0,3.14],
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

# get MyModel
#model = acw.getClusteringSample()
model = acw.createClusteringIsingModel(N, distance)

#print(model)


params = {
	"type": 3,
  "num_executions": 10,
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






