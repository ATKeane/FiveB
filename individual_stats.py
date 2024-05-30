#Code for generating .CSVs for each individual player.

import pandas as pd
import os.path

def individual_stats(week):
    #total_weeks = input("How many weeks so far?")
    total_weeks = week
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
            #player_totals = player_totals.append(week_game)
            player_totals = pd.concat([player_totals,week_game])

       
    for player in players:
        player_sheet = player_totals[player_totals['Name']==player]
        file_name = player + ".csv"
        player_sheet.to_csv(os.path.join('Individual Stats/', file_name))
