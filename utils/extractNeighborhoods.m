function neighbors = extractNeighborhoods(img, neighborhoodSize, neighborOrder)
    % Extract local neighborhoods for RXD calculation
    halfSize = floor(neighborhoodSize / 2);
    paddedImg = padarray(img, [halfSize, halfSize], 0);
    [rowsPadded, colsPadded] = size(paddedImg);

    neighbors = zeros(rowsPadded - neighborhoodSize + 1, colsPadded - neighborhoodSize + 1, neighborhoodSize^2);

    for i = halfSize + 1 : rowsPadded - halfSize
        for j = halfSize + 1 : colsPadded - halfSize
            patch = getNeighbors(paddedImg, neighborhoodSize, i, j);
            switch neighborOrder
                case 0
                    patch = patch';
                    patch = patch(:);
                case 1
                    patch = patch(:);
                otherwise
                    patch = getDiagonalOrder(patch);
            end
            neighbors(i - halfSize, j - halfSize, :) = patch;
        end
    end

    % Reshape for RXD: (numPixels x neighborhoodSize^2)
    [x, y, z] = size(neighbors);
    neighbors = reshape(neighbors, [x, y, z]);
end