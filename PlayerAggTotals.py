#Code for combining everybody's results from every game into individual summaries.

import pandas as pd
import os.path
from percentage_stats import *

player_names = pd.read_csv("PlayerList.csv")
players = list(player_names["Player"])

player_totals = pd.DataFrame()
grouped_results = pd.DataFrame()

for player in players:

    file_name = player + ".csv"
    path = (os.path.join('Individual Stats/', file_name))
    player_csv = pd.read_csv(path)
    player_totals = player_totals.append(player_csv)


agg_totals =gamebook_agg(player_totals)

print(agg_totals)
agg_totals.to_csv(os.path.join('AggTotals/', 'agg_totals.csv'))
