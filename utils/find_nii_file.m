function nii_file_path = find_nii_file(nifti_filename, root_folder)
    % Find the NIfTI file in the root folder
    % This function assumes a simple search implementation. Modify as needed.
    nii_files = dir(fullfile(root_folder, '**', nifti_filename));
    if ~isempty(nii_files)
        nii_file_path = fullfile(nii_files(1).folder, nii_files(1).name);
    else
        nii_file_path = [];
    end
end