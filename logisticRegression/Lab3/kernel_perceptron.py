import numpy as np
from numpy import linalg
def linear_kernel(x1, x2):
	return np.dot(x1,x2)

def polynomial_kernel(x, y, degree=3):
    return (1+np.dot(x,y))**degree

def gaussian_kernel(x, y, sigma=4.0):
    return np.exp(-(np.linalg.norm(x-y))**2/(2*(sigma**2)))

class KernelPerceptron(object):

    def __init__(self, kernel=linear_kernel, iterations=1):
        self.kernel = kernel
        self.iterations = iterations
        self.alpha = None

    def fit(self, X, y):
        ''' find the alpha values here'''
        m = X.shape[0]
        self.alpha = np.zeros(m,dtype=np.float64)
        gramMatrix = np.zeros((m,m))
        for i in range(0,m):
            for j in range(0,m):
                gramMatrix[i,j] = self.kernel(X[i],X[j])
        for j in range(self.iterations):
            for i in range(0,m):
                if np.sign(np.sum(self.alpha * y * gramMatrix[:,i]))!=y[i]:
                    self.alpha[i]+=1.0
        boolean = self.alpha > 0
        self.alpha = self.alpha[boolean]
        self.test = X[boolean]
        self.value = y[boolean]

    def project(self, X):
        '''return projected values from alpha and corresponding support vectors'''
        m = X.shape[0]
        n = self.test.shape[0]
        projectedValues = np.zeros(m)
        for i in range(0,m):
            total = 0
            for j in range(n):
                total+=self.alpha[j] * self.value[j] * self.kernel(X[i],self.test[j])
            projectedValues[i]=total
        return projectedValues

    def predict(self, X):
        X = np.atleast_2d(X)
        return np.sign(self.project(X))
