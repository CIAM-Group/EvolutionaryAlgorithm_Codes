function [Population,FrontNo,CrowdDis,Count_1,Count_2] = EnvironmentalSelection(Population,N,Problem,Count_1,Zmin,Count_2)
% The environmental selection of NSGA-II

%------------------------------- Copyright --------------------------------
% Copyright (c) 2022 BIMK Group. You are free to use the PlatEMO for
% research purposes. All publications which use this platform or any code
% in the platform should acknowledge the use of "PlatEMO" and reference "Ye
% Tian, Ran Cheng, Xingyi Zhang, and Yaochu Jin, PlatEMO: A MATLAB platform
% for evolutionary multi-objective optimization [educational forum], IEEE
% Computational Intelligence Magazine, 2017, 12(4): 73-87".
%--------------------------------------------------------------------------
    
    %Alpha
    Alpha = 50;
    %% Non-dominated sorting
    [FrontNo,MaxFNo] = NDSort(Population.objs,Population.cons,N);
    Next = FrontNo < MaxFNo;
    %% ESD-ES
    if sum(FrontNo == 1) > N
        Count_1 = Count_1+1;
    else
        Count_1 = max(0,Count_1-1);
    end
    %Implement CFES or DFES according to condition
    if Count_1 > Alpha && sum(FrontNo == 1) > N
        [Population,Count_2] = ESD_ES(Population(FrontNo == 1),N,Zmin,Count_2);
        [FrontNo,~] = NDSort(Population.objs,Population.cons,N);
        CrowdDis = CrowdingDistance(Population.objs,FrontNo);
    else
    %% Calculate the crowding distance of each solution
        CrowdDis = CrowdingDistance(Population.objs,FrontNo);

        %% Select the solutions in the last front based on their crowding distances
        Last     = find(FrontNo==MaxFNo);
        [~,Rank] = sort(CrowdDis(Last),'descend');
        Next(Last(Rank(1:N-sum(Next)))) = true;

        %% Population for next generation
        Population = Population(Next);
        FrontNo    = FrontNo(Next);
        CrowdDis   = CrowdDis(Next);
    end
end

function [Population,Count_2] = ESD_ES(Population,N,Zmin,Count_2)
    %Beta
    Beta = 50;
    Gamma = 1.3;
    Fitness = Population.objs;
    [N1,M] = size(Fitness);
    Index = false(1,N1);
    K = 6;
    %GMM
    N_pdf=zeros(N1, K);
    para_sigma_inv=zeros(M, M, K);
    RegularizationValue = 0.001;
    MaxIter = 300;
    TolFun = 1e-8;
    %构建GMM
    gmm = fitgmdist(Fitness,K,'RegularizationValue',RegularizationValue,'CovarianceType','diagonal','Start','plus','Options',statset('Display','final','MaxIter',MaxIter,'TolFun',TolFun));
    mu = gmm.mu;
    sigma = gmm.Sigma;
    ComponentProportion = gmm.ComponentProportion;
    %计算概率，进行聚类
    for k=1:K
        sigma_inv=1./sigma(:,:,k);  %sigma的逆矩阵,(X_dim, X_dim)的矩阵
        para_sigma_inv(:, :, k)=diag(sigma_inv);  %sigma^(-1)
    end
    for k=1:K
        coefficient=(2*pi)^(-M/2)*sqrt(det(para_sigma_inv(:, :, k)));  %高斯分布的概率密度函数e左边的系数
        X_miu=Fitness-repmat(mu(k,:), N1, 1);  %X-miu: (X_num, X_dim)的矩阵
        exp_up=sum((X_miu*para_sigma_inv(:, :, k)).*X_miu,2);  %指数的幂，(X-miu)'*sigma^(-1)*(X-miu)
        N_pdf(:,k)=coefficient*exp(-0.5*exp_up);
    end
    responsivity=N_pdf.*repmat(ComponentProportion,N1,1);  %响应度responsivity的分子，（X_num,K）的矩阵
    responsivity=responsivity./repmat(sum(responsivity,2),1,K);  %responsivity:在当前模型下第n个观测数据来自第k个分模型的概率，即分模型k对观测数据Xn的响应度
    %聚类
    [~,Label]=max(responsivity,[],2);
    %计算条件数
    condinum = zeros(K,1);
    for i = 1:size(sigma,3)
        if sum(sum(sum(isnan(sigma))))>0||sum(sum(sum(isinf(sigma))))>0
            condinum(i) = inf;
        else
            condinum(i) = max(sigma(:,:,i))/min(sigma(:,:,i));
        end
    end
    [~,I] = sort(condinum,'ascend');
    fit = sum(Fitness,2);
    %CFES
    if Count_2 <= Beta
        current_pop = find(Label == I(1));
        if length(current_pop) <=N
            Index(current_pop) = true;
            while sum(Index)<N
                ran = randi([1,K]);
                c = intersect(find(Label == I(ran)),find(~Index));
                [~,Min] = min(fit(c));
                Index(c(Min)) = true;
            end
        else
            [~,order] = sort(fit(current_pop));
            Index(current_pop(order(1:N)))=true;
        end
        New = sum(max(Fitness(Index))-Zmin);
        rc = sum(max(Fitness)-Zmin)/New;
        if rc <= Gamma
            Count_2 = Count_2 + 1;
        else 
            Count_2 = max(0,Count_2-1);
        end
    else  
    %DFES
        % The outlier set
        A = [];
        for i = 1:M           
            theta = 3;
            fit_norm = normalize(Fitness(:,i));
            c = find(fit_norm>theta);
            A = union(A,c);
        end
        current_pop = find(~Index);
        current_pop = setdiff(current_pop,A);
        
        if N1-length(A) > N
            %Choose solutions according to angle
            current_pop = Diversity_choose(Population,Index,current_pop,N);
            Index(current_pop) = true;
        else
            Index(current_pop) = true;
            while sum(Index) < N
                i = randi(M);
                [~,Min] = min(Fitness(A,i));
                Index(A(Min)) = true;
                A(Min) = [];
            end
        end
%         current_pop = find(~Index);
%         current_pop = Diversity_choose(Population,Index,current_pop,N);
%         Index(current_pop) = true;
    end

    Population = Population(Index);
end

%% Choose solution according to angle
function current_pop = Diversity_choose(Population,Index,current_pop,N)
    PopObj1 = Population(Index).objs;
    PopObj2 = Population(current_pop).objs;
    % Association operation in the algorithm

    [N1,~] = size(PopObj1);
    [N2,~] = size(PopObj2);
    PopObj = [PopObj1;PopObj2];
    
    %% Calculate the fitness value of each solution
%     fit = sum(PopObj,2);
    
    %% Angle between each two solutions
    angle = acos(1-pdist2(PopObj,PopObj,'cosine'));
    angle(logical(eye(length(angle)))) = inf;%将自己与自己的角度定义为inf
%     Distance = pdist2(PopObj,PopObj);
    %% Niching
    Choose = [true(1,N1),false(1,N2)];
%     Zmin = min(PopObj,[],1);
    if ~any(Choose)
        % Select the extreme solutions first
        [~,Extreme]        = min(PopObj2,[],1);
        Choose(N1+Extreme) = true;
    end
    while sum(Choose) < N
        % Maximum vector angle first
        Select  = find(Choose);
        Remain  = find(~Choose);
        [~,rho] = max(min(angle(Remain,Select),[],2));
        Choose(Remain(rho)) = true;
    end
    Choose1 = Choose(N1+1:end);
    current_pop = current_pop(Choose1);
end