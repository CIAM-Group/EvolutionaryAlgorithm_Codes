classdef MOP_CH < PROBLEM
    % <multi/many> <real> <large/none> <expensive/none>
    % Benchmark MOP proposed by Zhenkun Wang, Li Qingyan, Yang Qite, 
    % and Hisao Ishibuchi.
    %------------------------------- Reference --------------------------------
    %Wang Z, Li Q, Yang Q, et al. The dilemma between eliminating 
    %dominance-resistant solutions and preserving boundary solutions of 
    %extremely convex Pareto fronts[J]. Complex & Intelligent Systems, 
    %2021: 1-10.
    %------------------------------- Copyright --------------------------------
    % Copyright (c) 2018-2019 BIMK Group. You are free to use the PlatEMO for
    % research purposes. All publications which use this platform or any code
    % in the platform should acknowledge the use of "PlatEMO" and reference "Ye
    % Tian, Ran Cheng, Xingyi Zhang, and Yaochu Jin, PlatEMO: A MATLAB platform
    % for evolutionary multi-objective optimization [educational forum], IEEE
    % Computational Intelligence Magazine, 2017, 12(4): 73-87".
    %--------------------------------------------------------------------------
    
    methods
        %% Initialization
        function Setting(obj)
            if isempty(obj.M);obj.M = 3;end
            if isempty(obj.D);obj.D = obj.M + 9;end
            obj.lower    = zeros(1,obj.D);
            obj.upper    = ones(1,obj.D);
            obj.encoding = 'real';
        end
        %% Calculate objective values
        function PopObj = CalObj(obj,PopDec)
            [N,D]  = size(PopDec);
            M      = obj.M;         
            %% dynamic distance function
            g = zeros(N,M);
            k = zeros(N,M);
            for i = 1:N
                for j = 1 : M
                    xm = PopDec(i,M+j-1:M:D);
                    g(i,j) = 100*(length(xm) +sum( (xm - 0.5).^2 - cos(20*pi*(xm - 0.5))));
                end
            end         
            k(:,1) = 1 - PopDec(:,1);
            k(:,M) = prod(PopDec(:,1:M-1),2);
            for i = 2 : M-1
                k(:,i) = (1-PopDec(:,i)).*prod(PopDec(:,1:i-1),2);
            end
            F = 0.25;
            PopObj = (1+g).*(1-k.^F);
        end
        %% Sample reference points on Pareto front
        function P = GetOptimum(obj,N)
            P = UniformPoint(N,obj.M);
            P = 1-(P.^0.25);
        end
        %% Generate the image of Pareto front
        function R = GetPF(obj)
            if obj.M == 2
                R = obj.GetOptimum(100);
            elseif obj.M == 3
                a = linspace(0,pi/2,10)';
                R = {1-sqrt(sin(a)*cos(a')),1-sqrt(sin(a)*sin(a')),1-sqrt(cos(a))*ones(size(a'))};
            else
                R = [];
            end
        end   
    end
end