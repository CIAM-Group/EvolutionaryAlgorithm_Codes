% ------------------------------------------------------------------------%
% This function preprocesses the population before R-metric computation,
% i.e., 1. Filters the irrelevant solutions; 2. Translate the trimmed
% solutions to the virture position.
%
% Author:  Dr. Ke Li @ University of Exeter
% Contact: k.li@exeter.ac.uk (https://coda-group.github.io/)
% Last modified: 25/12/2016
% ------------------------------------------------------------------------%

function [new_data, new_size] = preprocessing_asf(data, ref_point, w_point, radius)

    datasize = size(data, 1);

    if datasize == 0
        new_data = data;
        new_size = datasize;
        return;
    end

    %% Step 1: identify representative point
    ref_matrix  = ref_point(ones(1, datasize), :);
    w_matrix    = w_point(ones(1, datasize), :);
    diff_matrix = (data - ref_matrix) ./ (w_matrix - ref_matrix);
    agg_value   = max(diff_matrix, [], 2);
    [~, idx]    = min(agg_value);
    zp          = data(idx, :);

    %% Step 2: trim data
    trimed_data = trim_cubic(data, zp, radius); % trim as a cubic
    trimed_size = size(trimed_data, 1);

    %% Step 3: transfer trimmed data to the reference line
    % find k
    temp = (zp - ref_point) ./ (w_point - ref_point);
    [~, kIdx] = max(temp, [], 2);

    % find zl
    temp = (zp(kIdx) - ref_point(kIdx)) / (w_point(kIdx) - ref_point(kIdx));
    zl   = ref_point + temp * (w_point - ref_point);

    % solution transfer
    temp = zl - zp;
    shift_direction = temp(ones(1, trimed_size), :);
    new_data  = trimed_data + shift_direction;
    new_size  = size(new_data, 1);

end