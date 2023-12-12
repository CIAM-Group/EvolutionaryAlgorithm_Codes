function [hf,MaxFEs,gfs,s_l_s] = AutoSAEA(FUN,D,LB,UB)

%% -------------- initialization----------------------
F=0.5;%control parameter for DE
CR=0.9;
apha = 2.5; % parameter for UCB
level = 5;  % parameter of L1 criterion for KNN 
initial_sample_size=100;    % ppopulation
NFEs=0;
MaxFEs=1000; 
CE=zeros(MaxFEs,2);
gfs = zeros(1,MaxFEs);
VRmin=repmat(LB,initial_sample_size,1);
VRmax=repmat(UB,initial_sample_size,1);
% -------------- generate initial samples-----------------------
gs = initial_sample_size;
sam=repmat(LB,initial_sample_size,1)+(repmat(UB,initial_sample_size,1)-repmat(LB,initial_sample_size,1)).*lhsdesign(initial_sample_size,D);

for i=1:initial_sample_size
    fitness(i) = FUN(sam(i,:));
    NFEs=NFEs+1;
    CE(NFEs,:)=[NFEs,fitness(i)];
    gfs(1,NFEs)=min(CE(1:NFEs,2));
end
hx=sam; hf=fitness;
id = 0;
% reward initialization
rbf_model = [];
gp_model =[];
knn_model =[];
prs_model =[];

Save_rp =[];
Save_rl = [];
Save_gl =[];
Save_ge = [];
Save_pp =[];
Save_pl =[];
Save_ki =[];
Save_ko =[];

num_arm = 8; % Number of combinatorial arms
in1 = randperm(num_arm); 
% -------------- Main loop -----------------------
while NFEs < MaxFEs
      id = id +1;  % recorde the number of loop 
      [~, sort_index] = sort(hf);
      ghf=hf(sort_index(1:gs));     ghx=hx(sort_index(1:gs),:); % Current population
      %% Select the t-th combinatorial arm
      if id <= num_arm
         if id == 1
            % -------------- {RBF, prescreening}----------------------
            offspring = DEoperator(ghx,gs,D,ghx,F,CR,VRmax,VRmin); % DE geneate offspring
            [hx, hf, reward_rp, NFEs, CE, gfs] = RBF_pre_arm(ghx, ghf, offspring, hx, hf, FUN, NFEs, CE, gfs);
            Save_rp = [Save_rp, reward_rp];
            rbf_model = [rbf_model;reward_rp];
            
         elseif id ==2
            % -------------- {GP, LCB} ----------------------
            offspring = DEoperator(ghx,gs,D,ghx,F,CR,VRmax,VRmin); % DE geneate offspring
            [hx, hf, reward_gl, NFEs, CE, gfs] = GP_lcb_arm(ghx, ghf, offspring, hx, hf, FUN, NFEs, CE, gfs);
            Save_gl = [Save_gl, reward_gl];
            gp_model =[gp_model; reward_gl];
            
         elseif id == 3 
            % -------------- {RBF, local search} ----------------------
            [hx, hf, reward_rl, NFEs,  CE, gfs] = RBF_ls_arm(ghx, ghf, hx, hf, FUN, NFEs, CE, gfs);
            Save_rl = [Save_rl, reward_rl];
            rbf_model = [rbf_model;reward_rl];
            
         elseif id == 4    
             % -------------- {GP, EI}----------------------
            offspring = DEoperator(ghx,gs,D,ghx,F,CR,VRmax,VRmin); % DE geneate offspring
            [hx, hf, reward_ge, NFEs, CE, gfs] = GP_ei_arm(ghx, ghf, offspring, hx, hf, FUN, NFEs, CE, gfs);
            Save_ge = [Save_ge, reward_ge];
            gp_model =[gp_model; reward_ge]; 
                        
         elseif id == 5
             % -------------- PRS prescreening----------------------
            offspring = DEoperator(ghx,gs,D,ghx,F,CR,VRmax,VRmin); 
            [hx, hf, reward_pp, NFEs, CE, gfs] = PRS_pre_arm(ghx, ghf, offspring, hx, hf, FUN, NFEs, CE, gfs);
            Save_pp = [Save_pp, reward_pp];
            prs_model = [prs_model;reward_pp];
            
         elseif id == 6 
             % -------------- {PRS,  local search}----------------------
            [hx, hf, reward_pl, NFEs, CE, gfs] = PRS_ls_arm(ghx, ghf, hx, hf, FUN, NFEs, CE, gfs);
            Save_pl = [Save_pl, reward_pl];
            prs_model = [prs_model;reward_pl];
            
         elseif id == 7
            % -------------- {KNN, L1-exploitation}----------------------
            offspring = DEoperator(ghx,gs,D,ghx,F,CR,VRmax,VRmin); 
            [hx, hf, reward_ki ,NFEs, CE, gfs] = KNN_eoi_arm(ghx, ghf, offspring, hx, hf, FUN, NFEs, level, CE, gfs);  
            Save_ki = [Save_ki, reward_ki];
            knn_model = [knn_model;reward_ki];
            
         elseif id == 8
            % -------------- {KNN, L1-exploration}----------------------
            offspring = DEoperator(ghx,gs,D,ghx,F,CR,VRmax,VRmin);
            [hx, hf, reward_ko ,NFEs, CE, gfs] = KNN_eor_arm(ghx, ghf, offspring, hx, hf, FUN, NFEs, level, CE, gfs);   
            Save_ko = [Save_ko, reward_ko];
            knn_model = [knn_model;reward_ko];

         end
      
      else

      %%  elect the high-level arm and low-level arm by TL-UCB 
          for i = 1 : 4
              if i ==1
                sum_reward = rbf_model;
                q_value_m = mean(rbf_model); % The value of RBF
              elseif i ==2 
                sum_reward = gp_model; 
                q_value_m = mean(gp_model);  % The value of GP
              elseif i ==3 
                sum_reward = prs_model; 
                q_value_m = mean(prs_model); % The value of PRS
              elseif i ==4
                sum_reward = knn_model; 
                q_value_m = mean(knn_model); % The value of KNN
              end
              U_model_value(i) = TL_UCB(sum_reward, id, q_value_m, apha);  % calculate UCB value of high-level arms
          end
          idx = find(U_model_value == max(U_model_value));
          if length(idx) >= 1 % if the max value of UCB exceed one arm, then select the arm at random
             in6 = randperm(size(idx, 1));
             idx = idx(in6(1));
          end
          
          if idx == 1 % RBF is selected at the first level arm
             for i =1 : 2
                 if i == 1
                    sum_reward = Save_rp;
                    q_value = mean(Save_rp);

                 elseif i ==2 
                    sum_reward = Save_rl; 
                    q_value = mean(Save_rl);

                 end
                 U_rbf_value(i) = TL_UCB(sum_reward, id, q_value, apha);  % calculate UCB values of low-level arms associated with the RBF
             end
             idx2 = find(U_rbf_value == max(U_rbf_value));
             if length(idx2) >= 1 % if the max value of UCB exceed one arm, then select the arm at random
                in6 = randperm(size(idx2, 1));
                idx2 = idx2(in6(1));
             end
             if idx2 == 1 
                  % -------------- {RBF, prescreening}----------------------
                offspring = DEoperator(ghx,gs,D,ghx,F,CR,VRmax,VRmin); 
                [hx, hf, reward_rp, NFEs,  CE, gfs] = RBF_pre_arm(ghx, ghf, offspring, hx, hf, FUN, NFEs, CE, gfs);
                Save_rp = [Save_rp, reward_rp]; 
                rbf_model = [rbf_model;reward_rp];

              elseif idx2 == 2 
                   % -------------- {RBF, local search}----------------------
                 [hx, hf, reward_rl,  NFEs,  CE, gfs] = RBF_ls_arm(ghx, ghf, hx, hf, FUN, NFEs, CE, gfs);
                 Save_rl = [Save_rl, reward_rl];
                 rbf_model = [rbf_model; reward_rl];

              end
          elseif idx == 2
             for i = 1 : 2
                 if i == 1
                    sum_reward = Save_gl;
                    q_value =  mean(Save_gl);

                 elseif i ==2 
                    sum_reward = Save_ge; 
                    q_value = mean(Save_ge); 

                 end
                 U_gp_value(i) = TL_UCB(sum_reward, id, q_value, apha);  % calculate UCB values of low-level arms associated with the gp
             end
             idx3 = find(U_gp_value == max(U_gp_value));
             if length(idx3) >= 1 
                 in6 = randperm(size(idx3, 1));
                 idx3 = idx3(in6(1));
             end
             if idx3 == 1 
                  % -------------- {GP, LCB}----------------------
                  offspring = DEoperator(ghx,gs,D,ghx,F,CR,VRmax,VRmin);
                  [hx, hf, reward_gl, NFEs, CE, gfs] = GP_lcb_arm(ghx, ghf, offspring, hx, hf, FUN, NFEs, CE, gfs);
                  Save_gl = [Save_gl, reward_gl];
                  gp_model =[gp_model; reward_gl]; 

             elseif idx3 == 2 
                 % -------------- {GP, EI}----------------------
                 offspring = DEoperator(ghx,gs,D,ghx,F,CR,VRmax,VRmin); 
                 [hx, hf, reward_ge, NFEs, CE, gfs] = GP_ei_arm(ghx, ghf, offspring, hx, hf, FUN, NFEs, CE, gfs);              
                 Save_ge = [Save_ge, reward_ge];
                 gp_model =[gp_model; reward_ge];

             end
          elseif idx == 3
              for i = 1 : 2
                  if i == 1
                    sum_reward = Save_pp;
                    q_value = mean(Save_pp);
                  elseif i ==2 
                    sum_reward = Save_pl; 
                    q_value = mean(Save_pl);
                  end
                  U_prs_value(i) = TL_UCB(sum_reward, id, q_value, apha);  % calculate UCB values of low-level arms associated with the prs 
              end
              idx4 = find(U_prs_value == max(U_prs_value));
              if length(idx4) >= 1 % if the max value of UCB exceed one arm, then select the arm at random
                 in6 = randperm(size(idx4, 1));
                 idx4 = idx4(in6(1));
              end
              if idx4 == 1
                  % -------------- {PRS, Prescreening}----------------------
                 offspring = DEoperator(ghx,gs,D,ghx,F,CR,VRmax,VRmin); % DE geneate offspring         
                 [hx, hf, reward_pp, NFEs, CE, gfs] = PRS_pre_arm(ghx, ghf, offspring, hx, hf, FUN, NFEs, CE, gfs);
                 Save_pp = [Save_pp, reward_pp];
                 prs_model = [prs_model;reward_pp];

              elseif idx4 == 2 
                 % -------------- {PRS, local search}----------------------
                [hx, hf, reward_pl, NFEs, CE, gfs] = PRS_ls_arm(ghx, ghf, hx, hf, FUN, NFEs, CE, gfs);
                Save_pl = [Save_pl, reward_pl];
                prs_model = [prs_model;reward_pl];

              end  
          elseif idx == 4 
              for i = 1 : 2
                  if i == 1
                    sum_reward = Save_ki ;
                    q_value = mean(Save_ki);
                 elseif i ==2 
                    sum_reward = Save_ko ; 
                    q_value = mean(Save_ko);
                 end      
                 U_knn_value(i) = TL_UCB(sum_reward, id, q_value, apha);   % calculate UCB values of low-level arms associated with the knn 
              end
              idx5 = find(U_knn_value == max(U_knn_value));
              if length(idx5) >= 1 % if the max value of UCB exceed one arm, then select the arm at random
                  in6 = randperm(size(idx5, 1));
                  idx5 = idx5(in6(1));
              end 

              if idx5 == 1
                   % -------------- {KNN, L1-exploitation}----------------------
                 offspring = DEoperator(ghx,gs,D,ghx,F,CR,VRmax,VRmin); % DE geneate offspring  
                 [hx, hf, reward_ki ,NFEs, CE, gfs] = KNN_eoi_arm(ghx, ghf, offspring, hx, hf, FUN, NFEs, level, CE, gfs);   
                 Save_ki = [Save_ki, reward_ki];
                 knn_model = [knn_model;reward_ki];
                 
              elseif idx5 == 2 
                  % -------------- {KNN, L1-exploration}----------------------
                 offspring = DEoperator(ghx,gs,D,ghx,F,CR,VRmax,VRmin); % DE geneate offspring
                 [hx, hf, reward_ko, NFEs, CE, gfs] = KNN_eor_arm(ghx, ghf, offspring, hx, hf, FUN, NFEs, level, CE, gfs);   
                 Save_ko = [Save_ko , reward_ko];
                 knn_model = [knn_model;reward_ko];

              end 
              if NFEs > 1000
                 break 
              end 
          end                 
     end
end
end