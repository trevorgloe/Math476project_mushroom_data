import pandas as pd
import numpy as np
from numpy import linalg as LA
from numpy.random import default_rng
import scipy.sparse
import networkx as nx
import matplotlib.pyplot as plt
import os
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

lat = lat_n[np.logical_not(np.isnan(lat_n))] # remove nans
lon = lon_n[np.logical_not(np.isnan(lon_n))]
print(lon)
# lat[lon<-140]='nan'
# lon[lon<-140]='nan'

#latlon = data[['latitude','longitude']].to_numpy()
latlon = np.vstack((lat, lon)).T
print(latlon)
#print(lat.shape)

def opt_reps(X, k, assign):
  (n, d) = X.shape
  reps = np.zeros((k, d))
  for i in range(k):
    in_i = [j for j in range(n) if assign[j] == i]
    print(in_i)
    reps[i,:]= np.sum(X[in_i,:],axis=0) / len(in_i)
  return reps

def opt_clust(X, k, reps):
  (n, d) = X.shape
  dist = np.zeros(n)
  assign = np.zeros(n, dtype=int)
  for j in range(n):
    dist_to_i = np.array([LA.norm(X[j,:] - reps[i,:]) for i in range(k)])
    assign[j] = np.argmin(dist_to_i)
    dist[j] = dist_to_i[assign[j]]
  G = np.sum(dist ** 2)
  print(G)
  return assign

def mmids_kmeans(X, k, maxiter=10):
  (n, d) = X.shape
  assign = rng.integers(0,k,n)
  reps = np.zeros((k, d), dtype=int)
  for iter in range(maxiter):
    reps = opt_reps(X, k, assign)
    assign = opt_clust(X, k, reps)
  return assign
  
assign = mmids_kmeans(latlon,4)
print(latlon)
print(assign)
plt.scatter(latlon[:,1], latlon[:,0], c=assign, s=2)
plt.show()
