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
# 2. ... work in progress ...

# Set seed
seed = 42
rd = random.Random()
rd.seed(seed)
utils.set_random_seed(seed)

# Read input space
input_space = pd.read_csv('input_space.csv')
# Read data sets
data_path = './datasets'
data_list = os.listdir(data_path)

# Initialize metrics
metrics = list()

# For each data set ...
for d in data_list:
    # ... read it,
    data = pd.read_csv(f'{data_path}/{d}')
    # drop row index,
    # data = data.iloc[:, 1:]
    # extract its ID,
    ID = d[:d.find('.csv')]
    # set hypercube parameters based on its ID,
    nclients = input_space[input_space['ID'] == ID].iloc[0].at['nclients']
    nnodes = data.shape[1]
    ssize = data.shape[0]
    # and record hypercube parameters
    record = {'nnodes':nnodes, 'nclient':nclients, 'ssize':ssize}
    
    ### Perform FCD
    
    ## 1. notears-admm
    # Create tensor of data
    data = np.array(data)[:ssize - ssize%nclients,:]
    input_data = data.reshape(nclients, ssize//nclients, nnodes)
    # Run algorithm
    start = time.time()
    G_pred  = notears_linear_admm(input_data, verbose=False) # Default settings
    # Postprocess output
    G_pred = postprocess(G_pred, threshold=0.3) # Default settings
    end = time.time()
    # Binarize output
    G_pred[np.abs(G_pred) > 0.5] = 1

    # 2. ... work in progress ...

    ### Compute metrics
    
    ## 1. notears-admm
    metric = record.copy()
    metric['alg'] = "notears-admm"
    # Read true graph
    G_true = pd.read_csv(f'./dags/{ID}.csv')
    # Cast graphs to adjacency matrices
    G_pred = np.array(G_pred)
    G_true = np.array(G_true)[:,1:]
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

# Return metrics
results_path = 'results'
metrics = pd.DataFrame.from_records(metrics)
if not os.path.exists(results_path):
  os.mkdir(results_path)
metrics.to_csv(f'{results_path}/metrics.csv')

### Unit tests
class Test(unittest.TestCase):

    # Assert input space is not empty
    def test_notempty(self):    
        self.assertTrue(input_space.shape[0] != 0)
        self.assertTrue(input_space.shape[1] != 0)

    # Metric number must be consistent
    def test_size(self):
        self.assertTrue(metrics.shape[0] != 0)
        self.assertTrue(metrics.shape[1] != 0)
        self.assertEqual(metrics.shape[0]/(len(np.unique(metrics['alg']))), len(data_list))
        self.assertEqual(input_space.shape[0], len(data_list))

    # Test metrics values
    def test_metric(self):
        self.assertEqual(metrics['shd'].dtype, float)
        self.assertEqual(metrics['auc'].dtype, float)
        self.assertEqual(metrics['time(s)'].dtype, float)
        self.assertEqual(sum(metrics['shd'] < 0), 0)
        self.assertEqual(sum(metrics['auc'] < 0), 0)
        self.assertEqual(sum(metrics['auc'] > 1), 0)
        self.assertEqual(sum(metrics['time(s)'] < 0), 0)
        
    # Results folder must exist and be not empty
    def test_folder(self):
        self.assertTrue(os.path.exists(results_path))
        self.assertTrue(len(os.listdir(results_path)) != 0)

