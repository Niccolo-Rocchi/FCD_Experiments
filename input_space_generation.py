import pandas as pd

# Number of nodes
nnodes = [5]

# Number of clients
nclients = 10

# Sample size
ssize = 1000

# Input space generation
input_space = pd.DataFrame({'nnodes':nnodes, 'nclients':nclients, 'ssize':ssize})

# Save input space
input_space.to_csv('input_space.csv')
