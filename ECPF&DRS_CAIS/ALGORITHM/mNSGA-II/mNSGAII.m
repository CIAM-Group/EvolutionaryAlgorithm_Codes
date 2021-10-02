classdef mNSGAII < ALGORITHM
 % <multi> <real>
% Nondominated sorting genetic algorithm II
% alpha --- 0.1 

%------------------------------- Reference --------------------------------
% K. Deb, A. Pratap, S. Agarwal, and T. Meyarivan, A fast and elitist
% multiobjective genetic algorithm: NSGA-II, IEEE Transactions on
% Evolutionary Computation, 2002, 6(2): 182-197.
%------------------------------- Copyright --------------------------------
% Copyright (c) 2018-2019 BIMK Group. You are free to use the PlatEMO for
% research purposes. All publications which use this platform or any code
% in the platform should acknowledge the use of "PlatEMO" and reference "Ye
% Tian, Ran Cheng, Xingyi Zhang, and Yaochu Jin, PlatEMO: A MATLAB platform
% for evolutionary multi-objective optimization [educational forum], IEEE
% Computational Intelligence Magazine, 2017, 12(4): 73-87".
%--------------------------------------------------------------------------
    properties
        Name        = 'mNSGAII';             	% Population size
    end
    methods
        function main(Algorithm,Problem)
          %% Generate random population
            alpha = Algorithm.ParameterSet(0.1);
            Population = Problem.Initialization();
            u = (1-alpha).*Population.objs + alpha/Problem.M.*repmat(sum(Population.objs,2),1,Problem.M);
            [~,FrontNo,CrowdDis] = EnvironmentalSelection_modified(Population,Problem.N,u);
          %% Optimization
            while Algorithm.NotTerminated(Population)
                MatingPool = TournamentSelection(2,Problem.N,FrontNo,-CrowdDis);
                Offspring  = OperatorGA(Population(MatingPool));
                Pop = [Population,Offspring];
                u = (1-alpha).*Pop.objs + alpha/Problem.M.*repmat(sum(Pop.objs,2),1,Problem.M);
                [Population,FrontNo,CrowdDis] = EnvironmentalSelection_modified(Pop,Problem.N,u);
            end
        end
    end
end