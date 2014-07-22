#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
	José Gómez Castaño
	Depto. Astrofísica y CC. de la Atmósfera - UCM

	jgomez03@pdi.ucm.esta

	Genera el fichero linktaskslost.csv con los enlaces a las tareas de LostAtNight
	que se pueden usar en fusion tables

	TODO
		Probar si se pueden subir directamente a Fusion Tables

'''


import urllib2
import json

hayProxy = True

# cargo las tareas acabadas de LostAtNight
if hayProxy == True:
	proxy = urllib2.ProxyHandler({'http': 'http://cidid08:casta04@proxy.adif.es:8080'})
	auth = urllib2.HTTPBasicAuthHandler()
	opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
	urllib2.install_opener(opener)
else:
	opener = urllib2.build_opener()	

req = urllib2.Request("http://crowdcrafting.org/api/task?app_id=1711&limit=10000")

f = opener.open(req)
json = json.loads(f.read())

f = open("linktaskslost.csv", "w")

f.writelines('idiss,lon,lat,linkTask,linkSmall\n')
print len(json)
for i in range(len(json)):

	linkTask = 'http://crowdcrafting.org/app/LostAtNight/task/' + str(json[i]['id'])
	line = json[i]['info']['idiss'] + ',' + json[i]['info']['citylon'] + ',' + json[i]['info']['citylat'] + ',' + linkTask + ',' + json[i]['info']['link_small'] + '\n'

	f.writelines(line) 

f.close()
