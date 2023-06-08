#Code for generating .CSVs for each individual player.

import pandas as pd
import os.path

#Commenting this out for now - fix for actual use. 
total_weeks = input("How many weeks so far?")
counter = 1
weeks = []
games = ["Game1","Game2"]
while counter <= int(total_weeks):
    weeks.append("Week" + str(counter))
    counter += 1


#Building a list of players
player_names = pd.read_csv("PlayerList.csv")
players = list(player_names["Player"])

#Creating an empty data frame - this will have each game appended onto it.
player_totals = pd.DataFrame()

#Iterating through.
#IMPROVEMENT NOTE: Move to a function for the week_location?
for week in weeks:
    for game in games:
        week_path = week + " Files/" + game + "/"
        week_file = week+game+".csv"
        week_game = pd.read_csv(week_path+week_file)
        player_totals = player_totals.append(week_game)

print(player_totals)
   
for player in players:
    player_sheet = player_totals[player_totals['Name']==player]
    file_name = player + ".csv"
    print(file_name)
    print(player_sheet)
    player_sheet.to_csv(os.path.join('Individual Stats/', file_name))
