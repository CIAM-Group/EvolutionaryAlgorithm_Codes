% ------------------------------------------------------------------------%
% This script is used to calculated the R-metric, R-IGD and R-HV in
% particular, for preference-based EMO algorithms. Note that herer we only
% consider the user preference elicited as a aspiration level vector in the
% objective space.
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

close all
clear
clc

format long

%% parameter settings
objDim     = 2;
numRun     = 1;
changeRun  = 99;
igdsamSize = 10000;
problem = 'FDA3';

%% set trimming radius
radius = 0.2;

%% only useful for the many-objective scenario (i.e., objDim > 3)
% no_layers = 2;                  % number of layers
% no_gaps   = [3, 2];             % specify the # of divisions on each layer
% shrink_factors = [1.0, 0.5];    % shrinkage factor for each layer

%% load path
addpath(['E:\dynamic preference data\dynamic preference\',problem]);
addpath(['E:\dynamic preference data\NUMS\',problem]);
addpath(['E:\dynamic preference data\rNSGA2\',problem]);
addpath(['E:\dynamic preference data\gNSGA2\',problem]);
addpath(['E:\dynamic preference data\STM\',problem]);
addpath(['E:\dynamic preference data\PF\',problem,'_pf']);

%% initialize data structure (here we use R-NSGA-II, MOEA/D-STM as example)
RNSGA2_IGD = zeros(numRun*(changeRun+1), 1);
RNSGA2_HV  = zeros(numRun*(changeRun+1), 1);

GNSGA2_IGD = RNSGA2_IGD;
GNSGA2_HV  = RNSGA2_HV;

STM_IGD = RNSGA2_IGD;
STM_HV = RNSGA2_HV;

NUMS_IGD = RNSGA2_IGD;
NUMS_HV = RNSGA2_HV;

%dynamic preference
PR_IGD = RNSGA2_IGD;
PR_HV = RNSGA2_HV;

%动态PF-HV
PF_HV = RNSGA2_HV;

for i = 1 : numRun
    for t = 0 : changeRun
        disp(['第',num2str(i),'次独立实验']);
        disp(['环境变化:',num2str(t)]);
        %% generate reference point
        ref_point = zeros(1, objDim);
        ref_point(1) = (cos(0.1*pi*t)).^2 + 0.1;
        for j = 2 : objDim
            ref_point(j) = (sin(0.1*pi*t)).^2 + 0.1;
        end
        
        %% set worst point
        %w_point = ref_point + 2 * ones(1, objDim);
        w_point = ref_point + 20 * ref_point/(sum(ref_point));
        
        %% load data
        PF = load(['NUMSMOEAD_',problem,'_t',int2str(t),'.txt']);
        PFsize = size(PF, 1);
        GNSGA2  = load(['gNSGAIIdynamic_',problem,'_t', int2str(t),'_run',int2str(i),'.txt']);
        RNSGA2  = load(['rNSGAIIdynamic_',problem,'_t', int2str(t),'_run',int2str(i),'.txt']);
        NUMS  = load(['NUMS_',problem,'_t', int2str(t),'_run',int2str(i),'.txt']);
        STM  = load(['rMOEADSTM_',problem,'_t', int2str(t),'_run',int2str(i),'.txt']);
        PR  = load(['PRMOEAD_',problem,'_t', int2str(t),'_run',int2str(i),'.txt']);
        
        data = [PR; GNSGA2 ;RNSGA2 ; NUMS; STM];
        %data = [PR ;STM ; NUMS];
        
         %% filter non-dominated data
        GNSGA2  = filter_NDS(GNSGA2, data);
        RNSGA2  = filter_NDS(RNSGA2, data);
        NUMS   = filter_NDS(NUMS, data);
        PR     = filter_NDS(PR, data);
        STM     = filter_NDS(STM, data);
        
       %% 调整PF
        PF = filter_PF(PF,w_point, ref_point, radius);
        PFsize = size(PF, 1);
        PF_HV((i-1)*(changeRun+1)+t+1) = Hypervolume_MEX(PF, w_point); % test
        
        %% preprocess filtered data
        [GNSGA2, GNSGA2_size]   = preprocessing_asf(GNSGA2, ref_point, w_point, radius);
        [RNSGA2, RNSGA2_size]   = preprocessing_asf(RNSGA2, ref_point, w_point, radius);
        [NUMS, NUMS_size]         = preprocessing_asf(NUMS, ref_point, w_point, radius);
        [STM, STM_size]         = preprocessing_asf(STM, ref_point, w_point, radius);
        [PR, PR_size]         = preprocessing_asf(PR, ref_point, w_point, radius);
        
        
        %% calculate R-IGD and R-HV
        [GNSGA2_IGD((i-1)*(changeRun)+t+1), GNSGA2_HV((i-1)*(changeRun+1)+t+1)] = cal_metric(GNSGA2, PF, w_point, GNSGA2_size, PFsize);
        [RNSGA2_IGD((i-1)*(changeRun+1)+t+1), RNSGA2_HV((i-1)*(changeRun+1)+t+1)] = cal_metric(RNSGA2, PF, w_point, RNSGA2_size, PFsize);
        [NUMS_IGD((i-1)*(changeRun+1)+t+1), NUMS_HV((i-1)*(changeRun+1)+t+1)]     = cal_metric(NUMS, PF, w_point, NUMS_size, PFsize);
        [STM_IGD((i-1)*(changeRun+1)+t+1), STM_HV((i-1)*(changeRun+1)+t+1)]     = cal_metric(STM, PF, w_point, STM_size, PFsize);
        [PR_IGD((i-1)*(changeRun+1)+t+1), PR_HV((i-1)*(changeRun+1)+t+1)]        = cal_metric(PR, PF, w_point, PR_size, PFsize);
 
    end
end

%% 修正HV，仅使用于动态问题
GNSGA2_HV = PF_HV - GNSGA2_HV;
RNSGA2_HV = PF_HV - RNSGA2_HV;
NUMS_HV = PF_HV - NUMS_HV;
PR_HV = PF_HV - PR_HV;
STM_HV = PF_HV - STM_HV;

%% extract effect R-metric values
GNSGA2_IGD  = GNSGA2_IGD(GNSGA2_IGD ~= -1);
RNSGA2_IGD  = RNSGA2_IGD(RNSGA2_IGD ~= -1);
NUMS_IGD     = NUMS_IGD(NUMS_IGD ~= -1);
STM_IGD     = STM_IGD(STM_IGD ~= -1);
PR_IGD     = PR_IGD(PR_IGD ~= -1);

GNSGA2_HV  = GNSGA2_HV(GNSGA2_HV ~= -1);
RNSGA2_HV  = RNSGA2_HV(RNSGA2_HV ~= -1);
NUMS_HV     = NUMS_HV(NUMS_HV ~= -1);
STM_HV     = STM_HV(STM_HV ~= -1);
PR_HV     = PR_HV(PR_HV ~= -1);

%% mean and std of R-IGD and R-HV
mean_IGD_PR = mean(PR_IGD);
std_IGD_PR  = std(PR_IGD);
mean_HV_PR  = mean(PR_HV);
std_HV_PR   = std(PR_HV);

mean_IGD_GNSGA2 = mean(GNSGA2_IGD);
std_IGD_GNSGA2  = std(GNSGA2_IGD);
mean_HV_GNSGA2  = mean(GNSGA2_HV);
std_HV_GNSGA2   = std(GNSGA2_HV);

mean_IGD_RNSGA2 = mean(RNSGA2_IGD);
std_IGD_RNSGA2  = std(RNSGA2_IGD);
mean_HV_RNSGA2  = mean(RNSGA2_HV);
std_HV_RNSGA2   = std(RNSGA2_HV);

mean_IGD_NUMS = mean(NUMS_IGD);
std_IGD_NUMS  = std(NUMS_IGD);
mean_HV_NUMS  = mean(NUMS_HV);
std_HV_NUMS   = std(NUMS_HV);

mean_IGD_STM = mean(STM_IGD);
std_IGD_STM  = std(STM_IGD);
mean_HV_STM  = mean(STM_HV);
std_HV_STM   = std(STM_HV);

%% print result
disp(problem);
disp(['PR-MOEA/D-dynamic: R-MIGD = ', num2str(mean_IGD_PR), '(', num2str(std_IGD_PR), ')', ', R-MHV = ', num2str(mean_HV_PR), '(', num2str(std_HV_PR), ')']);
disp(['g-NSGA2: R-MIGD = ', num2str(mean_IGD_GNSGA2), '(', num2str(std_IGD_GNSGA2), ')', ', R-MHV = ', num2str(mean_HV_GNSGA2), '(', num2str(std_HV_GNSGA2), ')']);
disp(['r-NSGA2: R-MIGD = ', num2str(mean_IGD_RNSGA2), '(', num2str(std_IGD_RNSGA2), ')', ', R-MHV = ', num2str(mean_HV_RNSGA2), '(', num2str(std_HV_RNSGA2), ')']);
disp(['r-MOEA/D-STM: R-MIGD = ', num2str(mean_IGD_STM), '(', num2str(std_IGD_STM), ')', ', R-MHV = ', num2str(mean_HV_STM), '(', num2str(std_HV_STM), ')']);
disp(['NUMS-MOEA/D: R-MIGD = ', num2str(mean_IGD_NUMS), '(', num2str(std_IGD_NUMS), ')', ', R-MHV = ', num2str(mean_HV_NUMS), '(', num2str(std_HV_NUMS), ')']);
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