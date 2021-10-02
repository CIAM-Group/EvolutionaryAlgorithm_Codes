classdef mDTLZ3 < PROBLEM
    % <multi/many> <real> <large/none> <expensive/none>
    % Benchmark MOP proposed Zhenkun Wang, Yew-Soon Ong, and Hisao Ishibuchi.
    %------------------------------- Reference --------------------------------
    % Wang Z, Ong Y S, Ishibuchi H. On scalable multiobjective test problems
    % with hardly dominated boundaries[J]. IEEE Transactions on Evolutionary
    % Computation, 2018, 23(2): 217-231
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
            if isempty(obj.D); obj.D = obj.M+7; end
            obj.lower    = zeros(1,obj.D);
            obj.upper    = ones(1,obj.D);
            obj.encoding = 'real';
        end
        function PopObj = CalObj(obj,PopDec)
            [N,D]  = size(PopDec);
            M      = obj.Global.M;
            g = zeros(N,M);
            for i = 1:N
                for j = 1 : M
                    xm = PopDec(i,M+j-1:M:D);
                    g(i,j) = 100*(length(xm) +sum( (xm - 0.5).^2 - cos(20*pi*(xm - 0.5))));
                end
            end
            PopObj = (1+g).*(1-fliplr(cumprod([ones(size(g,1),1),cos(PopDec(:,1:M-1)*pi/2)],2)).*[ones(size(g,1),1),sin(PopDec(:,M-1:-1:1)*pi/2)]);
        end
        %% Generate points on the Pareto front
        function R = GetOptimum(obj,N)
            if obj.M == 3
                num         = floor(sqrt(N));
                no          = num*num;
                [s,t]       = meshgrid(linspace(0,1,num),linspace(0,1,num));
                ps          = zeros(obj.M,no);
                ps(1,:)     = reshape(s,[1,no]);
                ps(2,:)     = reshape(t,[1,no]);
                ps(3:obj.M,:) = repmat(ps(2,:),[obj.M-2,1]).*repmat(ps(1,:),[obj.M-2,1]);
                pf          = zeros(3,no);
                pf(1,:)     = 1-cos(0.5*pi*ps(1,:)).*cos(0.5*pi*ps(2,:));
                pf(2,:)     = 1-cos(0.5*pi*ps(1,:)).*sin(0.5*pi*ps(2,:));
                pf(3,:)     = 1-sin(0.5*pi*ps(1,:));
                R = pf';
            end
        end
%         function R = GetOptimum(obj,N)
%             R = UniformPoint(N,obj.M);
%             R = 1 - R./repmat(sqrt(sum(R.^2,2)),1,obj.M);
%         end
        %% Generate the image of Pareto front
        function R = GetPF(obj)
            if obj.M == 2
                R = obj.GetOptimum(100);
            elseif obj.M == 3
                a = linspace(0,1,10)';
                A1 = 1-(cos(0.5*pi*a).*cos(0.5*pi*a'));
                A2 = 1-(cos(0.5*pi*a).*sin(0.5*pi*a'));
                A3 = 1-sin(0.5*pi*a);
                R = {A1,A2,A3*ones(size(a'))};
            else
                R = [];
            end
        end
    end
end