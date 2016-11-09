import sys
import re
import json
import html

def standings(file):

    f = open(file, "r", encoding="utf8")
    raw = f.read()

    pattern = "bf-top-bar-title-tournament-name.*>(.+)<"
    name = re.search(pattern, raw).groups()[0]

    # pattern = "fa fa-calendar-o.*>(.+)<"
    # date = re.search(pattern, raw).groups()[0]
    # print("DATE: {}".format(date))

    pattern = "text-muted.*>(.+)<.*\n.*td>(.+)<"
    results = re.findall(pattern, raw)

    data = {
        'name': name,
        'standings': { }
    }

    for result in results:
        standing = result[0]
        team = html.unescape(result[1])

        data['standings'][team] = { 'standing': standing }

    return data



if __name__ == "__main__":

    if len(sys.argv) != 2:
        print('./{} <standings>.html'.format(sys.argv[0]))
        sys.exit()

    file = sys.argv[1]

    data = standings(file)

    json.dump(data, sys.stdout, indent=2)
