## script to test the remove badpts function

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon
import os
import remove_badpts

curpath = os.getcwd()
temp = os.path.dirname(curpath)
datapath = os.path.join(temp,'mushroom_proj_data')

data = pd.read_csv('observations-319470.csv')
#print(data)

lat = data['latitude'].to_numpy()
lon = data['longitude'].to_numpy()
species = data['scientific_name'].to_numpy()

# print(lat)
# print(lon)
#print(species)

# cut off the lattiude and longitude 
lat[lon<-140]='nan'
lon[lon<-140]='nan'


boundary_path = os.path.join(datapath,'s77p41.shp')
remove_badpts.getgudpts(lat,lon,boundary_path)
