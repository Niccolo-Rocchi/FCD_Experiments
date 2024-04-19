# Import packages
import pandas as pd
import numpy as np
import torch
import sys
import os

## Import FCD code:
# 1. notears-admm
sys.path.append('./code/notears-admm')
from notears_admm import utils
from notears_admm.linear_admm import notears_linear_admm
from notears_admm.postprocess import postprocess
# 2. ... work in progress ...

# Set seed
utils.set_random_seed(42)
# Read input space
input_space = pd.read_csv('input_space.csv')
# Read data sets
data_path = './datasets'
data_list = os.listdir(data_path)

# For each data set ...
for d in data_list:
    # ... read it,
    data = pd.read_csv(f'{data_path}/{d}')
    # extract its ID,
    ID = d[:d.find('.csv')]
    # and set hypercube parameters based on its ID
    nclients = input_space[input_space['ID'] == ID].at[0,'nclients']
    nnodes = data.shape[1]
    ssize = int(data.shape[0]/float(nclients))
    
    ## Perform FCD
    
    # 1. notears-admm
    # Create tensor of data
    input_data = data.loc[: nclients * ssize, :]
    input_data = np.array(input_data).reshape(nclients, ssize, nnodes)
    # Run algorithm
    G_hat  = notears_linear_admm(input_data, lambda1=0.01, threshold=0.3, verbose=False) # Default settings

    # 2. ... work in progress ...
