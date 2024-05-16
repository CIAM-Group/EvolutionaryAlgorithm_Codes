
format long

%% parameter settings
objDim     = 3;
numRun     = 8;
igdsamSize = 10000;
problem = 'eMOEA';
test = 'dtlz1_test';
w_point = 2*ones(1,objDim);

%% set trimming radius
radius = 0.2;

%% only useful for the many-objective scenario (i.e., objDim > 3)
% no_layers = 2;                  % number of layers
% no_gaps   = [3, 2];             % specify the # of divisions on each layer
% shrink_factors = [1.0, 0.5];    % shrinkage factor for each layer

%% load path
addpath(['E:\ѧϰ\PlatEMO\PlatEMO-2.7\PlatEMO\Data\',problem]);

%% initialize data structure (here we use R-NSGA-II, MOEA/D-STM as example)
IGD = zeros(numRun, 1);
HV  = zeros(numRun, 1);

for i = 1 : numRun
        %% load data
        PF = mixDTLZ1;    % true PF
        PFsize = size(PF, 1);
        file  = load([problem,'_',test,'_M3_D7_',int2str(i),'.mat']);
        pop = file.result{2};
        pf = pop.objs;
        popsize = size(pf,1);
        [IGD(i),GD(i),HV(i)] = cal_metric(pf,PF,w_point,popsize,PFsize);
end

%% mean and std of IGD and HV
mean_IGD = mean(IGD);
mean_GD = mean(GD);
mean_HV = mean(HV);
std_IGD = std(IGD);
std_GD = std(GD);
std_HV = std(HV);

%% print result
disp(problem);
%disp(['IGD = ', num2str(mean_IGD), '(', num2str(std_IGD), ')', ', HV = ', num2str(mean_HV), '(', num2str(std_HV), ')']);
disp([' IGD_mean = ', num2str(mean_IGD) ]);
disp([' IGD_std = ',num2str(std_IGD)]);
disp([' GD_mean = ', num2str(mean_GD) ]);
disp([' GD_std = ',num2str(std_GD)]);
disp([' HV_mean = ', num2str(mean_HV) ]);
disp([' HV_std = ',num2str(std_HV)]);
disp('===================================================================');

% %% Wilcoxon rank sum test
% higd_array    = -1 * ones(2, 1);
% IGD_array     = [mean_IGD_STM; mean_IGD_RNSGA2];
% [~, best_idx] = min(IGD_array);
% if best_idx == 1
%     [~, higd_array(2)] = ranksum(STM_IGD, RNSGA2_IGD);
% else
%     [~, higd_array(1)] = ranksum(RNSGA2_IGD, STM_IGD);
% end
% disp(['Wilcoxon rank sum test IGD: ' num2str(higd_array(1)), ', ', num2str(higd_array(2))]);
%
% hhv_array     = -1 * ones(2, 1);
% HV_array      = [mean_HV_STM; mean_HV_RNSGA2];
% [~, best_idx] = max(HV_array);
% if best_idx == 1
%     [~, hhv_array(2)] = ranksum(STM_HV, RNSGA2_HV);
% else
%     [~, hhv_array(1)] = ranksum(RNSGA2_HV, STM_HV);
% end
% disp(['Wilcoxon rank sum test HV : ' num2str(hhv_array(1)), ', ', num2str(hhv_array(2))]);