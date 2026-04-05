function T = updateResultTable(T, selLabels, frame, mask, detRes, lowrankImg)
    for k = 1:length(selLabels)
        idx = find(T.LabelNumber == selLabels(k));
        binaryMask = (mask == selLabels(k));

        % Volumes
        T.LabelVolume(idx) = T.LabelVolume(idx) + nnz(binaryMask);
        plaqueMask = binaryMask & (detRes > 0);
        T.PlaqueVolume(idx) = T.PlaqueVolume(idx) + nnz(plaqueMask);
        T.NonPlaqueVolume(idx) = T.LabelVolume(idx) - T.PlaqueVolume(idx);

        % Values
        T.PlaqueValueInMRI(idx)     = T.PlaqueValueInMRI(idx) + sum(frame(plaqueMask));
        T.PlaqueValueInLowrank(idx) = T.PlaqueValueInLowrank(idx) + sum(lowrankImg(plaqueMask));
        T.NonPlaqueValueInMRI(idx)  = T.NonPlaqueValueInMRI(idx) + sum(frame(binaryMask & ~plaqueMask));
        T.NonPlaqueValueInLowrank(idx) = T.NonPlaqueValueInLowrank(idx) + sum(lowrankImg(binaryMask & ~plaqueMask));
    end
end