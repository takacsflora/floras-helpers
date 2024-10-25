import numpy as np
from scipy.stats import zscore

def cross_correlation(A, B, zscorea=True, zscoreb=True):
    '''Compute correlation for each column of A against
    every column of B (e.g. B is predictions).
    Parameters
    ----------
    A : 2D np.ndarray (n, p)
    B : 2D np.ndarray (n, q)
    Returns
    -------
    cross_corr : 2D np.ndarray (p, q)
    '''
    n = A.shape[0]

    # If needed
    if zscorea: A = zscore(A)
    if zscoreb: B = zscore(B)
    corr = np.dot(A.T, B)/float(n)
    return corr