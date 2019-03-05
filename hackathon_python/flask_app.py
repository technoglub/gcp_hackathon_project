#!/usr/bin/env python3
from flask import Flask
import json

app = Flask(__name__)

@app.route('/<variable>')
def ret_coords(variable):
    with open("json_updated.json") as f:
        json_data = f.read()
    json_data = json.loads(json_data)



    lat, lon = variable.split(",")
    lat = "{0:.4f}".format(float(lat))
    lon = "{0:.4f}".format(float(lon))

    j = lat+lon

    if j in json_data:
        new_json = json.dumps(json_data[j])



    return new_json


