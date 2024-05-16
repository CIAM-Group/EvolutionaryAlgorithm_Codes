% ------------------------------------------------------------------------%
% This function is used to calculate the IGD and HV value of the solution
% set processed by R-metric.
%
% Author: Dr. Ke Li
% Affliation: CODA Group @ University of Exeter
% Contact: k.li@exeter.ac.uk || https://coda-group.github.io/
%
% Reference: K. Li, K. Deb and X. Yao, "R-Metric: Evaluating the 
% Performance of Preference-Based Evolutionary Multi-Objective Optimization 
% Using Reference Points", IEEE Trans. on Evol. Comput., accepted for
% publication, July 2017.
% ------------------------------------------------------------------------%

function [IGD,GD, HV] = cal_metric(pop, PF, w_point, popsize, PFsize)

    if popsize == 0 % if there is no useful solution, IGD and HV is -1
        IGD = -1;
        HV  = -1;
    else
        %% IGD computation
        min_dist = zeros(PFsize, 1);
        for j = 1 : PFsize
            temp    = PF(j, :);
            tempMat = temp(ones(1, popsize), :);

            temp_dist   = (tempMat - pop) .^ 2;
            distance    = sum(temp_dist, 2);
            min_dist(j) = min(distance);
        end
        min_dist_IGD = sqrt(min_dist);
        IGD      = mean(min_dist_IGD);
        
        %% GD computation
        min_dist = zeros(popsize, 1);
        for j = 1 : popsize
            temp    = pop(j, :);
            tempMat = temp(ones(1, PFsize), :);

            temp_dist   = (tempMat - PF) .^ 2;
            distance    = sum(temp_dist, 2);
            min_dist(j) = min(distance);
        end
        min_dist_GD = sqrt(min_dist);
        GD      = mean(min_dist_GD);

        %% HV computation
        HV = Hypervolume_MEX(pop, w_point); % test
    end
end