#!/usr/bin/env python3
import os
import json

def main():
    with open("json.json") as file:
        j = json.loads(file.read())
    master = dict()
    i = 0
    for key in j:
        split = key.split(",")
        split[0] = "{0:.4f}".format(float(split[0]))
        split[1] = "{0:.4f}".format(float(split[1]))
        s = split[0] + split[1]

        if not s in master:
            master[s] = dict()
            master[s]["ASSAULT"] = 0
            master[s]["MURDER"] = 0
            master[s]["THEFT"] = 0
            master[s]["RAPE"] = 0
            master[s]["GTA"] = 0
            master[s]["ROBBERY"] = 0
            master[s]["OTHER"] = 0
            i = i + 1
        for keyz in master[s]:
            master[s][keyz] += j[key][keyz]

    json_ = json.dumps(master)
    print(json_)
    file = open("json_updated.json", 'w')
    file.write(json_)
    file.close()

main()
