VENV = env
PYTHON = $(VENV)/bin/python

# Perform FCD
fcd : env datasets notears-admm
	$(PYTHON) notears-admm.py
input_space.csv:
	$(PYTHON) input_space_generation.py
# Generate data
datasets: renv input_space.csv data_generation.r
	Rscript data_generation.r
# Activate venv
env: requirements.txt
	python -m venv $(VENV)
	$(PYTHON) -m pip install -r requirements.txt
# Activate renv
renv: renv.lock
	R -e 'install.packages("renv", repos = "http://cran.us.r-project.org"); renv::restore()'
# Download NOTEARS-ADMM source code
notears-admm:
	git clone https://github.com/ignavierng/notears-admm.git
# PHONY targets
.PHONY: clean
clean:
	 rm -rf $(VENV) renv __pycache__

