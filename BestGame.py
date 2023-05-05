#Code for determining the best game -

import pandas as pd

'''
def StatsDFPrepare(csv):
    GameStats = pd.read_csv(csv)
    return GameStats
'''
#week = input("What Week?")
#Temporary putting this in to speed up testing.
week = 2
Game1Stats = pd.read_csv("Week"+str(week)+"Game1.csv")
Game2Stats = pd.read_csv("Week"+str(week)+"Game2.csv")

#Adding the Weeks together
FullStats = Game1Stats.append(Game2Stats)

#Empty Dataframe to put the best game for each player into
BestGame = pd.DataFrame()

#Unique Index items - here each individual player.
players=FullStats.Name.unique()

for player in players:
    playerStats=FullStats[FullStats['Name']==player]
    BestGamePlayer = (playerStats[playerStats.OPS == playerStats.OPS.max()])
    BestGame = BestGame.append(BestGamePlayer)

#Sorting by name
BestGame = BestGame.sort_values(by=['Name'])

BestGame.to_csv("BestGame.csv")
