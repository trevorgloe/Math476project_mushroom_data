### script to test theoretical expression for the number of badly placed clusters

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon
import os
import random

def compute_err(clusters,species):
    # needs the array of clusters and the array of all species
    tot = 0

    for j in range(len(clusters)):
        # for every point, compute all the other points of the same species that are in other clusters
        #print('point spec = '+str(species[j]))
        #print('point clust = ' + str(clusters[j]))
        for pt in range(len(clusters)):
            #print('test_pt spec = '+str(species[pt]))
            #print('test cluster = '+str(clusters[pt]))
            if clusters[j] != clusters[pt] and species[pt] == species[j]:
                tot = tot + 1
                #print('added!')

    return tot

def compute_types(species):
    sum = 0
    uni_spec = np.unique(species)
    print('unique species = '+str(uni_spec))

    for i in range(len(uni_spec)):
        c = np.count_nonzero(species == uni_spec[i])
        sum = sum + c*(c-1)
        #print(species=uni_spec)
        #print(sum)

    return sum

def theory_err(species,numclust):
    # computes the theoretical error in the clustering
    tot_types = compute_types(species)

    return (k-1)/k * tot_types


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


# gimme some test data
# test_spec = [1,1,1,2,2,3,3,3,3,3]
test_spec = [1,1,1,1,2,3,1,2,3,1,2,3,3,4,4,4,4,4,4,4,4,4,5,5,5,5,5,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,7,7,7,7]

## make some random clusters
N = len(species)
k = 40  # number of clusters
clusters = np.zeros(N)

for i in range(N):
    clusters[i] = random.randint(1,k)

#clusters = [1,1,1,1,1,1,2,2,2,3,3,3,3]

print(species)
print(clusters)
print(theory_err(species,k))
print(compute_err(clusters,species))



