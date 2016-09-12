import sys
import json

def isSimilar(rosterA, rosterB):
    intersection = set(rosterA) & set(rosterB)
    similarity = float(len(intersection) / len(rosterA))
    # print('{} <-> {} = {}'.format(rosterA, rosterB, similarity))
    return 0.50 < similarity

def monthly(tournaments):
    # Last 4 (a month's worth of) tournaments
    dates = sorted(tournaments.keys())
    dates = dates[-4:]

    teams = { }
    for weekIndex, date in enumerate(dates):
        week = 4-weekIndex
        tournament = tournaments[date]

        for key in tournament['teams']:
            tournTeam = tournament['teams'][key]
            standing = int(tournTeam['standing'])

            isSimilarRoster = False
            for k in teams:
                team = teams[k]
                isSimilarRoster = isSimilar(tournTeam['roster'], team['roster'])
                if isSimilarRoster:
                    teams[k]['name'] = tournTeam['name']
                    teams[k]['week'][week] = standing
                    break

            if isSimilarRoster:
                continue

            obj = {
                'name': key,
                'roster': tournTeam['roster'],
                'week': {
                    week: standing
                }
            }
            teams[key] = obj

    # json.dump(teams, sys.stdout, indent=2, sort_keys=True)
    return teams

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
    weights = sys.argv[2]

    f = open(tournamentsFile, "r", encoding="utf8")
    tournaments = json.load(f)
    f.close()

    f = open(weights, "r", encoding="utf8")
    weights = json.load(f)
    f.close()

    teams = monthly(tournaments)
    for key in teams:
        team = teams[key]
        team['points'] = get_seed_points(weights, team)

    json.dump(teams, sys.stdout, indent=2, sort_keys=True)
