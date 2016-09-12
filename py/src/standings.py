import sys
import re
import json

def standings(file):

    f = open(file, "r", encoding="utf8")
    raw = f.read()

    pattern = "text-muted.*>(.+)<.*\n.*td>(.+)<"
    results = re.findall(pattern, raw)

    data = { }

    for result in results:
        standing = result[0]
        team = result[1]

        data[team] = { 'standing': standing }

    return data

    

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print('./{} <standings>.html'.format(sys.argv[0]))
        sys.exit()

    file = sys.argv[1]

    data = standings(file)

    json.dump(data, sys.stdout, indent=2)
