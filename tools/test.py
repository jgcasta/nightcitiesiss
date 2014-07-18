#!/usr/bin/python
#-*- coding: utf-8 -*-

import urllib2
import json
import asciitable
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

def getKey(item):
	return item[0]

imagen = ''
hayProxy = True

# cargo las tareas acabadas de LostAtNight
if hayProxy == True:
	proxy = urllib2.ProxyHandler({'http': 'http://cidid08:casta04@proxy.adif.es:8080'})
	auth = urllib2.HTTPBasicAuthHandler()
	opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
	urllib2.install_opener(opener)
else:
	opener = urllib2.build_opener()	

req = urllib2.Request("http://crowdcrafting.org/api/taskrun?app_id=1711&limit=1000")
f = opener.open(req)
json = json.loads(f.read())

f = open("test.csv", "w")
line =  'idiss,lon,lat\n'
f.writelines(line) 

puntos = []

for i in range(len(json)):

	if json[i]['info']['LONLAT'] != '':

		link = json[i]['info']['img_big'].split('/')

		idiss = link[8].split('.')[0]		# identificador de la imagen del voluntario
		lonlat = json[i]['info']['LONLAT']	# datos proporcionados por el voluntario
		
		lon = lonlat.split(',')[0]
		lat = lonlat.split(',')[1]

		punto = []
		punto.append(str(idiss))
		punto.append(lon)
		punto.append(lat)

		puntos.append(punto)

tmp = ''
contador = 0
images, lons, lats = [], [], []
for p in sorted(puntos, key=getKey ):

	if p[0] == tmp:

		contador = contador + 1

	else:

		print tmp , contador
		contador = 1
		tmp = p[0]


	line =  p[0] + ',' + p[1] + ',' + p[2] +  '\n'
	images.append(p[0])
	lons.append(float(p[1]))
	lats.append(float(p[2]))

	print p

	f.writelines(line) 

f.close()


map = Basemap(projection='merc', lat_0=0, lon_0=0,
    resolution = 'l', 
    llcrnrlon=-180, llcrnrlat=-75,
    urcrnrlon=180, urcrnrlat=75)
 
map.drawcoastlines()
map.drawcountries()
map.fillcontinents()
map.drawmapboundary()

x,y = map(lons, lats)
map.plot(x, y, 'bo', markersize=5)

for images, xpt, ypt in zip(images, x, y):
	if imagen == images:
		plt.text(xpt, ypt, images)
 

 
plt.show()
