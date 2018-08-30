#!/usr/bin/env python
'''
Dane Warren

Creates a dataset containing the statlines of rookie seasons of all running backs since 1950. Playoff games included.
'''
import cPickle as pickle
import json

'''
Resets running back data
'''
def resetData():
    data = {}
    data["gamesPlayed"] = 0
    data["rushing_attempts"] = 0
    data["rushing_yards"] = 0
    data["rushing_touchdowns"] = 0
    data["receiving_targets"] = 0
    data["receiving_receptions"] = 0
    data["receiving_yards"] = 0
    data["receiving_touchdowns"] = 0
    return data

'''
Obtains the rookie year stat line for the given player
@param gameStats: The individual game stats for every game going back to 1950
@param ID: The player's ID
@returns: A dictionary of the players' rookie year stat line
'''
def getRookieStats(gameStats, ID):
    data = resetData()
    year = 2500
    for game in gameStats:
        if game.get("player_id") == ID:
            if year > int(game.get("year")):
                data = resetData()
                year = int(game.get("year"))
            if year == int(game.get("year")):
                data["gamesPlayed"] += 1
                data["rushing_attempts"] += game.get("rushing_attempts")
                data["rushing_yards"] += game.get("rushing_yards")
                data["rushing_touchdowns"] += game.get("rushing_touchdowns")
                data["receiving_targets"] += game.get("receiving_targets")
                data["receiving_receptions"] += game.get("receiving_receptions")
                data["receiving_yards"] += game.get("receiving_yards")
                data["receiving_touchdowns"] += game.get("receiving_touchdowns")
    if data["rushing_attempts"] == 0:
        data["rushYpA"] = 0
        data["rushTDpA"] = 0
    else:
        data["rushYpA"] = float(data["rushing_yards"]) / float(data["rushing_attempts"])
        data["rushTDpA"] = float(data["rushing_touchdowns"]) / float(data["rushing_attempts"])
    if data["receiving_receptions"] == 0:
        data["airYpR"] = 0
        data["airTDpR"] = 0
    else:
        data["airYpR"] = float(data["receiving_yards"]) / float(data["receiving_receptions"])
        data["airTDpR"] = float(data["receiving_touchdowns"]) / float(data["receiving_receptions"])
    if data["gamesPlayed"] == 0:
        data["rushYpG"] = 0
        data["rushTDpG"] = 0
        data["airYpG"] = 0
        data["airTDpG"] = 0
    else:
        data["airYpG"] = float(data["receiving_yards"]) / float(data["gamesPlayed"])
        data["airTDpG"] = float(data["receiving_touchdowns"]) / float(data["gamesPlayed"])
        data["rushYpG"] = float(data["rushing_yards"]) / float(data["gamesPlayed"])
        data["rushTDpG"] = float(data["rushing_touchdowns"]) / float(data["gamesPlayed"])

    data["fantasyPoints"] = float((data["rushing_yards"]+data["receiving_yards"])/float(10) + (data["receiving_touchdowns"] + data["rushing_touchdowns"])*6 + data["receiving_receptions"])
    if data["gamesPlayed"] > 0:
        data["fantasyPointsPerGame"] = data["fantasyPoints"] / data["gamesPlayed"]
    else:
        data["fantasyPointsPerGame"] = 0

    return data

def main():
    file = open('../../datasets/pkl_datasets/rbgames.pkl')
    gameStats = pickle.load(file)
    file.close()

    file = open("../../datasets/pkl_datasets/runningbacksIDName.pkl","rb")
    rbs = pickle.load(file)
    file.close()
    
    data = {}
    rbData = []
    for rb in rbs.keys():
        data = getRookieStats(gameStats, rb)
        data["ID"] = rb
        data["name"] = rbs[rb]
        rbData.append(data)

    file = open("../../datasets/pkl_datasets/rookie_rbStats.pkl","wb")
    pickle.dump(rbData, file)
    file.close()
    print(rbData)

if __name__ == "__main__":
    main()
