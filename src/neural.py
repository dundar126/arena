import numpy as np


class NeuralNetwork(object):
	def __init__(self):
		# Define layer sizes and starting weights
		self.input_layer_size = 2
		self.hidden_layer_size = 3
		self.output_layer_size = 1

		self.weight1 = np.random.randn(self.input_layer_size, self.hidden_layer_size)
		self.weight2 = np.random.randn(self.hidden_layer_size, self.output_layer_size)

	# Move forward through network
	def forward(self, inp):
		self.combined_weights = np.dot(inp, self.weight1)
		self.weight_activity = self.sigmoid(self.combined_weights)
		self.output_activity = np.dot(self.weight_activity, self.weight2)
		predicted_output = self.sigmoid(self.output_activity)
		return predicted_output

	# Sigmoid activation function
	def sigmoid(self, inp):
		return 1 / (1 + np.exp(-inp))

	def delta_sigmoid(self, inp):
		return np.exp(-inp) / ((1 + np.exp(-inp)) ** 2)

	# Returns cost for a given input versus a known output
	def cost(self, inp, output):
		return 0.5 * sum((output - self.forward(inp)) ** 2)

	# Used to determine how to reduce the cost by calculating the gradient of cost
	def delta_cost(self, inp, output):
		self.predicted_output = self.forward(inp)

		delta_output_activity = self.delta_sigmoid(self.output_activity)
		delta2 = np.multiply(-(output-self.predicted_output), delta_output_activity)
		dcost_dweight2 = np.dot(self.weight_activity.T, delta2)
		delta_combined_weights_activity = self.delta_sigmoid(self.combined_weights)
		delta1 = np.dot(delta2, self.weight2.T) * delta_combined_weights_activity
		dcost_dweight1 = np.dot(inp.T, delta1)

		return dcost_dweight1, dcost_dweight2
