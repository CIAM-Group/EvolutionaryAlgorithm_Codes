function [hx, hf, reward,  NFEs,  CE, gfs] = RBF_pre_arm(ghx, ghf, offspring, hx, hf, FUN, NFEs, CE, gfs)
 % {RBF, prescreening}   
         srgtOPT=srgtsRBFSetOptions(ghx, ghf', @my_rbfbuild, [],'CUB', 0.0002,1);
         srgtSRGT = srgtsRBFFit(srgtOPT);
         % Prediction by rbf
         fitnessModel= my_rbfpredict(srgtSRGT.RBF_Model, srgtSRGT.P, offspring);
         [~,sidx]=min(fitnessModel);         % Get the best point indexs
         candidate_position = offspring(sidx, :);
         [~,ih,~] = intersect(hx,candidate_position,'rows');  
         
         if isempty(ih)==1
            candidate_fit=FUN(candidate_position);  % Evaluation
            NFEs = NFEs + 1;
            % save candidate into dataset, and sort dataset
            hx=[hx; candidate_position];  hf=[hf, candidate_fit];       % update history database
            % update CE for plotting
            CE(NFEs,:)=[NFEs,candidate_fit];
            gfs(1,NFEs)=min(CE(1:NFEs,2));
            % update the low level arm reward 
            Arm = num2str('RBF_prescreening ');
            [reward] = Low_level_r(ghf, hf, candidate_fit, NFEs, Arm);
         else
             reward = 0; % current database has not update 
         end

end