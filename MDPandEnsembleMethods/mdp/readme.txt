Generation of MDP file:(Assumptions)
1) Didn't consider transitions from a wall node and towards a wall node.
2) Reaching end state gets reward of 100000 and travelling in the grid(and thus wasting time) gets a reward of -100.
3) Number of states is given as N*M(which contains wall nodes and end node as well).
4) discount = 0.9

Solving MDP file:(Assumptions and evaluation instructions)
1) I considered numStates to is the size of superset which contains all the states that ever appear in the transitions.
2) Output contains value, policy pairs of each state from 0 to numStates-1.
3) If we cannot get a policy or value for a state(like wall nodes, which don't appear in the transitions), I wrote 0, -1 for that state.
4) Works for any general MDP file satisfying above assumptions.

Design of MDP:
	Design is based on what is given in the problem statement with the above assumptions mentioned
	
Algorithm Used:
	1) I used Value Iteration algorithm to update Value for each state(as mentioned in slides)
	2) Convergence criteria used:
	
		abs(V_new[i] - V_old[i]) >= epsilon   where  epsilon = (2*discount*1e-10)/(1-discount)
		
	3) After convergence is reached we can get policies from the values of each node(as mentioned in slides)
