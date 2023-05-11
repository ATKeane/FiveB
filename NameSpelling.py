from Levenshtein import distance
import pandas as pd

def Name_Check (BoxScore):
    correct_names_df = pd.read_csv('PlayerList.csv')
    correct_names = list(correct_names_df["Player"])
    incorrect_names = list(BoxScore["Player"])

    '''
    correct_names_df = pd.read_csv('PlayerList.csv')
    incorrect_names_df = pd.read_csv('Team1.csv')
    correct_names = list(correct_names_df["Player"])
    incorrect_names = list(incorrect_names_df["Player"])
    '''
    for i in range(len(incorrect_names)):
        if incorrect_names[i] in correct_names:
            continue
        misspelling = 100
        for cor_name in correct_names:
            inc_name = incorrect_names[i]
            dist_name = distance(inc_name,cor_name)
            if dist_name < misspelling:
                misspelling = dist_name
                correction = cor_name
        if misspelling > 0:
            request_change = input("Y/N Would you like to correct the name: " + incorrect_names[i] + " into " + correction)
            if request_change == "Y":
                incorrect_names[i] = correction
            else:
                print("Assuming Guest player - Remove from sheets later")
    BoxScore["Player"]=incorrect_names
    print(incorrect_names)
    return(BoxScore)
                



