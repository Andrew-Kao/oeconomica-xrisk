import pdb
import numpy as np

# contains info about payoffs and probabilities of success given observed success/failure

# payoff: (dprk, usa)
# pss: P(Success | US obs. success), psf: P(Success | US obs. failure)
state = {
	("ss","aa"): ((-2,-3),(-2,2)), ("sf","aa"): ((-2,-3),(-2,2)), ("fs","aa"): ((-2,-3),(-2,2)), ("ff","aa"): ((-2,-3),(-2,2)),
	("ss","ar"): ((-2,-3),(-2,2)), ("sf","ar"): ((-2,-3),(0,0)), ("fs","ar"): ((0,0),(-2,2)), ("ff","ar"): ((0,0),(0,0)),
	("ss","ra"): ((0,-1),(0,-1)), ("sf","ra"): ((0,-1),(-2,2)), ("fs","ra"): ((-2,-3),(0,-1)), ("ff","ra"): ((-2,-3),(-2,2)),
	("ss","rr"): ((0,-1),(0,-1)), ("sf","rr"): ((0,-1),(0,0)), ("fs","rr"): ((0,0),(0,-1)), ("ff","rr"): ((0,0),(0,0))
}
pss = .75 
psf = .25

# first one is success, second letter is failure
usaprofiles = ["aa", "ar", "ra", "rr"]
dprkprofiles = ["ss", "sf", "fs", "ff"]

def solveGame(state, pss, psf):

	# 4x4 matrix containing info about payoffs, and the action profiles associated with it
	nashMatrix = [[0 for x in range(4)] for y in range(4)]

	usabr = 0  # dummy, 1 if this is a best response
	dprkbr = 0
	i = 0
	j = 0
	for usamove in usaprofiles:
		for dprkmove in dprkprofiles:
			nashMatrix[i][j] = [usamove, dprkmove, expectedPayoff(usamove, dprkmove, state, pss, psf), usabr, dprkbr]
			j += 1
		i +=1 
		j = 0
	
	# Determine best responses and equilibria
	nashMatrix = findBR(nashMatrix)

	print nashMatrix
	return nashMatrix

# usa, dprk are expected payoffs for the usa, dprk
def expectedPayoff(usamove,dprkmove, state,pss, psf):
	dprk = state[dprkmove, usamove][0][0] * pss + state[dprkmove, usamove][1][0] * psf
	usa = state[dprkmove, usamove][0][1] * pss + state[dprkmove, usamove][1][1] * psf
	return (dprk, usa)

# find the best responses given payoffs to a nash matrix
def findBR(nashMatrix):

	# given a us move, what is the dprk best response?
	score = float("-inf")
	i = 0
	j = 0
	for usamove in usaprofiles:

		# find max score
		for dprkmove in dprkprofiles:
			if nashMatrix[i][j][2][0] > score:
				score = nashMatrix[i][j][2][0]
			j += 1
		j = 0
		
		print(score)
		# fill in best responses
		for dprkmove in dprkprofiles:
			if nashMatrix[i][j][2][0] == score:
				nashMatrix[i][j][4] = 1
			j += 1
		i +=1
		j = 0
		score = float("-inf")


	# given a us move, what is the dprk best response?
	score = float("-inf")
	i = 0
	j = 0
	for dprkmove in dprkprofiles:

		# find max score
		for usamove in usaprofiles:
			if nashMatrix[j][i][2][1] > score:
				score = nashMatrix[j][i][2][1]
			j += 1
		j = 0
		
		# fill in best responses
		for dprkmove in dprkprofiles:
			if nashMatrix[j][i][2][1] == score:
				nashMatrix[j][i][3] = 1
			j += 1
		i +=1
		j = 0
		score = float("-inf")

	return nashMatrix

# find the Nash Equilibria given best responses
def findNash(nashMatrix):

	return


solveGame(state, pss, psf)




















