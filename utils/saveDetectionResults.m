function saveDetectionResults(outputFilePath, fileName, data, prefix, extension)
    % Helper function to save results
    outputFolderPath = fullfile(outputFilePath, strcat(fileName, '_', prefix, '.', extension));
    if strcmp(extension, 'mat')
        save(outputFolderPath, 'data');
    else
        imwrite(data, outputFolderPath);
    end
end