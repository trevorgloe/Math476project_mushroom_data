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
    
    #point = geopandas.GeoDataFrame.from_file('points.shp') 
    poly  = geopandas.GeoDataFrame.from_file(boundary_path)

    points = []
    for pt in range(len(all_lat)):
        points.append(Point(all_lat[pt],all_lon[pt]))
    print(points)

    d = {'geometry': points}
    mushies = geopandas.GeoDataFrame(d)
    
    #pointInPolys = sjoin(mushies, poly, how='left')
    #grouped = pointInPolys.groupby('index_right')
    #res = list(grouped)
    print(poly)
    print(mushies)
    #print(res)

    for idx,row in poly.iterrows():
        print(row['geometry'])