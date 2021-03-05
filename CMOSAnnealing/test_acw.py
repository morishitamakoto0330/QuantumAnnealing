import json
import acw
import os

f = open('hoge.txt','r')
result = f.read()
result_json = json.loads(result)

acw.print_spins(result_json['result']['spins'])




