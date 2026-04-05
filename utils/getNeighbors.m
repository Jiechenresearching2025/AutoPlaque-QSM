function neighbors = getNeighbors(matrix,neighborhoodSize, row, col)
    % matrix: input matrix
    % row, col: coordinates of the current pixel
    
    % Define the size of the neighborhood
    % neighborhoodSize = 5;
    
    % Calculate the half-size of the neighborhood
    halfSize = floor(neighborhoodSize / 2);
    
    % Get the dimensions of the matrix
    [rows, cols] = size(matrix);
    
    % Initialize the neighbors matrix
    neighbors = zeros(neighborhoodSize, neighborhoodSize);
    
    % Loop through the neighborhood
    for i = -halfSize:halfSize
        for j = -halfSize:halfSize
            % Calculate the row and column indices for the current neighbor
            rowIndex = row + i;
            colIndex = col + j;
            
            % Check if the indices are within the matrix bounds
            if rowIndex >= 1 && rowIndex <= rows && colIndex >= 1 && colIndex <= cols
                % Assign the value of the current neighbor to the neighbors matrix
                neighbors(i + halfSize + 1, j + halfSize + 1) = matrix(rowIndex, colIndex);
            else
                % If the indices are out of bounds, assign a default value (e.g., 0)
                neighbors(i + halfSize + 1, j + halfSize + 1) = 0;
            end
        end
    end

end
