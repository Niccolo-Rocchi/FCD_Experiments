library(bnlearn)

# Set seed
set.seed(42)

# Graph generation
n.nodes <- 5
nodes <- sprintf('%s', seq(1, n.nodes))
G <- random.graph(nodes, method='melancon')

# Parameters generation
params <- list()
for (x in nodes(G)) {
  pars <- parents(G, x)
  pars.coef <- rep(1, length(pars))
  names(pars.coef) <- pars
  params[[x]] <- list(coef=c('(Intercept)'=0, pars.coef), sd=1)
}

# Bayesian network fit
bn <- custom.fit(G, params)

# Data generation
nsamples <- 1000
data <- rbn(bn, nsamples)
write.csv(data, 'data.csv')
