"""
QSM Plaque Detection - Main Entry Point
Project: ADDA Framework (Amyloid Detection-Derived Analysis)
Author:  Jie Chen, Ph.D.  (Python port)
Description: Batch processing for plaque quantification in 5xFAD Alzheimer's
             mouse models using high-resolution QSM.

Usage:
    python main.py
    python main.py --config config.yaml
"""

import sys
import warnings
from pathlib import Path

from utils.find_folders_and_files import find_folders_and_files
from core.process_subject import process_subject


# ---------------------------------------------------------------------------
# Configuration  (mirrors main.m cfg struct)
# ---------------------------------------------------------------------------

def build_default_config() -> dict:
    cfg = {
        "path": {
            # Edit this to point at your data root
            "parent": "/path/to/your/QSM_Data",
        },
        "pattern": {
            "qsm":   "qsm_mean2.nii",
            "label": "166_label_V5.nii.gz",
        },
        "params": {
            # Target anatomical labels (matching MATLAB: [1:46, 49, 53, 55, 57, 58, 65])
            "desiredLabels": list(range(1, 47)) + [49, 53, 55, 57, 58, 65],
            "neiSize":   3,      # Neighbourhood patch side length
            "neiOrder":  0,      # 0 = row-major (MATLAB default), 1 = col-major
            "energy":    0.25,   # SVD cumulative energy threshold for rank estimation
            "sparse":   -0.02,   # Sparse threshold (pixels below this are "rare")
        },
    }
    return cfg


def load_yaml_config(yaml_path: str) -> dict:
    """Optional YAML override for cfg (requires PyYAML)."""
    try:
        import yaml
    except ImportError:
        warnings.warn("PyYAML not installed; falling back to default config.")
        return build_default_config()

    with open(yaml_path, "r") as f:
        user_cfg = yaml.safe_load(f)

    cfg = build_default_config()
    # Deep-merge user overrides
    for section, values in user_cfg.items():
        if section in cfg and isinstance(values, dict):
            cfg[section].update(values)
        else:
            cfg[section] = values
    return cfg


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Parse optional --config argument
    cfg_path = None
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--config" and i < len(sys.argv):
            cfg_path = sys.argv[i + 1]
            break

    cfg = load_yaml_config(cfg_path) if cfg_path else build_default_config()

    parent_dir = cfg["path"]["parent"]
    qsm_pat    = cfg["pattern"]["qsm"]
    label_pat  = cfg["pattern"]["label"]

    # Step 1 - Resource discovery
    print(f"Scanning for files in: {parent_dir}")
    try:
        results = find_folders_and_files(parent_dir, qsm_pat, label_pat)
    except FileNotFoundError as e:
        warnings.warn(f"Resource Discovery Failed: {e}")
        return

    if not results:
        warnings.warn("Resource Discovery Failed: No matching NIfTI files found.")
        return

    # Step 2 - Batch processing
    for subject_info in results:
        subject_folder = subject_info.folder
        try:
            process_subject(subject_folder, subject_info, cfg)
        except Exception as e:
            print(f"Critical Error in Folder: {subject_folder}")
            print(f"Message: {e}")
            import traceback
            traceback.print_exc()
            continue


if __name__ == "__main__":
    main()
