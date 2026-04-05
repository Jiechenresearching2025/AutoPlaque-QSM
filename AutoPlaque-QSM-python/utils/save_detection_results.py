"""
save_detection_results - persist detection maps as PNG (or .mat) files.
"""

import os
import numpy as np
from pathlib import Path
from PIL import Image


def save_detection_results(
    output_file_path: str,
    file_name: str,
    data: np.ndarray,
    prefix: str,
    extension: str,
) -> None:
    """
    Save *data* to disk.

    Parameters
    ----------
    output_file_path : str, destination directory
    file_name        : str, base file name (no extension)
    data             : ndarray, image or array to save
    prefix           : str, appended after file_name  (e.g. 'Plaque_Mask')
    extension        : str, 'png', 'jpg', or 'mat'
    """
    out_path = Path(output_file_path) / f"{file_name}_{prefix}.{extension}"

    if extension == "mat":
        import scipy.io as sio
        sio.savemat(str(out_path), {"data": data})
    else:
        # Ensure uint8 range for image writing
        arr = np.array(data)
        if arr.dtype == bool:
            arr = arr.astype(np.uint8) * 255
        elif arr.max() <= 1.0 and arr.dtype != np.uint8:
            arr = (arr * 255).astype(np.uint8)
        else:
            arr = arr.astype(np.uint8)
        Image.fromarray(arr).save(str(out_path))
