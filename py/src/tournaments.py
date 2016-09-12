#!/usr/bin/python

import sys
import json

def tournaments(tournaments, tournament):
    date = tournament['date']
    data = tournaments
    data[date] = tournament
    return data



if __name__ == "__main__":

    if len(sys.argv) != 3:
        print('./{} <tournaments>.json <tournament>.json'.format(sys.argv[0]))
        sys.exit()

    tournamentsFile = sys.argv[1]
    tournamentFile = sys.argv[2]

    f = open(tournamentsFile, "r", encoding="utf8")
    _tournaments = json.load(f)
    f.close()

    f = open(tournamentFile, "r", encoding="utf8")
    tournament = json.load(f)
    f.close()

    data = tournaments(_tournaments, tournament)

    f = open(tournamentsFile, "w", encoding="utf8")
    json.dump(data, f, indent=2, sort_keys=True)
    f.close()
