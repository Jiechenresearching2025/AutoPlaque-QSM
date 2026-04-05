function saveResults(T, folder, baseName)
    csvFile = fullfile(folder, strcat(erase(baseName,'.nii'), '.csv'));
    matFile = fullfile(folder, strcat(erase(baseName,'.nii'), '.mat'));
    deleteIfExists(csvFile); deleteIfExists(matFile);
    writetable(T, csvFile);
    % save(matFile, 'T');
end