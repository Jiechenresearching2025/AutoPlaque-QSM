%% QSM Plaque Detection Main Entry
% Project: ADDA Framework (Amyloid Detection-Derived Analysis)
% Author: Jie Chen, Ph.D.
% Description: batch processing for plaque quantification 
%              in 5xFAD Alzheimer's mouse models using high-resolution QSM.

clear; close all;

%% [Step 1] Configuration Setup
% Centralizing parameters for maintainability and future JSON/YAML integration.
cfg = struct();

% Path Configuration
% Note: Using high-field 9.4T Bruker MRI data paths.
cfg.path.parent = "/run/user/1000/gvfs/smb-share:server=wanglab-hdd2.local,share=wanglab_hdd2/UTSW/Jie/QSM_plaque/bad";
cfg.pattern.qsm = "qsm_mean2.nii";
cfg.pattern.label = "166_label_V5.nii.gz";

% Algorithm Hyperparameters
cfg.params.desiredLabels = [1:46, 49, 53, 55, 57, 58, 65];
cfg.params.neiSize       = 3;
cfg.params.neiOrder      = 0;
cfg.params.energy        = 0.25; 
cfg.params.sparse        = -0.02;

%% [Step 2] Resource Discovery
% Search for valid data directories matching the defined patterns.
fprintf('Scanning for files in: %s\n', cfg.path.parent);
res = findFoldersAndFiles(cfg.path.parent, cfg.pattern.qsm, cfg.pattern.label);
if isempty(res)
    warning('Resource Discovery Failed: No matching NIfTI files found.');
    return;
end

%% [Step 3] Batch Processing Execution
% Iterating through subjects with error isolation to ensure pipeline stability.
for i = 1:length(res)
    subjectFolder = res(i).folder;
    
    % try
        % Modularized call to the processing engine
        processSubject(subjectFolder, res(i), cfg);
    % catch ME
    %     % Error logging without halting the entire batch
    %     fprintf('Critical Error in Folder: %s\n', subjectFolder);
    %     fprintf('Message: %s\n', ME.message);
    %     continue; 
    % end
end