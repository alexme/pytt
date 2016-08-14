import numpy as np

import pdb

def gbm(s0_v, drift_v, cov_mat, dt):
    # checks
    n = drift_v.size
    if s0_v.size != n:
        raise ValueError()
    cov_mat = np.array(cov_mat, ndmin=2)
    if cov_mat.shape != (n, n):
        raise ValueError()
    # init
    s = s0_v
    l = np.linalg.cholesky(cov_mat)
    dt_sqrt = np.sqrt(dt)
    mu_v = dt * drift_v
    #
    while True:
        yield s
        dw = dt_sqrt * np.random.normal(size=n)
        inc = mu_v + np.dot(l, dw)
        s *= np.exp(inc)

def fetch_rand_covar(nb_assets, trials=25):
    x = np.random.normal(scale=0.01, size=(nb_assets, trials))
    return np.cov(x)

def gbm_source(nb_assets):
    s0 = 100.0 * np.ones(nb_assets)
    m = np.zeros(nb_assets)
    v = fetch_rand_covar(nb_assets)
    yield from gbm(s0, m, v, 1.0)
