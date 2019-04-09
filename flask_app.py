#!/usr/bin/env python3
from flask import Flask, request, Response
import json
from sqlalchemy import and_
# user library that contains the format for table entries.
import modals

''' FEATURE:
    
    Safest route to location. 
    User picks place to go via map
    google maps api gives us path based on our own parameters <---- DO this first, fail faster
    Display the path
    
'''


app = Flask(__name__)

db = modals.CloudDB()


@app.route('/testing')
def make_db_query():

    ''' hits the database based on url parameters '''

    data_array = []
    # ip.addr/testing?lat=12.34&lon=43.21
    lat = request.args.get('lat', None)
    lon = request.args.get('lon', None)
    # Thre's no reason we should take anything other than numbers as an input
    try:
        lat = float(lat)
        lon = float(lon)
    except Exception as e: # Can't give hackers any clues so same output as any other generic error.
        return "No data available"

    if lat is None or lon is None:
        return "No data available"


    upper_lat = float(lat + 0.1)
    upper_lon = float(lon + 0.1)
    lower_lat = float(lat - 0.1)
    lower_lon = float(lon - 0.1)


    for entry in db.Session.query(modals.Location).filter(and_(
        modals.Location.longitude <= upper_lon, modals.Location.longitude >= lower_lon,
        modals.Location.latitude <= upper_lat, modals.Location.latitude >= lower_lat
                                                                    )):
        d = entry.__dict__
        entry_json = dict()
        for i, j in d.items():
            if i != "_sa_instance_state" and i != "id":
                entry_json[i] = j

        data_array.append(entry_json)

    data_to_ret = json.dumps(data_array)
    db.Session.flush()
    db.Session.commit()

    return data_to_ret


@app.route('/testing/dump')
def dump_db():
    ''' Gets all the data from the db and print it as json '''

    def generate(t):
        for k in t:
            for v in k.items():
                yield str(v) + '\n'
    a = []
    for entry in db.Session.query(modals.Location).limit(2000).all():
        a.append(entry.__dict__)

    return Response(generate(a), mimetype="text")


@app.route("/single")
def get_single():

    schema = modals.get_location_schematic()
    schema["rapes"] = 0
    lat = request.args.get('lat', None)
    lon = request.args.get('lon', None)
    # Thre's no reason we should take anything other than numbers as an input
    try:
        lat = float(lat)
        lon = float(lon)
    except Exception as e: # Can't give hackers any clues so same output as any other generic error.
        return "No data available"

    upper_lat = float(lat + 0.01)
    upper_lon = float(lon + 0.01)
    lower_lat = float(lat - 0.01)
    lower_lon = float(lon - 0.01)

    data_array = []

    for entry in db.Session.query(modals.Location).filter(and_(
        modals.Location.longitude <= upper_lon, modals.Location.longitude >= lower_lon,
        modals.Location.latitude <= upper_lat, modals.Location.latitude >= lower_lat
                                                                    )):
        d = entry.__dict__
        entry_json = dict()
        for i, j in d.items():
            if i != "_sa_instance_state" and i != "id":
                entry_json[i] = j

        data_array.append(entry_json)

    for i in data_array:
        for k, v in i.items():
            if k == "longitude" or k == "latitude":
                continue
            schema[k] += v

    return json.dumps(schema)



@app.route('/')
def ret_none():
    return "No data available"


@app.route('/json')
def ret_json():
    with open("json_updated.json") as f:
        json_data = f.read()
    return json_data


@app.errorhandler(404)
def get404d(num):

    return "Got that 404, bro"


@app.route('/<variable>')
def ret_coords(variable):

    comma_count = 0
    for i, v in enumerate(variable):
        if ',' == v:
            comma_count += 1

    if not comma_count == 1:
        return "Got that comma problem!"

    if not ',' in variable:
        return "Invalid format"

    # Read the formatted data and compare it to the GPS coordinates
    with open("json_updated.json") as f:
        json_data = f.read()

    # convert the json string into a dictionary
    json_data = json.loads(json_data)

    # get the latitude and longitude from the URL with ',' as a delimiter
    lat, lon = variable.split(',')

    try:
        lat = "{0:.2f}".format(float(lat))
        lon = "{0:.2f}".format(float(lon))
    except Exception as e:
        return "There was an exception: " + str(e)
    j = lat+lon

    new_json = dict()
    # set default values for JSON
    new_json = {
        "ASSAULT": 0, "MURDER": 0, "THEFT": 0, "RAPE": 0, "GTA": 0, "ROBBERY": 0, "OTHER": 0
    }
    new_json = json.dumps(new_json)

# checks if there's a coordinates stored
    if j in json_data:
        new_json = json.dumps(json_data[j])
    return new_json


if __name__ == "__main__":

    app.run("0.0.0.0", debug=False, port=80)
