classdef MOEAD_Gen< ALGORITHM
% <multi> <real>
% Multiobjective evolutionary algorithm based on decomposition
% rho --- 0.01 --- value of rho

%------------------------------- Reference --------------------------------
% Q. Zhang and H. Li, MOEA/D: A multiobjective evolutionary algorithm based
% on decomposition, IEEE Transactions on Evolutionary Computation, 2007,
% 11(6): 712-731.
%------------------------------- Copyright --------------------------------
% Copyright (c) 2018-2019 BIMK Group. You are free to use the PlatEMO for
% research purposes. All publications which use this platform or any code
% in the platform should acknowledge the use of "PlatEMO" and reference "Ye
% Tian, Ran Cheng, Xingyi Zhang, and Yaochu Jin, PlatEMO: A MATLAB platform
% for evolutionary multi-objective optimization [educational forum], IEEE
% Computational Intelligence Magazine, 2017, 12(4): 73-87".
%---
    properties
        Name        = 'MOEAD_Gen';             	% Population size
    end
    methods
        function main(Algorithm,Problem)
        %% Parameter setting
        rho = Algorithm.ParameterSet(0.01);

        %% Generate the weight vectors
        [W,Problem.N] = UniformPoint(Problem.N,Problem.M);
        T = ceil(Problem.N/10);

        %% Detect the neighbours of each solution
        B = pdist2(W,W);
        [~,B] = sort(B,2);
        B = B(:,1:T);
        %% Generate random population
        Population = Problem.Initialization();
        Z = min(Population.objs,[],1);
        nadir = max(Population.objs,[],1);
        %% Optimization
        while Algorithm.NotTerminated(Population)
            % For each solution
            for i = 1 : Problem.N
                % Choose the parents
                P = B(i,randperm(size(B,2)));
                % Generate an offspring
                Offspring = OperatorGAhalf(Population(P(1:2)));
                % Update the ideal point
                Z = min(Z,Offspring.obj);
                nadir = max(nadir,Offspring.obj);

                % Update the neighbours
                % MOEA/D-Gen
                delta = 0.01;
                kk = abs(Population(P).objs-(repmat(Z,T,1)-delta));
                k = abs(Offspring.obj - (Z - delta));
                g_old = max((kk + rho.*repmat(sum(kk,2),1,Problem.M)).*W(P,:),[],2);
                g_new = max((k + rho.*repmat(k,T,1)).*W(P,:),[],2);
                Population(P(g_old>=g_new)) = Offspring;

            end
        end
        end
        end
        end
        