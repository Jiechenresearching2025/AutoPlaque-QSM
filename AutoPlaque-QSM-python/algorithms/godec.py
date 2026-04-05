"""
GoDec Algorithm - Randomized Low-rank & Sparse Matrix Decomposition in Noisy Case

Reference:
    Tianyi Zhou and Dacheng Tao, "GoDec: Randomized Lo-rank & Sparse Matrix
    Decomposition in Noisy Case", ICML 2011
"""

import numpy as np
from scipy.sparse import lil_matrix


def godec(X: np.ndarray, rank: int, card: int, power: int = 1):
    """
    GoDec decomposition: X ≈ L (low-rank) + S (sparse)

    Parameters
    ----------
    X     : ndarray, shape (n, p), input data matrix
    rank  : int, upper bound on rank of L
    card  : int, upper bound on cardinality (nnz) of S
    power : int >= 0, power scheme exponent (higher → more accurate, slower)

    Returns
    -------
    L    : ndarray, low-rank component
    S    : ndarray, sparse component
    RMSE : list of float, residual norms per iteration
    error: float, ||X - L - S|| / ||X||
    """
    iter_max = 100
    error_bound = 1e-4

    transposed = False
    m, n = X.shape
    if m < n:
        X = X.T
        transposed = True
    num = min(X.shape)

    L = X.copy().astype(np.float64)
    S = np.zeros_like(L)
    RMSE = []

    for it in range(1, iter_max + 1):
        # --- Update L ---
        Y2 = np.random.randn(num, rank)
        for _ in range(power + 1):
            Y1 = L @ Y2
            Y2 = L.T @ Y1
        Q, _ = np.linalg.qr(Y2)

        L_new = (L @ Q) @ Q.T

        # --- Update S ---
        T = L - L_new + S
        L = L_new
        flat = T.ravel()
        idx = np.argpartition(np.abs(flat), -card)[-card:]   # top-card indices
        S = np.zeros_like(X)
        S.ravel()[idx] = flat[idx]

        # --- Stopping criterion ---
        T.ravel()[idx] = 0.0
        rmse_val = np.linalg.norm(T)
        RMSE.append(rmse_val)
        print(f"  GoDec iter {it}: RMSE = {rmse_val:.6f}")

        if rmse_val < error_bound or it >= iter_max:
            break
        else:
            L = L + T

    LS = L + S
    norm_X = np.linalg.norm(X)
    error = np.linalg.norm(LS - X) / norm_X if norm_X > 0 else 0.0

    if transposed:
        L, S = L.T, S.T

    return L, S, RMSE, error
