function [hx, hf, reward,  NFEs,  CE, gfs] = RBF_ls_arm(ghx, ghf, hx, hf, FUN, NFEs, CE, gfs)

% {RBF, local search}

        a1 = 100;
        Dim = size(hx, 2);
        Max_NFE = a1*Dim+1000; minerror = 1e-20;  %The parameter settings are consistent with the comparison algorithm-ESA

        srgtOPT=srgtsRBFSetOptions(ghx, ghf', @my_rbfbuild, [],'CUB', 0.0002,1);
        srgtSRGT = srgtsRBFFit(srgtOPT);
        flag = 1;
        [candidate_position,~, ~] = DE_optimizer(Dim,Max_NFE,srgtSRGT,minerror,ghx, flag); %Use DE search the optimum of local RBF model
        [~,ih,~] = intersect(hx,candidate_position,'rows');  

        if isempty(ih)==1
           candidate_fit=FUN(candidate_position);  % Evaluation
           NFEs = NFEs + 1;
           % save candidate into dataset, and sort dataset

           hx=[hx; candidate_position];  hf=[hf, candidate_fit];    

           % update gfs for plotting
           CE(NFEs,:)=[NFEs,candidate_fit];
           gfs(1,NFEs)=min(CE(1:NFEs,2));
           % update the low level arm reward 
           Arm = num2str('RBF_local_search ');
           [reward] = Low_level_r(ghf, hf, candidate_fit, NFEs, Arm);
        else
           reward = 0; % current database has not update 
          
        end
        
end