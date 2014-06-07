'''
	Generate linktasks.csv file with links to every task in crowdcrafting

'''


import urllib2
import json

req = urllib2.Request("http://crowdcrafting.org/api/task?app_id=1608")
opener = urllib2.build_opener()
f = opener.open(req)
json = json.loads(f.read())

f = open("linktasks.csv", "w")

f.writelines('idiss,lon,lat,linkTask,linkSmall\n')

for i in range(len(json)):

	linkTask = 'http://crowdcrafting.org/app/nightcitiesiss/task/' + str(json[i]['id'])
	line = json[i]['info']['idiss'] + ',' + json[i]['info']['citylon'] + ',' + json[i]['info']['citylat'] + ',' + linkTask + ',' + json[i]['info']['link_small'] + '\n'

	f.writelines(line) 

f.close()