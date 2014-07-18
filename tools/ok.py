#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
	José Gómez Castaño
	Depto. Astrofísica y CC. de la Atmósfera - UCM

	jgomez03@pdi.ucm.es

	Genera un mapa con las imágenes procesadas en las tareas de LostAtNight
	y un fichero para la nueva generación de tareas okParaNight.csv

	@pre Necesita tener disponible completa.csv con todas las imágenes disponibles

	El flujo final para publicar las imágnes de LostAtNight en NigtCitiesISS es
	
		Ejecutar ok.py 
		Ejecutal ordenar.py
		Subir el fichero final okUpload.csv

'''

import urllib2
import json
import asciitable
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import time


# Define la clave por la que se ordena el array de imágenes final
def getKey(item):
	return item[0]

# si se quiere pintar el nombre de la imagen sobre el mapa se pone su identificador aqui
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

# cargo las características de todas las imágenes
lista = asciitable.read('../completa.csv') 

puntos = []

f = open("okParaNight.csv", "w")
linea = "ISS-ID,loncity,latcity,lens,large,coordimage,CoordFLAG\n"
f.writelines(linea)

for i in range(len(json)):

	if json[i]['info']['LONLAT'] != '':

		link = json[i]['info']['img_big'].split('/')
		idiss = link[8].split('.')[0]		# identificador de la imagen del voluntario

		for j in range(len(lista)):

			if (idiss == lista[j]['ISS-ID']):
				
				#genero un array con los posiciones de las imágenes para el mapa final

				lon = lista[j]['loncity']
				lat = lista[j]['latcity']

				punto = []
				punto.append(str(idiss))
				punto.append(lon)
				punto.append(lat)
				punto.append(lista[j]['lens'])
				punto.append(lista[j]['large'])
				punto.append(lista[j]['coordimage'])

				puntos.append(punto)




tmp = ''
contador = 0
total = 0
images, lons, lats = [], [], []
for p in sorted(puntos, key=getKey ):

	if p[0] == tmp:

		contador = contador + 1

	else:
		total = total + 1
		contador = 1
		tmp = p[0]


	line =  p[0] + ',' + str(p[1]) + ',' + str(p[2]) + ',' + p[3] + ',' + p[4] + ',' + p[5] +   ',5.0\n'
	f.writelines(line)
	print line
	images.append(p[0])
	lons.append(p[1])
	lats.append(p[2])

print total
f.close()

map = Basemap(projection='merc', lat_0=0, lon_0=0,
    resolution = 'l', 
    llcrnrlon=-180, llcrnrlat=-75,
    urcrnrlon=180, urcrnrlat=75)
 
#map.bluemarble()

map.drawcoastlines()
map.drawcountries()
map.fillcontinents()
map.drawmapboundary()

x,y = map(lons, lats)
map.plot(x, y, 'go', markersize=5)

# Si hay un identificador de imagen definido, se pinta su etiqueta sobre el mapa
for images, xpt, ypt in zip(images, x, y):
	if imagen == images:
		plt.text(xpt, ypt, images)

 

plt.title('Imagenes identificadas ' +  time.strftime("%d/%m/%Y %H:%M:%S")) 
plt.show()
