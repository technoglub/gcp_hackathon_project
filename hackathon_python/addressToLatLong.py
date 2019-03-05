#!/usr/bin/env python3
from geopy.geocoders import Nominatim
import re
import string

class findcor:

    def __init__(self):
        pass

    def findlatlongkey(locate):
        strlist = locate.split(" ")
        if("BLOCK" in strlist):#find block, if exist remove
            strlist.remove("BLOCK")
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
