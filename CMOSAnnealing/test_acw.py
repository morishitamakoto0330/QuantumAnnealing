import json
import acw
import os

# read result.txt as JSON data
f = open('result.txt','r')
result = f.read()
result_json = json.loads(result)

#print(result_json)
acw.print_spins(result_json['result']['spins'])




