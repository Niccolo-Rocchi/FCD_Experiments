import pandas as pd
import numpy as np
import torch

import sys
sys.path.append('./notears-admm')
from notears_admm import utils
from notears_admm.linear_admm import notears_linear_admm
from notears_admm.postprocess import postprocess

# Set seed
utils.set_random_seed(42)

# Read input space
input_space = pd.read_csv('input_space.csv')
nclients = input_space['nclients'].loc[0]

# Read data
data = pd.read_csv('data.csv')
nnodes = data.shape[1]
ssize = int(data.shape[0]/float(nclients))

# Set parameters
lambda1 = 0.01 # default
# threshold = 0.3 # default

# Create tensor of data
input_data = data.loc[: nclients * ssize, :]
input_data = np.array(input_data).reshape(nclients, ssize, nnodes)

# Run algorithm
G_hat  = notears_linear_admm(input_data, lambda1=lambda1, verbose=True)
