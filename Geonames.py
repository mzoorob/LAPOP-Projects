__author__ = 'zoorobmj'

import re
import csv
import urllib2
import os
from time import sleep

# (optional) update me to confirm that coordinates are in-country
# COUNTRY = "Bolivia"
USERNAME = "" # geonames username

def readcsv(filename):
    interviewcoords = []
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            interviewcoords.append([val.encode("utf-8") for val in row])
    return interviewcoords


def get_place(lat, lon, idx=None, id=None):

    baseurl = "http://api.geonames.org/findNearbyPlaceName?"
    apiQuery = "lat="+str(lat)+"&lng="+str(lon)+"&localCountry=TRUE&username="+USERNAME
    url = baseurl+apiQuery

    # visit the website and retrieve the page corresponding to these coordinates
    req = urllib2.urlopen(url)
    sleep(1)
    content1 = req.read()
    encoding=req.headers['content-type'].split('charset=')[-1]
    content = unicode(content1, encoding)

    # these are the codes we are looking for
    code1 = re.compile("<name>([^(]*)\</name>")
    code2 = re.compile("<geonameId>([^(]*)\</geonameId>")
    codelat = re.compile("<lat>([^(]*)\</lat>")
    codelon = re.compile("<lng>([^(]*)\</lng>")
    code3 = re.compile("<distance>([^(]*)\</distance>")

    # country check
    country_check = re.compile("<countryName>(.*)</countryName>")

    # find those codes in the website content
    name = re.findall(code1, content)
    if not name:
        name2 = re.compile("<name>(.*)</name>")
        name = re.findall(name2, content)
    print "name", name
    geoid = re.findall(code2, content)
    dist = re.findall(code3, content)
    lat_co = re.findall(codelat, content)
    lon_co = re.findall(codelon, content)

    country_given = re.findall(country_check, content)
    # print country_given
    # if country_given:
            # if country_given[0] != COUNTRY:
                # print "not in country eh"
                # return "Error (Coordinate not in assigned Country)", "Error", "Error", "Error", "Error"

    # error checking.
    for item in [name, geoid, dist]:
        if len(item) != 1:
            print url, id

    # if there are values, return them
    try:
        return [name[0], geoid[0], dist[0], lat_co[0], lon_co[0], country_given[0]]
    # otherwise return errors
    except:
        try:
            return ["Error", "Error", "Error", "Error", "Error", country_given[0]]
        except:
            return ["Error", "Error", "Error", "Error", "Error", "Error"]


def save_csv(output, filename):
    with open(filename, "wb") as f:
        writer = csv.writer(f)
        for row in output:
            writer.writerow([val.encode("utf-8") for val in row])

if __name__ == '__main__':
    folder = "C:\Users\zoorobmj\PycharmProjects\Geonames"   # my directory
    files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    idx = 1
    for f in files:
        interviewcoords = readcsv(f)
        interviewcoords[0].extend(["Place_Name","GeoID", "Distance", "Place_Lat", "Place_Lon", "Ctryname"])
        for row in interviewcoords[1:]:
            if str(row[1]) == "0":
                row.extend(["No GPS Coords", "No GPS Coords", "No GPS Coords", "No GPS Coords", "No GPS Coords", "No GPS Coords"])
            else:
                row.extend(get_place(row[1], row[2], id=row[0]))
                idx += 1
            if idx % 50 == 0:
                print idx
                sleep(2)

        save_csv(interviewcoords, f[0:-4]+"geooutput.csv")
        print f + " is finished"


