% ------------------------------------------------------------------------%
% This is the function to sample weight vecotrs using multiple-layer method
%
% Author: Dr. Ke Li
% Affliation: CODA Group @ University of Exeter
% Contact: k.li@exeter.ac.uk || https://coda-group.github.io/
% ------------------------------------------------------------------------%

function W = multi_layer_weight(objDim, no_layers, no_gaps, shrink_factors)
    
    layer_sizes = zeros(1, no_layers);
    
    %% get the number of sample size on each layer
    for i = 1 : no_layers
        layer_sizes(i) = nchoosek(objDim + no_gaps(i) - 1, no_gaps(i));
    end
    
    %% weight vectors in the first layer
    cur_layer = initweight(objDim, layer_sizes(1));
    W = cur_layer';
    for i = 2 : no_layers
        %% generate a temporary layer
        temp_layer = initweight(objDim, layer_sizes(i));
        %% shrink the temporary layer (coordinate transformation)
        cur_layer = (1 - shrink_factors(i)) / objDim * ones(objDim, layer_sizes(i)) + shrink_factors(i) * temp_layer;
        %% incorporate the current layer into the whole weight vector set
        W = [W; cur_layer'];
    end
end