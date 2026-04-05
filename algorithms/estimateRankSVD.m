function lr = estimateRankSVD(img, energyThreshold)
    % Estimate low-rank value using cumulative energy from SVD
    [~, S, ~] = svd(img);
    singularValues = diag(S);
    energy = cumsum(singularValues.^2) / sum(singularValues.^2+0.000001);
    lr = find(energy >= energyThreshold, 1);
end