#This is the code for the actual inputing of results.

import pandas as pd
import os.path
from percentage_stats import *
from NameSpelling import Name_Check

#These preparing steps could be cleaned up by doing it in one function.
def StatsDFPrepare(csv):
    TeamStats = pd.read_csv(csv)
    TeamStats = Name_Check(TeamStats)
    playerlist = list(TeamStats["Player"])
    TeamStats = TeamStats.set_index("Player")
    return TeamStats,playerlist

#Moving this toward weekly files instead. Order of use - put the csv files in the game folders, go from there.
week = input("What week is this being run for? (Use an integer to describe)")
week = "Week" +str(week)
games = ["Game1","Game2"]

#Running this for both games.
for game in games:
    csv_location = week + " Files/" + game + "/"
    Team1Stats,playerlistVisitor = StatsDFPrepare(csv_location + "Team1.csv")
    Team2Stats,playerlistHome = StatsDFPrepare(csv_location + "Team2.csv")
    inning = 1
    batterVisitor = 0
    batterHome = 0
    plate_appearance_id = 1
    narrative=[]
    playerdict = {}
    plate_appearance_dict = {}
    total_plate_appearances = (sum(Team1Stats.count())+sum(Team2Stats.count()))
    keys = playerlistVisitor+playerlistHome
    values = ["PA", "Single", "Double", "Triple", "Home Run", "RBI","R","Fielder's Choice","Fly Out","Pop Out","Ground Out", "Line Out", "Strike Out","SAC","Skips"]
    for i in keys:
        results = {}
        for x in values:
            results[x] = 0
        playerdict[i]=results


    def atbatresults(playerlist, batternumber,playerdict,TeamStats,plate_appearance_dict, plate_appearance_id):
        story = []
        player_scored = []
        outs = 0
        while outs <3:
            currentbatter = playerlist[(batternumber%len(playerlist))]
            plate_appearance_number = str(playerdict[currentbatter]["PA"]+1)
            plate_appearance_score =  TeamStats.loc[currentbatter, plate_appearance_number]
            outcomes={"1":"Single","2":"Double","3":"Triple","4":"Home Run","C":"Fielder's Choice", "F":"Fly Out", "P":"Pop Out", "G": "Ground Out", "L": "Line Out", "K": "Strike Out"}
            #building a plate appearance row for the dictionary plate_apperance_dict. Can we clean this up?
            pa_columns = {}
            pa_columns["name"]=currentbatter
            for x in values:
                pa_columns[x]=0
            plate_appearance_dict[plate_appearance_id]=pa_columns

            #Breaking if the Plate Appearance is blank - for walk offs, etc.
            if pd.isna(plate_appearance_score):
                break

            #Isolating the hit/out type.
            result = plate_appearance_score[0]

            #Skipping players that missed a plate appearance. The final tally will be PA-Skips.
            if result == "X":
                batternumber += 1
                playerdict[currentbatter]["PA"]+=1
                playerdict[currentbatter]["Skips"]+=1
                story.append("We skipped " + currentbatter + "'s turn!")
                continue

            #Normal at bats.
            if result in outcomes.keys():
                batternumber += 1
                playerdict[currentbatter]["PA"]+=1
                if outcomes[result] in ["Fly Out","Ground Out","Pop Out", "Line Out", "Strike Out"]:
                    outs += 1
                    story.append(currentbatter + " was out by " + outcomes[result])
                elif outcomes[result] =="Fielder's Choice":
                    outs += 1
                    story.append(currentbatter + " hit into a Fielder's Choice!")
                else:
                    story.append(currentbatter + " hit a " + outcomes[result])
                playerdict[currentbatter][outcomes[result]]+= 1
                plate_appearance_dict[plate_appearance_id][outcomes[result]]+=1
                runs = plate_appearance_score[1]
                if runs not in ["1"]:
                    runs = 0
                #Keeping a record of who scored.
                else:
                    player_scored.append(currentbatter)
                #Can I take an int value here ealier? The hold up is how to track invalid entries.
                rbis = plate_appearance_score[2]
                if rbis not in ["1","2","3","4","0"]:
                    print("Setting RBIs to zero")
                    rbis = 0
                #Trying to pop from the scoring.
                elif int(rbis) <= len(player_scored):
                    for i in range(0,int(rbis)):
                        story.append(player_scored[0] + " came in on the hit!")
                        player_scored.pop(0)
                else:
                    print("ERROR WITH THE RBIS AROUND HERE! FIX THIS INNING!")
                    story.append("ERROR WITH THE RBIS! AROUND HERE! FIX THIS INNING!")
                playerdict[currentbatter]["RBI"]+=int(rbis)
                plate_appearance_dict[plate_appearance_id]["RBI"] +=int(rbis)
                
                playerdict[currentbatter]["R"]+=int(runs)
                plate_appearance_dict[plate_appearance_id]["R"]+=int(runs)

                extraouts = plate_appearance_score[3] 
                if extraouts not in ["0","1","2","3"]:
                    extraouts = 0
                    print("Setting Extra Outs to Zero")
                else:
                    outs +=int(extraouts)
                #SAC FLYS
                if int(rbis) > 0 and result == "F":
                    playerdict[currentbatter]["SAC"]+=1

                plate_appearance_id +=1
            else:
                print("Something's wrong with the csv.")
                break
        #Adding in something to check for rbis and runs.
        if sum(player["RBI"] for player in playerdict.values() if player) < sum(player["R"] for player in playerdict.values() if player):
            story.append("MISTAKE THIS INNING ON RUNS, " + str(player_scored) + " ARE NOT ACCOUNTED FOR")
        return (batternumber,playerdict,story,plate_appearance_dict, plate_appearance_id)

    while batterVisitor + batterHome < total_plate_appearances:
        narrative.append("Top of the " + str(inning) + " inning")
        batterVisitor,playerdict,inningresults,plate_appearance_dict,plate_appearance_id=atbatresults(playerlistVisitor,batterVisitor,playerdict,Team1Stats,plate_appearance_dict,plate_appearance_id)
        narrative += inningresults
        narrative.append("Bottom of the " + str(inning) + " inning")
        if (inning >= 9) and (batterVisitor + batterHome == total_plate_appearances):
            break
        inning += 0.5
        batterHome,playerdict,inningresults,plate_appearance_dict,plate_appearance_id=atbatresults(playerlistHome,batterHome,playerdict,Team2Stats, plate_appearance_dict,plate_appearance_id)
        narrative +=inningresults
        inning += 0.5

        
    #Box Score For Both Teams. Using each player name as an index. Do I like this?
    gamebook = pd.DataFrame.from_dict(playerdict, orient = 'index')
    gamebook.index.names=['Name']

    #Making reseting the index to make a names column.
    gamebook = gamebook.reset_index()

    #Removing Exclamation Point From Names, in case of switched at bats.
    gamebook['Name'] = gamebook['Name'].str.replace('!', '')

    #Aggregating plate appearances on name, in case of switched at bats.
    gamebook = gamebook_agg(gamebook)

    #Removing Guest players from the book. 
    correct_names_df = pd.read_csv('PlayerList.csv')
    correct_names = list(correct_names_df["Player"])
    gamebook = gamebook[gamebook.Name.isin(correct_names)]

    #Scores, wins, losses. Future notes: Should be able to combine into one function?
    visitor_book = gamebook.loc[gamebook['Name'].isin(playerlistVisitor)]
    visitor_score = visitor_book['R'].sum()
    visitor_book['TeamScore'] = visitor_score
    
    home_book = gamebook.loc[gamebook['Name'].isin(playerlistHome)]
    home_score = home_book['R'].sum()
    home_book['TeamScore'] = home_score

    #Work on this next! Maybe do one function for everything?

    if visitor_score == home_score:
        visitor_book['Win'] = 0.5
        visitor_book['Loss'] = 0.5
     
        home_book['Win']=0.5
        home_book['Loss'] =0.5
    elif visitor_score > home_score:
        visitor_book['Win']=1
        visitor_book['Loss']=0
        home_book['Win']=0
        home_book['Loss']=1
    else:
        visitor_book['Win']=0
        visitor_book['Loss']=1
        home_book['Win']=1
        home_book['Loss']=0


    gamebook = visitor_book.append(home_book)
    gamebook['PA']=gamebook['PA']-gamebook["Skips"]
    gamebook=gamebook.drop(columns=['Skips'])

    #Building the advanced stats with the percentage function.
    gamebook = percentage_stats(gamebook)

    #Path to the folder
    path = (week + " Files/" + game + "/")


    #Gamebook CSV (Box Score, both teams)    
    gamebook_title = week + game
    gamebook.to_csv(os.path.join(path, gamebook_title + ".csv"))

    #Plate Appearance csv
    plate_appearance_rundown = pd.DataFrame.from_dict(plate_appearance_dict, orient = 'index')
    plate_appearance_rundown.to_csv(os.path.join(path, gamebook_title + "PA.csv"))

    #Narrative File, basic info.

    narrativetitle=os.path.join(path, gamebook_title+".txt")
    narrativetxt = open(narrativetitle,"w")
    for line in narrative:
        narrativetxt.write(" " + line)
    narrativetxt.close()


