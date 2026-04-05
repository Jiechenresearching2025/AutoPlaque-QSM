# AutoPlaque-QSM: QSM-based Plaque Quantification Pipeline

## Overview
This repository provides a MATLAB pipeline for the automated detection and quantification of amyloid plaques in **5xFAD Alzheimer's disease mouse models**. 

Designed for high-resolution **9.4T Bruker MRI** data, the framework utilizes **GoDec (Low-Rank + Sparse Decomposition)** and **RXD (Reed-Xiaoli Detector)** algorithms. It is specifically optimized to differentiate AD phenotypes by quantifying plaque burden and spatial distribution across various anatomical regions.

## Key Features
- **Modular Architecture**: Clear separation of `algorithms/`, `core/`, and `utils/` for professional-grade maintainability.
- **Advanced Signal Processing**: Leverages GoDec to isolate sparse plaque signals from complex 9.4T MRI backgrounds.
- **Automated Batch Processing**: Efficiently handles large datasets with robust error handling and recursive file discovery.
- **ROI-specific Metrics**: Provides detailed quantification (volume and susceptibility) for specific brain labels.

## Directory Structure
```text
DetectionOfBetaAmyloid/
├── main.m                 # Entry point: User configuration and batch scheduling
├── algorithms/            # Core Algorithms: GoDec, RXD, SVD Rank Estimation
├── core/                  # Pipeline Logic: Subject orchestration and file discovery
├── utils/                 # Helper Functions: NIfTI I/O, Masking, and Table Init
└── setup_project.sh       # Automation script for directory restructuring

## Getting Started

### 1. Prerequisites
- **MATLAB**: R2024b or later is recommended.
- **Toolboxes**: **Image Processing Toolbox** (required for morphological operations).

### 2. Installation
1. Clone the repository to your local machine:
   \`\`\`bash
   git clone https://github.com/Jiechenresearching2025/AutoPlaque-QSM.git
   cd AutoPlaque-QSM
   \`\`\`
2. (Optional) Run the restructuring script to ensure folders are set up correctly:
   \`\`\`bash
   chmod +x setup_project.sh
   ./setup_project.sh
   \`\`\`

### 3. Usage
1. Open MATLAB and navigate to the project root.
2. Edit \`main.m\` to configure your data paths:
   \`\`\`matlab
   cfg.path.parent = '/path/to/your/QSM_Data'; 
   cfg.pattern.qsm = 'qsm_mean2.nii';
   \`\`\`
3. Run \`main.m\`. The script will:
   - Automatically add all sub-folders to the MATLAB path.
   - Scan for subject folders containing both QSM and Label files.
   - Process each slice and save results in a \`Results\` sub-folder for each subject.

### 4. Output
Within each subject's \`Results\` directory, the pipeline generates:
- **Plaque Detection Maps**: PNG visualizations of detected areas.
- **Quantitative Table**: A \`.mat\` file containing volume and mean susceptibility for each ROI.
- **Reconstructed NIfTI**: 3D detection volumes for further neuroimaging analysis.

## Research & Citation
This pipeline is part of the research presented in:
> *Chen, J., Han, X., Liu, Z., Zhou, C., Hu, R., Tabassam, S., ... & Wang, N. (2025). Detecting Beta-amyloid Plaque via Low Rank Based Orthogonal Projection and Spatial-spectrum Detector Using High-resolution Quantitative Susceptibility Mapping for Preclinical Studies. IEEE Transactions on Biomedical Engineering.**.*

## Author
**Jie Chen, Ph.D.** MRI Physics, Electrical Engineering & Neuroimaging  
EOF

# 
git add README.md
git commit -m "docs: write comprehensive README.md and sync to GitHub"
git push origin main