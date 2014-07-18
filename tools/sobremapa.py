#!/usr/bin/python
#-*- coding: utf-8 -*-

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
#import numpy as np
 
#map = Basemap(projection='robin', lat_0=0, lon_0=0, resolution='l', area_thresh=1000.0)

map = Basemap(projection='merc', lat_0=0, lon_0=0,
    resolution = 'l', 
    llcrnrlon=-180, llcrnrlat=-75,
    urcrnrlon=180, urcrnrlat=75)
 
map.drawcoastlines()
map.drawcountries()
map.fillcontinents(color = 'coral')
map.drawmapboundary()


lons = [-135.3318, -134.8331, -134.6572]
lats = [57.0799, 57.0894, 56.2399]
x,y = map(lons, lats)
map.plot(x, y, 'bo', markersize=5)
 

 
labels = ['Sitka', 'Baranof Warm Springs', 'Port Alexander']
for label, xpt, ypt in zip(labels, x, y):
    plt.text(xpt+10000, ypt+5000, label)
 
plt.show()