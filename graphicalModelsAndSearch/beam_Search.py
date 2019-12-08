import sys
import argparse
import numpy as np
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
beam_size = 20
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
        SEQSCORE = np.zeros((N, T))
        BACKPTR = np.zeros((N, T))
        # Initialization
        for i in range(0, N):
            if(testlist[0] in emission_dict):
                SEQSCORE[i, 0] = transition_matrix[special, i] + \
                    emission_dict[testlist[0]][i]
            else:
                SEQSCORE[i, 0] = transition_matrix[special, i] + \
                    np.log(lbd*1e-8)
            BACKPTR[i, 0] = i
        for t in range(1, T):
            for i in range(0, N):
                temp = np.zeros((N))
                iterlist = np.argsort(SEQSCORE[:,t-1])[N-beam_size:N]
                for j in range(N):
                    if(testlist[t] in emission_dict and j in iterlist and j != special1 and j != special and i != special1 and i != special):
                        temp[j] = (
                            SEQSCORE[j, t-1] + transition_matrix[j, i] + emission_dict[testlist[t]][j])
                    elif(j in iterlist and j != special1 and j != special and i != special1 and i != special):
                        temp[j] = (
                            SEQSCORE[j, t-1] + transition_matrix[j, i] + np.log(1/1e10))
                    else:
                        temp[j] = (-1e10)
                SEQSCORE[i, t] = max(temp)
                BACKPTR[i, t] = np.argmax(temp)
        C = np.zeros((T))
        for i in range(N):
            SEQSCORE[i, T-1] += transition_matrix[i, special1]
        C[T-1] = np.argmax(SEQSCORE[:, T-1])
        for i in range(T-2, -1, -1):
            C[i] = BACKPTR[int(C[i+1]), i]
        for i in range(T):
            g.write(tagset[int(C[i])])
            g.write(' ')
        g.write('\n')
