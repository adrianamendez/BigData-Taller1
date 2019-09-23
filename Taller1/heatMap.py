import glob
import tarfile

import gmaps.datasets
import pathlib
import gmaps
import gmaps.datasets
import json
from ipywidgets.embed import embed_minimal_html
listLocations = []

def heatMap():
    locations = listLocations
    #locations = gmaps.datasets.load_dataset_as_df('acled_africa')
    fig = gmaps.figure(map_type='ROADMAP')
    heatmap_layer = gmaps.heatmap_layer(locations)
    fig.add_layer(heatmap_layer)
    embed_minimal_html('/Users/evergarden/Documents/PyProyects/Taller1/export.html', views=[fig])


def processAll():
    tar = tarfile.open("/Users/evergarden/Documents/PyProyects/Taller1/JsonFiles/Frag 04.tar.gz", "r:gz")
    for member in tar.getmembers():
        f = tar.extractfile(member)
        if f:
            data = f.read()
                # parse file
            obj = json.loads(data)
            print(data)
            for data in obj:
                latitudes = True
                if not (-180.0 <= data['location']['coordinates'][1] <= 180.0):
                    latitudes = False
                        # print(currentDirectory)
                if not (-90.0 <= data['location']['coordinates'][0] <= 90.0):
                    latitudes = False
                        # print(currentDirectory)

                if (latitudes):
                        # print(data['location']['coordinates'])
                    if (data['location']['coordinates'][1] >= -30.0):
                        tempLat = data['location']['coordinates'][0]
                        tempLon = data['location']['coordinates'][1]
                        data['location']['coordinates'][0] = round(tempLon,4)
                        data['location']['coordinates'][1] = round(tempLat,4)
                        listLocations.append(data['location']['coordinates'])
                    else:
                        tempLatElse = data['location']['coordinates'][0]
                        tempLonElse = data['location']['coordinates'][1]
                        data['location']['coordinates'][0] = round(tempLatElse, 4)
                        data['location']['coordinates'][1] = round(tempLonElse, 4)
                        listLocations.append(data['location']['coordinates'])
            heatMap()


processAll()