import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
random.seed(42)


def visualize(points):
	''' Write the code here '''
	A = np.zeros((0,2))
	B = np.zeros((0,2))
	for i in points:
		if i[0][0] == 'A':
			b = np.zeros((1,2))
			b[0][0] = i[1]
			b[0][1] = i[2]
			A = np.append(A,b,axis=0)
		else:
			b = np.zeros((1,2))
			b[0][0] = i[1]
			b[0][1] = i[2]
			B = np.append(B,b,axis=0)
	hull = ConvexHull(A)
	plt.plot(A[:,0], A[:,1], 'o')
	for simplex in hull.simplices:
		plt.plot(A[simplex, 0], A[simplex, 1], 'k-')
	hull = ConvexHull(B)
	plt.plot(B[:,0], B[:,1], 'o')
	for simplex in hull.simplices:
		plt.plot(B[simplex, 0], B[simplex, 1], 'k-')
	plt.show()
	

def grade():
	A,B = [],[]
	for i in range(3):
		A.append('A'+str(i))
		B.append('B'+str(i))

	points  = [3,5,7]
	allpoints = []
	till = 3
	for i in range(till):
		coords = np.array([(A[i], random.random()*(100.0/points[i]), random.random()*(100.0)) for _ in range(points[i])])
		coords1 = np.array([(B[i], 25 + random.random()*(100.0/points[i]), random.random()*(100.0)) for _ in range(points[i])]) 
		allpoints.extend(coords)
		allpoints.extend(coords1)

	random.shuffle(allpoints)
	visualize(allpoints)
	return allpoints

grade()
