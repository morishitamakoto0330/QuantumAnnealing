import json
import acw
import os

# read result.txt as JSON data
#f = open('hoge.txt','r')
#f = open('result.txt','r')
#f = open('result_clustering_sample_2.txt','r')
#f = open('result_clustering_sample_3.txt','r')
f = open('result_clustering.txt','r')
result = f.read()
result_json = json.loads(result)

#print(result_json)
acw.print_spins(result_json['result']['spins'])




