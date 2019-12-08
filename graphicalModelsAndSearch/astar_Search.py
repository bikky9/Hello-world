import sys
import argparse
import numpy as np
import heapq
import ast

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Input file name")
parser.add_argument("-m", "--model", help="model file name")
parser.add_argument("-o", "--output", help="output file name")

args = parser.parse_args()

f = open(args.model, 'r')
l = ast.literal_eval(f.read())
tagset = l["tagset"]
transition_matrix = np.array(l["transition_matrix"])
emission_dict = l["emission_dict"]
for keys in emission_dict.keys():
    emission_dict[keys] = np.array(emission_dict[keys])
lbd = 1e-6
N = len(tagset)


special = tagset.index('<s>')
special1 = tagset.index('</s>')

f = open(args.input, 'r')
g = open(args.output, 'w')
testlist = []
for line in f:
        testlist = []
        for i in line.split():
            testlist.append(i)
        T = len(testlist)
        SEQSCORE = np.zeros((N, T)) - 10000
        BACKPTR = np.zeros((N, T))
        # Initialization
        l = []
        for i in range(0, N):
            if(testlist[0] in emission_dict):
                SEQSCORE[i, 0] = transition_matrix[special, i] + emission_dict[testlist[0]][i]
                l.append([SEQSCORE[i,0],i,0])
            else:
                SEQSCORE[i, 0] = transition_matrix[special, i] + np.log(lbd*1e-8)
                l.append([SEQSCORE[i,0],i,0])
            BACKPTR[i, 0] = i
        heapq.heapify(l)
        while(l[0][2] != T-1):
            t = l[0][2] + 1
            j = l[0][1]
            for i in range(0, N):
                if(testlist[t] in emission_dict and j != special1 and j != special and i != special1 and i != special):
                    temp = (SEQSCORE[j, t-1] + transition_matrix[j, i] + emission_dict[testlist[t]][j])
                elif(j != special1 and j != special and i != special1 and i != special):
                    temp = (SEQSCORE[j, t-1] + transition_matrix[j, i] + np.log(1/1e10))
                else:
                    temp = (-1e10)
                if(SEQSCORE[i,t]<temp):
                    SEQSCORE[i,t] = temp
                    heapq.heappush(l,[SEQSCORE[i,t],i,t])
                    BACKPTR[i, t] = j
            heapq.heappop(l)
        C = np.zeros((T))
        for i in range(N):
            SEQSCORE[i, T-1] += transition_matrix[i, special1]
        C[T-1] = np.argmax(SEQSCORE[:, T-1])
        C[T-1] = l[0][1]
        for i in range(T-2, -1, -1):
            C[i] = BACKPTR[int(C[i+1]), i+1]
        for i in range(T):
            g.write(tagset[int(C[i])])
            g.write(' ')
        g.write('\n')
