classdef emUF4 < PROBLEM
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
            obj.lower    = [0,0,zeros(1,obj.D-2)-2];
            obj.upper    = [1,1,zeros(1,obj.D-2)+2];
            obj.encoding = 'real';
        end
        %% Calculate objective values
        function PopObj = CalObj(obj,X)
            J1 = 4 : 3 : obj.D;
            J2 = 5 : 3 : obj.D;
            J3 = 3 : 3 : obj.D;
            Y  = X - sin(6*pi*repmat(X(:,1),1,obj.D)+repmat(1:obj.D,size(X,1),1)*pi/obj.D);
            hY = abs(Y)./(1+exp(2*abs(Y)));
            hY(:,J1) = 100 * hY(:,J1);
            PopObj(:,1) = X(:,1)                  + 2*mean(hY(:,J1),2);
            PopObj(:,2) = 1-X(:,1)+X(:,1).*X(:,2) + 2*mean(hY(:,J2),2);
            PopObj(:,3) = 1-sqrt(X(:,1).*X(:,2))  + 2*mean(hY(:,J3),2);
        end
        %% Generate points on the Pareto front
        function R = GetOptimum(obj,N)
            R = UniformPoint(N,obj.M);
            R = R./repmat(sum(R,2),1,obj.M);
            R(:,obj.M) = R(:,obj.M).^0.5;
            R = 1-R;
        end
        %% Generate the image of Pareto front
        function R = GetPF(obj)
        	if obj.M == 2
                R = obj.GetOptimum(100);
            elseif obj.M == 3
                a = linspace(0,1,20)';
                R = {a*ones(size(a')),1-a*ones(size(a'))+(a*a'),1-(a*a').^0.5};
            else
                R = [];
            end
        end
    end
end