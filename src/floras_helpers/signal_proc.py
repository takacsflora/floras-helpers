# generic

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


def schmitt(x, thresh, minwid=0):
    """
    Schmitt trigger 
    """
    if thresh.size < 2:
        xmax = np.max(x)
        xmin = np.min(x)
        low = (xmax - xmin) * (1 - thresh) / 2
        high = xmax - low
        low = xmin + low
    else:
        low, high = thresh

    c = (x > high).astype('int') - (x < low).astype('int')
    c[1:] = c[1:] * (c[1:] != c[:-1])
    t = np.where(c)[0]
    t= np.delete(t,1 + np.where(c[t[1:]] == c[t[:-1]])[0])  # remove duplicates (i.e. wherre two 1s or -1s follow each other)

    if minwid >= 1:
        t = t[t[1:] - t[:-1] >= minwid]
        t = np.delete(t,[1 + np.where(c[t[1:]] == c[t[:-1]])[0]])  # remove duplicates


    y = np.zeros(c.size)
    y[t] = 2 * c[t]
    y[t[0]] = c[t[0]]
    y = np.cumsum(y)

    return y, t