PYTHON = env/bin/python

# Perform FCD
all: input_space.csv datasets notears-admm
	@echo 'Performing FCD ...'
	@$(PYTHON) notears-admm.py
	@echo 'DONE'
# Generate input space
input_space.csv: input_space_generation.py
	@echo 'Generating input space ...'
	@$(PYTHON) input_space_generation.py
# Generate data
datasets: data_generation.r input_space.csv
	@echo 'Generating data sets ...'
	@Rscript data_generation.r
# Download NOTEARS-ADMM source code
notears-admm:
	git clone https://github.com/ignavierng/notears-admm.git
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
