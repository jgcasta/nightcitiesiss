#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
	José Gómez Castaño
	Depto. Astrofísica y CC. de la Atmósfera - UCM

	jgomez03@pdi.ucm.es

	A partir de la identificación de una imagen genera un mapa de ubicación de todas las localizaciones 
	seleccionadas por los usuarios, las coordenadas y muestra tambien la imagen

'''

import asciitable
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import time
import requests
import Image
from StringIO import StringIO

# si se quiere pintar el nombre de la imagen sobre el mapa se pone su identificador aqui
idiss = 'ISS034-E-38784'
hayProxy = False

# cargo las características de todas las imágenes
lista = asciitable.read('../completa.csv') 
images, lons, lats = [], [], []

print '----------------------------------------'
print 'Data image ' + idiss
for j in range(len(lista)):

	if (idiss == lista[j]['ISS-ID']):

		lon = lista[j]['loncity']
		lat = lista[j]['latcity']

		images.append(idiss)
		lons.append(lon)
		lats.append(lat)

		print lista[j]['ISS-ID'], lon, lat		
print '----------------------------------------'

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
map.plot(x, y, 'ro', markersize=5)


plt.title('ISS image locations for  ' +  idiss) 
plt.show()



# visualizo la imagen
images, xpt, ypt = images[0], x[0], y[0]

plt.text(xpt, ypt, images)

tmpMission=idiss.split('-E-')
mission = tmpMission[0]
idIss = tmpMission[1]
link = "http://eol.jsc.nasa.gov/sseop/images/ESC/%s/%s/%s-E-%s.JPG" % ('small',mission, mission,idIss)
r = requests.get(link)
im = Image.open(StringIO(r.content))
im.show()
