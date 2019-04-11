import modals
from sqlalchemy import and_
import datetime

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

    ''' Notes as of 3/9/2019
    lon lower: -122.59
    lon upper: -73.7088
    lat upper: 47.3116
    lat lower: 33.706
    
    Date recent: 03/31/2019
    date oldest: 01/01/2001 ; There are older dates, but I figure they're not relevant
    '''
    # the bounds of the current data set.
    # TODO: make a function to do this automatically
    start_yr = 2001
    start_month = 1
    start_day = 1
    end_yr = 2019
    end_month = 3
    end_day = 31

    cur_yr = 2001
    cur_mnth = 2
    cur_day = 1

    oldest_dt = datetime.datetime(start_yr, start_month, start_day)
    newest_dt = datetime.datetime(end_yr, end_month, end_day)

    dt_rng_old = oldest_dt
    dt_rng_new = datetime.datetime(start_yr, start_month + 1, start_day)


    done = False
    cnt = 0

    # TODO: I need to make a dictionary that contains a dictionary DB entry, and a month counter to divide each
    # entry by the amount of months of data it has

    while not done:

        master_list = []

        # get entries based on the month.
        for entry in db.Session.query(master).filter(and_(master.date < dt_rng_new,
                                                          master.date >= dt_rng_old)):

            master_list.append(entry.__dict__)

        if len(master_list) != 0:
            add_to_user_interface(master_list)

        cur_mnth += 1
        if cur_mnth > 12:
            cur_mnth = 1
            cur_yr += 1

        dt_rng_old = dt_rng_new
        dt_rng_new = datetime.datetime(cur_yr, cur_mnth, cur_day)



if __name__ == "__main__":
    transform()
