### Script to remove all the points whos lat and lon put them outside of the california state boundaries
#
# Takes all the points, returns only the points who are within the california state boundaries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import descartes
from shapely.geometry import Point, Polygon
import os
import fiona
from geopandas.tools import sjoin
import geopandas
from shapely.geometry import shape,mapping, Point, Polygon, MultiPolygon

def getgudpts(all_lat,all_lon,boundary_path):
    # all_lat and all_lon are numpy arrays of all the points, boundary_path is the path to the shapefile containing the california boundary
    

    # get shape file for the boundaries 
    poly  = geopandas.GeoDataFrame.from_file(boundary_path)

    # create list of points we want to consider
    points = []
    for pt in range(len(all_lat)):
        points.append(Point(all_lon[pt],all_lat[pt]))
    #print(points)

    # geopandas dataframe for points
    d = {'geometry': points}
    mushies = geopandas.GeoDataFrame(d)

    # regular pandas dataframe for the points (with column for whether they are in the boundaries or not)
    d = np.vstack([all_lon,all_lat,np.zeros(len(all_lon))]).T
    test_pts = pd.DataFrame(d,columns=['longitude','latitude','in bounds'])

    print(test_pts)
    
    #pointInPolys = sjoin(mushies, poly, how='left')
    #grouped = pointInPolys.groupby('index_right')
    #res = list(grouped)
    print(poly)
    print(mushies)
    #print(res)

    # make figure to plot to check
    plt.figure()

    # interate through all polygons stored in the shape file
    for idx,row in poly.iterrows():
        #print(row['geometry'])
        # if type(row['geometry'])==class 'shapely.geometry.multipolygon.MultiPolygon':
        # need a separate thing to do if its a polygon or multipolygon (have to iterate through multipolygons)
        if row['geometry'].geom_type== 'MultiPolygon':
            print(type(row['geometry']))
            # iterate through polygons
            for geom in row['geometry'].geoms:
                plt.plot(*geom.exterior.xy,color='b')

                # iterate through points in the dataframe
                for idx,mushroom in mushies.iterrows():
                    #print(mushroom[1]['geometry'])
                    # print(idx)
                    pt = mushroom['geometry']
                    
                    # check if point is within the polygon
                    if pt.within(geom):
                        print('found point in boundarys!')
                        # if the point is in there, add 1 to the point in the column in the dataframe (should not be more than 1 if the polygons aren't overlapping)
                        test_pts['in bounds'].iloc[idx] = test_pts['in bounds'].iloc[idx]+1

        else:
            plt.plot(*row['geometry'].exterior.xy,color='b')
            # iterate through points
            for idx,mushroom in mushies.iterrows():
                #print(mushroom[1]['geometry'])
                # print(idx)
                pt = mushroom['geometry']
                
                # check if point is within the polygon
                if pt.within(row['geometry']):
                    print('found point in boundarys!')
                    # if point is in there, add 1 to the column in the dataframe
                    test_pts['in bounds'].iloc[idx] = test_pts['in bounds'].iloc[idx]+1


    # print(test_pts['in bounds'].to_numpy())

    #shape = Polygon(poly['geometry'].iloc[37])
    #slo = poly['geometry'].iloc[50]

    # plt.figure()
    # main = slo.geoms[0]
    # plt.plot(*main.exterior.xy)
    # for mushroom in mushies.iterrows():
    #     #print(mushroom[1]['geometry'])
    #     pt = mushroom[1]['geometry']
    #     print(pt.within(main))
        # if pt.within(geom):
        #     print('found point inside!')
    #plt.plot(*geom.exterior.xy)
    #print(shape)

    
    

    #plt.plot(*shape.exterior.xy)
    # plot all the points with a color according to whether they are in the boundaries, for debugging purposes
    plt.scatter(all_lon,all_lat,s=2,c=test_pts['in bounds'].to_numpy())

    # make new arrays of the lat and lon that are within the boundaries
    # need to dynamically allocate them
    temp_new_lat = []
    temp_new_lon = []

    for idx,row in test_pts.iterrows():
        if row['in bounds']>0:
            temp1 = row['latitude']
            print(temp1)
            temp2 = row['longitude']
            temp_new_lat.append(temp1)
            temp_new_lon.append(temp2)

    new_lat = np.array(temp_new_lat)
    new_lon = np.array(temp_new_lon)
    
    print(new_lat)
    print(new_lon)

    return new_lat,new_lon
    # plt.show()

