import sys
import json

def tournament(date, rosters, standings):

    data = {
        'date': date,
        'name': standings['name'],
        'teams': standings['standings']
    }
    for team in rosters:
        if team in data['teams']:
            data['teams'][team]['name'] = team
            data['teams'][team]['roster'] = rosters[team]

    return data



if __name__ == "__main__":

    if len(sys.argv) != 4:
        print('./{} date <rosters>.json <standings>.json'.format(sys.argv[0]))
        sys.exit()

    date = sys.argv[1]
    rostersFile = sys.argv[2]
    standingsFile = sys.argv[3]

    f = open(rostersFile, "r", encoding="utf8")
    rosters = json.load(f)
    f.close()

    f = open(standingsFile, "r", encoding="utf8")
    standings = json.load(f)
    f.close()

    data = tournament(date, rosters, standings)
    json.dump(data, sys.stdout, indent=2)
