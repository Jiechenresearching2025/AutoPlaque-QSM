"""
create_nii_from_pngs - reconstruct a 3-D NIfTI plaque mask from per-slice PNG files.
"""

import os
import re
import numpy as np
import nibabel as nib
from pathlib import Path
from PIL import Image

from utils.file_utils import find_nii_file


def create_nii_from_pngs(nifti_filename: str, root_folder: str) -> None:
    """
    Assemble slice-wise PNG detection masks into a compressed NIfTI volume.

    Parameters
    ----------
    nifti_filename : str, e.g. 'qsm_mean2.nii'
    root_folder    : str, subject directory (will be searched recursively)
    """
    # Strip any trailing '$' (MATLAB artefact)
    nifti_filename = nifti_filename.rstrip("$")

    # 1. Locate the NIfTI file
    nii_path = find_nii_file(nifti_filename, root_folder)
    if nii_path is None:
        raise FileNotFoundError(f"NIfTI file '{nifti_filename}' not found under '{root_folder}'")

    # 2. Load volume & header
    nii_img = nib.load(nii_path)
    nii_data = nii_img.get_fdata()
    nii_affine = nii_img.affine
    nii_header = nii_img.header.copy()

    x, y, z = nii_data.shape
    mask_data = np.zeros((x, y, z), dtype=np.uint8)

    # 3. Iterate slices
    nii_folder = str(Path(nii_path).parent)
    nii_stem   = Path(nii_path).name.replace(".nii.gz", "").replace(".nii", "")
    mask_folder = Path(nii_folder) / "Results"

    sparse_threshold = -0.02   # matches MATLAB constant

    for i in range(y):
        # Filename pattern matches MATLAB: '<stem>_<i+1>_detection_DSSC_detection.png'
        mask_file = mask_folder / f"{nii_stem}_{i + 1}_detection_DSSC_detection.png"

        if mask_file.is_file():
            mask_img = np.array(Image.open(str(mask_file)).convert("L"))
            mask_img = (mask_img > 0).astype(np.float64)

            # Element-wise product with the raw QSM slice
            qsm_slice = nii_data[:, i, :]
            mask_temp = mask_img * qsm_slice
            mask_temp[mask_temp > sparse_threshold] = 0
            mask_temp[mask_temp <= sparse_threshold] = 1

            mask_data[:, i, :] = mask_temp.astype(np.uint8)
        else:
            print(f"Mask for index {i + 1} not found. Using zero matrix.")

    # 4. Write output NIfTI
    out_path = Path(nii_folder) / f"{nii_stem}_plaque_mask.nii.gz"
    new_header = nii_header
    new_header.set_data_dtype(np.uint8)
    out_img = nib.Nifti1Image(mask_data, nii_affine, new_header)
    nib.save(out_img, str(out_path))
    print(f"Created NIfTI file: {out_path}")
