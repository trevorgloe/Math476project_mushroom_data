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

# initialize directory to save figures
fig_dir = os.path.join(temp,'figures')

lat_n = data['latitude'].to_numpy()
lon_n = data['longitude'].to_numpy()
species = data['scientific_name'].to_numpy()


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

lat_nfungi = np.copy(lat_n)
lon_nfungi = np.copy(lon_n)
# print(lat_nfungi)
lat_nfungi[species=='Fungi'] = 'nan'
lon_nfungi[species=='Fungi'] = 'nan'

bad_lat = lat_nfungi[np.logical_not(np.isnan(lat_n))] # remove nans
bad_lon = lon_nfungi[np.logical_not(np.isnan(lon_n))]
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

## plot of all clusters (not very helpful cause of the colors)
street_map = gpd.read_file(os.path.join(datapath,'s77p41.shp'))
fig, ax = plt.subplots(figsize=(15,15))
street_map.plot(ax=ax,color=[0.9,0.9,0.9])
plt.scatter(latlon[:,1], latlon[:,0], c=clusts, s=2)


## make a plot of different sets of the clusters, each containing 7 clusters
max_clustn = np.max(clusts)
max_clustinset = 7
print(max_clustn)

# create sets of clusters
# effectively parition the set of cluster numbers so that each partition contains exactly max_clustinset numbers
clust_sets = []
# current set of cluters
curset = []
# the number of clusters currently in the set (to be iterated)
numclust = 0
# current cluster
clusti = 0
while clusti < max_clustn:
    # current cluster set
    curset.append(clusti)
    clusti = clusti + 1
    #print(clust_sets)

    if len(curset)>max_clustinset:
        clust_sets.append(curset)
        curset = []

# get the last couple clusters in there, which has less than max_clustinset cluster numbers
if len(curset) == 0 and clusti==max_clustn:
    curset.append(max_clustn)
clust_sets.append(curset)

print(clust_sets)

# now make a new plot for each cluster set
for clustset in clust_sets:
    # find all the points that belong to a cluster in the set
    # initialize array of logicals for the points in one of the clusters
    inclust = np.zeros(len(latlon[:,0]))
    for idx in range(len(inclust)):
        # if point is in one of the clusters, make that spot in inclust equal to 
        if clusts[idx] in clustset:
            inclust[idx] = 1

    # convert to boolean array
    inclust = np.array(inclust, dtype=bool)
    #print(inclust)
    templat = latlon[:,0]
    templon = latlon[:,1]

    # get only the values in the desired clusters
    clustlat = templat[inclust]
    clustlon = templon[inclust]
    clustc = clusts[inclust]

    
    # make plot
    fig, ax = plt.subplots(figsize=(15,15))
    street_map.plot(ax=ax,color=[0.9,0.9,0.9])
    plt.scatter(clustlon, clustlat, c=clustc, s=9)
    plt.title('Clusters '+str(clustset),fontsize=30)
    #plt.xlabel('Longitude (deg)', fontsize=14, fontweight='bold')
    #plt.ylabel('Latitude (deg)', fontsize=14, fontweight='bold')
    plt.scatter(-120.6625,35.3050,color='g',marker='x',label='Cal Poly Campus')
    plt.legend(fontsize=30)
    ax.tick_params(axis='both', which='major', labelsize=30)
    ax.tick_params(axis='both', which='minor', labelsize=28)
    plt.xlim(-121.295,-120.4)
    plt.ylim(34.98,35.842)
    #plt.tight_layout()
    plt.savefig(os.path.join(fig_dir,str(clustset)+'.png'), transparent=True)


# print some additional information
print(len(np.unique(clusts)))
print(np.unique(clusts))

fig,ax = plt.subplots(figsize=(30,15))
dn = hier.dendrogram(Z)
# Hide X and Y axes label marks
ax.xaxis.set_tick_params(labelbottom=False)
#ax.yaxis.set_tick_params(labelleft=False)

# Hide X and Y axes tick marks
ax.set_xticks([])
#ax.set_yticks([])
plt.savefig('tree_dia.png',transparent=True)

plt.show()
