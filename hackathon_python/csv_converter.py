import csv
from geopy.geocoders import Nominatim
import re
import string

def findlatlongkey(locate):

    locate.replace(" E ","EAST")

    strlist = locate.split(" ")
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
    if ("&" in strlist):
        index = strlist.find("&")
        strlist = strlist[:index]
    locate = " ".join(strlist)
    geolocator = Nominatim(user_agent="find coordinates",
                           format_string="%s, San Bernardino, CA")
    location = geolocator.geocode(locate)
    print(location.address)
    #print("Latitude,   Longitude")
    #print(location.latitude, location.longitude)
    intone = str(location.latitude)[:-4]
    inttwo = str(location.longitude)[:-4]

    retkey = ",".join([intone, inttwo])
    return retkey

def findlatlongfull(locate):

    strlist = locate.split(" ")
    if("BLOCK" in strlist):#find block, if exist remove
        strlist.remove("BLOCK")
    if ("W" in strlist):
        strlist.remove("W")
    if ("E"  in strlist):
        strlist.remove("E")
    if ("N" in strlist):
        strlist.remove("N")
    if ("S" in strlist):
        strlist.remove("S")
    if ("&" in strlist):
        index = strlist.find("&")
        strlist = strlist[:index]
    locate = " ".join(strlist)
    geolocator = Nominatim(user_agent="find coordinates",
                           format_string="%s, San Bernardino, CA")
    location = geolocator.geocode(locate)
    print(location.address)
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
       a = []
       for row in csv_reader:
           if b:
                a.append(row[2])
           else:
               b = True
    listofKey = list(map(findlatlongfull, a))
    print(listofKey)


main()
