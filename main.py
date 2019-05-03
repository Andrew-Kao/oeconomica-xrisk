import pdb
import numpy as np

# contains info about payoffs and probabilities of success given observed success/failure

# payoff: (dprk, usa)
# pss: P(Success | US obs. success), psf: P(Success | US obs. failure)
state = {
	("ss","aa"): ((-2,-3),(-2,2)), ("sf","aa"): ((-2,-3),(-2,2)), ("fs","aa"): ((-2,-3),(-2,2)), ("ff","aa"): ((-2,-3),(-2,2)),
	("ss","ar"): ((-2,-3),(0,-1)), ("sf","ar"): ((-2,-3),(0,0)), ("fs","ar"): ((-2,-3),(0,-1)), ("ff","ar"): ((-2,-3),(0,0)),
	("ss","ra"): ((0,-1),(-2,-3)), ("sf","ra"): ((0,-1),(-2,-3)), ("fs","ra"): ((0,0),(-2,2)), ("ff","ra"): ((0,0),(-2,2)),
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

	i = 0
	j = 0
	for usmove in usaprofiles:
		for dprkmove in dprkprofiles:
			print(i,j)
			nashMatrix[i][j] = (expectedPayoff(usmove, dprkmove, state, pss, psf), usmove, dprkmove)
			j += 1
		i +=1 
		j = 0
	


	return XYZ

# usa, dprk are expected payoffs for the usa, dprk
def expectedPayoff(usmove,dprkmove, state,pss, psf):
	dprk = state[dprkmove, usmove][0][0] * pss + state[dprkmove, usmove][1][0] * psf
	usa = state[dprkmove, usmove][0][1] * pss + state[dprkmove, usmove][1][1] * psf
	return (dprk, usa)

# 
def findBR(nashMatrix):

	return 


solveGame(state, pss, psf)
