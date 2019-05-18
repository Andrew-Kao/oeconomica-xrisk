import pdb
import numpy as np
from anytree import Node, RenderTree
from sympy import *


### The Tree
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


# contains info about payoffs and probabilities of success given observed success/failure

# payoff: (dprk, usa), firs tentry of tuple is payoff when actual success
# pss: P(Success | US obs. success), psf: P(Success | US obs. failure)
state = {
	("ss","aa"): ((-2,-3),(-2,2)), ("sf","aa"): ((-2,-3),(-2,2)), ("fs","aa"): ((-2,-3),(-2,2)), ("ff","aa"): ((-2,-3),(-2,2)),
	("ss","ar"): ((-2,-3),(-2,2)), ("sf","ar"): ((-2,-3),(0,0)), ("fs","ar"): ((0,0),(-2,2)), ("ff","ar"): ((0,0),(0,0)),
	("ss","ra"): ((0,-1),(0,-1)), ("sf","ra"): ((0,-1),(-2,2)), ("fs","ra"): ((-2,-3),(0,-1)), ("ff","ra"): ((-2,-3),(-2,2)),
	("ss","rr"): ((0,-1),(0,-1)), ("sf","rr"): ((0,-1),(0,0)), ("fs","rr"): ((0,0),(0,-1)), ("ff","rr"): ((0,0),(0,0))
}

def tree_to_states(top):
	'''
	'''
	rv = {}
	for outcome in top.children:
		out = outcome.name[0].lower() 	
		for dpm in outcome.children:
			dp_move = dpm.name[0] 		# 's' or 'f'
			for usm in dpm.children:
				us_move = usm.name[0] #'r' or 'a'
				dp_payoff = usm.dprk
				us_payoff = usm.usa
				key = out + dp_move + us_move
				val = (dp_payoff, us_payoff)
				rv[key] = val

	return rv
