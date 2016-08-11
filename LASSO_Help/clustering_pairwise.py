__author__ = 'zoorobmj'


import math
from sklearn import metrics
import numpy as np
import pandas as pd
from random import randint


def clustering(array):
    pairs = []
    for list in array:
        print list
        for distance in list:
            current = None
            if distance == 0:
                continue
            else:
                if not current:
                    current = distance
                else:
                    if distance < current:
                        currrent = distance
            pairs.append(current)

    return pairs


def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d


if __name__ == '__main__':
    df = pd.read_csv('dom.csv', sep=',', header=0)
    df['Cluster'] = 0
    X = df.copy()

    parishes = pd.unique(df.Parish.ravel())

    counter = 1
    for parish in parishes:
        print parish
        # df.to_csv('gren-out.csv')
        X = df[df.Parish == parish].copy().reset_index(drop=True)
        print X
        while len(X) > 0:
            if len(X) > 3:
                random = randint(0, len(X)-1)
                print "random number: ", random
                pin1 = X.iloc[random].iloc[1]
                lat = float(X.iloc[random].iloc[2])
                long = float(X.iloc[random].iloc[3])
                # print lat, long
                pins = []
                distances = []
                for i in X.index:
                    pins.append(X.ix[i][1])
                    lat2 = X.ix[i][2]
                    long2 = X.ix[i][3]
                    distances.append(distance([lat, long], [lat2, long2]))
                # print "at this point:"

                distances = np.asarray(distances)
                print distances

                rel_min = np.min(distances[np.nonzero(distances)])
                # print rel_min
                itemindex = np.where(distances == rel_min)
                print itemindex

                indexX = itemindex[0][0]
                print "index is:", indexX

                pin2 = X.loc[indexX][1]
                print pin2

                print X

                index1 = df.Pins[df.Pins == pin1].index.tolist()[0]
                index2 = df.Pins[df.Pins == pin2].index.tolist()[0]

                X = X[X.Pins != pin1].reset_index(drop=True)
                X = X[X.Pins != pin2].reset_index(drop=True)

                df.set_value(index1,'Cluster', counter)
                df.set_value(index2,'Cluster', counter)
                length = len(X)
                print "length is ", length
                counter += 1
            elif len(X) == 3:
                p1 = X.loc[0][1]
                p2 = X.loc[1][1]
                p3 = X.loc[2][1]
                index1 = df.Pins[df.Pins == p1].index.tolist()[0]
                index2 = df.Pins[df.Pins == p2].index.tolist()[0]
                index3 = df.Pins[df.Pins == p3].index.tolist()[0]
                df.set_value(index1,'Cluster', counter)
                df.set_value(index2,'Cluster', counter)
                df.set_value(index3,'Cluster', counter)
                X = X[X.Pins != p1].reset_index(drop=True)
                X = X[X.Pins != p2].reset_index(drop=True)
                X = X[X.Pins != p3].reset_index(drop=True)
                counter += 1
            else:
                p1 = X.loc[0][1]
                p2 = X.loc[1][1]
                index1 = df.Pins[df.Pins == p1].index.tolist()[0]
                index2 = df.Pins[df.Pins == p2].index.tolist()[0]
                df.set_value(index1,'Cluster', counter)
                df.set_value(index2,'Cluster', counter)
                X = X[X.Pins != p1].reset_index(drop=True)
                X = X[X.Pins != p2].reset_index(drop=True)
                counter += 1

    df.to_csv('dom-out.csv')







