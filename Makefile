PYTHON = env/bin/python3

# Perform FCD
results/metrics.csv: input_space.csv dags datasets fcd.py code
	@echo 'Performing FCD ...'
	@$(PYTHON) fcd.py
# Generate input space
input_space.csv: input_space.py
	@echo 'Generating input space ...'
	@$(PYTHON) input_space.py
# Generate DAGs and datasets
dags datasets: generation.py input_space.csv
	@echo 'Generating DAGs and datasets ...'
	@$(PYTHON) generation.py
	
# PHONY targets
.PHONY: clean init
clean:
	@echo 'Cleaning  ...'
	@-rm  input_space.csv
	@-rm -r results datasets dags env renv __pycache__
init:
	# Python virtual environment (env)
	@echo 'Setting up env ...'
	@python3 -m venv env
	@$(PYTHON) -m pip install -r requirements.txt
	# Download FCD repositories
	@git submodule update --init
