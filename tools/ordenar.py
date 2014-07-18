#!/usr/bin/python
#-*- coding: utf-8 -*-


'''
	José Gómez Castaño
	Depto. Astrofísica y CC. de la Atmósfera - UCM

	jgomez03@pdi.ucm.esta

	Hay que eliminar del fichero final las imágenes con coordenadas 0,0

'''

import asciitable

lista = asciitable.read('okParaNight.csv') 

f = open("okUpload.csv", "w")
linea = "ISS-ID,loncity,latcity,lens,large,coordimage,CoordFLAG\n"
f.writelines(linea)

tmp = ''

for i in lista:

	id = i['ISS-ID'] + str(i['loncity']) + str(i['latcity'])

	if id != tmp:

		tmp = id 
		linea = i['ISS-ID'] + ',' + str(i['loncity']) + ',' + str(i['latcity']) + ',' + i['lens'] + ',' + i['large'] + ',' + i['coordimage'] + ',' + str(i['CoordFLAG']) + '\n'

		f.writelines(linea)


f.close()