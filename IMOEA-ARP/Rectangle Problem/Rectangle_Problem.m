classdef Rectangle_Problem < PROBLEM
% <multi/many> <real> <large/none> <expensive/none>
% Benchmark MOP proposed by Deb, Thiele, Laumanns, and Zitzler

%------------------------------- Reference --------------------------------
% K. Deb, L. Thiele, M. Laumanns, and E. Zitzler, Scalable test problems
% for evolutionary multiobjective optimization, Evolutionary multiobjective
% Optimization. Theoretical Advances and Applications, 2005, 105-145.
%------------------------------- Copyright --------------------------------
% Copyright (c) 2022 BIMK Group. You are free to use the PlatEMO for
% research purposes. All publications which use this platform or any code
% in the platform should acknowledge the use of "PlatEMO" and reference "Ye
% Tian, Ran Cheng, Xingyi Zhang, and Yaochu Jin, PlatEMO: A MATLAB platform
% for evolutionary multi-objective optimization [educational forum], IEEE
% Computational Intelligence Magazine, 2017, 12(4): 73-87".
%--------------------------------------------------------------------------

    methods
        %% Default settings of the problem
        function Setting(obj)
            if isempty(obj.M); obj.M = 4; end
            if isempty(obj.D); obj.D = 2; end
            obj.lower    = ones(1,obj.D)*(-10000);
            obj.upper    = ones(1,obj.D)*(10000);
            obj.encoding = 'real';
        end
        %% Calculate objective values
        function PopObj = CalObj(obj,PopDec)
              a1 = 1;
              a2 = 3;
              b1 = 1;
              b2 = 3;
              PopObj = zeros(size(PopDec,1),obj.M);
              PopObj(:,1) = abs(PopDec(:,1)-a1);
              PopObj(:,2) = abs(PopDec(:,1)-a2);
              PopObj(:,3) = abs(PopDec(:,2)-b1);
              PopObj(:,4) = abs(PopDec(:,2)-b2);
        end
        %% Generate points on the Pareto front
        function R = GetOptimum(obj,N)

            a1 = 1;
            a2 = 3;
            b1 = 1;
            b2 = 3;
            P = [];
            for i = a1:(a2-a1)/(sqrt(N)-1):a2
                for j = b1:(b2-b1)/(sqrt(N)-1):b2
                    P = [P;i,j];
                end
            end
            R = zeros(N,obj.M);
            R(:,1) = abs(P(:,1)-a1);
            R(:,2) = abs(P(:,1)-a2);
            R(:,3) = abs(P(:,2)-b1);
            R(:,4) = abs(P(:,2)-b2);
        end
        %% Generate the image of Pareto front
        function R = GetPF(obj)
            if obj.M == 2
                R = obj.GetOptimum(100);
            elseif obj.M == 3
                a = linspace(0,1,10)';
                R = {a*a'/2,a*(1-a')/2,(1-a)*ones(size(a'))/2};
            else
                R = [];
            end
        end
    end
end