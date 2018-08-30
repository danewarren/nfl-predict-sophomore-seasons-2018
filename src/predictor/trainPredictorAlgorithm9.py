#!/usr/bin/env python                                                         
'''                                                                           
Dane Warren 

TRAINING ONLY RECEIVING YARDS PER GAME
Predict the second season of veteran players based on their rookie seasons with various amounts of k neighbors.

TO DO

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
	else: #They are equal OR both horrible
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
       
	similarity = 1 * (airYpGSim)

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

def main():
    file = open("../../datasets/pkl_datasets/trainRookies.pkl","rb")
    trainRookies = pickle.load(file)
    file.close()

    file = open("../../datasets/pkl_datasets/trainSophomores.pkl","rb")
    trainSophomores = pickle.load(file)
    file.close()
    
    kRatings = {}
#    kRatings["name"] = "kRatings"
    k7 = {}
#    k7["name"] = "k7"
    k8 = {}
#    k8["name"] = "k8"
    k9 = {}
#    k9["name"] = "k9"
    #Get the best k value from 1 to 237 The number of training people - 1
    for k in range(1, len(trainSophomores)):
        kRatings[k] = 0
	k7[k] = 0
	k8[k] = 0
        k9[k] = 0
        #Loop through every running back who had touched the ball at least 100 times in both their rookie and sophomore seasons.
        for rookie in trainRookies:
            neighbors = {}
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
	    for sophomore in trainSophomores:
		    if rookie["ID"] == sophomore["ID"]:
			    predictiveRating = similarityScore(neighborFPPG, sophomore["fantasyPointsPerGame"])
			    kRatings[k] += (float(predictiveRating) / float(len(trainSophomores) - 1))
			    
			    if(predictiveRating >= .7):
				    k7[k] += (float(1) / float(len(trainSophomores) - 1))
			    if(predictiveRating >= .8):
				    k8[k] += (float(1) / float(len(trainSophomores) - 1))
			    if(predictiveRating >= .9):
				    k9[k] += (float(1) / float(len(trainSophomores) - 1))

    print("RESULTS FROM ALGORITHM 9: ONLY RECEIVING YARDS PER GAME")

    print("max k7:")
    maxK7 = getMax(k7)
    print(maxK7)
    
    print("max k8:")
    maxK8 = getMax(k8)
    print(maxK8)

    print("max k9:")
    maxK9 = getMax(k9)
    print(maxK9)
    
    print("max kRating:")
    maxKRating = getMax(kRatings)
    print(maxKRating)

    print("alt k7 values:")
    altK7 = {}
    altK7[maxK8.keys()[0]] = k7[maxK8.keys()[0]]
    altK7[maxK9.keys()[0]] = k7[maxK9.keys()[0]]
    altK7[maxKRating.keys()[0]] = k7[maxKRating.keys()[0]]
    print(altK7)

    print("alt k8 values:")
    altK8 = {}
    altK8[maxK7.keys()[0]] = k8[maxK7.keys()[0]]
    altK8[maxK9.keys()[0]] = k8[maxK9.keys()[0]]
    altK8[maxKRating.keys()[0]] = k8[maxKRating.keys()[0]]
    print(altK8)

    print("alt k9 values:")
    altK9 = {}
    altK9[maxK8.keys()[0]] = k9[maxK8.keys()[0]]
    altK9[maxK7.keys()[0]] = k9[maxK7.keys()[0]]
    altK9[maxKRating.keys()[0]] = k9[maxKRating.keys()[0]]
    print(altK9)

    print("alt kRating values:")
    altKRating = {}
    altKRating[maxK8.keys()[0]] = kRatings[maxK8.keys()[0]]
    altKRating[maxK9.keys()[0]] = kRatings[maxK9.keys()[0]]
    altKRating[maxK7.keys()[0]] = kRatings[maxK7.keys()[0]]
    print(altKRating)
    
if __name__ == "__main__":
    main()
