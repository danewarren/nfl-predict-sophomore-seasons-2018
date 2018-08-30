#!/usr/bin/env python                                                         
'''                                                                           
Dane Warren 

Dalvin Cook:  ONLY YARDS PER GAME
Predict the second season of Aaron Jones based on his rookie season using Algorithm 7 with k=12 neighbors..
'''

import cPickle as pickle

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
	else: #They are equal OR both horrible (<= 0)
		similarity = 1
	return similarity

'''
@param player1: The first player
@param player2: The second player
@returns: The similarity rating of the two players
'''
def getSimilarity(player1, player2):
        rushYpASim = similarityScore(player1["rushYpA"], player2["rushYpA"])
        rushYpGSim = similarityScore(player1["rushYpG"], player2["rushYpG"])
        rushTDpGSim = similarityScore(player1["rushTDpG"], player2["rushTDpG"])
        rushTDpASim = similarityScore(player1["rushTDpA"], player2["rushTDpA"])
        airYpGSim = similarityScore(player1["airYpG"], player2["airYpG"])
        airYpRSim = similarityScore(player1["airYpR"], player2["airYpR"])
	airTDpGSim = similarityScore(player1["airTDpG"], player2["airTDpG"])
        airTDpRSim = similarityScore(player1["airTDpR"], player2["airTDpR"])
       
	similarity = .5 * (rushYpGSim + airYpGSim)

	if player1["ID"] == player2["ID"]:
		similarity = 0

	return similarity

'''
@param key: The key
@param value: The value
@returns: The dictionary of the key and the value
'''
def createDict(key, value):
	dict = {}
	dict[key] = value
	return dict

'''
@param inputRookie: The rookie to get neighbors for
@param trainRookies: The dataset of all rookie seasons
@returns: All neighbors and similarity scores. neighbors[ID] = score
'''
def getNeighbors(inputRookie, trainRookie):
	neighbors = {}
	for rookie in trainRookie:
		if rookie != inputRookie:
			similarity = getSimilarity(rookie, inputRookie)			
			neighbors[rookie["ID"]] = similarity
	return neighbors

'''
@param neighbors: List of all possible neighbors
@returns: Dictionary sorted into list by value
'''
def dictValueSort(dict):
    sort = []
    for value in sorted(dict.values()):
        for key in dict.keys():
            if dict[key] == value:
		sort.append(createDict(key, value))
    return sort

'''
@param k: The number of neighbors to return
@param sortedList: An already sorted list
@returns: The k nearest neighbors
'''
def kNearestNeighbors(k, sortedList):
	return sortedList[-k:]

'''
@param dict: A dictionary
@returns: The maximum value of the dictionary, with its key
'''
def getMax(dict):
	max = 0
	for key in dict:
		if dict[key] > max:
			max = dict[key]
	best = {}
	for key in dict:
            if dict[key] == max:
                    best[key] = max
	return best

'''
@returns: The rookie statline of the player
'''
def getRookieAaronJones():
	data = {}
	data["ID"] = 4458
	data["gamesPlayed"] = 4
	data["rushing_attempts"] = 74
	data["rushing_yards"] = 354
	data["rushing_touchdowns"] = 2
	data["receiving_targets"] = 16
	data["receiving_receptions"] = 11
	data["receiving_yards"] = 90
	data["receiving_touchdowns"] = 0

	data["rushYpA"] = float(data["rushing_yards"]) / float(data["rushing_attempts"])
        data["rushTDpA"] = float(data["rushing_touchdowns"]) / float(data["rushing_attempts"])
	data["airYpR"] = float(data["receiving_yards"]) / float(data["receiving_receptions"])
        data["airTDpR"] = float(data["receiving_touchdowns"]) / float(data["receiving_receptions"])
	data["airYpG"] = float(data["receiving_yards"]) / float(data["gamesPlayed"])
        data["airTDpG"] = float(data["receiving_touchdowns"]) / float(data["gamesPlayed"])
        data["rushYpG"] = float(data["rushing_yards"]) / float(data["gamesPlayed"])
        data["rushTDpG"] = float(data["rushing_touchdowns"]) / float(data["gamesPlayed"])

	data["fantasyPoints"] = float((data["rushing_yards"]+data["receiving_yards"])/float(10) + (data["receiving_touchdowns"] + data["rushing_touchdowns"])*6 + data["receiving_receptions"])
        data["fantasyPointsPerGame"] = data["fantasyPoints"] / data["gamesPlayed"]

	return data

def main():
    file = open("../../datasets/pkl_datasets/trainRookies.pkl","rb")
    trainRookies = pickle.load(file)
    file.close()

    file = open("../../datasets/pkl_datasets/trainSophomores.pkl","rb")
    trainSophomores = pickle.load(file)
    file.close()
    
    k = 12 #The best k value for this algorithm (7) is 12. 
    rookie = getRookieAaronJones() 
    
    neighbors = getNeighbors(rookie, trainRookies)
    sortedNeighbors = dictValueSort(neighbors)
    kNeighbors = kNearestNeighbors(k, sortedNeighbors)
	    
    totalNeighborFP = 0
    totalNeighborGames = 0
    for neighbor in kNeighbors:
	    for sophomore in trainSophomores:
		    if neighbor.keys()[0] == sophomore["ID"]:
			    totalNeighborFP += sophomore["fantasyPoints"]
			    totalNeighborGames += sophomore["gamesPlayed"]
    neighborFPPG = float(totalNeighborFP) / float(totalNeighborGames)
    floor = float(neighborFPPG) * float(.7756605492437657)
    ceiling = float(neighborFPPG) / float(.7756605492437657)
    
    print("Dalvin Cook: 85/100 touches")
    print("Projected: %f" % neighborFPPG)
    print("Floor: %f" % floor)
    print("Ceiling: %f" % ceiling)
    print("")


if __name__ == "__main__":
    main()
