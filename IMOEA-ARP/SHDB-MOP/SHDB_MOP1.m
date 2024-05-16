classdef SHDB_MOP1 < PROBLEM
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
        %% Default settings of the problem
        function Setting(obj)
            if isempty(obj.M); obj.M = 3; end
%             if isempty(obj.D); obj.D = obj.M+8; end
            if isempty(obj.D);obj.D = 4*obj.M-1; end
            obj.lower    = zeros(1,obj.D);
            obj.upper    = ones(1,obj.D);
            obj.encoding = 'real';
        end
        %% Calculate objective values
        function PopObj = CalObj(obj,PopDec)
            [N,D]  = size(PopDec);
            M      = obj.M;
            g = zeros(N,M);
            A = 1;
            for i = 1:N
                for j = 1 : M
                    xm = PopDec(i,M+j-1:M:D);
%                     g(i,j) = A*(length(xm) +sum( (xm - 0.5).^2 - cos(20*pi*(xm - 0.5))));
                    g(i,j) = A * sum((xm - 0.5).^2);
                end
            end
%             g      = 100*(obj.D-obj.M+1+sum((PopDec(:,obj.M:end)-0.5).^2-cos(20.*pi.*(PopDec(:,obj.M:end)-0.5)),2));
            F = 2;
            PopObj = (1+g).*(1-fliplr(cumprod([ones(size(g,1),1),cos(PopDec(:,1:M-1)*pi/2).^F],2)).*[ones(size(g,1),1),sin(PopDec(:,M-1:-1:1)*pi/2).^F]);
%             PopObj = (1-fliplr(cumprod([ones(size(g,1),1),cos(PopDec(:,1:M-1)*pi/2).^F],2)).*[ones(size(g,1),1),sin(PopDec(:,M-1:-1:1)*pi/2).^F]);
        end
        %% Generate points on the Pareto front
        function R = GetOptimum(obj,N)
            R = UniformPoint(N,obj.M);
            F = 2;
            R = 1-(R.^(F/2));
        end
        %% Generate the image of Pareto front
        function R = GetPF(obj)
            if obj.M == 2
                R = obj.GetOptimum(100);
            elseif obj.M == 3
                a = linspace(0,1,10)';
                F = 2;
                A1 =1-(cos(0.5*pi*a).*cos(0.5*pi*a')).^(F);
                A2 =1-(cos(0.5*pi*a).*sin(0.5*pi*a')).^(F);
                A3 =1-sin(0.5*pi*a).^(F);
                R = {A1,A2,A3*ones(size(a'))};
            else
                R = [];
            end
        end
    end
end