#!/usr/bin/env python
'''
Dane Warren

Creates a dictionary of every running back since 1950 and their IDs.
player[name] = ID
'''
import cPickle as pickle
import json

'''
@param players: JSON dataset of all NFL players since 1950
@returns: A dictionary containing all running backs and their respective IDs
'''
def getRunningBacks(players):
    nameID = {}
    for player in players[0]:
        if player.get("position") == "RB":
            nameID[player.get("player_id")] = player.get("name")
    return nameID

def main():
    players = [json.loads(line) for line in open('../../datasets/json_datasets/profiles.json')]
    rbs = getRunningBacks(players)
    file = open("../../datasets/pkl_datasets/runningbacksIDName.pkl","wb")
    pickle.dump(rbs, file)
    file.close()

if __name__ == "__main__":
    main()
