#!/usr/bin/env python 
'''
Dane Warren

Create a training dataset for the predictor. Dataset will contain all running backs who had at least 100 touches in both their rookie season and sophomore season. Contains 238 players since 1950.
'''

import cPickle as pickle



def getTrainPlayer(name, ID, rookie, sophomore):
    player = {}
    player["name"] = name
    player["ID"] = ID
    player["rookie"] = rookie
    player["sophomore"] = sophomore
    return player


'''
@param rookieStats: Rookie season statlines for all running backs
@param sophomoreStats: Second years statlines for all running backs
@param rbs: Dictionary[ID] = name of runningbacks
@returns: Dictionary[ID]=name of runningbacks w/ >= 100 touches in both seasons.
'''
def getTrainData(rookieStats, sophomoreStats, rbs):
    trainRBs = {}
    trainData = []
    for rb in rbs:
        for rookie in rookieStats:
            if rb == rookie["ID"]:
                rTouches = rookie["receiving_receptions"] + rookie["rushing_attempts"]
                if rTouches >= 100:
                    for sophomore in sophomoreStats:
                        if rb == sophomore["ID"]:
                            sTouches = sophomore["receiving_receptions"] + sophomore["rushing_attempts"]
                            if sTouches >= 100:
                                trainRBs = getTrainPlayer(rbs[rb], rb, rookie, sophomore)
                                trainData.append(trainRBs)
    return trainData


def main():
    file = open("../../datasets/pkl_datasets/rookie_rbStats.pkl","rb")
    rrbStats = pickle.load(file)
    file.close()

    file = open("../../datasets/pkl_datasets/sophomore_rbStats.pkl","rb")
    srbStats = pickle.load(file)
    file.close()
    
    file = open("../../datasets/pkl_datasets/runningbacksIDName.pkl")
    rbs = pickle.load(file)
    file.close()
    
    trainData = {}
    trainData = getTrainData(rrbStats, srbStats, rbs)

    file = open("../../datasets/pkl_datasets/trainData.pkl", "wb")
    pickle.dump(trainData, file)
    file.close()

    trainRookies = []
    trainSophomores = []
    i = 0
    for key in trainData:
        trainRookies.append(key["rookie"])
        trainSophomores.append(key["sophomore"])

    file = open("../../datasets/pkl_datasets/trainRookies.pkl", "wb")
    pickle.dump(trainRookies, file)
    file.close()

    file = open("../../datasets/pkl_datasets/trainSophomores.pkl", "wb")
    pickle.dump(trainSophomores, file)
    file.close()

if __name__ == "__main__":
    main()
