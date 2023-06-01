### script to make nice picture of data with all the points and the data without the bad points or unidentified points
#
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

# look at the species
num_fungi = np.count_nonzero(species =='Fungi')

print(len(np.unique(species)))
print(len(species))
print(num_fungi)

uni_species = np.unique(species)
# find the species with the highest occurances
# create dataframe of species with their respective counts
counts = np.zeros(uni_species.shape)
for i in range(len(uni_species)):
    counts[i] = np.count_nonzero(species == uni_species[i])

species_counts = pd.DataFrame(np.vstack((uni_species,counts)).T,columns=['Species','Occurances'])
# print(species_counts)
print(species_counts.to_string())

#print(lat)

## first plot of all points

fig = plt.figure()
# plt.scatter(lat,lon,s=1.0)

street_map = gpd.read_file(os.path.join(datapath,'s77p41.shp'))
fig, ax = plt.subplots(figsize=(15,15))
street_map.plot(ax=ax,color=[0.9,0.9,0.9])

river_map = gpd.read_file(os.path.join(datapath,os.path.join('NHD_Major_Rivers_and_Creeks','Major_Rivers_and_Creeks.shp')))
river_map.plot(ax=ax,color='blue')

river_map2 = gpd.read_file(os.path.join(datapath,os.path.join('NHD_Major_Lakes_and_Reservoirs','Major_Lakes_and_Reservoirs.shp')))
river_map2.plot(ax=ax,color='blue')

plt.scatter(lon,lat,color='r',s=2.0)

plt.xlabel('Longitude (deg)', fontsize=14, fontweight='bold')
plt.ylabel('Latitude (deg)', fontsize=14, fontweight='bold')

## plot slo as a green x
plt.scatter(-120.6625,35.3050,color='g',marker='x',label='Cal Poly Campus')
plt.legend()
plt.xlim(-121.295,-120.4)
plt.ylim(34.98,35.842)


## second plot of just good points
fig2 = plt.figure()

goodlat,goodlon,goodspec = remove_badpts.getgudpts_wspec(lat,lon,species,os.path.join(datapath,'s77p41.shp'))

street_map = gpd.read_file(os.path.join(datapath,'s77p41.shp'))
fig, ax = plt.subplots(figsize=(15,15))
street_map.plot(ax=ax,color=[0.9,0.9,0.9])

river_map = gpd.read_file(os.path.join(datapath,os.path.join('NHD_Major_Rivers_and_Creeks','Major_Rivers_and_Creeks.shp')))
river_map.plot(ax=ax,color='blue')

river_map2 = gpd.read_file(os.path.join(datapath,os.path.join('NHD_Major_Lakes_and_Reservoirs','Major_Lakes_and_Reservoirs.shp')))
river_map2.plot(ax=ax,color='blue')

# plt.scatter(lon,lat,color='r',s=2.0)

lat_nfungi = np.copy(goodlat)
lon_nfungi = np.copy(goodlon)
print(lat_nfungi)
lat_nfungi[goodspec=='Fungi'] = 'nan'
lon_nfungi[goodspec=='Fungi'] = 'nan'

plt.scatter(lon_nfungi,lat_nfungi,color='red',s=2)
plt.xlabel('Longitude (deg)', fontsize=14, fontweight='bold')
plt.ylabel('Latitude (deg)', fontsize=14, fontweight='bold')

## plot slo as a green x
plt.scatter(-120.6625,35.3050,color='g',marker='x',label='Cal Poly Campus')
plt.legend()
plt.xlim(-121.295,-120.4)
plt.ylim(34.98,35.842)

plt.show()