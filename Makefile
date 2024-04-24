PYTHON = env/bin/python3

# Perform FCD
metrics.csv: input_space.csv dags datasets fcd.py code
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
	@echo 'Cleaning metrics and input space...'
	@-rm  metrics.csv input_space.csv
	@echo 'Cleaning datasets and DAGs ...'
	@-rm -r datasets dags
	@echo 'Cleaning virtual environments ...'
	@-rm -r env renv
	@echo 'Cleaning pycache ...'
	@-rm -r __pycache__
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
