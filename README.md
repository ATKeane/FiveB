# FiveB
Repository For FiveB Files

How to set up files:
-Directories should follow "Week#/Game#" format, with the appropriate Week and Game numbers inserted. 

Files notes:
-Main.py
Run this for all the other files.

-ScoreBookCode.py 
This is the main source of the other csvs. This file takes the Team book notes from the csv files, and generates a gamebook from them, including a small narrative that gives a run down of the games.

-BestGame.py
This evaluates the games played per week, and selects the best game for each player. This needs to be updated to read from the directories.

-TopPlayers.py
This generates the top ten players of different stats. This needs to be updates to read from the directories.

-percentage_stats.py
This contains functions that aggregate the stats by player name, as well as calculates the percentage stats (such as batting average, slugging, etc) from the data frames.

-individual_stats.py
-This will generate individual csvs for each player in the league.

Team1, Team2 csvs - These are sample files to run off of. Enjoy the names! 
