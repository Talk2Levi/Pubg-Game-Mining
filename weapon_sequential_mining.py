import csv
import sys

import bisect

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

if len(sys.argv) != 2 or not sys.argv[1].isdigit():
    raise Exception("Please take a minimum support as argument.")

minsup = int( sys.argv[1] )

# ls is a generator, generators are like lists but data can only be used once, because it is not stored
ls = parse('kill_match_stats_final_0.csv')

matchList = {}

print("Start processing..")

# count = 10000
for row in ls:
    # process the rows here
    # if count < 0:
    #     break
    # count -= 1

    if row.get("killer_placement") != "" and float(row.get("killer_placement")) == 1.0:
        thisWeapon = row.get("killed_by")

        if (row.get("victim_placement") != "" and thisWeapon != 'Hit by Car' and thisWeapon != 'Uaz' and thisWeapon != 'Motorbike' 
            and thisWeapon != 'Dacia' and thisWeapon != 'Motorbike (SideCar)' and thisWeapon != 'Buggy' and thisWeapon != 'Pickup Truck' 
            and thisWeapon != 'Van' and thisWeapon != 'Boat' and thisWeapon != 'Aquarail' and thisWeapon != 'PG117' and thisWeapon != "Down and Out"
            and thisWeapon != 'Bluezone' and thisWeapon != 'Falling' and thisWeapon != 'Drown' and thisWeapon != 'death.Buff_FireDOT_C' 
            and thisWeapon != 'RedZone' and thisWeapon != 'Punch' and thisWeapon != 'Machete' and thisWeapon != 'Pan' and thisWeapon != 'Sickle' 
            and thisWeapon != 'Crowbar' and thisWeapon != 'Grenade' and thisWeapon != 'Molotov Cocktail'):

            if thisWeapon == 'death.WeapSawnoff_C':
                thisWeapon = 'Sawed-off'
            elif thisWeapon == 'death.ProjMolotov_DamageField_C' or thisWeapon == 'death.ProjMolotov_C':
                thisWeapon = 'Molotov Cocktail'
            elif thisWeapon == 'death.PG117_A_01_C':
                thisWeapon = 'PG117'

            if row.get("match_id") in matchList:
                theList = matchList[row.get("match_id")]
                bisect.insort(theList,  (float(row.get("victim_placement")), thisWeapon) ) 
            else:
                matchList[row.get("match_id")] = [ (float(row.get("victim_placement")), thisWeapon) ]

sequentialSet = {}

for value in matchList.values():
    value.reverse()
    i = 0
    lastWeapon = ''
    while(i < len(value)):
        ele = value[i]
        thisWeapon = ele[1]
        if thisWeapon == lastWeapon:
            value.pop(i)
        else:
            value.pop(i)
            value.insert(i, thisWeapon)
            i += 1
        lastWeapon = thisWeapon
    value = ' '.join(value)

    if value in sequentialSet:
        sequentialSet[value] += 1
    else:
        sequentialSet[value] = 1

# print(sequentialSet)

print("\n\nAll frequent sequence for weapon with minsup = " + str(minsup) + "\n")

for key in sequentialSet.keys():
    freq = sequentialSet[key]
    if freq >= minsup:
        print("<" + key + ">: " + str(freq))

print("\nEnd of processing.")