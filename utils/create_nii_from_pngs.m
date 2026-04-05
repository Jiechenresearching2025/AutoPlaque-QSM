function create_nii_from_pngs(nifti_filename, root_folder)
    % Create a NIfTI file from PNG mask images
    
    % Step 1: Find the NIfTI file
    nifti_filename = erase(nifti_filename,'$');
    nii_file_path = find_nii_file(nifti_filename, root_folder);
    if isempty(nii_file_path)
        error('NIfTI file not found');
    end
    
    % Step 2: Load the NIfTI file
    nii_data = niftiread(nii_file_path);
    nii_info = niftiinfo(nii_file_path);
    nii_info.Datatype = 'uint8'; % Set datatype for the output mask
    
    % Step 3: Prepare an empty matrix to store the mask images
    [x, y, z] = size(nii_data);
    mask_data_1 = zeros(x, y, z, 'uint8');
    % mask_data_2 = zeros(x, y, z, 'uint8');
    % Step 4: Find all PNG mask files in the 'Results' subfolder
    [nii_folder, nii_name] = fileparts(nii_file_path);
    mask_folder = fullfile(nii_folder, 'Results'); % Path to the mask folder
    
    % Process each slice
    for i = 1:y
        mask_file = fullfile(mask_folder, sprintf('%s_%d_detection_DSSC_detection.png', [erase(nii_name, '.nii')], i));
        
        if isfile(mask_file)
            % Step 5: Load the PNG mask and process it
            mask_img = imread(mask_file);
            mask_img(mask_img>0)=1;
            mask_temp_1 = double(mask_img) .* squeeze(nii_data(:, i,:));
            % % mask_temp_2 = double(mask_img) .* squeeze(nii_data(:, i, :));
            mask_temp_1(mask_temp_1>-0.02) = 0;
            mask_temp_1(mask_temp_1<=-0.02) = 1;
            
            % mask_temp_2(mask_temp_2>0) = 1;
            % mask_temp_2(mask_temp_2<0) = 0;
            % Assuming 'BW' is your binary mask (logical array)

            % % Define the minimum object size to keep (e.g., 10 pixels)
            % minObjectSize = 1; 
            % 
            % % Remove objects smaller than minObjectSize
            % BW2 = bwareaopen(mask_temp, minObjectSize); 
            % 
            % BW2 = fillHolesForEachIsland(BW2);

            mask_data_1(:, i, :) = mask_temp_1; % Insert the mask into the 3D volume
            % mask_data_2(:, i, :) = mask_temp_2; % Insert the mask into the 3D volume
        else
            % If the mask file does not exist, the corresponding slice remains zeros
            fprintf('Mask for index %d not found. Using zero matrix.\n', i);
        end
    end
    
    % % Step 6: Save the mask data into a new NIfTI file

    mask_nii_filename = fullfile(nii_folder, [nii_name '_plaque_mask.nii.gz']);

    nii_out = nii_info;                 % copy header
    nii_out.Datatype = 'uint8';         % label image
    nii_out.BitsPerPixel = 8;           
    nii_out.Transform = nii_info.Transform;   % KEEP spatial mapping
    nii_out.PixelDimensions = nii_info.PixelDimensions;
    nii_out.ImageSize = size(mask_data_1);
    
    niftiwrite(uint8(mask_data_1), mask_nii_filename, nii_out, 'Compressed', true);
    fprintf('Created NIfTI file: %s\n', mask_nii_filename);



    %  % Step 7: Save the mask data into a new NIfTI file
    % mask_nii_filename = fullfile(nii_folder, [nii_name '_Neibor_plaque_mask.nii.gz']);
    % % you may change based on your data.
    % temp = eye(4)*0.018;
    % temp(4,4) = 1;
    % nii_info.Transform.T = temp;
    % niftiwrite(mask_data_2, mask_nii_filename, nii_info, 'Compressed', true);
    % fprintf('Created NIfTI file: %s\n', mask_nii_filename);
end



