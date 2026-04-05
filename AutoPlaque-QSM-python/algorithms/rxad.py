"""
RXAD - Reed-Xiaoli Anomaly Detector
"""

import numpy as np


def rxad(img0: np.ndarray, K: np.ndarray, uU: np.ndarray,
         no_lines: int, no_rows: int) -> np.ndarray:
    """
    Compute the RXD anomaly score for every pixel.

    Parameters
    ----------
    img0     : ndarray, shape (n_features, n_pixels), flattened image columns
    K        : ndarray, shape (n_features, n_features), inverse covariance matrix
    uU       : ndarray, shape (n_features, 1) or (n_features,), mean vector
    no_lines : int, number of rows in the output map
    no_rows  : int, number of columns in the output map

    Returns
    -------
    RXAD_map : ndarray, shape (no_lines, no_rows)
    """
    uU = uU.ravel()
    _, N = img0.shape
    scores = np.zeros(N)
    for i in range(N):
        r = img0[:, i] - uU
        scores[i] = r @ K @ r

    return scores.reshape(no_lines, no_rows)
