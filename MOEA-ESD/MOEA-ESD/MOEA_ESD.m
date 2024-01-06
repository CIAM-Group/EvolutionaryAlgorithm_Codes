classdef MOEA_ESD < ALGORITHM
% <multi> <real/binary/permutation> <constrained/none>

%------------------------------- Reference --------------------------------
% K. Deb, A. Pratap, S. Agarwal, and T. Meyarivan, A fast and elitist
% multiobjective genetic algorithm: NSGA-II, IEEE Transactions on
% Evolutionary Computation, 2002, 6(2): 182-197.
%------------------------------- Copyright --------------------------------
% Copyright (c) 2022 BIMK Group. You are free to use the PlatEMO for
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
            %N1 in paper
            Count_1 = 0;
            %N2 in paper
            Count_2 = 0;
            Zmin = min(Population.objs,[],1);
            [~,FrontNo,CrowdDis,Count_1,Count_2] = EnvironmentalSelection(Population,Problem.N,Problem,Count_1,Zmin,Count_2);
            %% Optimization
            while Algorithm.NotTerminated(Population)
                MatingPool = TournamentSelection(2,Problem.N,FrontNo,-CrowdDis);
                Offspring  = OperatorGA(Population(MatingPool),{1,20,1,20});
                Zmin = min([Zmin;Offspring.objs],[],1);
                [Population,FrontNo,CrowdDis,Count_1,Count_2] = EnvironmentalSelection([Population,Offspring],Problem.N,Problem,Count_1,Zmin,Count_2);
            end
        end
    end
end