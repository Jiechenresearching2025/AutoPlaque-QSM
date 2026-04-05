function processSubject(subjectFolder, subjectInfo, cfg)
% PROCESSSUBJECT Orchestrates the analysis pipeline for a single subject.
%
% This function handles I/O, slice-wise iteration, and calls the core 
% detection algorithm (processNiiROI) for amyloid plaque quantification.
%
% INPUTS:
%   subjectFolder - String, path to the subject's directory.
%   subjectInfo   - Struct, contains 'qsm' and 'label' file names.
%   cfg           - Struct, global configuration with params and patterns.

    %% 1. Path Initialization
    % Construct absolute paths for NIfTI files
    qsmFile   = fullfile(subjectFolder, string(subjectInfo.qsm));
    labelFile = fullfile(subjectFolder, string(subjectInfo.label));
    outputDir = fullfile(subjectFolder, 'Results');

    % Ensure output directory exists for telemetry (PNGs, etc.)
    if ~exist(outputDir, 'dir'), mkdir(outputDir); end

    %% 2. Data Ingestion
    % Load 3D volumes from 9.4T Bruker MRI scans
    try
        qsmVol   = niftiread(qsmFile);
        labelVol = niftiread(labelFile);
    catch ME
        fprintf('Failed to read NIfTI: %s\n', ME.message);
        return;
    end

    [~, nSlices, ~] = size(qsmVol);
    
    % Initialize the quantitative results table for target ROIs
    resTable = initResultTable(cfg.params.desiredLabels);

    %% 3. Slice-wise Analysis Loop
    fprintf('--> Analyzing subject in: %s\n', subjectFolder);

    for j = 1:nSlices
        % Identifier for current slice (used for filename persistence)
        sliceID = sprintf('%s_slice_%03d', erase(string(subjectInfo.qsm), '.nii'), j);

        % Extract the current 2D frame and corresponding mask
        [frame, mask] = extractSlice(qsmVol, labelVol, j);
        
        % Filter for the desired labels (ROIs)
        [selectedROI, binaryMask] = makeWholeMask(mask, cfg.params.desiredLabels);

        % Skip slices that do not contain any target regions of interest
        if isempty(selectedROI), continue; end

        % 4. Call Core Detection Algorithm
        % Mapping global cfg.params to the processNiiROI interface
        [detectionMap, processedImg] = processNiiROI(...
            frame .* double(binaryMask), ... % Masked QSM frame
            sliceID, ...
            outputDir, ...
            cfg.params.neiSize, ...
            1, ... % doDecomposition (Hardcoded as 1 for ADDA-style detection)
            binaryMask, ...
            cfg.params.neiOrder, ...
            cfg.params.energy, ...
            cfg.params.sparse ...
        );

        % 5. Update Global Quantitative Metrics
        resTable = updateResultTable(resTable, selectedROI, ...
                                     frame, mask, detectionMap, processedImg);
    end

    %% 6. Data Persistence
    % Save aggregated results to disk and generate secondary NIfTI outputs
    saveResults(resTable, subjectFolder, string(subjectInfo.qsm));
    create_nii_from_pngs(cfg.pattern.qsm, subjectFolder);
    
    fprintf('Analysis Complete for Subject: %s\n', subjectFolder);
end