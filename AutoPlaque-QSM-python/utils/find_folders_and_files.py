"""
find_folders_and_files - recursive search for paired QSM + label NIfTI files.
"""

import os
from pathlib import Path
from typing import List
from dataclasses import dataclass, field


@dataclass
class SubjectInfo:
    folder: str
    qsm: List[str] = field(default_factory=list)
    label: List[str] = field(default_factory=list)


def find_folders_and_files(
    root_dir: str,
    pattern_qsm: str,
    pattern_label: str,
) -> List[SubjectInfo]:
    """
    Recursively locate subject folders that contain both a QSM file and a label file.

    Parameters
    ----------
    root_dir      : str, root directory to search
    pattern_qsm   : str, filename (exact) for the QSM NIfTI, e.g. 'qsm_mean2.nii'
    pattern_label : str, filename (exact) for the label NIfTI, e.g. '166_label_V5.nii.gz'

    Returns
    -------
    List[SubjectInfo], one entry per subject with matched file pairs
    """
    root = Path(root_dir)
    if not root.is_dir():
        raise FileNotFoundError(f"Root directory not found: {root_dir}")

    print(f"Scanning for file pairs under: {root_dir}")

    # Collect all matches
    all_qsm = {f.parent: f.name for f in root.rglob(pattern_qsm)}
    all_label = {f.parent: f.name for f in root.rglob(pattern_label)}

    if not all_qsm or not all_label:
        import warnings
        warnings.warn("No matching file pairs were discovered.")
        return []

    results: List[SubjectInfo] = []
    for folder, qsm_name in all_qsm.items():
        if folder in all_label:
            results.append(SubjectInfo(
                folder=str(folder),
                qsm=[qsm_name],
                label=[all_label[folder]],
            ))

    print(f"Resource Discovery Success: Identified {len(results)} subjects with paired data.")
    return results
