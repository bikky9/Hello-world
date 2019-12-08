from copy import deepcopy
from itertools import cycle
from pprint import pprint as pprint
import sys
import argparse
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import random
import math



def RBFKernel(p1,p2,sigma=3):
	'''
	p1: tuple: 1st point
	p2: tuple: 2nd point
	Returns the value of RBF kernel
	'''
	# TODO [task3]
	# Your function must work for all sized tuples.
	value = np.exp(-(np.linalg.norm(np.subtract(p2,p1),axis=1))**2/(2*sigma**2))
	return value

def initializationrandom(data,C,seed=45):
	'''
	data: list of tuples: the list of data points
	C:int : number of cluster centroids
    seed:int : seed value for random value generator
	Returns a list of tuples,representing the cluster centroids and a list of list of tuples representing the cluster  
	'''
	centroidList =  []
	clusterLists = [[] for i in range(C)]
	# TODO [task3]:
	# Initialize the cluster centroids by sampling k unique datapoints from data and assigning a data point to a random cluster
	random.seed(seed)
	for i in data:
		clusterLists[random.randint(0,C-1)].append(i)
	for i in range(C):
		newcentroid = [0 for p in range(len(data[0]))]
		if(len(clusterLists[i])!=0):
			for j in range(0,len(clusterLists[i])):
				newcentroid = [newcentroid[k] + clusterLists[i][j][k] for k in range(len(newcentroid))]
			centroidList.append(tuple([float(x)/len(clusterLists[i]) for x in newcentroid]))
		else:
			centroidList.append(newcentroid)
	 
	assert len(centroidList) == C
	assert len(clusterLists) == C
	return centroidList,clusterLists

def firstTerm(p):
	'''
	p: a tuple for a  datapoint
	'''
	value = RBFKernel(p,[p])
	'''
	# TODO [task3]:
	# compute the first term in the summation of distance.
	'''
	return value

def secondTerm(data,pi_k):
	'''
	data : list of tuples: the list of data points
	pi_k : list of tuples: the list of data points in kth cluster
	'''
	value = 2*np.sum(RBFKernel(data,pi_k))
	'''
	# TODO [task3]:
	# compute the second term in the summation of distance.
	'''
	return value/len(pi_k)

def thirdTerm(pi_k):
	'''
	pi_k : list of tuples: the list of data points in kth cluster
	'''
	value = 0
	'''
	# TODO [task3]:
	# compute the third term in the summation of distance.
	'''
	for i in pi_k:
		value+=np.sum(RBFKernel(i,pi_k))
	return value/(len(pi_k)**2)

def hasconverged(prevclusterList,clusterList,C):
	'''
	prevclusterList : list of (list of tuples): the list of lists of  tuples of datapoints in a cluster in previous iteration
	clusterList: list of (list of tuples): the list of lists of tuples of datapoints in a cluster
	C: int : number of clusters
	'''
	'''
	# TODO [task3]:
	check if the cluster membership of the clusters has changed or not.If not,return True. 
	'''
	prevclusterList = [np.sort(prevclusterList[i]) for i in range(len(prevclusterList))]
	clusterList = [np.sort(clusterList[i]) for i in range(len(clusterList))]
	return np.array_equal(prevclusterList,clusterList)
	
def kernelkmeans(data,C,maxiter=10):
	'''
	data : list of tuples: the list of data points
	C: int : number of clusters
	'''
	centroidList,clusterLists = initializationrandom(data,C)
	'''
	# TODO [task3]:
	# iteratively modify the cluster centroids.
	# Stop only if convergence is reached, or if max iterations have been exhausted.
	# Save the results of each iteration in all_centroids.
	# Tip: use deepcopy() if you run into weirdness.
	'''


	for k in range(maxiter):
		newclusterLists = [[] for i in range(C)]
		newcentroidList = []
		gram = []
		for i in clusterLists:
			gram.append(thirdTerm(i))

		for i in data:
			minimumdistance = float('inf')
			minimumcentroid = 0
			for j in range(C):
				distance = firstTerm(i)-secondTerm(i,clusterLists[j])+gram[j]
				if(distance < minimumdistance):
					minimumdistance = distance
					minimumcentroid = j
			newclusterLists[minimumcentroid].append(i)

		for i in range(C):
			newcentroid = [0 for i in range(len(data[0]))]
			if(len(newclusterLists[i])!=0):
				for j in range(0,len(newclusterLists[i])):
					newcentroid = [newcentroid[k] + newclusterLists[i][j][k] for k in range(len(newcentroid))]
				newcentroidList.append(tuple([float(x)/len(newclusterLists[i]) for x in newcentroid]))
			else:
				newcentroidList.append(newcentroid)

		if(hasconverged(clusterLists,newclusterLists,C)):
			return newcentroidList,newclusterLists
		clusterLists = newclusterLists
		centroidList = newcentroidList

	return clusterLists,centroidList




def plot(clusterLists,centroidList,C):
	color = iter(cm.rainbow(np.linspace(0,1,C)))
	plt.figure("result")
	plt.clf()
	for i in range(C):
	    col = next(color)
	    memberCluster = np.asmatrix(clusterLists[i])
	    plt.scatter(np.ravel(memberCluster[:,0]),np.ravel(memberCluster[:,1]),marker=".",s =100,c = col)
	color = iter(cm.rainbow(np.linspace(0,1,C)))
	for i in range(C):
	    col = next(color)
	    plt.scatter(np.ravel(centroid[i][0]),np.ravel(centroid[i][1]),marker="*",s=400,c=col,edgecolors="black")
	plt.show()

filePath1 = "datasets/mouse.csv"
filePath2 = "datasets/3lines.csv"
mouse  = np.loadtxt(open(filePath1, "rb"), delimiter=",", skiprows=1)
lines3 = np.loadtxt(open(filePath2, "rb"), delimiter=",", skiprows=1)
clusterResult, centroid = kernelkmeans(mouse,C=3)
plot(clusterResult, centroid,C = 3)
clusterResult,centroid = kernelkmeans(lines3,C=3)
plot(clusterResult, centroid,C = 3)
#save the plots accordingly

