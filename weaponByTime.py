import pandas


def main():
    kill_stats = pandas.read_csv('kill_match_stats_final_0.csv')
    time_dict = {}
    minutes = 5
    while minutes < 60:
        seconds = minutes * 60
        stats = kill_stats.loc[(kill_stats['time'] < seconds)&(kill_stats['time'] > seconds-60)&(kill_stats['killer_placement'] < 2)]
        stats = stats[['time', 'killed_by']].values
        time_dict[minutes] = stats
        minutes = minutes + 5

    for minute in time_dict:
        stats = time_dict[minute]
        tally = {}
        for row in stats:
            weapon = row[1]
            if weapon not in tally:
                tally[weapon] = 1
            else:
                tally[weapon] += 1
        time_dict[minute] = tally

    for minute in time_dict:
        stat = time_dict[minute]
        max_count = None
        second_count = None
        max_weapon = None
        second_weapon = None
        third_count = None
        third_weapon = None
        filter = ['Punch', 'Down and Out', 'Bluezone', 'Falling']
        for w, c in stat.items():
            if w in filter:
                continue
            if max_count is None or c > max_count:
                max_count = c
                max_weapon = w
            elif second_count is None or c > second_count:
                second_count = c
                second_weapon = w
            elif third_count is None or c > third_count:
                third_count = c
                third_weapon = w
        time_dict[minute] = [(max_weapon, max_count), (second_weapon, second_count), (third_weapon, third_count)]

    for i, v in time_dict.items():
        print(i, v)
