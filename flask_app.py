#!/usr/bin/python3
from flask import Flask
import json


app = Flask(__name__)

@app.route('/')
def ret_none():
    return "No data available\n";

@app.route('/<variable>')
def ret_coords(variable):

    print(variable)
    #Read the formatted data and compare it to the GPS coordinates
    with open("json_updated.json") as f:
        json_data = f.read()

    #convert the json string into a dictionary
    json_data = json.loads(json_data)

    #get the latitude and longitude from the URL with ',' as a delimiter
    lat, lon = variable.split(',')

    print(lat)
    print(lon)

    lat = "{0:.2f}".format(float(lat))
    lon = "{0:.2f}".format(float(lon))

    j = lat+lon

    new_json = dict()
    #set default values for JSON
    new_json = {
    "ASSAULT": 0, "MURDER": 0, "THEFT": 0, "RAPE": 0, "GTA": 0, "ROBBERY": 0, "OTHER": 0
    }
    new_json = json.dumps(new_json)
    #checks if there's a coordinates stored
    if j in json_data:
        new_json = json.dumps(json_data[j])
    return new_json

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)