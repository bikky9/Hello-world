import argparse
import numpy as np

def getTransitions(maze, i, j):
    reward_free = -1
    reward_wall = reward_free
    reward_end = 1e7
    N = maze.shape[0]
    M = maze.shape[1]

    def getPos(t):
        return t[0]*M + t[1]

    def North(i, j):
        if i-1 < 0:
            return -1
        return (i-1, j)

    def East(i, j):
        if j+1 > M-1:
            return -1
        return (i, j+1)

    def South(i, j):
        if i+1 > N-1:
            return -1
        return (i+1, j)

    def West(i, j):
        if j-1 < 0:
            return -1
        return (i, j-1)

    transitions = []

    nextPos = North(i, j)
    if maze[nextPos] == 1:
        transitions.append("transition", getPos((i, j)), 0, getPos(nextPos), reward_wall, 1)
    elif maze[nextPos] != 3:
        transitions.append("transition", getPos((i, j)), 0, getPos(nextPos), reward_free, 1)
    elif maze[nextPos] == 3:
        transitions.append("transition", getPos((i, j)), 0, getPos(nextPos), reward_end, 1)

    nextPos = East(i, j)
    if maze[nextPos] == 1:
        transitions.append("transition", getPos((i, j)), 0, getPos(nextPos), reward_wall, 1)
    elif maze[nextPos] != 3:
        transitions.append("transition", getPos((i, j)), 1, getPos(nextPos), reward_free, 1)
    elif maze[nextPos] == 3:
        transitions.append("transition", getPos((i, j)), 1, getPos(nextPos), reward_end, 1)

    nextPos = West(i, j)
    if maze[nextPos] == 1:
        transitions.append("transition", getPos((i, j)), 0, getPos(nextPos), reward_wall, 1)
    elif maze[nextPos] != 3:
        transitions.append("transition", getPos((i, j)), 2, getPos(nextPos), reward_free, 1)
    elif maze[nextPos] == 3:
        transitions.append("transition", getPos((i, j)), 2, getPos(nextPos), reward_end, 1)

    nextPos = South(i, j)
    if maze[nextPos] == 1:
        transitions.append("transition", getPos((i, j)), 0, getPos(nextPos), reward_wall, 1)
    elif maze[nextPos] != 3:
        transitions.append("transition", getPos((i, j)), 3, getPos(nextPos), reward_free, 1)
    elif maze[nextPos] == 3:
        transitions.append("transition", getPos((i, j)), 3, getPos(nextPos), reward_end, 1)


    return transitions

def genMDP(gridFile, outputfile):
    def getPos(t):
        return t[0]*M + t[1]
        
    gridFile = open(gridFile, "r")
    O = open(outputfile, "w")
	maze = []
    # parse through the file to Number of rows and columns
    for line in gridFile:
    	row = []
        for word in line.split():
            row.append(int(word))
        maze.append(row)
    maze = np.asarray(maze)
    N = maze.shape[0]
    M = maze.shape[1]
    O.write("numStates " + str(N*M) + "\n")
    O.write("numActions " + "4" + "\n")
    O.write("start", getPos(np.argwhere(maze == 2)[0]))
    end = [getPos(i) for i in np.argwhere(maze == 3)]
    O.write("end", *end)
    #getting all possible transitions from every node
    transition = []
    for i in range(N):
        for j in range(M):
            if(maze[i, j] == 3 or maze[i, j] == 1):
                continue
            transition += getTransitions(maze, i, j)
    for i in transition:
        O.write("transition ")
        for j in i:
            O.write(" " + str(j))
        O.write("\n")
    O.write("discount " + str(0.9) + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file name")
    parser.add_argument("-m", "--mdpfile", help="mdp file name")
    args = parser.parse_args()
    genMDP(args.input, args.mdpfile)
