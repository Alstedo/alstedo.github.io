from monthly import *

import sys
import json

def seedings(tournaments, weights):

    data = tournaments
    for key in data:
        data[key]['points'] = get_seed_points(weights, data[key])

    return data

def get_seed_points(weights, team):
    points = 0

    for week in team['week']:
        standing = team['week'][week]

        if standing >= 33:
            standing = 33

        standing = str(standing)
        week = str(week)

        points = points + weights['weights'][standing]['weeks'][week]

    return points



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
