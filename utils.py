import modals
from sqlalchemy import and_

''' utilities to convert data from one database to another '''


db = modals.CloudDB()


def convert_master_to_user(db_item):
    # first iteration of converting master_db entries to user_interface entries
    interface_schematic = modals.get_location_schematic()  # the dictionary to manipulate
    usr_schema = modals.UserInterface()

    desc = db_item["description"].lower()


    # This is part of the code that we would want to tune.
    if "assault" in desc:
        interface_schematic["assaults"] += 1
    elif "murder" in desc:
        interface_schematic["murders"] += 1
    elif "theft" in desc or "larceny" in desc:
        interface_schematic["thefts"] += 1
    elif "rape" in desc:
        interface_schematic["rapes"] += 1
    elif "grand" in desc and "theft" in desc and "auto" in desc:
        interface_schematic["gta"] += 1
    elif "robbery" in desc:
        interface_schematic["robberies"] += 1
    else:
        interface_schematic["other"] += 1

    db_item["latitude"] = interface_schematic["latitude"]
    db_item["longitude"] = interface_schematic["longitude"]

    # create the sqlAlchemy object to be inserted into the new table
    usr_schema = modals.UserInterface(latitude=interface_schematic["latitude"], longitude=interface_schematic["longitude"],
                                      assaults=interface_schematic["assaults"], murders=interface_schematic["murders"],
                                      thefts=interface_schematic["thefts"], rapes=interface_schematic["rapes"],
                                      gta=interface_schematic["gta"], robberies=interface_schematic["robberies"],
                                      other=interface_schematic["other"])
    return usr_schema


def add_to_user_interface(master_list):
    # Iterates through a list of entries and then saves them in a database all at once.
    # Much faster than individual commits
    done = False
    bulk_entries = []
    while not done:
        for entry in master_list:
            usr_entry = convert_master_to_user(entry)
            bulk_entries.append(usr_entry)

    # db.Session.bulk_save_objects(bulk_entries)
    # db.Session.commit()
    # db.Session.close()


def transform():
    master = modals.MasterCrimeTable
    n_lower = 0
    lim = 60000
    total_entries = 3000000
    ''' Notes as of 3/9/2019
    lon lower: -122.59
    lon upper: -73.7088
    lat upper: 47.3116
    lat lower: 33.706
    '''
    # the bounds of the current data set.
    # TODO: make a function to do this automatically
    latL = 25.72
    latU = 50.13
    lonL = -125.9
    lonU = -50.71

    lat = latL
    lon = lonL
    n = lim
    done = False
    lat_mid = (latU - latL) / 2 + latL
    lon_mid = (lonU - lonL) / 2 + lonL
    cnt = 0
    while not done:
        if cnt % 4 == 0:
            lat_upper = lat_mid
            lon_upper = lon_mid
            lat_lower = latL
            lon_lower = lonU
        elif cnt % 4 == 1:
            lat_upper = latU
            lon_upper = lon_mid
            lat_lower = lat_mid
            lon_lower = lonL
        elif cnt % 4 == 2:
            lat_upper = lat_mid
            lon_upper = lonU
            lat_lower = lonL
            lon_lower = lon_mid
        else:
            lat_upper = latU
            lon_upper = lonU
            lat_lower = lat_mid
            lon_lower = lon_mid

        master_list = []

        # I need to change this to something that makes more sense.
        for entry in db.Session.query(master).filter(and_(master.longitude < lon_upper,
                                                          master.longitude >= lon_lower)).limit(500):

            master_list.append(entry.__dict__)

        if len(master_list) != 0:
            add_to_user_interface(master_list)

        print(len(master_list))
        lat += 20
        if lat >= latU:
            lon += 20
            lat = -latL
        cnt += 1
    print("n", n)


if __name__ == "__main__":
    transform()
