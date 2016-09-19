import sys
import json

def isSimilar(rosterA, rosterB):
    a = [name.lower() for name in rosterA]
    b = [name.lower() for name in rosterB]

    intersection = set(a) & set(b)
    return len(intersection) >= 2

def results(tournaments):
    dates = sorted(tournaments.keys())

    results = {
        'count': 0,
        'teams': { }
    }
    for weekIndex, date in enumerate(dates):
        week = weekIndex+1
        tournament = tournaments[date]

        for key in tournament['teams']:
            tournTeam = tournament['teams'][key]
            standing = int(tournTeam['standing'])

            isSimilarRoster = False
            for _id in results['teams']:
                team = results['teams'][_id]

                isSimilarRoster = isSimilar(tournTeam['roster'], team['roster'])
                if isSimilarRoster:
                    results['teams'][_id]['name'] = tournTeam['name']
                    results['teams'][_id]['roster'] = tournTeam['roster']
                    results['teams'][_id]['week'][week] = standing

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

            _id = str(results['count'])
            results['teams'][_id] = obj
            results['count'] = results['count'] + 1

    return results
