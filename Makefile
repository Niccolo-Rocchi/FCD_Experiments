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
dags datasets: data_generation.r input_space.csv
	@echo 'Generating DAGs and datasets ...'
	@Rscript data_generation.r
	
# PHONY targets
.PHONY: clean
clean:
	@echo 'Cleaning  ...'
	@-rm  input_space.csv
	@-rm -r results datasets dags env renv __pycache__
install:
	# Python virtual environment (env)
	@echo 'Setting up env ...'
	@python3 -m venv env
	@$(PYTHON) -m pip install -r requirements.txt
	# R virtual environment (renv)
	@echo 'Setting up renv ...'
	@R -e 'install.packages("renv", repos = "http://cran.us.r-project.org"); renv::restore()'
	# Download FCD repositories
	@git submodule update --init
