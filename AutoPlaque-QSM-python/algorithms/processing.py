"""
Core algorithm wrappers:
  - estimate_rank_svd
  - apply_godec
  - perform_rxd
  - threshold_dssc
  - process_nii_roi
"""

import os
import numpy as np
from PIL import Image

from algorithms.godec import godec
from algorithms.rxad import rxad
from utils.extract_neighborhoods import extract_neighborhoods
from utils.save_detection_results import save_detection_results


# ---------------------------------------------------------------------------
# estimate_rank_svd
# ---------------------------------------------------------------------------

def estimate_rank_svd(img: np.ndarray, energy_threshold: float) -> int:
    """
    Estimate the low-rank value using cumulative energy from SVD.

    Parameters
    ----------
    img              : 2-D ndarray
    energy_threshold : float in (0, 1], e.g. 0.25

    Returns
    -------
    lr : int, estimated rank
    """
    _, s, _ = np.linalg.svd(img, full_matrices=False)
    denom = np.sum(s ** 2) + 1e-7
    energy = np.cumsum(s ** 2) / denom
    hits = np.where(energy >= energy_threshold)[0]
    return int(hits[0]) + 1 if len(hits) > 0 else len(s)


# ---------------------------------------------------------------------------
# apply_godec
# ---------------------------------------------------------------------------

def apply_godec(img: np.ndarray, rank: int, sparse_threshold: float) -> np.ndarray:
    """
    Apply GoDec decomposition to denoise image and project out low-rank component.

    Parameters
    ----------
    img              : 2-D ndarray
    rank             : int
    sparse_threshold : float, values below this are counted as "rare"

    Returns
    -------
    img_out : 2-D ndarray (projected residual)
    """
    rows = img.shape[0]
    rare_count = int(np.sum(img < sparse_threshold))
    L, S, _, _ = godec(img, rank, rare_count, power=2)

    # Orthogonal projection: P = I - L * pinv(L^T L) * L^T
    LtL = L.T @ L
    P = np.eye(rows) - L @ np.linalg.pinv(LtL) @ L.T
    return P @ (L + S)


# ---------------------------------------------------------------------------
# perform_rxd
# ---------------------------------------------------------------------------

def perform_rxd(neighbors: np.ndarray) -> np.ndarray:
    """
    Compute RXD anomaly detection map from neighborhood feature tensor.

    Parameters
    ----------
    neighbors : ndarray, shape (H, W, n_features)

    Returns
    -------
    DSSC : ndarray, shape (H, W)
    """
    x, y, z = neighbors.shape
    data = neighbors.reshape(x * y, z).T          # shape: (n_features, n_pixels)
    mean_vec = data.mean(axis=1, keepdims=True)   # (n_features, 1)
    diff = data - mean_vec
    cov_mat = (diff @ diff.T) / data.shape[1]
    K = np.linalg.pinv(cov_mat)
    return rxad(data, K, mean_vec, x, y)


# ---------------------------------------------------------------------------
# threshold_dssc
# ---------------------------------------------------------------------------

def threshold_dssc(dssc: np.ndarray, threshold: float = 50.0) -> np.ndarray:
    """
    Binary threshold: values > threshold → 255, else → 0.

    Parameters
    ----------
    dssc      : ndarray
    threshold : float

    Returns
    -------
    ndarray of same shape, dtype uint8-like (values 0 or 255)
    """
    out = dssc.copy()
    out[out > threshold] = 255
    out[out <= threshold] = 0
    return out


# ---------------------------------------------------------------------------
# process_nii_roi  (main detection engine per slice)
# ---------------------------------------------------------------------------

def process_nii_roi(
    image_frame: np.ndarray,
    slice_id: str,
    output_dir: str,
    neighborhood_size: int,
    do_decomposition: bool,
    roi_mask: np.ndarray,
    neighbor_order: int,
    energy_threshold: float,
    sparse_threshold: float,
):
    """
    Execute GoDec decomposition and RXD detection on a single QSM slice.

    Parameters
    ----------
    image_frame       : 2-D ndarray, QSM slice (already masked)
    slice_id          : str, identifier used for output filenames
    output_dir        : str, directory to write PNG outputs
    neighborhood_size : int, patch half-extent for RXD feature extraction
    do_decomposition  : bool, whether to run GoDec
    roi_mask          : 2-D ndarray or None, binary mask restricting detection
    neighbor_order    : int, 0 = row-major, 1 = col-major
    energy_threshold  : float, cumulative SVD energy for rank estimation
    sparse_threshold  : float, value below which pixels count as sparse

    Returns
    -------
    detection_map : 2-D ndarray (binary, values 0/255)
    processed_img : 2-D ndarray (uint8, after normalisation)
    """
    # 1. Precision management
    processed_img = image_frame.astype(np.float64)

    # 2. Rank estimation & GoDec denoising
    estimated_rank = estimate_rank_svd(processed_img, energy_threshold)
    if do_decomposition:
        processed_img = apply_godec(processed_img, estimated_rank, sparse_threshold)

    # 3. Normalise to [0, 255]  (mat2gray equivalent)
    mn, mx = processed_img.min(), processed_img.max()
    if mx > mn:
        processed_img = (processed_img - mn) / (mx - mn) * 255.0
    else:
        processed_img = np.zeros_like(processed_img)
    processed_img = processed_img.astype(np.uint8)

    # 4. Neighbourhood feature extraction
    neighbors = extract_neighborhoods(processed_img, neighborhood_size, neighbor_order)

    # 5. RXD anomaly detection
    detection_map = perform_rxd(neighbors)

    # 6. ROI masking
    if roi_mask is not None and roi_mask.size > 0:
        detection_map = detection_map * (roi_mask > 0).astype(np.float64)

    # 7. Binary thresholding (heuristic constant = 50 for normalised RXD maps)
    detection_map = threshold_dssc(detection_map, threshold=50.0)

    # 8. Save PNG outputs
    os.makedirs(output_dir, exist_ok=True)
    base_file_name = f"{slice_id}_plaque_detection"
    save_detection_results(output_dir, base_file_name, detection_map, "Plaque_Mask", "png")
    save_detection_results(output_dir, base_file_name, ~detection_map.astype(bool), "Inverse_Mask", "png")

    return detection_map, processed_img
