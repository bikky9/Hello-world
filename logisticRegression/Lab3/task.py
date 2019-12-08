import numpy as np
import math
from utils import *

def preprocess(X, Y):
	''' TASK 1
	X = input feature matrix [N X D] 
	Y = output values [N X 1]
	Convert data X, Y obtained from read_data() to a usable format by gradient descent function
	Return the processed X, Y that can be directly passed to grad_descent function
	NOTE: X has first column denote index of data point. Ignore that column 
	and add constant 1 instead (for bias part of feature set)
	'''
	ans_X=np.ones((X.shape[0],1))
	for i in range(1,X.shape[1]):
		if(isinstance(X[0][i],str)):
			labels = list(set(X[:,i]))
			x=one_hot_encode(X[:,i], labels)
			num_of_columns2 = x.shape[1]
			for j in range(0,num_of_columns2):
				ans_X=np.insert(ans_X,ans_X.shape[1],x[:,j],axis=1)
		else:
			ans_X=np.insert(ans_X,ans_X.shape[1],(X[:,i]-np.mean(X[:,i]))/np.std(X[:,i]),axis=1)
	for i in range(Y.shape[0]):
		if(Y[i,0]=='yes'):
			Y[i,0] = 1
		else:
		 Y[i,0] = 0
	return ans_X.astype('float'),Y.astype('float')

def sigmoid(phi,w):
	'''returns sigmoid of W.T*phi
	'''
	return 1/(1+(1/(math.exp(phi.T @ w))))
def logistic_train(X, Y, lr=0.1, max_iter = 500):
	''' TASK 1
	X 			= input feature matrix [N X D]
	Y 			= output values [N X 1]
	lr 			= learning rate
	max_iter 	= maximum number of iterations of gradient descent to run
	Return the trained weight vector [D X 1] after performing gradient descent
	'''
	N = X.shape[0]
	D = X.shape[1]
	w = np.zeros((D,1))
	vfunc = np.vectorize(sigmoid,signature='(n),(n)->()')
	expected = np.transpose(vfunc(X,w.T))
	expected = np.reshape(expected,(N,1))
	num_iter = 0
	while((not np.array_equal(np.sign(expected), Y)) and num_iter<max_iter):
		w = w + lr*((1/N)*((Y-expected).T @ X).T)
		num_iter+=1
		expected = np.transpose(vfunc(X,w.T))
		expected = np.reshape(expected,(N,1))
	return w
def logistic_predict(X, Weights):
	''' TASK 1
	X 			= input feature matrix [N X D]
	Weights		= weight vector
	Return the predictions as [N X 1] vector
	'''
	vfunc = np.vectorize(sigmoid,signature='(n),(n)->()')
	expected = np.transpose(vfunc(X,Weights.T))
	expected = np.reshape(expected,(X.shape[0],1))
	i = expected > 0.5
	expected[i] = 1
	j = expected <=0.5
	expected[j] = 0

	return expected
