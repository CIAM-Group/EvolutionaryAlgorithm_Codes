function [Population,FrontNo,CrowdDis] = EnvironmentalSelection_OR(Population,N,FS)
% The environmental selection of NSGA-II with essential objective Fs

%------------------------------- Copyright --------------------------------
% Copyright (c) 2018-2019 BIMK Group. You are free to use the PlatEMO for
% research purposes. All publications which use this platform or any code
% in the platform should acknowledge the use of "PlatEMO" and reference "Ye
% Tian, Ran Cheng, Xingyi Zhang, and Yaochu Jin, PlatEMO: A MATLAB platform
% for evolutionary multi-objective optimization [educational forum], IEEE
% Computational Intelligence Magazine, 2017, 12(4): 73-87".
%--------------------------------------------------------------------------

    Objs=Population.objs;   
    [~,M]=size(Objs);  
%     %% normalized the objective function value 
%     minObjs=repmat(min(Objs,[],1),size(Objs,1),1);
%     maxObjs=repmat(max(Objs,[],1),size(Objs,1),1);
%     Objs=(Objs-minObjs)./(maxObjs-minObjs); 

    %alpha=max(0,0.8*(M-3)/M);
    alpha=0.1;
    for i=1:M
       m_Objs(:,i)=(1-alpha)*Objs(:,i)+alpha/M*sum(Objs,2);
    end       
    Objs=m_Objs;
    Objs=Objs(:,FS);

          
     %% Non-dominated sorting
    [FrontNo,MaxFNo] = NDSort(Objs,Population.cons,N);
    Next = FrontNo < MaxFNo;
    
    %% Calculate the crowding distance of each solution
    CrowdDis = CrowdingDistance(Objs,FrontNo);
    
    %% Select the solutions in the last front based on their crowding distances
    Last     = find(FrontNo==MaxFNo);
    [~,Rank] = sort(CrowdDis(Last),'descend');
    Next(Last(Rank(1:N-sum(Next)))) = true;
    
    %% Population for next generation
    Population = Population(Next);
    FrontNo    = FrontNo(Next);
    CrowdDis   = CrowdDis(Next);
end