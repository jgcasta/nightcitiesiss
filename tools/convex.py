#!/usr/bin/python
#-*- coding: utf-8 -*-


'''
	José Gómez Castaño
	Depto. Astrofísica y CC. de la Atmósfera - UCM

	jgomez03@pdi.ucm.esta

	Cáculo de la geometría ConvexHull envolvente de los puntos procedentes de la localizacion

	Para obtener el valor final de la posición de la imagen, calcular el centroide de la goemtría

'''


from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
import numpy as np

points = np.random.rand(30, 2)   # 30 random points in 2-D
hull = ConvexHull(points)

puntosCvh = []

plt.plot(points[:,0], points[:,1], 'o')
for simplex in hull.simplices:
    plt.plot(points[simplex,0], points[simplex,1], 'k-')

    # Los puntos a procesar para el cálculo del centroide
    puntosCvh.append(points[simplex,0],points[simplex,1])
    

# posición del centroide calculado
centroide = np.mean(puntosCvh, axis=0)

# Calculamos, para cada uno de los puntos de la localizacion, la distancia al centroide
for p in hull.simplices:
	distance = sqrt((centroide[0]-points[simplex,0]) * (centroide[0]-points[simplex,0]) ) # ................ seguir aqui........
