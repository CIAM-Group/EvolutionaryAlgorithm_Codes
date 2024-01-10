function On_GMMOR(Global)
% <algorithm> <O>
% On_GMMOR
% beta --- 0.1 --- Determine the number of gap generations 
% Kmax --- 5 --- The maximum number of clusters

%------------------------------- Reference --------------------------------
% G. Li, Z. Wang, Q. Zhang, and J. Sun, Offline and Online Objective
% Reduction via Gaussian Mixture Model Clustering, IEEE Transactions on
% Evolutionary Computation, 2023, 27(2): 341-354.
%------------------------------- Copyright --------------------------------
% Copyright (c) 2018-2019 BIMK Group. You are free to use the PlatEMO for
% research purposes. All publications which use this platform or any code
% in the platform should acknowledge the use of "PlatEMO" and reference "Ye
% Tian, Ran Cheng, Xingyi Zhang, and Yaochu Jin, PlatEMO: A MATLAB platform
% for evolutionary multi-objective optimization [educational forum], IEEE
% Computational Intelligence Magazine, 2017, 12(4): 73-87".
%--------------------------------------------------------------------------

%% parameters of On-GMMOR
[beta,Kmax]= Global.ParameterSet(0.1,5);
Ggap=ceil(beta*Global.maxgen);
%regularization parameter lambda in HLHA
Lambda=1;
%% Generate random population
Population = Global.Initialization(); 
%% The initial objective set: include all objectives
All_Fs=[1:Global.M];
%% The flag is used to indicate whether optimize all objectives 
All_objective = true; 
while Global.NotTermination(Population)       
      %% Approximation stage
       if All_objective   
          %% The non-dominated ranking and CrowdDis of each solution
           [Population,FrontNo,CrowdDis] = EnvironmentalSelection_OR(Population,Global.N,All_Fs);         
           MatingPool = TournamentSelection(2,Global.N,FrontNo,-CrowdDis);
           Offspring  = GA(Population(MatingPool));          
           [Population,FrontNo,~] = EnvironmentalSelection_OR([Population,Offspring],Global.N,All_Fs);           
          %% Objective Reudction   
           if all(FrontNo==1)
              [K, Fs, P]=GMMOR(Population,All_Fs, Lambda,Kmax);
              All_objective=false;
              Reduce_flag(1:K)=true;
           end
       end
     
       %% Optimize each subproblem
       if ~All_objective    
           for k=1:K
               %% optimization
                Population_k=P{k};                         
                if rand<1-Global.gen/Global.maxgen
                   [Population,FrontNo,CrowdDis] = EnvironmentalSelection_OR(Population,Global.N,Fs{k});
                   if length(Population_k)==1
                      MatingPool = TournamentSelection(2,length(Population_k)+1,FrontNo,-CrowdDis);  
                   else
                      MatingPool = TournamentSelection(2,length(Population_k),FrontNo,-CrowdDis); 
                   end
                   Offspring  = GA(Population(MatingPool));
                else
                   [Population_k,FrontNo_k,CrowdDis_k] = EnvironmentalSelection_OR(Population_k,length(Population_k),Fs{k});                   
                   if length(Population_k)==1
                      MatingPool = TournamentSelection(2,length(Population_k)+1,FrontNo_k,-CrowdDis_k);
                   else
                     MatingPool = TournamentSelection(2,length(Population_k),FrontNo_k,-CrowdDis_k);
                   end
                   Offspring  = GA(Population_k(MatingPool));
                end
                [Population_k,~] = EnvironmentalSelection_OR([Population_k,Offspring],length(Population_k),Fs{k});                 
                P{k}=Population_k;              
              %% objective reduction
                if length(Fs{k})>3 && Reduce_flag(k)
                    [~,FrontNo,~] = EnvironmentalSelection_OR(Population_k,length(Population_k),Fs{k});
                    if sum(FrontNo==1)==length(Population_k)
                      Objectives=Population_k.objs;  
                      Objectives=Objectives(:,Fs{k});
                      new_Fs=LHA(Objectives,Lambda);
                      RFs=Fs{k}(new_Fs);
                      if length(RFs)==length(Fs{k})
                        if all(RFs==Fs{k})
                           Reduce_flag(k)=false;
                        end
                      end
                      Fs{k}=RFs;
                    end      
                end
           end   
          %% return to all objectives
           if mod(Global.gen,Ggap)==0
              All_objective=true;              
           end  
           
           Population=[];
           for k=1:K
               Population=[Population,P{k}];
           end          
           K
           for k=1:K
              Fs{k}        
           end
           disp('*****')
       end

      
       
          
      
       
    
%       %% identification phase 
%       for k=1:K
%           Population_k=P{k};
% %           [~,FrontNo,CrowdDis] = EnvironmentalSelection_OR(Population_k,length(Population_k),Fs{k});          
% %           MatingPool = TournamentSelection(2,length(Population_k),FrontNo,-CrowdDis);
% %           Offspring  = GA(Population_k(MatingPool));
% %           [Population_k,~,~] = EnvironmentalSelection_OR([Population_k,Offspring],length(Population_k),Fs{k});
% %           
%           [Population,Fitness] = EnvironmentalSelection_OR_SDE(Population,Global.N,Fs{k});
%            MatingPool = TournamentSelection(2,length(Population_k),Fitness);
%            Offspring  = GA(Population(MatingPool));
%           [Population_k,~] = EnvironmentalSelection_OR_SDE([Population_k,Offspring],length(Population_k),Fs{k});
%           
%           P{k}=Population_k;
%           Population(Index{k})=Population_k;
%       end
%       if mod(Global.gen,G1)==0;
%          for k=1:K
%              Population_k=P{k};
%              Objectives=Population_k.objs;  
%              Objectives=Objectives(:,Fs{k});
%              new_Fs=NLHA(Objectives,Lambda);
%              Fs{k}=Fs{k}(new_Fs);
%          end
%       end     
%       
      
     

%       if phase && mod(Global.gen,Ggap)==0
%          % Change to the partitioning phase GMMOR
%          [K, Index, Fs, P]   = GMMOR(Population,Lambda,Kmax)
%          phase = false;   
%       elseif ~phase && mod(Global.gen,Ggap)==0
%          % Change to the approximation phase
%          K=1; Fs{1}=[1:Global.M];Index{1}=[1:Global.N]; P{1}=Population; phase = true;
%      end
 end
    
    
    
    
    
%     %% Phase 1
%     % SDE
%     % MatingPool = TournamentSelection(2,Global.N,Fitness);
%     % Offspring  = GA(Population(MatingPool));
%     % [Population,Fitness] = EnvironmentalSelection_SDE([Population,Offspring],Global.N);   
%     %NSGAII
%     Gcycle=Gcycle+1
%     gen=0;
%     for gen=1:G/2
%         MatingPool = TournamentSelection(2,Global.N,FrontNo,-CrowdDis); 
%         Offspring  = GA(Population(MatingPool));
%         [Population,FrontNo,CrowdDis] = EnvironmentalSelection_OR([Population,Offspring],Global.N,[1:Global.M]); 
%     end
%          
%     %% use GMM to cluster and do objective reduction 
% 
%     [IDx,~]=GMM_cluster(Population.objs,Kmax);   
%     % The number of Clusters                 
%     K=max(IDx) ;                
%     %itentify the essential objective for each cluster
%     Objectives=Population.objs;  
%     Fs=[];
%     for k=1:K                       
%         Fs{k}=NLHA(Objectives(IDx==k,:),lambda);  
%         P{k}=Population(IDx==k);
%     end       
%     K=length(Fs)
%     for i=1:K
%        Fs{i}
%     end
%     %% Optimize each subproblems
%     while gen<G
%         for k=1:K     
%             Population_k=P{k};           
%             [~,FrontNo,CrowdDis] = EnvironmentalSelection_OR(Population_k,length(Population_k),Fs{k});           
%             if mod(length(Population_k),2)~=0
%                MatingPool = TournamentSelection(2,length(Population_k)+1,FrontNo,-CrowdDis);                   
%             else
%                MatingPool = TournamentSelection(2,length(Population_k),FrontNo,-CrowdDis);                                 
%             end  
%             Offspring_k = GA(Population_k(MatingPool));                          
%             Offspring_k = Offspring_k(1:length(Population_k));  
%             [Population_k,~,~] = EnvironmentalSelection_OR([Population_k,Offspring_k],length(Population_k),Fs{k});  
%             Population(IDx==k)=Population_k;
%         end    
%         gen=gen+1;
%     end
% end
% 
    
    