function DSSC = thresholdDSSC(DSSC, threshold)
    % Apply simple thresholding to DSSC map
    DSSC(DSSC > threshold) = 255;
    DSSC(DSSC <= threshold) = 0;
end