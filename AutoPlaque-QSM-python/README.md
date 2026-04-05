# AutoPlaque-QSM — Python Port

> Python translation of the original MATLAB pipeline for automated amyloid plaque detection
> in 5xFAD Alzheimer's mouse models using high-resolution 9.4T QSM data.

## Directory Structure

```
AutoPlaque-QSM-python/
├── main.py                        # Entry point: configuration & batch scheduling
├── requirements.txt
├── algorithms/
│   ├── __init__.py
│   ├── godec.py                   # GoDec low-rank + sparse decomposition
│   ├── rxad.py                    # Reed-Xiaoli Anomaly Detector
│   └── processing.py              # estimate_rank_svd, apply_godec, perform_rxd,
│                                  #   threshold_dssc, process_nii_roi
├── core/
│   ├── __init__.py
│   └── process_subject.py         # Per-subject pipeline orchestration
└── utils/
    ├── __init__.py
    ├── extract_neighborhoods.py   # Local patch feature extraction for RXD
    ├── extract_slice.py           # 3-D → 2-D sagittal slice extraction
    ├── find_folders_and_files.py  # Recursive paired-file discovery
    ├── file_utils.py              # find_nii_file, delete_if_exists
    ├── save_detection_results.py  # PNG / MAT persistence
    ├── mask_utils.py              # make_whole_mask, reduce_mask_size, get_neighbors
    ├── result_table.py            # init / update / save pandas result table
    └── create_nii_from_pngs.py   # Reconstruct 3-D NIfTI from per-slice PNGs
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Edit the `build_default_config()` section inside `main.py` (or supply a YAML file):

```python
cfg["path"]["parent"]    = "/path/to/your/QSM_Data"
cfg["pattern"]["qsm"]    = "qsm_mean2.nii"
cfg["pattern"]["label"]  = "166_label_V5.nii.gz"
```

2. Run:

```bash
python main.py
# or with a YAML override:
python main.py --config config.yaml
```

### Optional YAML config (`config.yaml`)

```yaml
path:
  parent: /data/QSM_Study
pattern:
  qsm: qsm_mean2.nii
  label: 166_label_V5.nii.gz
params:
  neiSize: 3
  neiOrder: 0
  energy: 0.25
  sparse: -0.02
```

## MATLAB → Python Mapping

| MATLAB file                        | Python equivalent                                  |
|------------------------------------|----------------------------------------------------|
| `algorithms/GoDec.m`               | `algorithms/godec.py` → `godec()`                 |
| `algorithms/RXAD.m`                | `algorithms/rxad.py` → `rxad()`                   |
| `algorithms/applyGoDec.m`          | `algorithms/processing.py` → `apply_godec()`      |
| `algorithms/estimateRankSVD.m`     | `algorithms/processing.py` → `estimate_rank_svd()`|
| `algorithms/performRXD.m`          | `algorithms/processing.py` → `perform_rxd()`      |
| `algorithms/thresholdDSSC.m`       | `algorithms/processing.py` → `threshold_dssc()`   |
| `algorithms/processNiiROI.m`       | `algorithms/processing.py` → `process_nii_roi()`  |
| `core/processSubject.m`            | `core/process_subject.py` → `process_subject()`   |
| `utils/extractNeighborhoods.m`     | `utils/extract_neighborhoods.py`                   |
| `utils/extractSlice.m`             | `utils/extract_slice.py`                           |
| `utils/findFoldersAndFiles.m`      | `utils/find_folders_and_files.py`                  |
| `utils/find_nii_file.m`            | `utils/file_utils.py` → `find_nii_file()`         |
| `utils/deleteIfExists.m`           | `utils/file_utils.py` → `delete_if_exists()`      |
| `utils/saveDetectionResults.m`     | `utils/save_detection_results.py`                  |
| `utils/makeWholeMask.m`            | `utils/mask_utils.py` → `make_whole_mask()`       |
| `utils/reduceMaskSize.m`           | `utils/mask_utils.py` → `reduce_mask_size()`      |
| `utils/getNeighbors.m`             | `utils/mask_utils.py` → `get_neighbors()`         |
| `utils/initResultTable.m`          | `utils/result_table.py` → `init_result_table()`   |
| `utils/updateResultTable.m`        | `utils/result_table.py` → `update_result_table()` |
| `utils/saveResults.m`              | `utils/result_table.py` → `save_results()`        |
| `utils/create_nii_from_pngs.m`     | `utils/create_nii_from_pngs.py`                   |
| `main.m`                           | `main.py`                                          |

## Key Design Notes

- **GoDec**: Pure NumPy implementation using `np.linalg.qr` and `np.argpartition`
  for efficient top-k sparse selection.
- **Erosion**: MATLAB `imerode(..., strel('disk', r))` → `skimage.morphology.erosion(disk(r))`.
- **NIfTI I/O**: `niftiread` / `niftiwrite` → `nibabel.load` / `nibabel.save`.
- **Image I/O**: `imwrite` / `imread` → `PIL.Image`.
- **Result table**: MATLAB `table` → `pandas.DataFrame`; saved as CSV.
- **Index convention**: All internal loops use 0-based indexing; the 1-based MATLAB
  slice index is converted at the `extract_slice` boundary.

## Citation

> Chen, J., Han, X., Liu, Z., Zhou, C., Hu, R., Tabassam, S., ... & Wang, N. (2025).
> *Detecting Beta-amyloid Plaque via Low Rank Based Orthogonal Projection and
> Spatial-spectrum Detector Using High-resolution Quantitative Susceptibility Mapping
> for Preclinical Studies.* IEEE Transactions on Biomedical Engineering.
