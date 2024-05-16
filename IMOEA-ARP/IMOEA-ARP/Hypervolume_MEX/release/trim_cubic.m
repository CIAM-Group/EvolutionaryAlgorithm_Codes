% ------------------------------------------------------------------------%
% This function trims the irrelevant solutions for R-metric computation.
%
% Author: Dr. Ke Li
% Affliation: CODA Group @ University of Exeter
% Contact: k.li@exeter.ac.uk || https://coda-group.github.io/
% ------------------------------------------------------------------------%

function filtered_pop = trim_cubic(pop, centroid, range)

    [popsize, objDim] = size(pop);
    
    centroid_matrix = centroid(ones(1, popsize), :);
    
    diff_matrix = pop - centroid_matrix;

    radius      = range / 2.0;
    flag_matrix = abs(diff_matrix) < radius;
    flag_sum    = sum(flag_matrix, 2);
    
    filtered_idx = flag_sum == objDim;
    filtered_pop = pop(filtered_idx, :);

end