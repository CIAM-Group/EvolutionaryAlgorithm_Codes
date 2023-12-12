
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Author: Lindong Xie (Email: 12132679@mail.sustech.edu.cn)
% IEEE Transactions on Evolutionary Computation
% Surrogate-Assisted Evolutionary Algorithm with Model and Infill Criterion Auto-Configuration
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clc;
clear all;
addpath(genpath(pwd));

% Experiment Parameter
TestFuns = {'CEC05_f1'; 'CEC05_f2'; 'CEC05_f3'; 'CEC05_f4'; 'CEC05_f5'; 'CEC05_f6'; 'CEC05_f7';
    'CEC05_f8';  'CEC05_f9'; 'CEC05_f10';'CEC05_f11'; 'CEC05_f12'; 'CEC05_f13'; 'CEC05_f14'; 'CEC05_f15'; };

TestFuns2 = {'CEC15_f1'; 'CEC15_f2'; 'CEC15_f3'; 'CEC15_f4'; 'CEC15_f5'; 'CEC15_f6'; 'CEC15_f7'; 'CEC15_f8'; 'CEC15_f9'; 'CEC15_f10'; 
    'CEC15_f11'; 'CEC15_f12'; 'CEC15_f13'; 'CEC15_f14';'CEC15_f15'};   

dims =[10, 30];                          % Dimensions
Runs = 20;                               % Number of runs

d = size(dims,2);
o = length(TestFuns) + length(TestFuns2); % Two bechmark sets 

f_bias_set = [-450 -450 -450 -450 -310 390 -180 -140 -330 -330 90 -460 -130 -300 120];
f_bias_set2 = [1:15]*100; 

% runs according to dims and objs.
for i = 1:d
    for j = 1:o
        if j <= length(TestFuns)
            f_bias = f_bias_set(j);
            fname = cell2mat(TestFuns(j));                  
            FUN=@(x) feval(fname,x);
            [Xmin, Xmax] = variable_domain(fname); 
        else
            probelm_index = j-length(TestFuns);
            f_bias = f_bias_set2(probelm_index);
            fname = cell2mat(TestFuns2(probelm_index));   
            FUN= @(x)(cec15problems('eval',x,probelm_index));
            Xmin = -100;
            Xmax = 100;             
        end
        LB = repmat((Xmin),1,dims(i));             
        UB = repmat((Xmax),1,dims(i),1);
        [gsamp1,time_cost] = RUN_AutoSAEA(Runs,dims(i),FUN, LB, UB, fname, f_bias);
    end
end
save Result                     