# script to read the initial data

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon

data = pd.read_csv('observations-319470.csv')
print(data)

lat = data['latitude'].to_numpy()
lon = data['longitude'].to_numpy()

print(lat)
print(lon)

# cut off the lattiude and longitude 
lat[lon<-140]='nan'
lon[lon<-140]='nan'

print(lat)

fig = plt.figure()
plt.scatter(lat,lon,s=1.0)

street_map = gpd.read_file('s77p41.shp')
fig, ax = plt.subplots(figsize=(15,15))
street_map.plot(ax=ax,color=[0.9,0.9,0.9])

river_map = gpd.read_file('Inland_Creek_Combining_Designation.shp')
river_map.plot(ax=ax,color='blue')

plt.scatter(lon,lat,color='r',s=2.0)

plt.show()