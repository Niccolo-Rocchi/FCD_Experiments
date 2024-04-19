library(bnlearn)

# Set seed
set.seed(42)

# Set directory where to save datasets
dirname <- 'datasets/'
unlink(dirname, recursive = TRUE)
dir.create(dirname, showWarnings = FALSE)

# Read input space
input_space <- read.csv('input_space.csv')

# For any input tuple ...
for (i in seq(1, nrow(input_space))) {
  # ... unpack it
  nnodes <- input_space[i, 'nnodes']
  ssize <- input_space[i, 'ssize']
  ID <- input_space[i, 'ID']

  # Generate DAG
  nodes <- sprintf('%s', seq(1, nnodes))
  G <- random.graph(nodes, method='melancon')

  # Generate parameters
  params <- list()
  for (x in nodes(G)) {
    pars <- parents(G, x)
    pars.coef <- rep(1, length(pars))
    names(pars.coef) <- pars
    params[[x]] <- list(coef=c('(Intercept)'=0, pars.coef), sd=1)
  }

  # Fit DAG with parameters
  bn <- custom.fit(G, params)

  # Generate data
  data <- rbn(bn, ssize)
  
  # Save data
  write.csv(data, paste0(dirname, 'data_', ID, '.csv'))
}

