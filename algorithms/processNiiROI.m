function [detectionMap, processedImg] = processNiiROI(imageFrame, sliceID, outputDir, neighborhoodSize, doDecomposition, roiMask, neighborOrder, energyThreshold, sparseThreshold)
% PROCESSNIIROI Executes GoDec decomposition and RXD detection on a QSM slice.
%
% This engine isolates amyloid plaques by decomposing the MRI signal into 
% low-rank and sparse components, followed by statistical anomaly detection.
%
% USAGE:
%   [mask, img] = processNiiROI(frame, 'idx_01', './Results', 3, 1, mask, 0, 0.25, -0.02)

    %% 1. Input Validation and Precision Management
    if nargin < 9
        error('QSM:Algorithm:InsufficientArgs', '9 input arguments are required for the detection pipeline.');
    end

    % Convert to double for high-precision linear algebra operations (SVD/GoDec)
    processedImg = double(imageFrame);
    
    %% 2. Dimensionality Reduction & Denoising (GoDec)
    % Step 1: Rank estimation via SVD cumulative energy distribution
    % This step is critical for separating background tissue from sparse plaque signals.
    estimatedRank = estimateRankSVD(processedImg, energyThreshold);

    % Step 2: Low-rank + Sparse Decomposition
    % Decomposition is only performed if a valid rank is estimated.
    if doDecomposition
        processedImg = applyGoDec(processedImg, estimatedRank, sparseThreshold);
    end

    %% 3. Feature Space Transformation
    % Normalize to [0, 255] to standardize RXD sensitivity across different 5xFAD subjects.
    processedImg = uint8(255 * mat2gray(processedImg));

    % Extract neighborhood-based feature matrix to account for local spatial correlations.
    neighbors = extractNeighborhoods(processedImg, neighborhoodSize, neighborOrder);

    %% 4. Statistical Anomaly Detection (RXD)
    % Reed-Xiaoli Detector (RXD): Identifies pixels deviating from local background statistics.
    detectionMap = performRXD(neighbors);

    %% 5. ROI Constraint & Binary Thresholding
    % Restrict detection results to the specific anatomical labels provided.
    if ~isempty(roiMask)
        detectionMap = detectionMap .* double(roiMask > 0);
    end

    % Apply adaptive thresholding to convert the probability map to a binary mask.
    % Constant 50 is the heuristic for normalized RXD maps in this framework.
    detectionMap = thresholdDSSC(detectionMap, 50);

    %% 6. Data Persistence (Telemetry)
    % Ensure output directory existence before attempting to save visualization PNGs.
    if ~exist(outputDir, 'dir'), mkdir(outputDir); end
    
    % Generate descriptive filenames for result traceability
    baseFileName = sprintf('%s_plaque_detection', string(sliceID));
    
    saveDetectionResults(outputDir, baseFileName, detectionMap, 'Plaque_Mask', 'png'); 
    saveDetectionResults(outputDir, baseFileName, ~detectionMap, 'Inverse_Mask', 'png');

end