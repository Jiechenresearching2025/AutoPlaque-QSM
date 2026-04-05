function DSSC = performRXD(neighbors)
    % Compute RXD anomaly detection map
    [x, y, z] = size(neighbors);
    neighbors = reshape(neighbors, [x*y, z]);
    data = neighbors';
    meanVec = mean(data, 2);
    covMat = ((data - meanVec) * (data - meanVec)') / size(data, 2);
    DSSC = RXAD(data, pinv(covMat), meanVec, x, y);
end