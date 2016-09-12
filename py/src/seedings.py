from monthly import *

import sys
import json

def seedings(tournaments, weights):

    for key in tournaments:
        team = tournaments[key]
        team['points'] = get_seed_points(weights, team)

    return data



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('./{} <tournaments>.json <weights>.json'.format(sys.argv[0]))
        sys.exit()

    tournamentsFile = sys.argv[1]
    weightsFile = sys.argv[2]

    f = open(tournamentsFile, "r", encoding="utf8")
    tournaments = json.load(f)
    f.close()

    f = open(weightsFile, "r", encoding="utf8")
    weights = json.load(f)
    f.close()

    data = monthly(tournaments)
    teams = seedings(data, weights)
    _list = sorted(teams.items(), key=lambda item: item[1]['points'], reverse=True)

    for index, obj in enumerate(_list):
        rank = index+1
        team = obj[1]
        print("{},{},{}".format(rank, team['name'], team['points']))
