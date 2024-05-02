# Instructions

## Without containerization
1. Install dependencies: `make init`
2. Execute code: `make`
3. Clean folder:  `make clean`

## With containerization
1. Ensure to clean local directory: `make clean`
2. Build image: `docker build . -t fcd`
3. Run container: `docker run -d --rm -v fcd_results:/workspace/results fcd`
3. Results will be available at `/var/lib/docker/volumes/fcd_results/_data/`

