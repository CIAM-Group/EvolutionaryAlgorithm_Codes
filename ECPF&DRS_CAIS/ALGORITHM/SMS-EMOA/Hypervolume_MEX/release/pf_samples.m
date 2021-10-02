% ------------------------------------------------------------------------%
% This function is used to obtain the PF samples for calculating the R-IGD.
% Basically, it at first samples a set of PF points from the whole PF.
% Then, it trims the data according to the DM's preference information.
%
% Author: Dr. Ke Li
% Affliation: CODA Group @ University of Exeter
% Contact: k.li@exeter.ac.uk || https://coda-group.github.io/
% ------------------------------------------------------------------------%

function [PF, PFsize] = pf_samples(objDim, no_layers, no_gaps, ...
    shrink_factors, igdsamSize, problem_id, radius, ref_point, w_point)

    % sample a set of points from the whole PF
    IGD_reference = samplingIGD(objDim, no_layers, no_gaps, ...
        shrink_factors, igdsamSize, problem_id);
    igdsamSize    = size(IGD_reference, 1);
    
    % find the representative point in the set
    ref_matrix  = ref_point(ones(1, igdsamSize), :);
    w_matrix    = w_point(ones(1, igdsamSize), :);
    diff_matrix = (IGD_reference - ref_matrix) ./ (w_matrix - ref_matrix);
    agg_value   = max(diff_matrix, [], 2);
    [~, idx]    = min(agg_value);
    target      = IGD_reference(idx, :);
    
    % find the points used to calculate the R-IGD
    PF     = trim_cubic(IGD_reference, target, radius); % trim as a cubic
    PFsize = size(PF, 1);
    
end