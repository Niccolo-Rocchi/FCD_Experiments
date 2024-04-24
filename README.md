# Instructions

## Without containerization
1. Install dependencies: `make install`
2. Execute code: `make`
3. Clean folder:  `make clean`

## With containerization
1. Ensure to clean local directory: `make clean`
2. Build image: `docker build . -t fcd`

### For an interactive CLI
1. Run container: `docker run -it --rm fcd`
2. Execute code inside container: `make`
3. Results are inside the container at `/workspace/results/`

### For a detached container with volume
1. Run container: `docker run -d --rm -v fcd_results:/workspace/results fcd make`
2. Results are locally at `/var/lib/docker/volumes/fcd_results/_data/`
