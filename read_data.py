# script to read the initial data

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('observations-319470.csv')
print(data)

lat = data['latitude'].to_numpy()
lon = data['longitude'].to_numpy()

print(lat)
print(lon)

fig = plt.figure()
plt.scatter(lat,lon,s=1.0)
plt.show()