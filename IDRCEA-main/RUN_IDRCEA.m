function [gsamp1 ,time_cost] = RUN_IDRCEA(runs, D, FUN, LB, UB, fname,f_bias)
time_begin=tic;
warning('off');
addpath(genpath(pwd));

for r=1:runs
    % main loop
    fprintf('\n');
    disp(['FUNCTION: ', fname,' RUN: ', num2str(r)]);  
    fprintf('\n');
    [hisf,mf,gfs]= IDRCEA(FUN,D,LB,UB); 
    fprintf('Best fitness (PSO-final): %e\n',min(hisf));       
    gsamp1(r,:)=gfs(1:mf);
end    

%%%%%%%%%%%%%%%%%%%%% Output options %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
samp_mean   = mean(gsamp1(:,end));
samp_mean_error = samp_mean - f_bias;
std_samp    = std(gsamp1(:,end));
gsamp1_ave  = mean(gsamp1,1);

% Time Complexity
time_cost=toc(time_begin);
save(strcat('result/NFE',num2str(mf),'_',fname,' runs=',num2str(runs),' Dim=',num2str(D)));
end
