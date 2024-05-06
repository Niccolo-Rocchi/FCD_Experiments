import pandas as pd
import numpy as np
import os
import pytest


def test_input_space():
    input_space = pd.read_csv('input_space.csv')
    
    # Not empty
    assert input_space.shape[0] != 0
    assert input_space.shape[1] != 0
    # Not zero values
    assert sum(input_space['nnodes'] == 0) == 0
    assert sum(input_space['nclients'] == 0) == 0
    assert sum(input_space['ssize'] == 0) == 0
    # Different IDs
    assert len(np.unique(input_space['ID'])) == input_space.shape[0]
    # Consistency
    nnodes = np.unique(input_space['nnodes'])
    nclients = np.unique(input_space['nclients'])
    ssize = np.unique(input_space['ssize'])
    assert len(nnodes)*len(ssize)*len(nclients) == input_space.shape[0]

def test_ids():
    input_space = pd.read_csv('input_space.csv')
    input_ids = list(input_space['ID'])
    input_ids.sort()
    data_ids = pd.read_csv('data_ids.csv')
    ids = list(data_ids['ids'])
    ids.sort()
    datasets = os.listdir('datasets')
    datasets_ids = [d.split('.')[0] for d in datasets]
    datasets_ids.sort()
    dags = os.listdir('dags')
    dags_ids = [d.split('.')[0] for d in dags]
    dags_ids.sort()
    metrics = pd.read_csv('results/metrics.csv')
    metrics_ids = list(np.unique(metrics['ID']))
    metrics_ids.sort()
    
    # IDs must coincide
    assert len(input_ids) != 0
    assert input_ids == ids
    assert input_ids == datasets_ids
    assert input_ids == dags_ids
    assert input_ids == metrics_ids

def test_metrics():
    input_space = pd.read_csv('input_space.csv')
    metrics = pd.read_csv('results/metrics.csv')
    
    # Consistent with input
    assert metrics.shape[0]/(len(np.unique(metrics['alg']))) == input_space.shape[0]
    # Consistent types
    assert metrics['shd'].dtype == float
    assert metrics['auc'].dtype == float
    assert metrics['time(s)'].dtype == float
    assert sum(metrics['shd'] < 0) == 0
    assert sum(metrics['auc'] < 0) == 0
    assert sum(metrics['auc'] > 1) == 0
    assert sum(metrics['time(s)'] < 0) == 0
