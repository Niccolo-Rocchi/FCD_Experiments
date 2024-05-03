# Import packages
import pandas as pd
import random
import numpy as np
import time
import cdt
import sys
import os
import unittest

# Suppress all warnings
import warnings
warnings.filterwarnings("ignore")

## Import FCD code:
# 1. notears-admm
sys.path.append('./code/notears-admm')
from notears_admm import utils
from notears_admm.linear_admm import notears_linear_admm
from notears_admm.postprocess import postprocess
# 2. FedC2SL (FedPC)
sys.path.append('./code/FedC2SL/FedC2SL')
from alg.FedPC import pc
# 3. ... work in progress ...

# Set seed
seed = 42
rd = random.Random()
rd.seed(seed)
utils.set_random_seed(seed)

# Read input space
input_space = pd.read_csv('input_space.csv')
# Read IDs and cast to list
ids = pd.read_csv('data_ids.csv')
ids = list(ids['ids'])
# Read data sets path
data_path = './datasets'

# Initialize metrics
metrics = list()

# For each ID
for id in ids:
    # Read data set
    data = pd.read_csv(f'{data_path}/{id}.csv')
    # Set hypercube parameters based on ID
    nclients = input_space[input_space['ID'] == id].iloc[0].at['nclients']
    nnodes = input_space[input_space['ID'] == id].iloc[0].at['nnodes']
    ssize = input_space[input_space['ID'] == id].iloc[0].at['ssize']
    # Perform tests on consistency of data set
    assert(nnodes == data.shape[1])
    assert(ssize == data.shape[0])
    # Record hypercube parameters
    record = {'nnodes':nnodes, 'nclient':nclients, 'ssize':ssize}
    # Cast data to numpy array
    data = np.array(data)[:ssize - ssize%nclients,:]
    # Read true graph and cast to numpy array
    G_true = pd.read_csv(f'./dags/{id}.csv')
    G_true = np.array(G_true)[:,1:]
    
    ### Perform FCD
    
    ## 1. notears-admm
    # Create input data
    input_data = data.reshape(nclients, ssize//nclients, nnodes)
    # Run algorithm
    start = time.time()
    G_pred  = notears_linear_admm(input_data, verbose=False) # Default settings
    # Postprocess output (package function)
    G_pred = postprocess(G_pred, threshold=0.3) # Default settings
    end = time.time()
    # Binarize output
    G_pred[np.abs(G_pred) > 0.5] = 1

    ## 1.1. notears-admm metrics
    metric = record.copy()
    metric['alg'] = "notears-admm"
    # Compute ``Structural Hamming Distance'' (SHD)
    shd = cdt.metrics.SHD(G_true, G_pred)
    metric['shd'] = shd
    # Compute ``Area under the precision recall curve''' (AUC)
    auc = cdt.metrics.precision_recall(G_true, G_pred)[0]
    metric['auc'] = auc
    # Compute time
    metric['time(s)'] = end - start
    ## Return metrics
    metrics.append(metric)

    ## 2. FedC2SL (FedPC)
    # Create input data
    input_data = data.copy()
    # Run algorithm
    start = time.time()
    G_pred = pc(input_data, indep_test='fed_cit', client_num=nclients, show_progress=False) # Default settings
    end = time.time()
    # Get the adjacency matrix (`causal-learn` function)
    G_pred = G_pred.G.graph

    ## 2.1. FedC2SL (FedPC) metrics
    metric = record.copy()
    metric['alg'] = "FedC2SL(FedPC)"
    # Compute ``Structural Hamming Distance'' (SHD)
    shd = cdt.metrics.SHD(G_true, G_pred)
    metric['shd'] = shd
    # Compute ``Area under the precision recall curve''' (AUC)
    auc = cdt.metrics.precision_recall(G_true, G_pred)[0]
    metric['auc'] = auc
    # Compute time
    metric['time(s)'] = end - start
    ## Return metrics
    metrics.append(metric)
    
    ## 3. ... work in progress ...

# Create metrics folder, or empty it
results_path = 'results'
try:
    os.mkdir(results_path)
except:
    for filename in os.listdir(results_path):
      os.unlink(os.path.join(results_path, filename))
      
# Write metrics
metrics = pd.DataFrame.from_records(metrics)
metrics.to_csv(f'{results_path}/metrics.csv')

### Unit tests
class Test(unittest.TestCase):

    # Assert input space is not empty
    def test_notempty(self):    
        self.assertTrue(input_space.shape[0] != 0)
        self.assertTrue(input_space.shape[1] != 0)

    # Results folder must exist and metrics are unique
    def test_folder(self):
        self.assertTrue(os.path.exists(results_path))
        self.assertTrue(len(os.listdir(results_path)) == 1)

    # Metric shape must be consistent
    def test_size(self):
        data_list = list(os.listdir(data_path))
        metrics = pd.read_csv(f'{results_path}/metrics.csv')
        self.assertTrue(metrics.shape[0] != 0)
        self.assertTrue(metrics.shape[1] != 0)
        self.assertEqual(metrics.shape[0]/(len(np.unique(metrics['alg']))), len(data_list))
        self.assertEqual(input_space.shape[0], len(data_list))

    # Test metrics values
    def test_metric(self):
        metrics = pd.read_csv(f'{results_path}/metrics.csv')
        self.assertEqual(metrics['shd'].dtype, float)
        self.assertEqual(metrics['auc'].dtype, float)
        self.assertEqual(metrics['time(s)'].dtype, float)
        self.assertEqual(sum(metrics['shd'] < 0), 0)
        self.assertEqual(sum(metrics['auc'] < 0), 0)
        self.assertEqual(sum(metrics['auc'] > 1), 0)
        self.assertEqual(sum(metrics['time(s)'] < 0), 0)
        
