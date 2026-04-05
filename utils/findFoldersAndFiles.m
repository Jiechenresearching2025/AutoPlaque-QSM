function results = findFoldersAndFiles(rootDir, pattern1, pattern2)
% FINDFOLDERSANDFILES Efficiently locates paired QSM and Label files.
%
% This function performs a recursive search to identify subject folders 
% that contain both image modalities required for plaque detection.
%
% USAGE:
%   results = findFoldersAndFiles('/path/to/data', 'qsm_mean2.nii', '166_label_V5.nii.gz')

    % 1. Input Validation
    if nargin < 3
        error('QSM:InvalidInput', 'Missing required arguments: rootDir, pattern1, and pattern2.');
    end
    
    if ~exist(rootDir, 'dir')
        error('QSM:PathNotFound', 'The specified root directory does not exist: %s', rootDir);
    end

    % Initialize results structure
    results = struct('folder', {}, 'qsm', {}, 'label', {});
    
    % 2. High-Level Recursive Search
    % Perform bulk directory listing once to minimize metadata requests over network/SMB.
    fprintf('Scanning for file pairs under: %s\n', rootDir);
    allQsm   = dir(fullfile(rootDir, '**', pattern1));
    allLabel = dir(fullfile(rootDir, '**', pattern2));

    if isempty(allQsm) || isempty(allLabel)
        warning('QSM:NoMatches', 'No matching file pairs were discovered.');
        return;
    end

    % 3. Optimized In-Memory Grouping
    % Extract unique folders containing the primary QSM files to reduce processing overhead.
    qsmFolders = unique({allQsm.folder});
    idx = 1;

    % 4. Validating and Pairing Subjects
    for i = 1:numel(qsmFolders)
        currentDir = qsmFolders{i};

        % Efficiently check if this folder also contains a matching label file
        % by filtering the pre-loaded 'allLabel' list in memory.
        labelInThisFolder = allLabel(strcmp({allLabel.folder}, currentDir));
        
        if ~isempty(labelInThisFolder)
            results(idx).folder = currentDir;
            
            % Filter for QSM files in the current directory
            qsmInThisFolder = allQsm(strcmp({allQsm.folder}, currentDir));
            
            % Force output to cell arrays for downstream loop stability
            results(idx).qsm   = {qsmInThisFolder.name};
            results(idx).label = {labelInThisFolder.name};
            
            idx = idx + 1;
        end
    end
    
    fprintf('Resource Discovery Success: Identified %d subjects with paired data.\n', numel(results));
end