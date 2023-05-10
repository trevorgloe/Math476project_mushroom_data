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

fig = plt.figure()
plt.scatter(lat,lon,s=1.0)

street_map = gpd.read_file('Roads_-_All.shp')
fig, ax = plt.subplots(figsize=(15,15))
street_map.plot(ax=ax)

plt.show()