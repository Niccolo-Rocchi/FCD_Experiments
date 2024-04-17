# Perform FCD
fcd : venv data_gen | ./notears-admm
	. venv/bin/activate; \
	python notears-admm.py
# Generate data
data_gen: renv
	Rscript data_generation.r
# Activate venv
venv: requirements.txt
	python -m venv venv; \
	. venv/bin/activate; \
	pip install -r requirements.txt
# Activate renv
renv: renv.lock .Rprofile renv/activate.R renv/settings.json
	R -e "install.packages('renv')"
	R -e 'renv::restore()'
# Download NOTEARS-ADMM source code
./notears-admm:
	git clone https://github.com/ignavierng/notears-admm.git
	
