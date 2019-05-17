import pdb
import numpy as np
from anytree import Node, RenderTree
from sympy import *

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

top = Node("top")
Success = Node("Success", parent = top)
success = Node("success", parent = Success)
rss = Node("retreat", parent = success, dprk = 0, usa = -1)
ass = Node("attack", parent = success, dprk = -2, usa = -3)
failure = Node("failure", parent = Success)
rsf = Node("retreat", parent = failure, dprk = 0, usa = 0)
asf = Node("attack", parent = failure, dprk = -2, usa = -3)

Failure = Node("Failure", parent = top)
success = Node("success", parent = Failure)
rfs = Node("retreat", parent = success, dprk = 0, usa = -1)
afs = Node("attack", parent = success, dprk = -2, usa = 2)
failure = Node("failure", parent = Failure)
rff = Node("retreat", parent = failure, dprk = 0, usa = 0)
aff = Node("attack", parent = failure, dprk = -2, usa = 2)

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
	justNash = []

	eqnum = 0
	for eq in nashEquilibria:
		eqlbm = checkEq(state, eq)
		if eqlbm[0] == 0:
			justNash.append(eqlbm)
		else:
			pbe.append(eqlbm)
		eqnum += 1


	return [pbe,justNash]


# for each nash, determine: (1) for what beliefs does sequentially rationality hold? (2) what beliefs are supported?
# note - we only need to check the US, bc DPRK is deterministic
def checkEq(state, eq):

	alpha, q = symbols('alpha q')

	# trueeq = [boolean for whether it holds, actions - [eq], beliefs - [[alpha min, alpha max],[q min, q max]]]
	alphaL = [0,1]
	qL = [0,1]

	# When DPRK annouces success

	usRealStrat = eq[1][0]
	usFakeStrat = ''
	if usRealStrat == 'r':
		usFakeStrat = 'a'
	else:
		usFakeStrat = 'r'

	solnSucc = solve([ alpha* (globals()[usRealStrat+"ss"].usa) + (1-alpha)*(globals()[usRealStrat+"fs"].usa) >= \
		alpha* (globals()[usFakeStrat+"ss"].usa) + (1-alpha)*(globals()[usFakeStrat+"fs"].usa), alpha >= 0, alpha <= 1],dict = True)
	try:
		bounds = solnSucc.as_set().boundary
		alphaL[0], alphaL[1] = bounds
	except:
		alphaL[0] = solnSucc.as_set()
		alphaL[1] = solnSucc.as_set()
		pass


	# When DPRK announces failure
	usRealStrat = eq[1][1]
	usFakeStrat = ''
	if usRealStrat == 'r':
		usFakeStrat = 'a'
	else:
		usFakeStrat = 'r'

	solnSucc = solve([ alpha* (globals()[usRealStrat+"sf"].usa) + (1-alpha)*(globals()[usRealStrat+"ff"].usa) >= \
		alpha* (globals()[usFakeStrat+"sf"].usa) + (1-alpha)*(globals()[usFakeStrat+"ff"].usa), alpha >= 0, alpha <= 1],dict = True)
	try:
		bounds = solnSucc.as_set().boundary
		qL[0], qL[1] = bounds
	except:
		qL[0] = solnSucc.as_set()
		qL[1] = solnSucc.as_set()
		pass

	# use actual beliefs -- rational if it works

	rational = 1

	# alphaT is the belief constraint imposed by DPRK strategy
	# -1 stands in for undefined 
	dprkStrat = eq[0]
	if dprkStrat == "ss":
		alphaT = pss
		qT = -1
	elif dprkStrat == "sf":
		alphaT = 1
		qT = 0
	elif dprkStrat == "fs":
		alphaT = 0
		qT = 1
	else:
		alphaT = -1
		qT = psf

	# check that this is valid, update values to reflect qT/alphaT if so
	# print(str(qT) + " | " + str(alphaT))
	if qT == -1:
		if (alphaT < alphaL[0]) | (alphaT > alphaL[1]):
			rational = 0
		else:
			alphaL[0] = alphaT
			alphaL[1] = alphaT
	elif alphaT == -1:
		if (qT < qL[0]) | (qT > qL[1]):
			rational = 0
		else:
			qL[0] = qT
			qL[1] = qT
	else:
		if (alphaT < alphaL[0])| (alphaT > alphaL[1]) | (qT < qL[0]) | (qT > qL[1]):
			rational = 0
		elif dprkStrat == "sf":
			alphaL[0] = 1
			alphaL[1] = 1
			qL[0] = 0
			qL[1] = 0
		else:
			alphaL[0] = 0
			alphaL[1] = 0
			qL[0] = 1
			qL[1] = 1


	trueeq = [rational, eq, [alphaL,qL]]

	return trueeq



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


eqlbms = solveGame(state, pss, psf)
print(eqlbms[0])  # PBEs
print(eqlbms[1])  # non-PBEs, but still Nash




















