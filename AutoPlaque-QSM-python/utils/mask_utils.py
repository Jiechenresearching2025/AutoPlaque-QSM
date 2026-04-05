"""
Masking utilities.
"""

import numpy as np
from skimage.morphology import erosion, disk


# ---------------------------------------------------------------------------
# reduce_mask_size  (imerode equivalent)
# ---------------------------------------------------------------------------

def reduce_mask_size(binary_mask: np.ndarray, reduction_pixels: int) -> np.ndarray:
    """
    Erode *binary_mask* by a disk-shaped structuring element of radius *reduction_pixels*.

    Parameters
    ----------
    binary_mask      : 2-D ndarray (uint8 / bool)
    reduction_pixels : int, erosion radius

    Returns
    -------
    eroded : 2-D ndarray, same dtype as input
    """
    se = disk(reduction_pixels)
    eroded = erosion(binary_mask.astype(np.uint8), se)
    return eroded.astype(binary_mask.dtype)


# ---------------------------------------------------------------------------
# make_whole_mask
# ---------------------------------------------------------------------------

def make_whole_mask(mask: np.ndarray, desired_labels):
    """
    Build a binary ROI mask from *mask* by retaining only *desired_labels*.

    Parameters
    ----------
    mask           : 2-D ndarray (uint16), label map
    desired_labels : array-like of int, target label values

    Returns
    -------
    sel_labels  : 1-D ndarray, labels actually present in *mask* that overlap desired_labels
    mask_whole  : 2-D ndarray uint8, binary mask (1 inside ROI, 0 outside), after erosion
    """
    desired = np.asarray(desired_labels)
    labels = np.unique(mask)
    sel_labels = labels[np.isin(labels, desired)]
    mask_whole = np.isin(mask, sel_labels).astype(np.uint8)
    mask_whole = reduce_mask_size(mask_whole, 3)
    return sel_labels, mask_whole


# ---------------------------------------------------------------------------
# get_neighbors  (kept for completeness; vectorised path used in practice)
# ---------------------------------------------------------------------------

def get_neighbors(matrix: np.ndarray, neighborhood_size: int, row: int, col: int) -> np.ndarray:
    """
    Extract the neighborhood patch around (row, col) from *matrix*.

    Indices are 0-based (unlike the MATLAB 1-based original).

    Parameters
    ----------
    matrix            : 2-D ndarray
    neighborhood_size : int
    row, col          : int, centre pixel (0-based)

    Returns
    -------
    neighbors : 2-D ndarray, shape (neighborhood_size, neighborhood_size)
    """
    half = neighborhood_size // 2
    rows, cols = matrix.shape
    neighbors = np.zeros((neighborhood_size, neighborhood_size), dtype=matrix.dtype)
    for i in range(-half, half + 1):
        for j in range(-half, half + 1):
            ri, ci = row + i, col + j
            if 0 <= ri < rows and 0 <= ci < cols:
                neighbors[i + half, j + half] = matrix[ri, ci]
    return neighbors
