function [selLabels, maskWhole] = makeWholeMask(mask, desiredLabels)
    labels = unique(mask);
    selLabels = labels(ismember(labels, desiredLabels));
    maskWhole = uint8(ismember(mask, selLabels));
    maskWhole = reduceMaskSize(maskWhole, 3);
end