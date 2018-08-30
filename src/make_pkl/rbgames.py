#!/usr/bin/env python
'''
Dane Warren

Creates a list of all running back games since 1950
'''
import cPickle as pickle
import json

def getRbGames(games, rbs):
    rbgames = []
    for rb in rbs:
        for game in games[0]:
            if game.get("player_id") == rb:
                rbgames.append(game)
    return rbgames
            

def main():
    gameStats = [json.loads(line) for line in open('../../datasets/json_datasets/games.json')]
    file = open("../../datasets/pkl_datasets/runningbacksIDName.pkl","rb")
    rbs = pickle.load(file)
    file.close()
    
    rbgames = getRbGames(gameStats, rbs)

    file = open("../../datasets/pkl_datasets/rbgames.pkl","wb")
    pickle.dump(rbgames, file)
    file.close()
    print(rbgames)

if __name__ == "__main__":
    main()
