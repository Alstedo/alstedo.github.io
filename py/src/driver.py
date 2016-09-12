import sys
import os
import json

if len(sys.argv) != 2:
    print('./{} <rosters>.csv'.format(sys.argv[0]))
    sys.exit()

print(os.listdir())



# For every tournaments
#   roster csv to json
#   standings html to json
#   roster + standings to tournament json

# Add tournament json to tournaments json

# Get monthly (with points) json

# Extract this week's teams from monthly json
