function [Population,FrontNo,MaxFNo] = Reduce(Population)
% Delete one solution from the population

%------------------------------- Copyright --------------------------------
% Copyright (c) 2018-2019 BIMK Group. You are free to use the PlatEMO for
% research purposes. All publications which use this platform or any code
% in the platform should acknowledge the use of "PlatEMO" and reference "Ye
% Tian, Ran Cheng, Xingyi Zhang, and Yaochu Jin, PlatEMO: A MATLAB platform
% for evolutionary multi-objective optimization [educational forum], IEEE
% Computational Intelligence Magazine, 2017, 12(4): 73-87".
%--------------------------------------------------------------------------

    %% Identify the solutions in the last front
    [FrontNo,MaxFNo]   = NDSort(Population.objs,inf);
    %% solutions in the last front
    LastFront = find(FrontNo==MaxFNo);
    LastLength = length(LastFront);
      ReferPoint = max(Population(LastFront).objs,[],1)+0.2;
    HV = Hypervolume_MEX(Population(LastFront).objs,ReferPoint);
    
    if LastLength > 2
        hv = zeros(1,LastLength);
        hv(1) = Hypervolume_MEX(Population(LastFront(2:end)).objs,ReferPoint);
        hv(LastLength) = Hypervolume_MEX(Population(LastFront(1:end-1)).objs,ReferPoint);
        for i = 2 : LastLength-1
            Pop = [Population(LastFront(1:i-1)),Population(LastFront(i+1:end))];
            hv(i) = Hypervolume_MEX(Pop.objs,ReferPoint);
        end
        sms = HV - hv;
        [~,order] = min(sms);
        Population(LastFront(order(1))) = [];
    elseif LastLength < 2
        Population(LastFront) = [];
    else
        hv = zeros(1,LastLength);
        hv(1) = Hypervolume_MEX(Population(LastFront(end)).objs,ReferPoint);
        hv(LastLength) = Hypervolume_MEX(Population(LastFront(1)).objs,ReferPoint);
        sms = HV - hv;
        [~,order] = min(sms);
        Population(LastFront(order(1))) = [];
    end   
    FrontNo = NDSort(Population.objs,inf);
end