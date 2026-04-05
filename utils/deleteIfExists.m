function deleteIfExists(filePath)
    % Check if the file exists
    if exist(filePath, 'file')
        % If the file exists, delete it
        delete(filePath);
        disp(['File "', filePath, '" deleted successfully.']);
    else
        disp(['File "', filePath, '" does not exist.']);
    end
end
