import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg
import math
# def sigmoid(alpha,X,gramMatrix):
# 	'''returns sigmoid of W.T*phi
# 	'''
# 	return 1/(1+(1/(math.exp(phi.T @ w))))
def gaussian_kernel(x, y, sigma=1.0):
    return math.exp(-(np.linalg.norm(x-y))**2/(2*(sigma**2)))
def logistic_Kernel(X, Y, k, lr=0.01, max_iter = 100):
	''' TASK 1
	X 			= input feature matrix [N X D]
	Y 			= output values [N X 1]
	lr 			= learning rate
	max_iter 	= maximum number of iterations of gradient descent to run
	Return the trained weight vector [D X 1] after performing gradient descent
	'''
	X_train = X[0:900].reshape((900,2))
	Y_train = Y[0:900].reshape((900,1))
	X_test = X[900:1000].reshape((100,2))
	Y_test = Y[900:1000].reshape((100,1))
	N = X_train.shape[0]
	alpha = np.zeros((N,1))
	m = X_train.shape[0]
	expected = np.zeros((N,1))
	num_iter = 0
	gramMatrix = np.zeros((m,m))
	for i in range(0,m):
		for j in range(0,m):
			gramMatrix[i,j] = k(X_train[i],X_train[j])
	expected = (1/(1+np.exp(-alpha . T @ gramMatrix))).T
	while(num_iter<max_iter):
		alpha = alpha + lr*((1/N)*(gramMatrix.T @ (Y_train-expected)))
		num_iter+=1
		expected = (1/(1+np.exp(-alpha . T @ gramMatrix))).T
	n = X_test.shape[0]
	gramMatrix2 = np.zeros((m,n))
	for i in range(0,m):
		for j in range(0,n):
			gramMatrix2[i,j] = k(X_train[i],X_test[j])
	y = (1/(1+np.exp(-alpha . T @ gramMatrix2))).T
	y[y > 0.5] = 1
	y[y <= 0.5] = 0
	# print(str(int(np.sum(abs(Y_test-y))))+" mistakes out of 100")
	return np.sum(abs(Y_test-y))


if __name__ == "__main__":
	l = np.loadtxt("dataset1.txt")
	X = l[:,:2]
	Y = l[:,2]
	x = [0.5,1,2,3,4,5,6]
	y=[]
	y.append(logistic_Kernel(X,Y,lambda x1, x2: gaussian_kernel(x1, x2, sigma=0.5)))
	y.append(logistic_Kernel(X,Y,lambda x1, x2: gaussian_kernel(x1, x2, sigma=1)))
	y.append(logistic_Kernel(X,Y,lambda x1, x2: gaussian_kernel(x1, x2, sigma=2)))
	y.append(logistic_Kernel(X,Y,lambda x1, x2: gaussian_kernel(x1, x2, sigma=3)))
	y.append(logistic_Kernel(X,Y,lambda x1, x2: gaussian_kernel(x1, x2, sigma=4)))
	y.append(logistic_Kernel(X,Y,lambda x1, x2: gaussian_kernel(x1, x2, sigma=5)))
	y.append(logistic_Kernel(X,Y,lambda x1, x2: gaussian_kernel(x1, x2, sigma=6)))
	plt.plot(x,y)
	plt.show()