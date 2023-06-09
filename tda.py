from ripser import ripser
import pandas as pd
import numpy as np
from persim import plot_diagrams
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon
import os


def main():
	curpath = os.getcwd()
	temp = os.path.dirname(curpath)
	datapath = os.path.join(temp,'mushroom_proj_data')
	temp = pd.read_csv('observations-319470.csv')
	#print(temp["latitude"])
	df = pd.DataFrame({"observed_on":temp["observed_on"] ,"common_name":temp["common_name"],"scientific_name":temp["scientific_name"],"longitude":temp["longitude"],"latitude":temp["latitude"],"id":temp["id"]}).set_index("id")# , index = .to_list())
	lat = df['latitude'].to_numpy()
	lon = df['longitude'].to_numpy()
	lat[lon<-140]='nan'
	lon[lon<-140]='nan'
	lat[lon>-110]='nan'
	lat[lon>-110]='nan'
	lon[lat>40]='nan'
	lat[lat>40]='nan'
	idx = np.isfinite(lat)&np.isfinite(lon)
	lat,lon = lat[idx],lon[idx]
	newar = []
	for i in range(len(lat)):
		newar.append([lon[i],lat[i]])
	coords = np.array(newar)
	ripCoords = ripser(coords,do_cocycles=True)
	D = ripCoords["dperm2all"]
	#print(ripCoords["cocycles"])
	#print(ripCoords["dgms"])


	#Max H1
	dgm1 = ripCoords["dgms"][1]
	distances = dgm1[1]-dgm1[0]
	#medDist = np.median(distances)
	idx = np.argmax(distances)
	#cocycle = ripCoords["cocycles"][1][idx]
	thresh = dgm1[idx, 0] #Project cocycle onto edges less than or equal to death time
	#maxthresh = 0.115592
	#minthresh = 0.000215526
	#medianthresh = 0.00621516
	fig, ax = plt.subplots()
	plotCocycle2D(D, coords, 0.009)
	plt.title("1-Form Thresh=%g"%thresh)
	plt.scatter(coords[:,0],coords[:,1],s=1)
	#street_map = gpd.read_file(os.path.join(datapath,'s77p41.shp'))
	#street_map.plot(ax=ax,color=[0.9,0.9,0.9])
	river_map = gpd.read_file(os.path.join(datapath,os.path.join('NHD_Major_Rivers_and_Creeks','Major_Rivers_and_Creeks.shp')))
	river_map.plot(ax=ax,color='blue')
	river_map2 = gpd.read_file(os.path.join(datapath,os.path.join('NHD_Major_Lakes_and_Reservoirs','Major_Lakes_and_Reservoirs.shp')))
	river_map2.plot(ax=ax,color='blue')
	plt.ylim(35.280,35.315)
	plt.xlim(-120.7,-120.65)


	
	plt.savefig("fig.png",transparent=True)




	#
	#plt.figure()
	#plt.scatter(lon,lat,s=1.0)
	#plt.figure(2)
	#plot_diagrams(ripCoords["dgms"],show=True)
	#plt.show()


def drawLineColored(X, C):
    for i in range(X.shape[0]-1):
        plt.plot(X[i:i+2, 0], X[i:i+2, 1], c=C[i, :], linewidth = 3)

def plotCocycle2D(D, X,thresh):
    """
    Given a 2D point cloud X, display a cocycle projected
    onto edges under a given threshold "thresh"
    """
    #Plot all edges under the threshold
    N = X.shape[0]
    #t = np.linspace(0, 1, 10)
    #c = plt.get_cmap('Greys')
    #C = c(np.array(np.round(np.linspace(0, 255, len(t))), dtype=np.int32))
    #C = C[:, 0:3]

    for i in range(N):
        for j in range(N):
            if D[i, j] <= thresh:
            	plt.plot( (X[i,0],X[j,0]) , (X[i,1],X[j,1]) ,color="r", linewidth=0.5)
               # Y = np.zeros((len(t), 2))
                #Y[:, 0] = X[i, 0] + t*(X[j, 0] - X[i, 0])
                #Y[:, 1] = X[i, 1] + t*(X[j, 1] - X[i, 1])


                #drawLineColored(Y, C)
    #Plot cocycle projected to edges under the chosen threshold
   # for k in range(cocycle.shape[0]):
    #    [i, j, val] = cocycle[k, :]
     #   if D[i, j] <= thresh:
      #      [i, j] = [min(i, j), max(i, j)]
       #     a = 0.5*(X[i, :] + X[j, :])
        #    plt.text(a[0], a[1], '%g'%val, color='b')
    #Plot vertex labels
    #for i in range(N):
    #    plt.text(X[i, 0], X[i, 1], '%i'%i, color='r')
    #plt.axis('equal')




if __name__ == "__main__":
	main()