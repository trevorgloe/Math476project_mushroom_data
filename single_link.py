### compute single-linkage hierachical clustering on the data
#
#
import pandas as pd
import numpy as np
from numpy import linalg as LA
from numpy.random import default_rng
import scipy.sparse
import networkx as nx
import matplotlib.pyplot as plt
import os
import descartes
import geopandas as gpd
import remove_badpts
import scipy.spatial as spat
import scipy.cluster.hierarchy as hier

#np.seterr(divide='ignore', invalid='ignore')
rng = default_rng(12345)

curpath = os.getcwd()
temp = os.path.dirname(curpath)
datapath = os.path.join(temp,'mushroom_proj_data')

data = pd.read_csv('observations-319470.csv')

lat_n = data['latitude'].to_numpy()
lon_n = data['longitude'].to_numpy()


## look just at the slo area
lat_n[lon_n<-121.4]='nan'
lon_n[lon_n<-121.4]='nan'
lat_n[lon_n>-120.4]='nan'
lon_n[lon_n>-120.4]='nan'
lat_n[lat_n<35.0]='nan'
lon_n[lat_n<35.0]='nan'
lat_n[lat_n>36.0]='nan'
lon_n[lat_n>36.0]='nan'

# lat_n[lon_n<-140]='nan'
# lon_n[lon_n<-140]='nan'
# lat_n[lon_n>-110]='nan'
# lon_n[lon_n>-110]='nan'

bad_lat = lat_n[np.logical_not(np.isnan(lat_n))] # remove nans
bad_lon = lon_n[np.logical_not(np.isnan(lon_n))]
print(bad_lon)
print(bad_lat)
# lat[lon<-140]='nan'
# lon[lon<-140]='nan'

# remove points over the ocean
boundary_path = os.path.join(datapath,'s77p41.shp')
lat,lon = remove_badpts.getgudpts(bad_lat,bad_lon,boundary_path)

latlon = np.vstack((lat, lon)).T

# using euclidean distance for now
dist_mat = spat.distance.pdist(latlon,metric='euclidean')

Z = hier.linkage(dist_mat)

clusts = hier.fcluster(Z, 0.01, criterion='distance')

print(Z)
print(clusts)

street_map = gpd.read_file(os.path.join(datapath,'s77p41.shp'))
fig, ax = plt.subplots(figsize=(15,15))
street_map.plot(ax=ax,color=[0.9,0.9,0.9])
plt.scatter(latlon[:,1], latlon[:,0], c=clusts, s=2)
plt.show()
