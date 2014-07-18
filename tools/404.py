#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
	José Gómez Castaño
	Depto. Astrofísica y CC. de la Atmósfera - UCM

	jgomez03@pdi.ucm.esta

	Genera un mapa con las imágenes procesadas en las tareas de LostAtNight
	que los usuarios no han podido determinar su posición
	y un fichero con las características de estas

'''

import urllib2
import json
import asciitable
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import time

def getKey(item):
	return item[0]

imagen = ''
hayProxy = False

# cargo las tareas acabadas de LostAtNight
if hayProxy == True:
	proxy = urllib2.ProxyHandler({'http': 'http://cidid08:casta04@proxy.adif.es:8080'})
	auth = urllib2.HTTPBasicAuthHandler()
	opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
	urllib2.install_opener(opener)
else:
	opener = urllib2.build_opener()	

req = urllib2.Request("http://crowdcrafting.org/api/taskrun?app_id=1711&limit=10000")
f = opener.open(req)
json = json.loads(f.read())


lista = asciitable.read('../completa.csv') 

puntos = []


f = open("404ParaNight.csv", "w")
linea = "ISS-ID,nlon,nlat,CoordFLAG\n"
f.writelines(linea)

#imagenes que si se han reconocido
imgSi = []
for i in range(len(json)):
	if json[i]['info']['LONLAT'] != '':
		link = json[i]['info']['img_big'].split('/')

		idiss = link[8].split('.')[0]
		imgSi.append(idiss)


for i in range(len(json)):

	if json[i]['info']['LONLAT'] == '':

		link = json[i]['info']['img_big'].split('/')

		idiss = link[8].split('.')[0]		# identificador de la imagen del voluntario

		try:
			posicionImg = imgSi.index(idiss)
			imgEsta = True
			
		except:
			imgEsta = False
		
		#print idiss,imgEsta
		
		for j in range(len(lista)):
			

			if (idiss == lista[j]['ISS-ID']) and (imgEsta == False):

				lon = lista[j]['nlon']
				lat = lista[j]['nlat']

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

		#print tmp , contador
		contador = 1
		tmp = p[0]


		line =  p[0] + ',' + str(p[1]) + ',' + str(p[2]) +  '\n'
		print line
		images.append(p[0])
		lons.append(p[1])
		lats.append(p[2])

		# guardo las caracteristicas de las imágenes para cargarlas en NigtCitiesISS
		linea = p[0] + ',' + str(p[1]) + ',' +  str(p[2]) + ', 5.0'  + '\n' 
		f.writelines(linea)

	#print p

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
map.plot(x, y, 'ro', markersize=5)

for images, xpt, ypt in zip(images, x, y):
	if imagen == images:
		plt.text(xpt, ypt, images)
 

plt.title('Imagenes no identificadas. Se indican los puntos del Nadir ' +  time.strftime("%d/%m/%Y %H:%M:%S")) 
plt.show()
