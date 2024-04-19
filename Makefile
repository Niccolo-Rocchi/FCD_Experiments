PYTHON = env/bin/python

# Perform FCD
all: input_space.csv datasets fcd.py
	@echo 'Performing FCD ...'
	@$(PYTHON) fcd.py
# Generate input space
input_space.csv: input_space_generation.py
	@echo 'Generating input space ...'
	@$(PYTHON) input_space_generation.py
# Generate data
datasets: data_generation.r input_space.csv
	@echo 'Generating data sets ...'
	@Rscript data_generation.r
	
# PHONY targets
.PHONY: clean
clean:
	@echo 'Cleaning ...'
	@rm -rf env renv __pycache__
install:
	# Python virtual environment (venv)
	@echo 'Setting up venv ...'
	@python -m venv env
	@$(PYTHON) -m pip install -r requirements.txt
	# R virtual environment (renv)
	@echo 'Setting up renv ...'
	@R -e 'install.packages("renv", repos = "http://cran.us.r-project.org"); renv::restore()'
	# Download FCD repositories
	git submodule update --init
