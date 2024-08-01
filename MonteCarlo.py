import pandas as pd
import random 
lineups = pd.read_csv("Lineups.csv")
team = pd.read_csv("MyTeam.csv", index_col = "Name")
#print(team)
playerlist = []
rowcount = 0
while rowcount <= 2:
    #print((lineups.loc[rowcount, :].values.flatten().tolist()))
    #print(playerlist)
    playerlist.append(lineups.loc[rowcount, :].values.flatten().tolist())
    rowcount += 1
#Test lines
currentbatter = playerlist[1]
hit_chance = random.uniform(0,1)
#batter_avg = team[["Name"] == currentbatter]["AVG"]
#print(team)
#print(playerlist)
#print(team.loc['Andrew Keane'][1])
#print(team.loc[currentbatter])
#print(hit_chance)
#print(batter_avg)

#100 times!
#for
record = []
for lineup in playerlist:
    i= 1
    team_score = []
    while i <= 10000: 
        runs = 0
        bases = [0,0,0]
        batternumber = 0
        outs = 0
        while outs <27:
            #print(outs)
            #print(bases)
            #print(runs)
            currentbatter = lineup[(batternumber%len(lineup))]
            #print(currentbatter)
            hit_chance = random.uniform(0,1)
            batter_avg = team.loc[currentbatter][14]
            if hit_chance < batter_avg:
                #print("hit")
                hit_type = random.uniform(0,1)
                if hit_type < team.loc[currentbatter][19]:
                    runs += 1
                    runs += sum(bases)
                    bases = [0,0,0]
                    batternumber += 1
                    #print("Home run")
                elif hit_type < team.loc[currentbatter][20]:
                    runs += sum(bases)
                    bases = [0,0,1]
                    batternumber += 1
                    #print("Triple")
                elif hit_type < team.loc[currentbatter][21]:
                    runs += bases[2] + bases[1]
                    bases[2] = bases[0]
                    bases[1] = 1
                    bases[0] = 0
                    batternumber += 1
                    #print("double")
                else:
                    runs += bases[2]
                    bases[2] = bases[1]
                    bases[1] = bases[0]
                    bases[0] = 1
                    batternumber += 1
                    #print("single")
            else:
                outs += 1
                batternumber +=1
                #print("out")
                if (outs > 0) & (outs % 3 == 0):
                    bases=[0,0,0]
                    #print("Three out")
        team_score.append(runs)
        i += 1
    record.append((sum(team_score))/1000)
print(record)