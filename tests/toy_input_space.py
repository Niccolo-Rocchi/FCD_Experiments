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
nnodes = [4, 5] # number of nodes
nclients = [1, 2, 3] # number of clients
ssize = [100, 101] # sample size

# Input space generation
input_space = list()
for t in itertools.product(*[nnodes, nclients, ssize]):
    record = dict(zip(feature_names, t))
    record['ID'] = f'{uuid.UUID(int=rd.getrandbits(128))}'
    input_space.append(record)
input_space = pd.DataFrame.from_records(input_space)

# Save input space
input_space.to_csv('input_space.csv')
