classdef emUF3 < PROBLEM
% <multi> <real> <large/none>
% Unconstrained benchmark MOP

%------------------------------- Reference --------------------------------
% Q. Zhang, A. Zhou, S. Zhao, P. N. Suganthan, W. Liu, and S. Tiwari,
% Multiobjective optimization test instances for the CEC 2009 special
% session and competition, School of CS & EE, University of Essex, Working
% Report CES-487, 2009.
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
            obj.M = 3;
            if isempty(obj.D); obj.D = 30; end
            obj.lower    = zeros(1,obj.D);
            obj.upper    = ones(1,obj.D);
            obj.encoding = 'real';
        end
        %% Calculate objective values
        function PopObj = CalObj(obj,X)
            J1 = 4 : 3 : obj.D;
            J2 = 5 : 3 : obj.D;
            J3 = 3 : 3 : obj.D;
            Y  = X - repmat(X(:,1),1,obj.D).^(0.5*(1+3*(repmat(1:obj.D,size(X,1),1)-2)/(obj.D-2))); 
            Y(:,J1) = 100 * Y(:,J1);
            PopObj(:,1) = sqrt(X(:,1))                        + 2/length(J1)*(4*sum(Y(:,J1).^2,2)-2*prod(cos(20*Y(:,J1)*pi./sqrt(repmat(J1,size(X,1),1))),2)+2);
            PopObj(:,2) = 1-sqrt(X(:,1))+sqrt(X(:,1).*X(:,2)) + 2/length(J2)*(4*sum(Y(:,J2).^2,2)-2*prod(cos(20*Y(:,J2)*pi./sqrt(repmat(J2,size(X,1),1))),2)+2);
            PopObj(:,3) = 1-X(:,1).*X(:,2)                    + 2/length(J3)*(4*sum(Y(:,J3).^2,2)-2*prod(cos(20*Y(:,J3)*pi./sqrt(repmat(J3,size(X,1),1))),2)+2);
        end
        %% Generate points on the Pareto front
        function R = GetOptimum(obj,N)
            R = UniformPoint(N,obj.M);
            R = R./repmat(sum(R,2),1,obj.M);
            R(:,obj.M) = R(:,obj.M).^2;
            R = 1-R;
        end
        %% Generate the image of Pareto front
        function R = GetPF(obj)
        	if obj.M == 2
                R = obj.GetOptimum(100);
            elseif obj.M == 3
                a = linspace(0,1,20)';
                R = {a.^0.5*ones(size(a')),1-a.^0.5*ones(size(a'))+(a*a').^0.5,1-a*a'};
            else
                R = [];
            end
        end
    end
end