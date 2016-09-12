# Roster csv to JSON. Excludes teams that didn't check-in.

import sys
import csv
import json

def rosters(file):
    f = open(file, "r", encoding="utf8")
    reader = csv.reader(f)

    first = False
    data = {}

    for line in reader:
        if not first:
            first = True
            continue

        team = line[0]
        player = line[1]
        checkin = line[2]

        if not checkin:
            continue
        elif team in data:
            data[team].append(player)
        else:
            data[team] = [ player ]

    return data


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('./{} <rosters>.csv'.format(sys.argv[0]))
        sys.exit()

    file = sys.argv[1]

    data = rosters(file)

    json.dump(data, sys.stdout, indent=2)
