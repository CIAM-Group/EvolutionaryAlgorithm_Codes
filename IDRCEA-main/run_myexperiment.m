
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Code for the IDRCEA
%Copyright (c) 2023 CIAM Group@SDIM SUSTech.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clc;
clear all;
addpath(genpath(pwd));

% Experiment Parameter
TestFuns = {  'GRIEWANK'; 'ACKLEY'; 'ROSENBROCK'; 'ELLIPSOID'; 'RASTRIGIN';'CEC05_f1'; 'CEC05_f2'; 'CEC05_f3'; 'CEC05_f4'; 'CEC05_f5'; 'CEC05_f6'; 'CEC05_f7';
    'CEC05_f8';  'CEC05_f9'; 'CEC05_f10';'CEC05_f11'; 'CEC05_f12'; 'CEC05_f13'; 'CEC05_f14'; 'CEC05_f15';};

dims = [10 30 50 100];                     % Dimensions 
Runs = 20;                                 % Number of runs

d = size(dims,2);
o = length(TestFuns);

f_bias_set = [0 0 0 0 0 -450 -450 -450 -450 -310 390 -180 -140 -330 -330 90 -460 -130 -300 120]; 
% runs according to dims and objs.
for i = 1:d
    for j = 6:o
        f_bias = f_bias_set(j);
        fname = cell2mat(TestFuns(j));                  
        FUN=@(x) feval(fname,x);
        [Xmin, Xmax] = variable_domain(fname); 
        LB = repmat((Xmin),1,dims(i));             
        UB = repmat((Xmax),1,dims(i),1);
        [gsamp1,time_cost] = RUN_IDRCEA(Runs,dims(i),FUN, LB, UB, fname, f_bias);
    end
end
save Result                     