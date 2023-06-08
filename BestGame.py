#Code for determining the best game -

import pandas as pd
import os.path
from percentage_stats import total_bases
'''
def StatsDFPrepare(csv):
    GameStats = pd.read_csv(csv)
    return GameStats
'''
week = input("What Week?")
#Temporary putting this in to speed up testing.
#week = 2

#Fix This - Needless repeating.
path = ("Week" + week + " Files/")
path1 = ("Week" + week + " Files/" + "Game1/")
path2 = ("Week" + week + " Files/" + "Game2/")

Game1Stats = pd.read_csv(os.path.join(path1, "Week"+str(week)+"Game1.csv"))
Game2Stats = pd.read_csv(os.path.join(path2, "Week"+str(week)+"Game2.csv"))

#Adding the Weeks together
FullStats = Game1Stats.append(Game2Stats)

#Total Bases on FullStats
FullStats = total_bases(FullStats)

#Going through the ranking list, in order, to determine best game

def best_game(gamebook, ranking_list):
    BestGame = pd.DataFrame()
    players=gamebook.Name.unique()
    for player in players:
        playerStats=gamebook[gamebook['Name']==player]
        for stat in ranking_list:
            BestGamePlayer = (playerStats[playerStats[stat]==playerStats[stat].max()])
            if len(BestGamePlayer.index) == 1:
                BestGame = BestGame.append(BestGamePlayer)
                break
    return(BestGame)

ranking_list = ['OPS','Home Run','Total Bases','RBI','R','Win','PA']

BestGame =best_game(FullStats, ranking_list)

#Sorting by name
BestGame = BestGame.sort_values(by=['Name'])

BestGame.to_csv(os.path.join(path, "BestGame.csv"))
