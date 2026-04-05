"""
extract_neighborhoods - extract local patch features for RXD.
"""

import numpy as np


def extract_neighborhoods(
    img: np.ndarray,
    neighborhood_size: int,
    neighbor_order: int,
) -> np.ndarray:
    """
    Extract local neighbourhoods for every pixel of *img*.

    Parameters
    ----------
    img               : 2-D ndarray (uint8 or float)
    neighborhood_size : int, side length of the square patch (odd recommended)
    neighbor_order    : int
        0 → column-major flattening (MATLAB default 'patch = patch(:)' after transpose)
        1 → row-major flattening

    Returns
    -------
    neighbors : ndarray, shape (H, W, neighborhood_size**2)
        H, W = original image dimensions after valid convolution
    """
    half = neighborhood_size // 2
    padded = np.pad(img, half, mode='constant', constant_values=0).astype(np.float64)
    rows_p, cols_p = padded.shape
    H = rows_p - neighborhood_size + 1
    W = cols_p - neighborhood_size + 1
    n_feat = neighborhood_size ** 2
    neighbors = np.zeros((H, W, n_feat), dtype=np.float64)

    for i in range(H):
        for j in range(W):
            patch = padded[i: i + neighborhood_size, j: j + neighborhood_size]
            if neighbor_order == 0:
                # MATLAB: patch = patch'; patch = patch(:)  → column-major of transposed = row-major
                vec = patch.T.ravel(order='F')
            elif neighbor_order == 1:
                vec = patch.ravel(order='F')
            else:
                vec = _diagonal_order(patch)
            neighbors[i, j, :] = vec

    return neighbors


def _diagonal_order(patch: np.ndarray) -> np.ndarray:
    """Flatten patch in anti-diagonal order (fallback for neighbor_order >= 2)."""
    n = patch.shape[0]
    result = []
    for d in range(2 * n - 1):
        for r in range(max(0, d - n + 1), min(n, d + 1)):
            c = d - r
            result.append(patch[r, c])
    return np.array(result, dtype=np.float64)
