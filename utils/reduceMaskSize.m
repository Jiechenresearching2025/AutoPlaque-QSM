function erodedMask = reduceMaskSize(binaryMask, reductionPixels)
    % Perform erosion on the binary mask
    se = strel('disk', reductionPixels);
    erodedMask = imerode(binaryMask, se);
end