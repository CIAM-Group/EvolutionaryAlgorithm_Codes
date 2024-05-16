% ------------------------------------------------------------------------%
% This function is used to sample a set of evenly distributed weight
% vectors from a unit simplex according to the NBI paper.
%
% Author: Dr. Ke Li
% Affliation: CODA Group @ University of Exeter
% Contact: k.li@exeter.ac.uk || https://coda-group.github.io/
% ------------------------------------------------------------------------%

function W = initweight(objDim, N)
    
    U = floor(N^(1/(objDim-1)))-2;
    M = 0;
    while M<N
        U = U+1;
        M = noweight(U, 0, objDim); 
    end

    W      = zeros(objDim, M);
    C      = 0;
    V      = zeros(objDim, 1);
    [W, C] = setweight(W, C, V, U, 0, objDim, objDim);
    W      = W / (U + 0.0);

    pos     = (W < 1.0E-5);
    W(pos)  = 1.0E-5;

end

%%
function M = noweight(unit, sum, dim)

    M = 0;

    if dim == 1
        M = 1; 
        return;
    end

    for i = 0 : 1 : (unit - sum)
        M = M + noweight(unit, sum + i, dim - 1);
    end

end

%%
function [w, c] = setweight(w, c, v, unit, sum, objdim, dim)

    if dim == objdim
        v = zeros(objdim, 1);
    end

    if dim == 1
        c       = c + 1;
        v(1)    = unit - sum;
        w(:, c)  = v;
        return;
    end

    for i = 0 : 1 : (unit - sum)
        v(dim)  = i;
        [w, c]  = setweight(w, c, v, unit, sum + i, objdim, dim - 1);
    end

end
