"""
process_subject - orchestrate the analysis pipeline for a single subject.
"""

import os
import traceback
import numpy as np
import nibabel as nib
from pathlib import Path
from dataclasses import dataclass
from typing import Any

from algorithms.processing import process_nii_roi
from utils.extract_slice import extract_slice
from utils.mask_utils import make_whole_mask
from utils.result_table import init_result_table, update_result_table, save_results
from utils.create_nii_from_pngs import create_nii_from_pngs


def process_subject(subject_folder: str, subject_info: Any, cfg: dict) -> None:
    """
    Run the full QSM plaque detection pipeline on one subject.

    Parameters
    ----------
    subject_folder : str, absolute path to the subject directory
    subject_info   : SubjectInfo dataclass (has .qsm and .label list attributes)
    cfg            : dict with keys:
                       cfg['params']['desiredLabels']
                       cfg['params']['neiSize']
                       cfg['params']['neiOrder']
                       cfg['params']['energy']
                       cfg['params']['sparse']
                       cfg['pattern']['qsm']
    """
    params  = cfg["params"]
    pattern = cfg["pattern"]

    # 1. Paths
    qsm_filename   = subject_info.qsm[0]
    label_filename = subject_info.label[0]
    qsm_file   = str(Path(subject_folder) / qsm_filename)
    label_file = str(Path(subject_folder) / label_filename)
    output_dir = str(Path(subject_folder) / "Results")
    os.makedirs(output_dir, exist_ok=True)

    # 2. Load NIfTI volumes
    try:
        qsm_vol   = nib.load(qsm_file).get_fdata()
        label_vol = nib.load(label_file).get_fdata().astype(np.uint16)
    except Exception as e:
        print(f"Failed to read NIfTI: {e}")
        return

    _, n_slices, _ = qsm_vol.shape

    # 3. Initialise result table
    res_table = init_result_table(params["desiredLabels"])

    print(f"--> Analysing subject in: {subject_folder}")

    # 4. Slice-wise loop
    for j in range(1, n_slices + 1):
        slice_id = f"{qsm_filename.replace('.nii', '')}_slice_{j:03d}"

        frame, mask = extract_slice(qsm_vol, label_vol, j)
        sel_labels, binary_mask = make_whole_mask(mask, params["desiredLabels"])

        if sel_labels.size == 0:
            continue

        # Mask the QSM frame
        masked_frame = frame * binary_mask.astype(np.float64)

        detection_map, processed_img = process_nii_roi(
            image_frame       = masked_frame,
            slice_id          = slice_id,
            output_dir        = output_dir,
            neighborhood_size = params["neiSize"],
            do_decomposition  = True,
            roi_mask          = binary_mask,
            neighbor_order    = params["neiOrder"],
            energy_threshold  = params["energy"],
            sparse_threshold  = params["sparse"],
        )

        res_table = update_result_table(
            res_table, sel_labels, frame, mask, detection_map, processed_img
        )

    # 5. Persist results
    save_results(res_table, subject_folder, qsm_filename)
    create_nii_from_pngs(pattern["qsm"], subject_folder)

    print(f"Analysis Complete for Subject: {subject_folder}")
