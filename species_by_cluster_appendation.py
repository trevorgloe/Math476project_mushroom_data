# Take the clusters generated by the single-link algorithm and print the population of clusters
# any unkown fungi.  Run this code after single_link.py

# We need the species names associated with each longitude and latitude.
all_lat = data['latitude'].to_numpy()
all_lon = data['longitude'].to_numpy()
all_spe = data['scientific_name'].to_numpy()

species = []    #put down some space for our species list
index_offset = 0

# Now we run down the original longitude and latitude lists.  If their coordinates are in our
# doctored lists (only ones in SLO and only ones on land) then we add the corresponding species
# name to our species name list.

for j in range(len(all_lat)):
    if all_lat[j] == lat[j - index_offset] and all_lon[j] == lon[j - index_offset]:
        species.append(all_spe[j])
    else:
        index_offset = index_offset + 1

# Now we want a big list of all the unique identified scientific names (so no 'fungus' allowed.)

mushnames= []
for n in all_spe:
    if not n in mushnames and not n == "Fungi":
        mushnames.append(n)

# The next step is to form the cluster species matrix, wherein the (i,j)th entry is the number of 
# mushrooms of the j'th species in the i'th cluster (ordered as in the mushnames array).

clustnames = []
for x in clusts:
    if not x in clustnames:
        clustnames.append(x)

CSM = np.zeros((len(clustnames), len(mushnames)), int)
for i in range(len(clustnames)):
    for j in range(len(mushnames)):
        for k in range(len(species)):
            if clusts[k] == clustnames[i] and species[k] == mushnames[j]:
                CSM[i,j] = CSM[i,j] + 1


# Now let's identify the uknown mushrooms.
for j in range(len(species)):
    if species[j] == "Fungi":
        print("Uknown fungus:  long, lat =", lon[j], ",", lat[j])
        print("cluster population:")
        for k in range(len(mushnames)):
            if not CSM[clustnames == clusts[j], k] == 0:
                print(CSM[clustnames == clusts[j], k], mushnames[k])
        input()