#!/usr/bin/env python3
from flask import Flask, request
import json
from sqlalchemy import and_
# user library that contains the format for table entries.
import modals


app = Flask(__name__)

db = modals.CloudDB()


@app.route('/testing')
def make_db_query():

    ''' hits the database based on url parameters '''

    d_arr = []
    # ip.addr/testing?lat=12.34&lon=43.21
    lat = request.args.get('lat', None)
    lon = request.args.get('lon', None)

    lat = float(lat)
    lon = float(lon)

    upper_lat = float(lat + 0.1)
    upper_lon = float(lon + 0.1)
    lower_lat = float(lat - 0.1)
    lower_lon = float(lon - 0.1)

    if lat is None or lon is None:
        return "No data available"

    for entry in db.Session.query(modals.Location).filter(and_(
        modals.Location.longitude <= upper_lon, modals.Location.longitude >= lower_lon,
        modals.Location.latitude <= upper_lat, modals.Location.longitude >= lower_lat
                                                                    )):
        d = entry.__dict__
        entry_json = dict()
        for i, j in d.items():
            if i != "_sa_instance_state" and i != "id":
                entry_json[i] = j

        d_arr.append(entry_json)

    data_to_ret = json.dumps(d_arr)
    db.Session.flush()
    db.Session.commit()
    # threaded_session.remove()
    return data_to_ret


def get_valid_coords(lat, lon):

    ''' returns a list of coordinate tuples to check against the DB '''

    lat = float(lat)
    lon = float(lon)
    valid_coords = []
    range_x = 0.1
    range_y = 0.1
    for i in range(20):
        for j in range(20):
            # math: 20 * 0.01 is .2 so this list contains every coordinate +- 0.1 which is 400 coordinates... Maybe there's a query.get_if(latitude <= lat + 0.1 and latitude >= lat - 0.1)
            valid_coords.append(("{0:.2f}".format(lat + range_x), "{0:.2f}".format(lon + range_y)))
            range_y -= 0.01
        range_y = 0.1
        range_x -= 0.01
    return valid_coords


@app.route('/testing/dump')
def dump_db():

    a = []
    for entry in db.Session.query(modals.Location).all():
        a.append(entry.__dict__)

    to_ret = json.dumps(str(a))
    return to_ret

@app.route('/')
def ret_none():
    return "No data available";


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
    app.run("0.0.0.0", debug=True, port=5000)
