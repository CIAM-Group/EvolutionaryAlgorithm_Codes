classdef IMOEA_ARP< ALGORITHM
    % <multi> <real/binary/permutation>
    % S metric selection based evolutionary multiobjective optimization
    % refpoint --- 0.1 --- The parameter in grid location calculation    
    %------------------------------- Reference --------------------------------
    % M. Emmerich, N. Beume, and B. Naujoks, An EMO algorithm using the
    % hypervolume measure as selection criterion, Proceedings of the
    % International Conference on Evolutionary Multi-Criterion Optimization,
    % 2005, 62-76.
    %------------------------------- Copyright --------------------------------
    % Copyright (c) 2021 BIMK Group. You are free to use the PlatEMO for
    % research purposes. All publications which use this platform or any code
    % in the platform should acknowledge the use of "PlatEMO" and reference "Ye
    % Tian, Ran Cheng, Xingyi Zhang, and Yaochu Jin, PlatEMO: A MATLAB platform
    % for evolutionary multi-objective optimization [educational forum], IEEE
    % Computational Intelligence Magazine, 2017, 12(4): 73-87".
    %--------------------------------------------------------------------------
    
    methods
        function main(Algorithm,Problem)     
            %% Generate random population
            Population = Problem.Initialization();
            FrontNo  = NDSort(Population.objs,inf);
            refpoint = Algorithm.ParameterSet(0.1);
            gamma = 0.20;
            delta = 0.10;
            Zmin = min(Population.objs,[],1);
            Zmax = max(Population.objs,[],1);
            count = 0;
            %% Optimization
            while Algorithm.NotTerminated(Population)
                if count<gamma*(Problem.maxFE/Problem.N)
                    for i = 1 : Problem.N
                        Offspring = OperatorGAhalf(Population(randperm(end,2)));
                        [Population,FrontNo] = Reduce([Population,Offspring]);
                    end
                    nad = max(Population.objs,[],1);
                    if (sum(abs(Zmax-nad)./nad)/Problem.M)<=delta
                        count = count+1;
                    else
                        count = 0;
                    end
                    Zmax = min(Zmax,nad);
                else
                    %% 选取合适的theta参数
                    %% Iteration(DE)
                          PopObj = Population.objs;
                          DE_N = 50;
                          DE_Gen = 100;
                          DE_Fes = 0;
                          F = 0.5;
                          X = unifrnd(zeros(DE_N,1),ones(DE_N,1));
                          FX = zeros(DE_N,1);
                          SMS = zeros(size(PopObj,1),1);
                          for i = 1:length(X)
                            sigma = X(i);
                            ReferPoint = max(PopObj,[],1)+sigma;
                            for j = 1:size(PopObj,1)
                                hv1 = Hypervolume_MEX(PopObj,ReferPoint);
                                Pop = [PopObj(1:j-1,:);PopObj(j+1:end,:)];
                                hv2 = Hypervolume_MEX(Pop,ReferPoint);
                                SMS(j) = hv1-hv2;
                            end
                            FX(i) = std(SMS);
                            if X(i)<=0 || X(i)>1
                                FX(i) = FX(i)+1e10;
                            end
                          end
                          DE_Fes = DE_Fes+DE_N;
                          %Optimization
                          while DE_Fes<DE_N*DE_Gen
                            Mating = TournamentSelection(2,2*DE_N,FX);
                            Parent1 = X;
                            Parent2 = X(Mating(1:end/2));
                            Parent3 = X(Mating(end/2+1:end));
                            Offs = Parent1+F*(Parent2-Parent3);
                            FX_Offs = zeros(DE_N,1);
                            % calculate offsprings' fitness value
                            for i = 1:length(Offs)
                                sigma = Offs(i);
                                ReferPoint = max(PopObj,[],1)+sigma;
                                for j = 1:size(PopObj,1)
                                    hv1 = Hypervolume_MEX(PopObj,ReferPoint);
                                    Pop = [PopObj(1:j-1,:);PopObj(j+1:end,:)];
                                    hv2 = Hypervolume_MEX(Pop,ReferPoint);
                                    SMS(j) = hv1-hv2;
                                end
                                FX_Offs(i) = std(SMS);
                                if Offs(i)<=0 || Offs(i)>1
                                    FX_Offs(i) = FX_Offs(i)+1e10;
                                end
                            end
                            replace = FX>FX_Offs;
                            X(replace) = Offs(replace);
                            FX(replace) = FX_Offs(replace);
                            DE_Fes = DE_Fes+DE_N;
                          end
                          [~,index] = min(FX);
                          sigma = X(index);
                      
                    %% Stage 2
                    while Algorithm.NotTerminated(Population)
                        for i = 1 : Problem.N
                            Offspring = OperatorGAhalf(Population(randperm(end,2)));
                            [Population,FrontNo] = Reduce_adaptive([Population,Offspring],sigma);
                        end
                    end
                end
            end
        end
    end
end