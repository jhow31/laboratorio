import numpy as np


def deepln(a,b,c):
	print("Enter the two values for input layers")

	print('a = ')
	a = int(input())
# 2
	print('b = ')
	b = int(input())

	print('c= ')
	c = int(input())


	weights = {
		'node_0': np.array([-1, 1, 1]),
		'node_1': np.array([-2, 1, 2]),
		'node_2': np.array([[-3, 1, 3]]),
		'output_node': np.array([-1, 1])
	}

	input_data = np.array([a, b, c])

def relu(input):
    # Rectified Linear Activation
	output = max(input, 0)
	return(output)
	node_0_input = (input_data * weights['node_0']).sum()
	node_0_output = relu(node_0_input)

	node_1_input = (input_data * weights['node_1']).sum()
	node_1_output = relu(node_1_input)

	node_2_input = (input_data * weights['node_2']).sum()
	node_2_output = relu(node_2_input)

	hidden_layer_outputs = np.array([node_0_output, node_1_output])

	model_output = (hidden_layer_outputs * weights['output_node']).sum()

	print(model_output)
	print(hidden_layer_outputs)
	print(node_0_output)
	print(node_1_output)
	print(node_2_output)
