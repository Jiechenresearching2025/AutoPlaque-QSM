#!/bin/bash

# =================================================================
# Project: DetectionOfBetaAmyloid Restructuring Script
# Author: Jie Chen, Ph.D.
# Description: Automatically organizes files into a modular 
#              industrial-grade directory structure.
# =================================================================

echo "Starting project restructuring..."

# 1. Create directory hierarchy
mkdir -p algorithms core utils config

# 2. Move Core Algorithms (Signal Processing)
# These are your academic innovations
mv applyGoDec.m estimateRankSVD.m performRXD.m \
   thresholdDSSC.m processNiiROI.m ./algorithms/ 2>/dev/null

# 3. Move Pipeline Orchestration
# These manage the subject-level logic
mv processSubject.m findFoldersAndFiles.m ./core/ 2>/dev/null

# 4. Move Utility Functions
# Helper functions for I/O and data formatting
mv create_nii_from_pngs.m extractNeighborhoods.m extractSlice.m \
   initResultTable.m makeWholeMask.m reduceMaskSize.m \
   saveDetectionResults.m ./utils/ 2>/dev/null

# 5. Create a placeholder for README if it doesn't exist
if [ ! -f README.md ]; then
    touch README.md
    echo "# DetectionOfBetaAmyloid" >> README.md
    echo "Plaque detection pipeline for 5xFAD mouse models using 9.4T QSM." >> README.md
fi

echo "Restructuring complete!"
ls -R