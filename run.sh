#!/usr/bin/bash

# Download code
git clone https://github.com/ignavierng/notears-admm.git

# Generate data 
Rscript data_generation.r

# Activate venv
python -m venv venv
source venv/bin/activate
pip install $(cat requirements.txt)

# Run code
python notears-admm.py
