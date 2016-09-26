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
        'teams': []
    }
    for weekIndex, date in enumerate(dates):
        week = weekIndex+1
        tournament = tournaments[date]

        for key in tournament['teams']:
            tournTeam = tournament['teams'][key]
            standing = int(tournTeam['standing'])

            isSimilarRoster = False
            for index in range(len(results['teams'])):

                isSimilarRoster = isSimilar(tournTeam['roster'], results['teams'][index]['roster'])
                if isSimilarRoster:
                    results['teams'][index]['name'] = tournTeam['name']
                    results['teams'][index]['roster'] = tournTeam['roster']
                    results['teams'][index]['weeks'][week] = standing

                    break

            if isSimilarRoster:
                continue

            obj = {
                'name': tournTeam['name'],
                'roster': tournTeam['roster'],
                'weeks': {
                    week: standing
                }
            }

            results['teams'].append(obj)

    results['numTeams'] = len(results['teams'])
    results['numWeeks'] = len(dates)
    return results
