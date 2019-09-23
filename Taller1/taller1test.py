import glob

import pathlib
import numpy as np
import pandas as pd
import gmaps
import gmaps.datasets
import json
from bs4 import BeautifulSoup
from ipywidgets.embed import embed_minimal_html

gmaps.configure(api_key='AIzaSyAGVtraGXcVWdjRfOCaFEIyP6humVVrJr4')

path = pathlib.Path('JsonFiles/')
listLocations = []

def mapperp1(document):

    f = open("demofile2.txt", "w")

    soup = BeautifulSoup(document,features="lxml")
    title = soup.findAll('title')
    places = soup.findAll('places')
    topics = soup.findAll('topics')

    for wordtitle in title:
        title_final = str(wordtitle.string)
        title_final = title_final.split()

        for wordtitlefinal in title_final:
            print(('%s\t%s' % ("A "+wordtitlefinal, "1")), file=f)

    for wordplaces in places:
        places_final = str(wordplaces.string)

        places_final = places_final.split()

        for wordplacesfinal in places_final:
            print(('%s\t%s' % ("B "+wordplacesfinal, "1")), file=f)

    for wordtopics in topics:
        topics_final = str(wordtopics.string)
        topics_final = topics_final.split()

        for wordtopicsfinal in topics_final:
            print(('%s\t%s' % ("C "+wordtopicsfinal,"1")), file=f)

    f.close()

def processHeatMap(document):

    f = open("heatMap.txt", "w")
    data = document.read_json()
    data.inserted_date = document.to_datetime(data.inserted_date)

    bogota = np.array([[-74.2891, 4.5745], [-73.9529, 4.8763]])

    data.location = data.location.apply(str)

    data2 = data.location.str.rsplit(':', expand=True)

    data2 = data2.iloc[:, 2].str.replace(']}', "").str.rsplit(', ', expand=True)
    data2.iloc[:, 0] = data2.iloc[:, 0].str.replace('[', "")
    data2.columns = ['long', 'lat']
    data = pd.concat([data.drop(['location'], axis=1), data2], axis=1)
    data[['long', 'lat']] = data[['long', 'lat']].astype(float).round(4)
    listLocations.append(data2.columns)
    print(listLocations)

    f.close()

def coordinatesGidBogota():
    bogotaZone =  np.array([ 4.8763, -73.9529], [4.5745, -74.2891],[4.89287, -74.30987], [4.6082, -73.9377])


def heatMap():
    locations = listLocations
    #locations = gmaps.datasets.load_dataset_as_df('acled_africa')
    fig = gmaps.figure(map_type='ROADMAP')
    heatmap_layer = gmaps.heatmap_layer(locations)
    fig.add_layer(heatmap_layer)
    embed_minimal_html('/Users/evergarden/Documents/PyProyects/Taller1/export.html', views=[fig])


def reducerp1():
    word2titles = {}
    word2places = {}
    word2OptionA = {}
    word2OptionB = {}
    word2OptionC = {}
    counterA = 0
    counterB = 0
    counterC = 0
    top = 9
    document = open("demofile2.txt", "r")
    for line in list(document):
        line = line.strip()

        # parse the input we got from mapper.py
        word_titles, count_titles = line.split('\t', 1)
        word_places, count_places = line.split('\t', 1)
        # convert count (currently a string) to int
        try:
            count_titles = int(count_titles)
            count_places = int(count_places)
        except ValueError:
            continue

        try:
            word2titles[word_titles] = word2titles[word_titles] + count_titles
            word2places[word_places] = word2places[word_places] + count_places
        except:
            word2titles[word_titles] = count_titles
            word2places[word_places] = count_places

        # write the tuples to stdout
        # Note: they are unsorted

    word2titles2 = sorted(word2titles.items(), key=lambda x: x[1], reverse=True)
    for word in word2titles2:
        menu = word[0].split()
        final_word = str(menu[1]) +" "+str(word[1])


        if menu[0] == "A":
            if counterA <= top:
                word2OptionA[counterA] = final_word
                counterA += 1
        if menu[0] == "B":
            word2OptionB[counterB] = final_word
            counterB += 1
        if menu[0] == "C":
            word2OptionC[counterC] = final_word
            counterC += 1

    print("Encuentre las 10 palabras más frecuentes que aparecen en los títulos de las noticias que hay en el dataset ")
    for word in word2OptionA.values():
        print(word)

    print("Indique cuáles son los países donde se reportan las noticias y cuántas veces aparece cada uno en el dataset. ")
    for word in word2OptionB.values():
        print(word)

    print("Indique cuántas noticias se publican en cada tema que aparece en el dataset. ")
    for word in word2OptionC.values():
        print(word)


    document.close()



def processAll():
        for file in glob.glob("/Users/evergarden/Documents/PyProyects/Taller1/JsonFiles/*.json"):
            currentDirectory = pathlib.Path(file)
            with open(currentDirectory, 'r') as myfile:
                data = myfile.read()

            # parse file
            obj = json.loads(data)
            print(currentDirectory)
            for data in obj:
                latitudes = True
                if not (-180.0 <= data['location']['coordinates'][1] <= 180.0):
                    latitudes = False
                    # print(currentDirectory)
                if not (-90.0 <= data['location']['coordinates'][0] <= 90.0):
                    latitudes = False
                    # print(currentDirectory)

                if(latitudes):
                    # print(data['location']['coordinates'])
                    if(data['location']['coordinates'][1] >= -30.0):
                        tempLat = data['location']['coordinates'][0]
                        tempLon = data['location']['coordinates'][1]
                        data['location']['coordinates'][0] = tempLon
                        data['location']['coordinates'][1] = tempLat
                        listLocations.append(data['location']['coordinates'])
                    else:
                        listLocations.append(data['location']['coordinates'])
        heatMap()

processAll()


