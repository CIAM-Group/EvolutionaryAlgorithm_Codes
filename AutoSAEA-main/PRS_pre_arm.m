function [hx, hf, reward,  NFEs,  CE, gfs] = PRS_pre_arm(ghx, ghf, offspring, hx, hf, FUN, NFEs, CE, gfs)

 % Use PRS arm with prescreening to collaboratively select infill solution 
         srgtOPT=srgtsPRSSetOptions(ghx, ghf');
         srgtSRGT = srgtsPRSFit(srgtOPT);
         % Prediction of prs
         fitnessModel    = srgtsPRSEvaluate(offspring, srgtSRGT);        
         [~,sidx]=min(fitnessModel);         % sort point based on fitness, get point indexs
         candidate_position = offspring(sidx, :);
         [~,ih,~] = intersect(hx,candidate_position,'rows');
         
         if isempty(ih)==1
            candidate_fit=FUN(candidate_position); 
            NFEs = NFEs + 1;
            hx=[hx; candidate_position];  hf=[hf, candidate_fit];       % update database
            
            % update gfs for plotting       
            CE(NFEs,:)=[NFEs,candidate_fit];
            gfs(1,NFEs)=min(CE(1:NFEs,2));
            % update the low level arm reward 
            Arm = num2str('PRS_prescreening');
            [reward] = Low_level_r(ghf, hf, candidate_fit, NFEs, Arm);

         else
             reward = 0; % current database has not update 
         end

end