#Top 10 Players for each category
#Must correct Eric's name - use Lowkey for week1. 
import pandas as pd
from percentage_stats import *

#Commenting out for now - put back when actually doing it.
#total_weeks = int(input("What week are we up to? Enter integer only (i.e. enter 1,2, etc.)"))
total_weeks = 2
#Starting with Week1 - We expect to always have something to start
SeasonTotals = pd.read_csv("Week1.csv")
count =2

while count <= total_weeks:
    csv_name = "Week" + str(count) + ".csv"
    new_week = pd.read_csv(csv_name)
    SeasonTotals = SeasonTotals.append(new_week)
    count += 1

'''
Week1 = pd.read_csv("Week1.csv")
Week2 = pd.read_csv("Week2.csv")

SeasonTotals = Week1.append(Week2)
'''


SeasonTotals = gamebook_agg(SeasonTotals)
SeasonTotals = percentage_stats(SeasonTotals)


#The Season Totals csv
SeasonTotals.to_csv("SeasonTotals.csv")

#Making Top 10 Csv.
top_ten = pd.DataFrame()

#Adding Hits, Extra base hits, total games, total bases.
SeasonTotals['Total Bases'] = SeasonTotals['Single']+ (2*SeasonTotals['Double']) + (3*SeasonTotals['Triple'])+(4*SeasonTotals['Home Run'])
SeasonTotals['Extra Base Hits'] = SeasonTotals['Double'] + SeasonTotals['Triple']+SeasonTotals['Home Run']
SeasonTotals['Hits'] = SeasonTotals['Extra Base Hits']+SeasonTotals['Single']
SeasonTotals['Games'] = SeasonTotals['Win']+SeasonTotals['Loss']

#Unluckiest Players
SeasonTotals['Bad Luck Score']=(SeasonTotals['Hits']-SeasonTotals['R'])+SeasonTotals['Line Out']

#Categories directly from the sheets
top_categories = ['PA', 'Single', 'Double', 'Triple', 'Home Run', 'RBI', 'R', 'SAC', 'TeamScore', 'Win', 'Loss', 'AVG', 'SLG', 'OBP', 'OPS', 'Extra Base Hits', 'Hits','Games', 'Total Bases', 'Bad Luck Score']

#Making Mini Dataframes of each category
for category in top_categories:
    top_players = SeasonTotals.nlargest(10, category)
    top_players = top_players[['Name',category]]
    top_ten = top_ten.append(top_players)

print(top_ten)
top_ten.to_csv("TESTTEN.csv")
