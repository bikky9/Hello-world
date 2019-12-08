import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_3D(x, y, z):
	fig = plt.figure()
	ax = Axes3D(fig)
	ax.scatter(xs=x, ys=y, zs=z, zdir='z')
	plt.show()

def plot_2D(x, y):
	plt.plot(x, y, 'o')
	plt.show()

def plot_alongside_data(X, Y, f):
	if X.shape[1] == 1:
		# 2D plot
		min_ranges = [min(X[:, i]) for i in range(X.shape[1])]
		max_ranges = [max(X[:, i]) for i in range(X.shape[1])]
		n_points = X.shape[0]
		X_test = [np.linspace(mi, ma, n_points) for mi, ma in zip(min_ranges, max_ranges)]
		X_test = np.stack(X_test).T
		Y_test = f(X_test)
		plt.plot(X, Y, 'o')
		plt.plot(X_test, Y_test)
		plt.show()
	elif X.shape[1] == 2:
		# 3D plot
		min_ranges = [min(X[:, i]) for i in range(X.shape[1])]
		max_ranges = [max(X[:, i]) for i in range(X.shape[1])]
		P = [np.linspace(mi, ma, 20) for mi, ma in zip(min_ranges, max_ranges)]
		X_test = np.transpose([np.tile(P[0], len(P[1])), np.repeat(P[1], len(P[0]))])
		Y_test = f(X_test)
		fig = plt.figure()
		ax = Axes3D(fig)
		ax.scatter(xs=X[:,0], ys=X[:,1], zs=Y, zdir='z',c='orange')
		X, Y = np.meshgrid(P[0], P[1])
		Z = Y_test.reshape(len(P[0]), len(P[1]))
		surf = ax.plot_surface(X, Y, Z)
		plt.show()

def read_data(path):
	with open(path, 'r') as f:
		lines = f.readlines()
		lines = [list(map(lambda s: float(s.strip()), x.split(','))) for x in lines]
		lines = np.asarray(lines)
		Y = lines[:, -1:]
		X = lines[:, :-1]
	return X, Y

def kernel_ridge_regression(K, X, Y, lmbda=0.0):
	"""
	K : accepts two inputs of dimensionality D each
	X : [N x D]
	Y : [N x 1]
	"""
	## YOUR CODE BELOW
	N = X.shape[0]
	D = X.shape[1]
	gramMatrix = np.zeros((N,N))
	for i in range(0,N):
		for j in range(0,N):
			gramMatrix[i,j] = K(X[i],X[j])
	alpha = np.linalg.inv(gramMatrix + lmbda*np.identity(N)) @ Y
	def F(X_test):
		m = X_test.shape[0]
		Y_test = np.zeros((m,1))
		for j in range(m):
			s=0
			for i in range(N):
				s+=alpha[i,0]*K(X_test[j],X[i])
			Y_test[j,0] = s
		return Y_test
	return F
def gaussian_kernel(x_i, x_j, sigma=1.0):
	## YOUR CODE BELOW
	return np.exp(-(np.linalg.norm(x_i-x_j))**2/(2*(sigma**2)))

def my_kernel(x_i, x_j):
	## YOUR CODE BELOW
	# return (1+np.dot(x_i,x_j))**3
	# return  np.dot(x_i,x_j)
	# return np.exp(-(np.linalg.norm(x_i-x_j))**2/(2*(100**2)))
	return ((1+np.dot(x_i,x_j))**3)*np.exp(-(np.linalg.norm(x_i-x_j))**2/(2*(1**2)))
	pass

if __name__ == '__main__':
	X, Y = read_data('problem4_1.csv')
	F = kernel_ridge_regression(lambda x1, x2: gaussian_kernel(x1, x2, sigma=10), X, Y, lmbda=0.01)
	plot_alongside_data(X, Y, F)

	X, Y = read_data('problem4_2.csv')
	F = kernel_ridge_regression(my_kernel, X, Y, lmbda=0.01)
	plot_alongside_data(X, Y, F)