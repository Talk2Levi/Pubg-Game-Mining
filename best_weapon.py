# import pandas as pd
# import numpy as np 
import matplotlib.pyplot as plt
import csv

from operator import itemgetter

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
    with open(csv_filepath, "r") as file:
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
ls = parse('kill_match_stats_final_0.csv')

# to get the next row of data, call next(ls)

weaponList = {}

# generators can also be processed like a list, however, previous rows are not stored in memory,
# they will be gone if they are not stored somewhere else
count = 10000
for row in ls:
    # process the rows here
    # if count < 0:
    #     break
    # count -= 1

    if row.get("killer_placement") != "" and float(row.get("killer_placement")) <= 10:
        if row.get("killed_by") in weaponList:
            weaponList[row.get("killed_by")] += 1
        else:
            weaponList[row.get("killed_by")] = 1

popList = set()
changeList = set()

for key in weaponList.keys():
    if key == 'Down and Out' or key == 'Bluezone' or key == 'Falling' or key == 'Drown' or key == 'death.Buff_FireDOT_C' or key == 'RedZone':
        popList.add(key)
    if key == 'death.WeapSawnoff_C' or key == 'death.ProjMolotov_DamageField_C' or key == 'death.PG117_A_01_C' or key == 'death.ProjMolotov_C':
        changeList.add(key)

for key in popList:
    weaponList.pop(key)

for key in changeList:
    if key == 'death.WeapSawnoff_C':
        weaponList['Sawed-off'] = weaponList[key]
        weaponList.pop(key)
    elif key == 'death.ProjMolotov_DamageField_C' or key == 'death.ProjMolotov_C':
        weaponList['Molotov Cocktail'] = weaponList[key]
        weaponList.pop(key)
    elif key == 'death.PG117_A_01_C':
        weaponList['PG117'] = weaponList[key]
        weaponList.pop(key)

sortedWeaponList = dict(sorted(weaponList.items(), key=itemgetter(1), reverse=True))

for key in sortedWeaponList.keys():
    if key == 'Punch' or key == 'Machete' or key == 'Pan' or key == 'Sickle' or key == 'Crowbar':
        sortedWeaponList[key] = [sortedWeaponList.get(key), 'black']
    elif key == 'SKS' or key == 'Win94' or key == 'S12K' or key == 'Mini 14' or key == 'Mk14' or key == 'Kar98k' or key == 'M24' or key == 'AWM' or key == 'VSS':
        sortedWeaponList[key] = [sortedWeaponList.get(key), 'royalblue']
    elif key == 'P92' or key == 'P1911' or key == 'R1895' or key == 'Crossbow' or key =='P18C' or key == 'R45':
        sortedWeaponList[key] = [sortedWeaponList.get(key), 'darkred']
    elif key == 'AKM' or key == 'M16A4' or key == 'SCAR-L' or key == 'M416' or key == 'M249' or key == 'AUG' or key == 'DP-28':
        sortedWeaponList[key] = [sortedWeaponList.get(key), 'forestgreen']
    elif key == 'Tommy Gun' or key == 'UMP9' or key == 'Micro UZI' or key == 'Vector' or key == 'Groza':
        sortedWeaponList[key] = [sortedWeaponList.get(key), 'yellow']
    elif key == 'S1897' or key == 'S686' or key == 'Sawed-off':
        sortedWeaponList[key] = [sortedWeaponList.get(key), 'red']
    elif key == 'Hit by Car' or key == 'Uaz' or key == 'Motorbike' or key == 'Dacia' or key == 'Motorbike (SideCar)' or key == 'Buggy' or key == 'Pickup Truck' or key == 'Van' or key == 'Boat' or key == 'Aquarail' or key == 'PG117':
        sortedWeaponList[key] = [sortedWeaponList.get(key), 'grey']
    elif key == 'Grenade' or key == 'Molotov Cocktail':
        sortedWeaponList[key] = [sortedWeaponList.get(key), 'pink']
    else:
        print("undefined")
        print(key)


valueList = [row[0] for row in sortedWeaponList.values()]
colorList = [row[1] for row in sortedWeaponList.values()]

plt.barh( range(len(sortedWeaponList)), valueList, color=colorList, tick_label=list(sortedWeaponList.keys()) )
plt.title("Kill count vs Weapon in top 10 players")
plt.xlabel("Kill count")
plt.ylabel("Weapon types")
plt.yticks(fontsize = 5)
plt.show()