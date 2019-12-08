import argparse
import numpy as np
import collections

def parse(mdpfile):
    f = open(mdpfile, "r")
    temp = f.readline()
    numStates = int(temp.split()[1])
    temp = f.readline()
    numActions = int(temp.split()[1])
    temp = f.readline()
    start = int(temp.split()[1])
    temp = f.readline()
    end = []
    for i in temp.split():
        if(i != "end"):
            end.append(int(i))
    states = collections.defaultdict(lambda: collections.defaultdict(list))
    temp = f.readline()
    temp = temp.split()
    while(temp[0] == "transition"):
        states[int(temp[1])][int(temp[2])].append([int(temp[3]), int(temp[4]), int(temp[5])])
        temp = f.readline()
        temp = temp.split()
    states = dict(states)
    discount = float(temp[1])
    return numStates, numActions, start, end, states, discount

def solve(numStates, numActions, start, end, states, discount):
    epsilon = (2*discount*1e-10)/(1-discount)

    def check(V_new, V_old):
        for i in V_new.keys():
            if(abs(V_new[i] - V_old[i]) >= epsilon):
                return True
        return False
    
    V_old = collections.defaultdict(lambda : 0)
    V_new = collections.defaultdict(lambda: 0)
    P = {}

    for i in states.keys():
        V_old[i] = 0
        V_new[i] = 0
    
    for s in states.keys():
        l = {}
        for i in states[s].keys():
            temp = 0
            for j in states[s][i]:
                temp += j[2]*j[1] + discount*V_old[j[0]]
            l[i] = temp
        V_new[s] = max(l.values())
        for key, value in l.items():
            if value == V_new[s]:
                P[s] = key    
    while(check(V_new, V_old)):
        for i in V_new.keys():
            V_old[i] = V_new[i]
        for s in states.keys():
            l = {}
            for i in states[s].keys():
                temp = 0
                for j in states[s][i]:
                    temp += j[2]*j[1] + discount*V_old[j[0]]
                l[i] = temp
            V_new[s] = max(l.values())
            for key, value  in l.items():    # for name, age in dictionary.iteritems():  (for Python 2.x)
                if value == V_new[s]:
                    P[s] = key

    return V_new, P
        

def final(outputfile, V, P, numStates):
    f = open(outputfile, "w")
    values = np.zeros((numStates))
    policies = np.ones((numStates))
    policies = -policies
    for i in V.keys():
        values[i] = V[i]
        policies[i] = P[i]
    for i in range(numStates):
        f.write(str.format('{0:.6f}',values[i])+" "+str(int(policies[i]))+"\n")
        

def genPath(grid, value_policy):
    gridFile = open(grid, 'r')
    maze = []
    for line in gridFile:
        row = []
        for word in line.split():
            row.append(int(word))
        maze.append(row)
    maze = np.asarray(maze)
    N = maze.shape[0]
    M = maze.shape[1]

    def getPos(t):
        return t[0] * M + t[1]

    def North(i, j):
        if i - 1 < 0:
            return i, j
        return i - 1, j

    def East(i, j):
        if j + 1 > M - 1:
            return i, j
        return i, j + 1

    def South(i, j):
        if i + 1 > N - 1:
            return i, j
        return i + 1, j

    def West(i, j):
        if j - 1 < 0:
            return i, j
        return i, j - 1

    value_policyFile = open(value_policy, 'r')
    policy = []
    for line in value_policyFile:
        value, action = line.split()
        policy.append(int(action))
    index = np.argwhere(maze == 2)[0]
    while maze[index[0], index[1]] != 3:
        if policy[getPos(index)] == 0:
            action = 'N'
            nextIndex = North(index[0], index[1])
        elif policy[getPos(index)] == 1:
            action = 'E'
            nextIndex = East(index[0], index[1])
        elif policy[getPos(index)] == 2:
            action = 'W'
            nextIndex = West(index[0], index[1])
        elif policy[getPos(index)] == 3:
            action = 'S'
            nextIndex = South(index[0], index[1])
        print(action, end=" ")
        index = nextIndex

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mdpfile", help="mdp file name")
    parser.add_argument("-o", "--output", help="output file name")
    args = parser.parse_args()
    numStates, numActions, start, end, states, discount = parse(args.mdpfile)
    V,P = solve(numStates, numActions, start, end, states, discount)
    final(args.output, V, P, numStates)
    # genPath('grid10.txt', args.output)
