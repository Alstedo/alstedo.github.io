import sys
import json

def isSimilar(rosterA, rosterB):
    a = [name.lower() for name in rosterA]
    b = [name.lower() for name in rosterB]

    intersection = set(a) & set(b)
    return len(intersection) >= 2

def results(tournaments):
    dates = sorted(tournaments.keys())

    teams = { }
    for weekIndex, date in enumerate(dates):
        week = weekIndex+1
        tournament = tournaments[date]

        for key in tournament['teams']:
            tournTeam = tournament['teams'][key]
            standing = int(tournTeam['standing'])

            isSimilarRoster = False
            for k in teams:
                team = teams[k]

                a = [name.lower() for name in team['roster']]
                b = [name.lower() for name in tournTeam['roster']]

                intersection = set(a) & set(b)

                print("{} <-> {} : {}".format(tournTeam['roster'], team['roster'], len(intersection) >= 2))


                isSimilarRoster = isSimilar(tournTeam['roster'], team['roster'])
                if isSimilarRoster:
                    teams[k]['name'] = tournTeam['name']
                    teams[k]['roster'] = tournTeam['roster']
                    teams[k]['week'][week] = standing
                    break

            if isSimilarRoster:
                continue

            obj = {
                'name': tournTeam['name'],
                'roster': tournTeam['roster'],
                'week': {
                    week: standing
                }
            }
            teams[key] = obj

    return teams
