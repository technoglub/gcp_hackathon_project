#! /usr/bin/python3

import modals
import csv
import datetime


def main():

    db = modals.CloudDB()

    list_of_data = []
    first_pass = True
    rows = 0
    with open("baltimorecity3335") as f:
        baltimore_crime_data = csv.reader(f)
        for row in baltimore_crime_data:
            rows += 1
            if rows > 50000:  # approx 1 year of data
                break
            if first_pass:
                first_pass = False
                continue
            dt = row[0]
            lon = row[10]
            lat = row[11]
            crime_type = row[4]
            data_to_enter = dict()
            data_to_enter["gta"] = 0
            data_to_enter["assault"] = 0
            data_to_enter["murder"] = 0
            data_to_enter["theft"] = 0
            data_to_enter["rape"] = 0
            data_to_enter["robbery"] = 0
            data_to_enter["other"] = 0

            dt = datetime.datetime.strptime(dt, "%m/%d/%Y")

            data_to_enter["CrimeDate"] = dt
            try:
                data_to_enter["longitude"] = float(lon)
                data_to_enter["latitude"] = float(lat)

            except Exception as e:
                print(e, row)
                continue

            if "assault" in row[4].lower():
                data_to_enter["assault"] += 1

            elif "murder" in row[4].lower():
                data_to_enter["murder"] += 1

            elif "theft" in crime_type.lower() or "larceny" in crime_type.lower():
                data_to_enter["theft"] += 1

            elif "rape" in crime_type.lower():
                data_to_enter["rape"] += 1

            elif "grand" in crime_type.lower() and \
                 "theft" in crime_type.lower() and \
                 "auto"  in crime_type.lower():
                data_to_enter["gta"] += 1

            elif "robbery" in crime_type.lower():
                data_to_enter["robbery"] += 1

            else:
                data_to_enter["other"] += 1

            list_of_data.append(data_to_enter)

    for count, data_item in enumerate(list_of_data):
        try:
            add_data_to_db(data_item, db)
        except:
            print(count, data_item)


def add_data_to_db(new_entry, db):
    data_to_enter = modals.Location(latitude=new_entry["latitude"], longitude=new_entry["longitude"],
                                    assaults=new_entry['assault'],
                                    murders=new_entry["murder"], rapes=new_entry["rape"],
                                    thefts=new_entry["theft"], gta=new_entry["gta"],
                                    robberies=new_entry["robbery"], other=new_entry["other"]
                                    )
    db.Session.add(data_to_enter)
    db.Session.flush()
    db.Session.close()


main()
