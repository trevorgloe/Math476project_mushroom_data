# script to read the initial data

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon
import os

curpath = os.getcwd()
temp = os.path.dirname(curpath)
datapath = os.path.join(temp,'mushroom_proj_data')

data = pd.read_csv('observations-319470.csv')
print(data)

lat = data['latitude'].to_numpy()
lon = data['longitude'].to_numpy()
species = data['scientific_name'].to_numpy()

# print(lat)
# print(lon)
print(species)

# cut off the lattiude and longitude 
lat[lon<-140]='nan'
lon[lon<-140]='nan'

print(lat)

fig = plt.figure()
plt.scatter(lat,lon,s=1.0)

street_map = gpd.read_file(os.path.join(datapath,'s77p41.shp'))
fig, ax = plt.subplots(figsize=(15,15))
street_map.plot(ax=ax,color=[0.9,0.9,0.9])

river_map = gpd.read_file(os.path.join(datapath,'NHD_Major_Rivers_and_Creeks/Major_Rivers_and_Creeks.shp'))
river_map.plot(ax=ax,color='blue')

river_map2 = gpd.read_file(os.path.join(datapath,'NHD_Major_Lakes_and_Reservoirs/Major_Lakes_and_Reservoirs.shp'))
river_map2.plot(ax=ax,color='blue')

plt.scatter(lon,lat,color='r',s=2.0)

plt.show()