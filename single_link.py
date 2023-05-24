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

#np.seterr(divide='ignore', invalid='ignore')
rng = default_rng(12345)

curpath = os.getcwd()
temp = os.path.dirname(curpath)
datapath = os.path.join(temp,'mushroom_proj_data')

data = pd.read_csv('observations-319470.csv')

lat_n = data['latitude'].to_numpy()
lon_n = data['longitude'].to_numpy()

lat_n[lon_n<-140]='nan'
lon_n[lon_n<-140]='nan'
lat_n[lon_n>-110]='nan'
lon_n[lon_n>-110]='nan'

bad_lat = lat_n[np.logical_not(np.isnan(lat_n))] # remove nans
bad_lon = lon_n[np.logical_not(np.isnan(lon_n))]
print(bad_lon)
# lat[lon<-140]='nan'
# lon[lon<-140]='nan'

# remove points over the ocean
boundary_path = os.path.join(datapath,'s77p41.shp')
lat,lon = remove_badpts.getgudpts(bad_lat,bad_lon,boundary_path)