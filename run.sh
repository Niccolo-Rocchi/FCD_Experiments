#!/usr/bin/bash

# Download source code
git clone https://github.com/ignavierng/notears-admm.git

# Generate data 
Rscript data_generation.r

# Run code
source venv/bin/activate
python notears-admm.py
