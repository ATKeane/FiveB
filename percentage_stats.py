#Function for calculating the percentage stats off of the dataframe:
import pandas as pd

#This should clean up the percentage stats on game, weekly, and season totals.

def percentage_stats(gamebook):
    #print("Percent gamebook below")
    #print(gamebook)
    gamebook['AVG']=(gamebook['Single']+gamebook['Double']+gamebook['Triple']+gamebook['Home Run'])/(gamebook['PA']-gamebook['SAC'])
    gamebook['SLG']=(gamebook['Single']+(2*gamebook['Double'])+(3*gamebook['Triple'])+(4*gamebook['Home Run']))/(gamebook['PA']-gamebook['SAC'])
    gamebook['OBP']=(gamebook['Single']+gamebook['Double']+gamebook['Triple']+gamebook['Home Run'])/(gamebook['PA'])
    gamebook['OPS']=gamebook['SLG']+gamebook['OBP']
    #print("Percent gamebook below after calc")
    #print(gamebook)
    return gamebook

#To do: Grouping by the index.
#This should tidy up all the aggregating we need to do for this. Sum only - calculate percentage stats after.

def gamebook_agg(gamebook):
    agg_dict = {}
    #This assumes the name column is in this slot.
    agg_dict[gamebook.columns[0]]="first"
    for col in gamebook.columns[1:]:
        agg_dict[col] = 'sum'
    gamebook = gamebook.groupby('Name').aggregate(agg_dict)
    #Reseting the index THIS DOESN'T WORK NEED TO FIX
    gamebook = gamebook.drop(columns=['Name'])
    gamebook = gamebook.reset_index()
    return gamebook


