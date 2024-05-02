# Import packages
import pyAgrum as gum
import pandas as pd
import random
import os
import unittest

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

data_ids = [x.split('.')[0] for x in os.listdir(datasets_path)]
data_ids = pd.DataFrame({'ids':data_ids})
data_ids.to_csv('data_ids.csv')

### Unit tests
class Test(unittest.TestCase):

  # Assert input space is not empty
  def test_notempty(self):
    self.assertTrue(input_space.shape[0] != 0)
    self.assertTrue(input_space.shape[1] != 0)

  # Datasets and DAGs folders must exist, and be not empty
  def test_folder(self):
    self.assertTrue(os.path.exists(datasets_path))
    self.assertTrue(os.path.exists(dags_path))
    self.assertTrue(len(os.listdir(datasets_path)) != 0)
    self.assertTrue(len(os.listdir(dags_path)) != 0)

  # Datasets and DAGs IDs must coincide
  def test_ids(self):
    data_names = os.listdir(datasets_path)
    dag_names = os.listdir(dags_path)
    self.assertEqual(len(data_names), len(dag_names))
    self.assertEqual(len(data_names), input_space.shape[0])
    self.assertEqual(len(data_names), data_ids.shape[0])
    data_names_ids = {x.split('.')[0] for x in data_names}
    dag_names_ids = {x.split('.')[0] for x in dag_names}
    self.assertEqual(data_names_ids, dag_names_ids)
    self.assertEqual(data_names_ids, set(data_ids['ids']))
