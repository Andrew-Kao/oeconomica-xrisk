import pdb
import numpy as np
from anytree import Node, RenderTree

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

# payoffs at bottom level?
top = Node("top")
Success = Node("Success", parent = top)
success = Node("success", parent = Success)
attack = Node("attack", parent = success)
retreat = Node("retreat", parent = success)
failure = Node("failure", parent = Success)
attack = Node("attack", parent = failure)
retreat = Node("retreat", parent = failure)

Failure = Node("Failure", parent = top)
success = Node("success", parent = Failure)
attack = Node("attack", parent = success)
retreat = Node("retreat", parent = success)
failure = Node("failure", parent = Failure)
attack = Node("attack", parent = failure)
retreat = Node("retreat", parent = failure)

print(RenderTree(top))

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
	nashEquilibria = findNash(nashMatrix)

	pbe = []

	eqnum = 0
	for eq in nashEquilibria:
		checkEq(state, eq)
		eqnum += 1

	return nashMatrix


# for each nash, determine: (1) for what beliefs does sequentially rationality hold? (2) what beliefs are supported?
# note - we only need to check the US, bc DPRK is deterministic
def checkEq(state, eq):

	# trueeq = [boolean for whether it holds, actions - [eq], beliefs - [[alpha min, alpha max],[q min, q max]]]
	trueeq = [0, eq, [[0,1],[0,1]]]

	# When DPRK annouces success


	# When DPRK announces failure

	return 



# find the Nash Equilibria given best responses
def findNash(nashMatrix):

	nashes = []

	i = 0
	j = 0
	for usamove in usaprofiles:
		for dprkmove in dprkprofiles:
			if nashMatrix[i][j][3] == 1 & nashMatrix[i][j][4]:
				nashes.append((dprkmove,usamove))
			j += 1
		i +=1 
		j = 0

	return nashes

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


# usa, dprk are expected payoffs for the usa, dprk
def expectedPayoff(usamove,dprkmove, state,pss, psf):
	dprk = state[dprkmove, usamove][0][0] * pss + state[dprkmove, usamove][1][0] * psf
	usa = state[dprkmove, usamove][0][1] * pss + state[dprkmove, usamove][1][1] * psf
	return (dprk, usa)


solveGame(state, pss, psf)




















