function [sliceFrame, sliceMask] = extractSlice(volumeImg, volumeLbl, sliceIdx)
% EXTRACTSLICE Extracts a 2D sagittal frame and its corresponding label mask.
%
% This function performs dimension reduction from 3D to 2D while ensuring 
% numerical precision for QSM analysis and categorical integrity for labels.
%
% INPUTS:
%   volumeImg - 3D double/float matrix (MRI Volume)
%   volumeLbl - 3D uint16/categorical matrix (Label Volume)
%   sliceIdx  - Integer, the index of the column (y-axis) to extract
%
% OUTPUTS:
%   sliceFrame - 2D double matrix (Ready for GoDec/RXD)
%   sliceMask  - 2D uint16 matrix (ROI Mask)

    %% 1. Dimensionality and Index Validation
    [nRows, nCols, nSlices] = size(volumeImg);

    if sliceIdx > nCols || sliceIdx < 1
        error('QSM:ExtractSlice:BoundsError', ...
              'Index %d is out of bounds for volume with %d columns.', sliceIdx, nCols);
    end

    %% 2. Extraction and Orientation Management
    % Using squeeze to remove the singleton dimension. 
    % Note: In your pipeline, slicing is performed along the 2nd dimension (y-axis).
    try
        sliceFrame = double(squeeze(volumeImg(:, sliceIdx, :)));
        sliceMask  = uint16(squeeze(volumeLbl(:, sliceIdx, :)));
    catch ME
        error('QSM:ExtractSlice:RuntimeError', ...
              'Failed to extract slice at index %d: %s', sliceIdx, ME.message);
    end

    %% 3. Post-Extraction Integrity Check
    % Ensure the frame is not empty and dimensions are consistent
    if isempty(sliceFrame)
        warning('QSM:ExtractSlice:EmptyFrame', 'Extracted frame at index %d is empty.', sliceIdx);
    end
end