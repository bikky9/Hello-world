import numpy as np
from utils import *
from numpy import linalg as LA
import time

def preprocess(X, Y):
	''' TASK 0
	X = input feature matrix [N X D] 
	Y = output values [N X 1]
	Convert data X, Y obtained from read_data() to a usable format by gradient descent function
	Return the processed X, Y that can be directly passed to grad_descent function
	NOTE: X has first column denote index of data point. Ignore that column 
	and add constant 1 instead (for bias part of feature set)

	Note : Remember to normalize input data before processing further
	'''
	# for i in range(1,X.shape[1]):
	# 	print(X.shape[1])
	# 	if(isinstance(X[0][i],str)):
	# 		labels = list(set(X[:,i]))
	# 		x=one_hot_encode(X[:,i], labels)
	# 		X=np.delete(X,i,axis=1)
	# 		num_of_columns2 = x.shape[1]
	# 		for j in range(0,num_of_columns2):
	# 			X=np.insert(X, i, x[:,j], axis=1)
	# 			i=i+1
	# print(X)
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
		
	return ans_X.astype('float'),Y.astype('float')
	pass

def ordinary_least_squares(X, Y, lr=0.01):
	''' TASK 2

	X = input feature matrix [N X D]
	Y = output values [N X 1]
	Return the weight vector W, [D X 1] 
	'''
	X = X.astype('float')
	Y = Y.astype('float')
	W=np.ones((X.shape[1],1)).astype('float')
	epsilon=1e-4
	gradient = -2.0 * (X.T @ (Y - (X @ W)))
	# for i in range(1000):
	# 	W=W-(lr/X.shape[0])*gradient
	# 	gradient = -2.0 * (X.T @ (Y - (X @ W)))
	# 	print((lr/X.shape[0])*LA.norm(gradient))
	current_error=2*sse(X,Y,W)
	next_error=sse(X,Y,W)
	while((abs(-next_error+current_error)/next_error)>epsilon):
		current_error=next_error
		W=W-(lr/X.shape[0])*gradient
		gradient = -2.0 * (X.T @ (Y - (X @ W)))
		next_error=sse(X,Y,W)
	return W
	pass

def grad_ridge(W, X, Y, _lambda):
	'''  TASK 3
	W = weight vector [D X 1]
	X = input feature matrix [N X D]
	Y = output values [N X 1]
	_lambda = scalar parameter lambda
	Return the gradient of ridge objective function (||Y - X W||^2  + lambda*||w||^2 )
	'''
	return -2.0 * (X.T @ (Y - (X @ W))) + 2.0 * _lambda * W
	pass

def ridge_grad_descent(X, Y, _lambda, max_iter=30000, lr=0.005, epsilon = 1e-4):
	''' TASK 3 - PART A
	X 			= input feature matrix [N X D]
	Y 			= output values [N X 1]
	_lambda 	= scalar parameter lambda
	max_iter 	= maximum number of iterations of gradient descent to run in case of no convergence
	lr 			= learning rate
	epsilon 	= gradient norm below which we can say that the algorithm has converged 
	Return the trained weight vector [D X 1] after performing gradient descent using Ridge Loss Function 
	NOTE: You may precompure some values to make computation faster
	'''
	X = X.astype('float')
	Y = Y.astype('float')
	W=np.ones((X.shape[1],1)).astype('float')
	gradient = grad_ridge(W, X, Y, _lambda)
	num_iter=1
	# for i in range(1000):
	# 	W=W-(lr/X.shape[0])*gradient
	# 	gradient = -2.0 * (X.T @ (Y - (X @ W)))
		#print((lr/X.shape[0])*LA.norm(gradient))
	while(LA.norm(gradient)>epsilon and num_iter<max_iter):
		W=W-(lr/X.shape[0])*gradient
		gradient = grad_ridge(W, X, Y, _lambda)
		num_iter+=1
	return W


def coord_grad_descent(X, Y, _lambda, max_iter=31000,lr=0.00002872):
	''' TASK 4
	X 			= input feature matrix [N X D]
	Y 			= output values [N X 1]
	_lambda 	= scalar parameter lambda
	max_iter 	= maximum number of iterations of gradient descent to run in case of no convergence
	Return the trained weight vector [D X 1] after performing gradient descent using Lasso Loss Function 
	'''
	X = X.astype('float')
	Y = Y.astype('float')
	W=np.ones((X.shape[1],1)).astype('float')
	epsilon=1e-4
	num_iter=1
	k = 38000
	gradient = -2.0 * (X.T @ (Y - (X @ W)))
	while(num_iter<max_iter):
		W1=W-(lr)*gradient
		if lr*LA.norm(gradient) < epsilon:
			break
		for i in range(len(W)):
			if(W1[i,0]>_lambda/k):
				W[i,0]=W1[i,0]-_lambda/k
			elif W1[i,0]<-_lambda/k:
				W[i,0]=W1[i,0]+_lambda/k
			else:
				W[i,0]=0
		gradient = -2.0 * (X.T @ (Y - (X @ W)))
		num_iter+=1
		# print(num_iter,sum(W == 0))
	return W

# def ista(X,Y_lambda,max_iter=1000):
# 	W=np.ones((X.shape[1],1))
# 	epsilon=1e-4
# 	lr=0.000028
# 	num_iter=1
# 	gradient = -2.0 * (X.T @ (Y - (X @ W)))
# 	while(LA.norm(gradient)>epsilon and num_iter<max_iter):
# 		W=W-(lr)*gradient
# 		for i in range(len(W)):
# 			if(W[i,0]>_lambda/2):
# 				W[i,0]=W[i,0]-_lambda/2
# 			elif W[i,0]<-_lambda/2:
# 				W[i,0]=W[i,0]+_lambda/2
# 			else:
# 				W[i,0]=0
# 		gradient = -2.0 * (X.T @ (Y - (X @ W)))
# 		num_iter+=1
# 		print(num_iter,LA.norm(gradient))
# 	return W
# 	pass

if __name__ == "__main__":
	X, Y = read_data("./dataset/train.csv")
	X, Y = preprocess(X, Y)
	trainX, trainY, testX, testY = separate_data(X, Y)


	# Uncomment the following lines to get variation of norm vs lambda for ridge gradient descent
	# lambdas = np.arange(0,101,10)
	# norms=[]
	# for i in lambdas:
	# 	norms.append((LA.norm(ridge_grad_descent(trainX,trainY,i)))**2)
	# plot_norm2(lambdas, norms)




	# Uncomment the following lines to get features vs their corresponding weights in rigde gradient descent
	# features = np.arange(trainX.shape[1])
	# W=ridge_grad_descent(trainX,trainY,100)
	# weights = []
	# weights_with_index = []
	# for i in range(X.shape[1]):
	# 	weights.append(abs(W[i,0]))
	# 	weights_with_index.append([abs(W[i,0]),i])
	# weights_with_index.sort()
	# weights_with_index.reverse()
	# for i in range(5):
	# 	print(weights_with_index[i][1])
	#  # 87 211 158 66 221
	# plot_norm2(features,weights)




	# Uncomment the following lines to get features vs their corresponding weights in coordinate gradient descent or lasso regression
	# features = np.arange(trainX.shape[1])
	# W=coord_grad_descent(trainX,trainY,10000)
	# weights = []
	# weights_with_index = []
	# for i in range(X.shape[1]):
	# 	weights.append(abs(W[i,0]))
	# 	weights_with_index.append([abs(W[i,0]),i])
	# weights_with_index.sort()
	# weights_with_index.reverse()
	# for i in range(5):
	# 	print(weights_with_index[i][1])
	# # 73 275 256 97 40
	# plot_norm2(features,weights)



	# Uncomment the following lines to plot Learing rate vs execution time and observed error for ridge-regression
	lr_values = np.arange(0.0045,0.0055,0.0001)
	observed_errors =[]
	execution_times = []
	for i in lr_values:
		init = time.time()
		W=ridge_grad_descent(trainX,trainY,100,50000,i)
		end = time.time()-init
		execution_times.append(end)
		observed_errors.append(LA.norm(trainY - trainX @ W))
	plot_norm2(lr_values,execution_times)
	plot_norm2(lr_values,observed_errors)
	
	
	


	# Uncomment the following lines to plot Learing rate vs execution time and observed error for ridge-regression
	lr_values = np.arange(0.00002865,0.00002874,0.00000001)
	observed_errors =[]
	execution_times = []
	for i in lr_values:
		init = time.time()
		W=coord_grad_descent(trainX,trainY,10000,40000,i)
		end = time.time()-init
		execution_times.append(end)
		observed_errors.append(LA.norm(trainY - trainX @ W))
	plot_norm2(lr_values,execution_times)
	plot_norm2(lr_values,observed_errors)