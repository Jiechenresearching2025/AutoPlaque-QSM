"""
extract_slice - extract a 2-D sagittal frame from 3-D MRI volumes.
"""

import numpy as np


def extract_slice(volume_img: np.ndarray, volume_lbl: np.ndarray, slice_idx: int):
    """
    Extract a 2-D sagittal frame and its corresponding label mask.

    Parameters
    ----------
    volume_img : 3-D ndarray (float/double), MRI volume
    volume_lbl : 3-D ndarray (int/uint16), label volume
    slice_idx  : int, 1-based index along the second (y) axis (MATLAB convention)

    Returns
    -------
    slice_frame : 2-D ndarray, dtype float64
    slice_mask  : 2-D ndarray, dtype uint16
    """
    n_rows, n_cols, n_slices = volume_img.shape
    # Convert 1-based MATLAB index to 0-based Python index
    j = slice_idx - 1

    if j < 0 or j >= n_cols:
        raise IndexError(
            f"slice_idx {slice_idx} is out of bounds for volume with {n_cols} columns."
        )

    slice_frame = volume_img[:, j, :].astype(np.float64)
    slice_mask = volume_lbl[:, j, :].astype(np.uint16)

    if slice_frame.size == 0:
        import warnings
        warnings.warn(f"Extracted frame at index {slice_idx} is empty.")

    return slice_frame, slice_mask
