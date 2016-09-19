from rosters import *
from standings import *
from tournament import *
from tournaments import *
from monthly import *
from seedings import *
from results import *

import sys
import os
from stat import *
import json

if len(sys.argv) != 2:
    print('./{} <rosters>.csv'.format(sys.argv[0]))
    sys.exit()

srcPath = os.path.dirname(os.path.realpath(__file__))
dataPath = srcPath + "/../data"

ROSTERS_FILE_NAME = "rosters.csv"
STANDINGS_FILE_NAME = "standings.html"
TOURNAMENT_FILE_NAME = "tournament.json"
TOURNAMENTS_FILE_NAME = "tournaments.json"
WEIGHTS_FILES_NAME = "weights.json"

TOURNAMENTS_PATH = dataPath + "/" + TOURNAMENTS_FILE_NAME
WEIGHTS_PATH = dataPath + "/" + WEIGHTS_FILES_NAME

dataDirs = []
for f in os.listdir(dataPath):
    pathname = os.path.join(dataPath, f)
    mode = os.stat(pathname).st_mode

    if S_ISDIR(mode):
        dataDirs.append(f)

f = open(TOURNAMENTS_PATH, "r", encoding="utf8")
_tournaments = json.load(f)
f.close()

f = open(WEIGHTS_PATH, "r", encoding="utf8")
_weights = json.load(f)
f.close()

for f in dataDirs:
    path = "{}/{}/".format(dataPath, f)

    TOURNAMENT_PATH = path + TOURNAMENT_FILE_NAME

    rostersFile = path + ROSTERS_FILE_NAME
    standingsFile = path + STANDINGS_FILE_NAME
    _rosters = rosters(rostersFile)
    _standings = standings(standingsFile)
    _tournament = tournament(f, _rosters, _standings)
    _tournaments = tournaments(_tournaments, _tournament)

    f = open(TOURNAMENT_PATH, "w", encoding="utf8")
    json.dump(_tournaments, f, indent=2, sort_keys=True, ensure_ascii=True)
    f.close()

f = open(TOURNAMENTS_PATH, "w", encoding="utf8")
json.dump(_tournaments, f, indent=2, sort_keys=True)
f.close()

_results = results(_tournaments)
json.dump(_results, sys.stdout, indent=2, sort_keys=True)

# Get monthly (with points) json
# _monthly = monthly(_tournaments)
# json.dump(_monthly, sys.stdout, indent=2, sort_keys=True)

# Extract this week's teams from monthly json
# _seedings = seedings(_monthly, _weights)

# _list = sorted(_seedings.items(), key=lambda item: item[1]['points'], reverse=True)
#
# for index, obj in enumerate(_list):
#     rank = index+1
#     team = obj[1]
#     print("{},{},{}".format(rank, team['name'], team['points']))
