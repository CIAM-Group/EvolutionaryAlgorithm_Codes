function [hx, hf, reward, NFEs, CE, gfs] = GP_ei_arm(ghx, ghf, offspring, hx, hf, FUN, NFEs, CE, gfs)

% {GP, EI}
      
try       
         theta =[];
         t_s = [ghx, ghf'];
         D = size(ghx, 2);
         [t_s, ~,~] = unique(t_s, 'rows'); 
         ghx = t_s(:, 1:D);
         ghf = t_s(:, D+1);
         try
            [dmodel, ~]=...
             dacefit_3(ghx,ghf,@regpoly0,@corrgauss,theta);
         
         catch
            [dmodel, ~]=...
            dacefit_3(ghx,ghf,@regpoly0,@corrgauss,theta);
         end

         Gbest = min(hf);
         for i = 1 : size(offspring, 1)
             [y,~, mse, ~] =  predictor(offspring(i, :),dmodel); 
             s         = sqrt(mse);
             EI(i)     = -(Gbest-y)*normcdf((Gbest-y)/s)-s*normpdf((Gbest-y)/s);
         end
         [~,I] = min(EI);
         candidate_position = offspring(I, :);
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
            Arm = num2str('GP_ei ');
            [reward] = Low_level_r(ghf, hf, candidate_fit, NFEs, Arm);

         else
             reward = 0;
         end
         
catch
         reward = 0;
end

end