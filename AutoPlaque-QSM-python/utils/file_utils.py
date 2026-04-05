"""
Miscellaneous utility helpers.
"""

import os
from pathlib import Path


# ---------------------------------------------------------------------------
# find_nii_file
# ---------------------------------------------------------------------------

def find_nii_file(nifti_filename: str, root_folder: str) -> str | None:
    """
    Recursively find a NIfTI file by name under *root_folder*.

    Returns the first match as an absolute path string, or None.
    """
    root = Path(root_folder)
    matches = list(root.rglob(nifti_filename))
    return str(matches[0]) if matches else None


# ---------------------------------------------------------------------------
# delete_if_exists
# ---------------------------------------------------------------------------

def delete_if_exists(file_path: str) -> None:
    """Delete *file_path* if it exists."""
    p = Path(file_path)
    if p.exists():
        p.unlink()
        print(f'File "{file_path}" deleted successfully.')
    else:
        print(f'File "{file_path}" does not exist.')
