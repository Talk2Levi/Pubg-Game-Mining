import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

# Data preprocessing
agg0 = pd.read_csv("./pubg-match-deaths/aggregate/agg_match_stats_0.csv")

agg0["won"] = agg0['team_placement'] == 1

agg0.loc[agg0['party_size'] != 1, ['player_assists', 'won']].groupby('player_assists').won.mean().plot.bar(figsize=(15,6), rot=0)
agg0.loc[agg0['party_size'] != 1, ['player_assists', 'won']].groupby('player_assists').won.mean().plot(figsize=(15,6), rot=0, c='r', linewidth=1.5)

# The Correlation between the number of players who killed and won the game
plt.title("Correlation of number of assist and won the game", fontsize=15)
plt.xlabel("Number of players who assisted", fontsize=15)
plt.ylabel("Chance of Win The Game", fontsize=15)
plt.show()
