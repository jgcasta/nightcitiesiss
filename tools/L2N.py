#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
	L2N.py 

	José Gómez Castaño
	Depto. Astrofísica y CC. de la Atmósfera - UCM

	jgomez03@pdi.ucm.esta

	Generate	404.csv	Images with no location - idiss,nlon,nlat,large
				l2n.csv	Located images to load into NightCitiesISS - ISS-ID,loncity,latcity,lens,large,CoordFLAG

	City,ISS-ID,lat,lon,latcity,loncity,nlat,nlon,MODEL,date,hour,alt,sunazt,sunelv,shu,lens,ap,ISO,Coments,NASA,CoordFLAG,URL,small,large,Thumbnail,coordimage

'''


import urllib2
import json
import asciitable

print 'Loading all images'

# contenido completo de la lista de imagenes
lista = asciitable.read('../completa.csv') 

# cargo las tareas de NigthCitiesISS para compararlas con las hechas en LostAtNight y luego cargar solo las que falten

print "Loading NigthCitiesISS tasks"

reqNight = urllib2.Request("http://crowdcrafting.org/api/task?app_id=1712&limit=2")
openerNight = urllib2.build_opener()
fNight = openerNight.open(reqNight)
jsonNight = json.loads(fNight.read())


idissNight = []

for i in range(len(jsonNight)):
	link = jsonNight[i]['info']['link_big'].split('/')
	idissNight.append(link[8].split('.')[0])

# cargo las tareas acabadas de LostAtNight

print 'Loading LostAtNight taskrun'

req = urllib2.Request("http://crowdcrafting.org/api/taskrun?app_id=1711&limit=1")
opener = urllib2.build_opener()
f = opener.open(req)
json = json.loads(f.read())


# 404.csv
f404 = open("404.csv", "w")
f404.writelines('idiss,nlon,nlat,large\n')

fl2n = open("l2n.csv", "w")
print "ISS-ID,loncity,latcity,lens,large,CoordFLAG\n"

# Para cada taera acabada en LostAtNight
for i in range(len(json)):

	link = json[i]['info']['img_big'].split('/')

	idiss = link[8].split('.')[0]		# identificador de la imagen del voluntario
	lonlat = json[i]['info']['LONLAT']	# datos proporcionados por el voluntario

	# Si no se tiene posicion se guarda en un fichero diferente para saber las imagenes con problemas
	if json[i]['info']['LONLAT'] == '':

		for k in range(len(lista)):

			if idiss == lista[k]['ISS-ID']:
				# These points can be displayed on a matplotlib map
				f404.writelines(lista[k]['ISS-ID'] + ',' + lista[k]['nlon'] + ',' + lista[k]['nlat'] + ',' + lista[k]['large'] + '\n')

	else:

		for j in range(len(idissNight)):
			print 'Lost : ' + idiss + ' Night ' +  idissNight[j]
			
			# Compruebo que no esta tarea no este ya en NightCitiesISS y guardo sus datos
			if idiss != idissNight[j]:
		
				#comparo con todas las tareas para obtener los datos que necesitemos de la lista general
				for k in range(len(lista)):

					if idiss == lista[k]['ISS-ID']:
						
						print idiss + ',' + lonlat + ',' + lista[k]['lens'] + ',' + lista[k]['large'] + ',5.0\n' 
			else:

				# si ya esta en NightCities, no hago nada
				print 'Ya esta en NightCitiesISS' + idiss

f404.close()
fl2n.close()
'''
f = open("linktasks.csv", "w")

f.writelines('idiss,lon,lat,linkTask,linkSmall\n')
print len(json)
for i in range(len(json)):

	linkTask = 'http://crowdcrafting.org/app/nightcitiesiss/task/' + str(json[i]['id'])
	line = json[i]['info']['idiss'] + ',' + json[i]['info']['citylon'] + ',' + json[i]['info']['citylat'] + ',' + linkTask + ',' + json[i]['info']['link_small'] + '\n'

	f.writelines(line) 

f.close()
'''