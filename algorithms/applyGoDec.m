function img = applyGoDec(img, rank, sparseThreshold)
    % Apply GoDec decomposition to denoise image
    [rows, ~] = size(img);
    rareCount = sum(img(:) < sparseThreshold);
    [L, S] = GoDec(img, rank, rareCount, 2);
    % Projection to remove low-rank component
    P = eye(rows) - L * pinv(L' * L) * L';
    img = P * (L + S);
end