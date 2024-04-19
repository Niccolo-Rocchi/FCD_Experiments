PYTHON = env/bin/python

# Perform FCD
fcd : input_space_generation.py data_generation.r notears-admm
	$(PYTHON) notears-admm.py
input_space_generation.py:
	$(PYTHON) input_space_generation.py
# Generate data
data_generation.r: input_space_generation.py
	Rscript data_generation.r
# Download NOTEARS-ADMM source code
notears-admm:
	git clone https://github.com/ignavierng/notears-admm.git
# PHONY targets
.PHONY: clean
clean:
	 rm -rf env renv __pycache__
install:
	# Python virtual environment (venv)
	python -m venv env
	$(PYTHON) -m pip install -r requirements.txt
	# R virtual environment (renv)
	R -e 'install.packages("renv", repos = "http://cran.us.r-project.org"); renv::restore()'
