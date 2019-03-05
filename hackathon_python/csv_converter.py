#!/usr/bin/env python3
import csv
from geopy.geocoders import Nominatim
import re
import string
import json

''' function for normalizing address strings '''
def sanitize_street_address(street_address_string):
    strlist = street_address_string.spit(' ')
    if("BLOCK" in strlist):#find block, if exist remove
        strlist.remove("BLOCK")
    if (" W " in strlist):
        strlist.remove(" W ")
    if (" E " in strlist):
        strlist.remove(" E ")
    if (" N " in strlist):
        strlist.remove(" N ")
    if (" S " in strlist):
        strlist.remove(" S ")
    return ' '.join(strlist)

def findlatlongkey(locate): # Here, `locate` is a string describing a street adress, or some other address resolvable by Nominatim's geolocation

    locate = sanitize_street_address(locate)

    geolocator = Nominatim(user_agent="find coordinates",
                           format_string="%s, San Bernardino, CA")
    location = geolocator.geocode(locate)
    #print("Latitude,   Longitude")
    #print(location.latitude, location.longitude)
    intone = str(location.latitude)[:-4]
    inttwo = str(location.longitude)[:-4]

    retkey = ",".join([intone, inttwo])
    return retkey

def findlatlongfull(locate):

    locate = sanitize_street_address(locate)

    geolocator = Nominatim(user_agent="find coordinates",
                           format_string="%s, San Bernardino, CA")
    location = geolocator.geocode(locate)
    #print("Latitude,   Longitude")
    #print(location.latitude, location.longitude)
    intone = str(location.latitude)
    inttwo = str(location.longitude)

    retkey = ",".join([intone, inttwo])
    return retkey


def main():

    with open("./csv.csv") as f:
       csv_reader = csv.reader(f)
       b = False
       locations = []
       master = dict()
       c = 0
       for row in csv_reader:
           if b:
                try:
                    s = findlatlongfull(row[2])
                    if not s in master:
                        master[s] = dict()
                        master[s]["ASSAULT"] = 0
                        master[s]["MURDER"] = 0
                        master[s]["THEFT"] = 0
                        master[s]["RAPE"] = 0
                        master[s]["GTA"] = 0
                        master[s]["ROBBERY"] = 0
                        master[s]["OTHER"] = 0

                    if "ASSAULT" in row[0]:
                        master[s]["ASSAULT"] += 1
                    elif "MURDER" in row[0]:
                        master[s]["MURDER"] += 1
                    elif "THEFT" in row[0]:
                        master[s]["THEFT"] += 1
                    elif "RAPE" in row[0]:
                        master[s]["RAPE"] += 1
                    elif "GTA" in row[0]:
                        master[s]["GTA"] += 1
                    elif "ROBBERY" in row[0]:
                        master[s]["ROBBERY"] += 1
                    else:
                        master[s]["OTHER"] += 1

                except:
                    locations.append("")
                    pass
           else:
               b = True

    print(master)
    json_ = json.dumps(master)
    print(json_)
    file = open("json.json", 'w')
    file.write(json_)
    file.close()

main()
