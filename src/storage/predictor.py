#!/usr/bin/env python
'''
Dane Warren

Obtain the k nearest neighbors of the given player and use the second seasons these neighbors to predict the second season of the given player.
'''

import cPickle as pickle

'''
@param rbID: The ID of the running back to get the stats for
@param rrbStats: A list containing dictionaries of rookie running back statlines
@returns: The rookie season statline of the given ID
'''
def getIndividualRookieStats(rbID, rrbStats):
    for player in rrbStats:
        if player["ID"] == rbID:
            print(player)
            return player
    return 0

'''
@param x: Number to compare to y
@param y: Number to compare to x
@returns: The similarity of the two numbers
'''
def similarityScore(x, y):
    if x < y and y != 0:
        similarity = float(x) / float(y)
    elif x > y and x != 0:
        similarity = float(y) / float(x)
    else: 
        similarity = 1
    if x < 0 or y < 0:
        similarity = 0
    if x == 0 and y == 0:
        similarity = 1
    return similarity

'''
@param rb: The stats of every rookie running back since 1950
@param stats: The given running back's rookie season stats
@param ID: The ID of the given running back
@returns: The similarity rating of the given rb and the next rb in the list
'''
def getSimilarity(rb, stats):
    similarity = 0

    if rb["gamesPlayed"] >= 8:

        rushYpASim = similarityScore(rb["rushYpA"], stats["rushYpA"])
        rushYpGSim = similarityScore(rb["rushYpG"], stats["rushYpG"])
        rushTDpGSim = similarityScore(rb["rushTDpG"], stats["rushTDpG"])
        rushTDpASim = similarityScore(rb["rushTDpA"], stats["rushTDpA"])
        airYpGSim = similarityScore(rb["airYpG"], stats["airYpG"])
        airYpRSim = similarityScore(rb["airYpR"], stats["airYpR"])
        airTDpGSim = similarityScore(rb["airTDpG"], stats["airTDpG"])
        airTDpRSim = similarityScore(rb["airTDpR"], stats["airTDpR"])

        similarity = .125 * (rushYpASim + rushYpGSim + rushTDpGSim + rushTDpASim + airYpGSim + airYpRSim + airTDpGSim + airTDpRSim)

    if rb["ID"] == stats["ID"]:
        similarity = 0

    return similarity

'''
@param k: The number of neighbors to return
@param inputRB: The stats of the given running back
@param rrbStats: The stats of every rookie running back
@returns: k nearest neighbors and the similarity scores
'''
def getNearestNeighbors(k, inputRB, rrbStats):
    nearestNeighbors = {}
    for rb in rrbStats:
        similarity = getSimilarity(rb, inputRB)
        if len(nearestNeighbors) < k:
            nearestNeighbors[rb["ID"]] = similarity
        else:
            sortedNums = sorted(nearestNeighbors.values())
            if(similarity > sortedNums[0]):
                sortedNames = sorted(nearestNeighbors, key=nearestNeighbors.get)
                del nearestNeighbors[sortedNames[0]]
                nearestNeighbors[rb["ID"]] = similarity
    return nearestNeighbors


def getNeighbors(inputRB, rrbStats):
    neighbors = {}
    for rb in rrbStats:
        neighbors[rb["ID"]] = getSimilarity(rb, inputRB)
    return neighbors

def getSophomoreStats(srbStats, ID):
    for player in srbStats:
        if player["ID"] == ID:
            if player["fantasyPoints"] == 0:
                return -1 #Player did not touch the ball in their second season
            return player
    return -1

def main():
    file = open("../../datasets/pkl_datasets/rookie_rbStats.pkl","rb")
    rrbStats = pickle.load(file)
    file.close()

    file = open("../../datasets/pkl_datasets/sophomore_rbStats.pkl","rb")
    srbStats = pickle.load(file)
    file.close()

    file = open("../../datasets/pkl_datasets/runningbacksNameID.pkl")
    rbs = pickle.load(file)
    file.close()

    #GET INPUT RB
    rbID = raw_input("Enter a running back. (Name or ID) \n")
    if rbID.isdigit():
        rbID = int(rbID)
    else:
        rbID = rbs[rbID]
    inputRB = getIndividualRookieStats(rbID, rrbStats)
    if inputRB["fantasyPoints"] == 0:
        print("This player did not touch the ball in their rookie season.")
        return
    if getSophomoreStats(srbStats, rbID) == "This player did not touch the ball in their sophomore season.":
        print("This player did not touch the ball in their sophomore season.")
        return
    
    #GET NEIGHBORS
    for rb in rrbStats:
        if rb["fantasyPoints"] == 0:
            rrbStats.remove(rb)
    neighbors = getNeighbors(inputRB, rrbStats)
    
    #SORT NEIGHBORS
    sortedNeighbors = []
    for value in sorted(neighbors.values()):
        for key in neighbors.keys():
            sort = {}
            if neighbors[key] == value:
                sort[key] = value
                sortedNeighbors.append(sort)

    #GET K NEAREST NEIGHBORS
    k = 5
    kNeighbors = sortedNeighbors[-k:]
    #GET NEIGHBOR SOPHOMORE STATS AND COMPARE
    stats = {}
    neighborStats = []
    maxPredictiveRating = 0
    bestK = 0
    bestNeighborFPPG = 0
    while k <= 40:
        kNeighbors = sortedNeighbors[-k:]
        totalNeighborFP = 0
        totalNeighborGames = 0
        for neighbor in kNeighbors:
            stats = getSophomoreStats(srbStats, neighbor.keys()[0])
            if stats["fantasyPoints"] != 0:
                totalNeighborFP += stats["fantasyPoints"]
                totalNeighborGames += stats["gamesPlayed"]
        neighborFPPG = float(totalNeighborFP) / float(totalNeighborGames)
        inputRBSophomoreStats = getSophomoreStats(srbStats, rbID)
        predictiveRating = similarityScore(neighborFPPG, inputRBSophomoreStats["fantasyPointsPerGame"])
        if predictiveRating > maxPredictiveRating:
            maxPredictiveRating = predictiveRating
            bestK = k
            bestNeighborFPPG = neighborFPPG
        k += 1
    print(bestK)
    print(maxPredictiveRating)
    print(bestNeighborFPPG)
    print(inputRBSophomoreStats["fantasyPointsPerGame"])
    print(getSophomoreStats(srbStats, 4418))

if __name__ == "__main__":
    main()
