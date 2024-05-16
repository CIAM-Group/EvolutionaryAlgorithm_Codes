% ------------------------------------------------------------------------%
% This is the main function to sample expected number of weight vectors on 
% the PF of a given test problem.
%
% Author: Dr. Ke Li
% Affliation: CODA Group @ University of Exeter
% Contact: k.li@exeter.ac.uk || https://coda-group.github.io/
% ------------------------------------------------------------------------%

function P = samplingIGD(objDim, no_layers, no_gaps, shrink_factors, sample_size, id)

    %% generate the reference vectors
    if objDim < 15
        W = initweight(objDim, sample_size);
        W = W';
    else
        W = multi_layer_weight(objDim, no_layers, no_gaps, shrink_factors);
    end
    
    %% ZDT1
    if id == 1
        step    = 1 / (sample_size - 1);
        P       = zeros(sample_size, objDim);
        f1      = 0 : step : 1;
        P(:, 1) = f1';
        P(: ,2) = ones(sample_size, 1) - sqrt(P(:, 1));
    %% ZDT2
    elseif id == 2
        step    = 1 / (sample_size - 1);
        P       = zeros(sample_size, objDim);
        f1      = 0 : step : 1;
        P(:, 1) = f1';
        P(: ,2) = ones(sample_size, 1) - P(:, 1).^2;
    %% ZDT3
    elseif id == 3
        step    = 1.0 / (sample_size - 1);
        f1      = 0 : step : 1;
        P(:, 1) = f1;
        P(:, 2) = 1 - sqrt(f1) - f1 .* sin(10 * pi * f1);
        P       = find_nondominated(P, 2);
    %% DTLZ1
    elseif id == 4
        denominator = sum(W, 2);
        deMatrix = denominator(:, ones(objDim, 1));
        
        P = W ./ (2 * deMatrix);
    %% DTLZ2 - DTLZ4
    elseif id == 5
        tempW = W .* W;
        denominator = sum(tempW, 2);
        deMatrix = denominator(:, ones(objDim, 1));

        P = W ./ sqrt(deMatrix);
    %% DTLZ5 - DTLZ6
    elseif id == 6
        theta = [0 : 1 / (sample_size - 1) : 1];
        f1    = cos(theta * pi / 2) * cos(pi / 4);
        f2    = cos(theta * pi / 2) * sin(pi / 4);
        f3    = sin(theta * pi / 2);
        
        P = zeros(sample_size, objDim);
        P(:, 1) = f1';
        P(:, 2) = f2';
        P(:, 3) = f3';
    %% DTLZ7
    elseif id == 7
        step = sqrt(sample_size);
        f1 = 0 : 1 / (step - 1) : 1;
        f2 = f1;

        P = zeros(step * step, objDim);
        for i = 1 : step
            for j = 1 : step
                idx = (i - 1) * step + j;
                P(idx, 1) = f1(i);
                P(idx, 2) = f2(j);
            end
        end
        t1 = P(:, 1) .* (ones(sample_size, 1) + sin(3 * pi * P(:, 1)));
        t2 = P(:, 2) .* (ones(sample_size, 1) + sin(3 * pi * P(:, 2)));
        P(:, 3) = 3 - t1 - t2;
        P = find_nondominated(P, objDim);
    elseif id == 8
        step    = 1 / (sample_size - 1);
        P       = zeros(sample_size, objDim);
        f1      = 0 : step : 1;
        P(:, 1) = f1';
        P(: ,2) = ones(sample_size, 1) - P(:, 1);
    else
        error('Bad id!');
    end
    
end

%% Find out the dominance relationship between 'a' and 'b'
function x = dominated_relationship(a, b, m)
% Input Parameters :  a->ind1; b->ind2; m-># of objectives??
% Output Parameters: 1->a dominates b; 2->b dominates a; 3->a equals b;
% 4->a and b are non-dominated to each other

    t = 0;
    q = 0;
    p = 0;

    e = 0.00001;
    for i = 1 : m
        if a(i) <= b(i)
            t = t + 1;
        end
        if  a(i) >= b(i)
            q = q + 1;
        end
        if  a(i) == b(i)
            p = p + 1;
        end
    end
    
    if t == m & p ~= m
        x = 1;
    elseif q == m & p ~= m
        x = 2;
    elseif p == m
        x = 3;
    else
        x = 4;
    end
end

%% Find out the non-dominated solutions in 'POP'
function NPOP = find_nondominated(POP, m)
% Input Parameter : POP->population; m-># of objectives
% Output Parameter: NPOP->non-dominated solutions

i = 1;
while i <= size(POP, 1)
    flag = 0;
    j = i + 1;
    while j <= size(POP, 1)
        x = dominated_relationship(POP(i, :), POP(j, :), m);
        if x == 2
            flag = 1;
            break;
        elseif x == 3
            POP(j, :) = [];
        elseif x == 1
            POP(j, :) = [];
        else
            j = j + 1;
        end
    end
    if flag == 1
        POP(i, :) = [];
    else
        i = i + 1;
    end
end
NPOP = POP;
end