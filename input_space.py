import pandas as pd
import numpy as np
import uuid
import random
import itertools
import unittest

# Set seed
seed = 42
rd = random.Random()
rd.seed(seed)

# Hypercube definition
feature_names = ['nnodes', 'nclients', 'ssize']
nnodes = [5] # number of nodes
nclients = [2] # number of clients
ssize = [100] # sample size

# Input space generation
input_space = list()
for t in itertools.product(*[nnodes, nclients, ssize]):
    record = dict(zip(feature_names, t))
    record['ID'] = f'{uuid.UUID(int=rd.getrandbits(128))}'
    input_space.append(record)
input_space = pd.DataFrame.from_records(input_space)

# Save input space
input_space.to_csv('input_space.csv')

### Unit tests
class Test(unittest.TestCase):

    # Data set shape must be consistent with input shapes
    def test_size(self):
        self.assertEqual(len(feature_names), input_space.shape[1]-1)
        self.assertEqual(len(nnodes)*len(ssize)*len(nclients), input_space.shape[0])

    # All IDs must be different
    def test_id(self):
        self.assertEqual(len(np.unique(input_space['ID'])), input_space.shape[0])
    
