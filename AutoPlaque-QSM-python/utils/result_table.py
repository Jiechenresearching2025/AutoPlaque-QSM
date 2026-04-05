"""
Result table utilities - initialise, update, and persist quantitative results.
"""

import os
import numpy as np
import pandas as pd
from pathlib import Path

from utils.file_utils import delete_if_exists


# ---------------------------------------------------------------------------
# init_result_table
# ---------------------------------------------------------------------------

def init_result_table(labels) -> pd.DataFrame:
    """
    Initialise an empty results DataFrame, one row per label.

    Columns match the MATLAB version:
        LabelNumber, LabelVolume, PlaqueVolume, NonPlaqueVolume,
        PlaqueValueInMRI, PlaqueValueInLowrank,
        NonPlaqueValueInMRI, NonPlaqueValueInLowrank
    """
    labels_arr = np.asarray(labels, dtype=np.uint16)
    n = len(labels_arr)
    return pd.DataFrame({
        "LabelNumber":           labels_arr,
        "LabelVolume":           np.zeros(n, dtype=np.float64),
        "PlaqueVolume":          np.zeros(n, dtype=np.float64),
        "NonPlaqueVolume":       np.zeros(n, dtype=np.float64),
        "PlaqueValueInMRI":      np.zeros(n, dtype=np.float64),
        "PlaqueValueInLowrank":  np.zeros(n, dtype=np.float64),
        "NonPlaqueValueInMRI":   np.zeros(n, dtype=np.float64),
        "NonPlaqueValueInLowrank": np.zeros(n, dtype=np.float64),
    })


# ---------------------------------------------------------------------------
# update_result_table
# ---------------------------------------------------------------------------

def update_result_table(
    T: pd.DataFrame,
    sel_labels,
    frame: np.ndarray,
    mask: np.ndarray,
    det_res: np.ndarray,
    lowrank_img: np.ndarray,
) -> pd.DataFrame:
    """
    Accumulate volume and susceptibility metrics into result table *T*.

    Parameters
    ----------
    T           : pd.DataFrame from init_result_table
    sel_labels  : array-like of uint16, labels present in this slice
    frame       : 2-D ndarray, original QSM slice
    mask        : 2-D ndarray, label map for this slice
    det_res     : 2-D ndarray, detection map (0 / 255)
    lowrank_img : 2-D ndarray, processed (low-rank projected) image

    Returns
    -------
    T : updated DataFrame
    """
    for lbl in sel_labels:
        row_idx = T.index[T["LabelNumber"] == lbl]
        if len(row_idx) == 0:
            continue
        idx = row_idx[0]

        binary_mask = (mask == lbl)
        T.at[idx, "LabelVolume"]  += int(np.count_nonzero(binary_mask))

        plaque_mask = binary_mask & (det_res > 0)
        T.at[idx, "PlaqueVolume"] += int(np.count_nonzero(plaque_mask))
        T.at[idx, "NonPlaqueVolume"] = T.at[idx, "LabelVolume"] - T.at[idx, "PlaqueVolume"]

        T.at[idx, "PlaqueValueInMRI"]      += float(frame[plaque_mask].sum())
        T.at[idx, "PlaqueValueInLowrank"]  += float(lowrank_img[plaque_mask].sum())
        non_plaque_mask = binary_mask & ~plaque_mask
        T.at[idx, "NonPlaqueValueInMRI"]     += float(frame[non_plaque_mask].sum())
        T.at[idx, "NonPlaqueValueInLowrank"] += float(lowrank_img[non_plaque_mask].sum())

    return T


# ---------------------------------------------------------------------------
# save_results
# ---------------------------------------------------------------------------

def save_results(T: pd.DataFrame, folder: str, base_name: str) -> None:
    """
    Write the results table to CSV (and optionally pickle).

    Parameters
    ----------
    T         : pd.DataFrame
    folder    : str, destination directory
    base_name : str, e.g. 'qsm_mean2.nii'  (extension stripped automatically)
    """
    stem = Path(base_name).stem.replace(".nii", "")   # handle .nii.gz
    csv_file = str(Path(folder) / f"{stem}.csv")
    delete_if_exists(csv_file)
    T.to_csv(csv_file, index=False)
    print(f"Results saved to: {csv_file}")
