PYTHON = env/bin/python3

# Perform FCD
results/metrics.csv: input_space.csv dags datasets fcd.py code
	@echo 'Performing FCD ...'
	@$(PYTHON) fcd.py
# Generate input space
input_space.csv: input_space_generation.py
	@echo 'Generating input space ...'
	@$(PYTHON) input_space_generation.py
# Generate DAGs and datasets
dags datasets: generation.py input_space.csv
	@echo 'Generating DAGs and datasets ...'
	@$(PYTHON) generation.py
	
# PHONY targets
.PHONY: clean install
clean:
	@echo 'Cleaning  ...'
	@-rm  input_space.csv
	@-rm -r results datasets dags env renv __pycache__
install:
	# Python virtual environment (env)
	@echo 'Setting up env ...'
	@python3 -m venv env
	@$(PYTHON) -m pip install -r requirements.txt
	# Download FCD repositories
	@git submodule update --init
