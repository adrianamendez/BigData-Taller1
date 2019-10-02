#!/usr/bin/env python
# coding: utf-8

# In[107]:


import numpy as np
import pandas as pd
import json, tarfile
import datetime as dt
import os


# In[146]:

def mapperPoint1():
    global longi, lati, ciudades, coord, coord2, dataF, repet
    longi = []
    lati = []

    dataF = pd.DataFrame()
    ciudades = ['bogotá', 'pereira', 'bucaramanga', 'cartagena', 'quito', 'guayaquil']
    coord = [[4.574, -74.289], [4.798, -75.782], [7.120, -73.133], [10.423, -75.562], [-0.216, -78.545],
             [-2.0535, -79.8576]]

    coord2 = [coord[i][0] * coord[i][1] for i in range(len(coord))]

    path = r'/Users/evergarden/Documents/PyProyects/Taller1/JsonFiles/Frag 4'

    for filename in os.listdir(path)[0:10]:

        vehic = filename[0:-5]
        data = pd.read_json(os.path.join(path, filename), orient='columns')
        data.inserted_date = pd.to_datetime(data.inserted_date)
        data = data.drop('location', axis=1)
        data['id'] = vehic

        z = open(os.path.join(path, filename), 'r').read()

        z = json.loads(z)

        if abs(z[5]['location']['coordinates'][0]) > 50:
            long = [round(z[i]['location']['coordinates'][0], 3) for i in range(len(z))]
            lat = [round(z[i]['location']['coordinates'][1], 3) for i in range(len(z))]

        else:
            long = [round(z[i]['location']['coordinates'][1], 3) for i in range(len(z))]
            lat = [round(z[i]['location']['coordinates'][0], 3) for i in range(len(z))]

        data['long'] = long
        data['lat'] = lat
        data = data.sort_values(by='inserted_date')
        data['minutes'] = [x.seconds / 60 for x in data.date.diff()]

        m = abs((data['long'][0] * data['lat'][0]) - coord2).min()  # compara la ubicación del id con todas las ciudades
        ind = list(abs((data['long'][0] * data['lat'][0]) - coord2)).index(m)  # el índice de la ciudad más cercana

        data['ciudad'] = ciudades[ind]  # identifica la ciudad como la más cercana
        data['Cord_X'] = round((data.long - coord[ind][1]) * 1000, 0)
        data['Cord_Y'] = round((data.lat - coord[ind][0]) * 1000, 0)
        data['sitio'] = data.Cord_X.apply(str) + '-' + data.Cord_Y.apply(str)
        data['latencia'] = (data.inserted_date - data.date).values.view('<i8') / 10 ** 9
        dataF = pd.concat([dataF, data])

        repet = pd.Series((dataF.Cord_X.diff() == 0) & (dataF.Cord_Y.diff() == 0))

    dataF = dataF[(dataF.number_of_satellites >= 10) & (repet != True)]
    dataF['diasem'] = dataF.date.dt.weekday_name
    dataF['hora'] = dataF.date.dt.hour
    dataF['index'] = 1
    dataF.reset_index(inplace=True)
    # print(dataF) este print corresponde al print de la salida del mapper
    dataF.to_csv(r'/Users/evergarden/Documents/PyProyects/Taller1/point1.csv') # este es el archivo que emulo de salida de mapper
    # dataF = dataF.loc[:,['ciudad', 'sitio','latencia','speed','diasem','hora']]

    # for h in range(len(dataF)):
    # print(dataF.loc[h,['ciudad', 'sitio','latencia','speed','diasem']].values.tolist())

def reducerPoint1():
    top = 9
    document = pd.read_csv("/Users/evergarden/Documents/PyProyects/Taller1/point1.csv")
    finalResult = document.groupby(['sitio','speed','hora','diasem']).ciudad.value_counts().nlargest(top)
    print(finalResult) # este print seria la salida del reducer

mapperPoint1()

result = dataF.loc[:, ['ciudad', 'sitio', 'latencia', 'speed', 'diasem', 'hora','index']].values.tolist()

reducerPoint1()
