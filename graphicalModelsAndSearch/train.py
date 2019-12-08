import argparse
import sys

import numpy as np
np.set_printoptions(threshold=sys.maxsize)


def split(word):
    for i in range(len(word)):
        if(word[i]=="_"):
            return word[0:i], word[i+1:]

def parse(train_file):
    ''' '''
    f = open(train_file,"r")
    wordlist = []
    taglist = []
    for line in f:
        wordlist.append('<s>')
        taglist.append('<s>')
        for i in line.split():
            word,tag = split(i)
            wordlist.append(word)
            taglist.append(tag)
        wordlist.append('</s>')
        taglist.append('</s>')
    return wordlist, taglist

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--train-file", help = "Training file name")
    parser.add_argument("-m","--model", help = "model file name")
    args = parser.parse_args()
    
    lbd = 1e-6
    wordlist, taglist = parse(args.train_file)
    tagset = set(taglist)
    tagset = list(tagset)
    N = len(tagset)
    transition_matrix = np.zeros((N,N))
    for k in range(1,len(taglist)):
        j = tagset.index(taglist[k])
        i = tagset.index(taglist[k-1])
        transition_matrix[i,j] += 1
    transition_matrix[transition_matrix == 0] = 1/1e8
    for i in range(N):
        transition_matrix[i,:] /= np.sum(transition_matrix, axis = 1)[i]
    transition_matrix = np.log(transition_matrix)


    wordset = set(wordlist)
    wordset = list(wordset)
    emission_matrix = np.zeros((len(wordset),N))
    for k in range(len(wordlist)):
        i = wordset.index(wordlist[k])
        j = tagset.index(taglist[k])
        emission_matrix[i,j] += 1
    emission_matrix = emission_matrix * (1-lbd) + lbd*1e-10
    emission_matrix = np.divide(emission_matrix, np.sum(emission_matrix, axis = 0))
    emission_matrix = np.log(emission_matrix)

    emission_dict = {}
    for i in range(len(wordset)):
        emission_dict[wordset[i]] = emission_matrix[i,:].tolist()

    f = open(args.model,'w')
    l = {}
    l["tagset"] = tagset
    l["transition_matrix"] = transition_matrix.tolist()
    l["emission_dict"] = emission_dict 
    f.write(str(l))
