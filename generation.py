# Import packages
import pyAgrum as gum
import pandas as pd
import random
import os

# Set seed
seed = 42
rd = random.Random()
rd.seed(seed)
gum.initRandom(seed = seed)

# Create folders for DAGs and datasets
dags_path = 'dags'
datasets_path = 'datasets'
if not os.path.exists(dags_path):
  os.mkdir(dags_path)
if not os.path.exists(datasets_path):
  os.mkdir(datasets_path)

# For each input in the input space...
input_space = pd.read_csv('input_space.csv')
for index in range(input_space.shape[0]):
    nnodes = int(input_space.iloc[index].at['nnodes'])
    ssize = int(input_space.iloc[index].at['ssize'])
    ID = input_space.iloc[index].at['ID']
    # generate BN,
    bn = gum.randomBN(n = nnodes, ratio_arc = 1)
    # save its adjacency matrix,
    bn_amat = pd.DataFrame(bn.adjacencyMatrix())
    bn_amat.to_csv(f'{dags_path}/{ID}.csv')
    # sample data from BN,
    data = gum.BNDatabaseGenerator(bn)
    data.drawSamples(ssize)
    data.setVarOrder([f'X0{x}' for x in bn.nodes()])
    # save data
    data.toCSV(f'{datasets_path}/{ID}.csv')
