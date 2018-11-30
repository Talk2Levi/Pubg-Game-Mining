import csv

# a list of headers available in the agg.csv files
headers1 = [
    "date",
    "game_size",
    "match_id",
    "match_mode",
    "party_size",
    "player_assists",
    "player_dbno",
    "player_dist_ride",
    "player_dist_walk",
    "player_dmg",
    "player_kills",
    "player_name",
    "player_survive_time",
    "team_id",
    "team_placement",
]

# list of headers available in the kill_match.csv files
headers2 = [
    'killed_by',
    'killer_name',
    'killer_placement',
    'killer_position_x',
    'killer_position_y',
    'map',
    'match_id',
    'time',
    'victim_name',
    'victim_placement',
    'victim_position_x',
    'victim_position_y'
]


def parse(csv_filepath):
    """ A method to parse the csv file given the pathe to the csv file.
    filepath - a string value of the path to the csv file.
    eg: "Downloads/pubg-match-deaths/aggregate/agg_match_stats_0.csv"
    return a generator that yields dicts of data
    """
    with open(filepath, "r") as file:
        headers = []
        for row in csv.reader(file):
            if not headers:
                headers = row
            else:
                entry = {}
                for i in range(len(row)):
                    header = headers[i]
                    entry[header] = row[i]
                yield entry


# ls is a generator, generators are like lists but data can only be used once, because it is not stored
ls = parse(path1)

# to get the next row of data, call next(ls)
row0 = next(ls) # row0 = ls[0]
row1 = next(ls) # row1 = ls[1]
row2 = next(ls) # row2 = ls[2]

# generators can also be processed like a list, however, previous rows are not stored in memory,
# they will be gone if they are not stored somewhere else
for row in ls:
    # process the rows here
    pass
