import numpy as np

class FullyConnectedLayer:
	def __init__(self, in_nodes, out_nodes, activation):
		# Method to initialize a Fully Connected Layer
		# Parameters
		# in_nodes - number of input nodes of this layer
		# out_nodes - number of output nodes of this layer
		self.in_nodes = in_nodes
		self.out_nodes = out_nodes
		self.activation = activation
		# Stores the outgoing summation of weights * feautres 
		self.data = None

		# Initializes the Weights and Biases using a Normal Distribution with Mean 0 and Standard Deviation 0.1
		self.weights = np.random.normal(0,0.1,(in_nodes, out_nodes))	
		self.biases = np.random.normal(0,0.1, (1, out_nodes))
		###############################################
		# NOTE: You must NOT change the above code but you can add extra variables if necessary 

	def forwardpass(self, X):
		# print('Forward FC ',self.weights.shape)
		# Input
		# activations : Activations from previous layer/input
		# Output
		# activations : Activations after one forward pass through this layer
		
		n = X.shape[0]  # batch size
		# INPUT activation matrix  		:[n X self.in_nodes]
		# OUTPUT activation matrix		:[n X self.out_nodes]

		###############################################
		# TASK 1 - YOUR CODE HERE
		if self.activation == 'relu':
			self.data = relu_of_X(X @ self.weights + self.biases)
		elif self.activation == 'softmax':
			self.data = softmax_of_X(X @ self.weights + self.biases)
		else:
			print("ERROR: Incorrect activation specified: " + self.activation)
			exit()

		return self.data
		###############################################
		
	def backwardpass(self, lr, activation_prev, delta):
		# Input
		# lr : learning rate of the neural network
		# activation_prev : Activations from previous layer
		# delta : del_Error/ del_activation_curr
		# Output
		# new_delta : del_Error/ del_activation_prev
		
		# Update self.weights and self.biases for this layer by backpropagation
		n = activation_prev.shape[0] # batch size

		###############################################
		# TASK 2 - YOUR CODE HERE
		if self.activation == 'relu':
			inp_delta = gradient_relu_of_X(self.data, delta)
		elif self.activation == 'softmax':
			inp_delta = gradient_softmax_of_X(self.data, delta)
		else:
			print("ERROR: Incorrect activation specified: " + self.activation)
			exit()
		new_delta = inp_delta @ self.weights . T
		self.weights = self.weights - lr * activation_prev . T @ inp_delta
		for i in range(n):
			self.biases = self.biases - lr * inp_delta[[i]]
		return new_delta
		###############################################

class ConvolutionLayer:
	def __init__(self, in_channels, filter_size, numfilters, stride, activation):
		# Method to initialize a Convolution Layer
		# Parameters
		# in_channels - list of 3 elements denoting size of input for convolution layer
		# filter_size - list of 2 elements denoting size of kernel weights for convolution layer
		# numfilters  - number of feature maps (denoting output depth)
		# stride	  - stride to used during convolution forward pass
		self.in_depth, self.in_row, self.in_col = in_channels
		self.filter_row, self.filter_col = filter_size
		self.stride = stride
		self.activation = activation
		self.out_depth = numfilters
		self.out_row = int((self.in_row - self.filter_row)/self.stride + 1)
		self.out_col = int((self.in_col - self.filter_col)/self.stride + 1)

		# Stores the outgoing summation of weights * feautres 
		self.data = None
		
		# Initializes the Weights and Biases using a Normal Distribution with Mean 0 and Standard Deviation 0.1
		self.weights = np.random.normal(0,0.1, (self.out_depth, self.in_depth, self.filter_row, self.filter_col))	
		self.biases = np.random.normal(0,0.1,self.out_depth)
		

	def forwardpass(self, X):
		# print('Forward CN ',self.weights.shape)
		# Input
		# X : Activations from previous layer/input
		# Output
		# activations : Activations after one forward pass through this layer
		n = X.shape[0]  # batch size
		# INPUT activation matrix  		:[n X self.in_depth X self.in_row X self.in_col]
		# OUTPUT activation matrix		:[n X self.out_depth X self.out_row X self.out_col]

		###############################################
		# TASK 1 - YOUR CODE HERE
		self.data = np.zeros((n, self.out_depth, self.out_row, self.out_col))
		for i in range(n):
			for z in range(self.out_depth):
				for x in range(0, self.out_row):
					for y in range(0, self.out_col):
						Z = X[i, :, x * self.stride:(x * self.stride + self.filter_row), y * self.stride:(y * self.stride + self.filter_col)]
						self.data[i, z, x, y] = sum(sum(sum(Z * self.weights[z]))) + self.biases[z]
		if self.activation == 'relu':
			return relu_of_X(self.data)
		elif self.activation == 'softmax':
			return softmax_of_X(self.data)
		else:
			print("ERROR: Incorrect activation specified: " + self.activation)
			exit()

		
		###############################################

	def backwardpass(self, lr, activation_prev, delta):
		# Input
		# lr : learning rate of the neural network
		# activation_prev : Activations from previous layer
		# delta : del_Error/ del_activation_curr
		# Output
		# new_delta : del_Error/ del_activation_prev
		
		# Update self.weights and self.biases for this layer by backpropagation
		n = activation_prev.shape[0] # batch size

		###############################################
		# TASK 2 - YOUR CODE HERE
		if self.activation == 'relu':
			delta = gradient_relu_of_X(self.data,delta)
		elif self.activation == 'softmax':
			delta = gradient_softmax_of_X(self.data,delta)
		else:
			print("ERROR: Incorrect activation specified: " + self.activation)
			exit()
		new_delta = np.zeros((n, self.in_depth, self.in_row, self.in_col))
		for i in range(n):
			for z in range(self.out_depth):
				for x in range(0, self.out_row):
					for y in range(0, self.out_col):
						new_delta[i, :, x * self.stride: (x * self.stride + self.filter_row), y * self.stride: (y * self.stride + self.filter_col)] += delta[i, z, x, y] * self.weights[z, :, :, :]
						self.weights[z] -= lr * delta[i, z, x, y] * activation_prev[i, :, x * self.stride:(x * self.stride + self.filter_row),  y * self.stride:(y * self.stride + self.filter_col)]
		for j in range(self.out_depth):
			self.biases[j] -= lr * sum(sum(sum(delta[:, j, :, :])))
		return new_delta
		###############################################
	
class AvgPoolingLayer:
	def __init__(self, in_channels, filter_size, stride):
		# Method to initialize a Convolution Layer
		# Parameters
		# in_channels - list of 3 elements denoting size of input for max_pooling layer
		# filter_size - list of 2 elements denoting size of kernel weights for convolution layer

		# NOTE: Here we assume filter_size = stride
		# And we will ensure self.filter_size[0] = self.filter_size[1]
		self.in_depth, self.in_row, self.in_col = in_channels
		self.filter_row, self.filter_col = filter_size
		self.stride = stride

		self.out_depth = self.in_depth
		self.out_row = int((self.in_row - self.filter_row)/self.stride + 1)
		self.out_col = int((self.in_col - self.filter_col)/self.stride + 1)

	def forwardpass(self, X):
		# print('Forward MP ')
		# Input
		# X : Activations from previous layer/input
		# Output
		# activations : Activations after one forward pass through this layer
		
		n = X.shape[0]  # batch size
		# INPUT activation matrix  		:[n X self.in_depth X self.in_row X self.in_col]
		# OUTPUT activation matrix		:[n X self.out_depth X self.out_row X self.out_col]

		###############################################
		# TASK 1 - YOUR CODE HERE
		raise NotImplementedError
		###############################################


	def backwardpass(self, alpha, activation_prev, delta):
		# Input
		# lr : learning rate of the neural network
		# activation_prev : Activations from previous layer
		# activations_curr : Activations of current layer
		# delta : del_Error/ del_activation_curr
		# Output
		# new_delta : del_Error/ del_activation_prev
		
		n = activation_prev.shape[0] # batch size

		###############################################
		# TASK 2 - YOUR CODE HERE
		raise NotImplementedError
		###############################################


# Helper layer to insert between convolution and fully connected layers
class FlattenLayer:
    def __init__(self):
        pass
    
    def forwardpass(self, X):
        self.in_batch, self.r, self.c, self.k = X.shape
        return X.reshape(self.in_batch, self.r * self.c * self.k)

    def backwardpass(self, lr, activation_prev, delta):
        return delta.reshape(self.in_batch, self.r, self.c, self.k)


# Function for the activation and its derivative
def relu_of_X(X):

	# Input
	# data : Output from current layer/input for Activation | shape: batchSize x self.out_nodes
	# Returns: Activations after one forward pass through this relu layer | shape: batchSize x self.out_nodes
	# This will only be called for layers with activation relu
	X[X < 0] = 0
	return X
	
def gradient_relu_of_X(X, delta):
	# Input
	# data : Output from next layer/input | shape: batchSize x self.out_nodes
	# delta : del_Error/ del_activation_curr | shape: batchSize x self.out_nodes
	# Returns: Current del_Error to pass to current layer in backward pass through relu layer | shape: batchSize x self.out_nodes
	# This will only be called for layers with activation relu amd during backwardpass
	X[X < 0] = 0
	X[X > 0] = 1
	return np.multiply(X,delta)
	# raise NotImplementedError
	
def softmax_of_X(X):
	# Input
	# data : Output from current layer/input for Activation | shape: batchSize x self.out_nodes
	# Returns: Activations after one forward pass through this softmax layer | shape: batchSize x self.out_nodes
	# This will only be called for layers with activation softmax
	exp = np.exp(X)
	denom = np.sum(exp,1).reshape(-1,1)
	return np.divide(exp,denom)
    # raise NotImplementedError
def gradient_softmax_of_X(X, delta):
	# Input
	# data : Output from next layer/input | shape: batchSize x self.out_nodes
	# delta : del_Error/ del_activation_curr | shape: batchSize x self.out_nodes
	# Returns: Current del_Error to pass to current layer in backward pass through softmax layer | shape: batchSize x self.out_nodes
	# This will only be called for layers with activation softmax amd during backwardpass
	# Hint: You might need to compute Jacobian first
	for i in range(X.shape[0]):
		Y = X[i,:].reshape(1,-1)
		Y = np.diagflat(Y) - Y . T @ Y
		X[i,:] = delta[i,:] @ Y
	return X
	
