classdef MOEADACN < ALGORITHM
% <multi/many> <binary/permutation>
% MOEA/D with the adaptive composite norm (ACN) strategy
% Tm --- 0.1 --- The size of neighborhood for mating
% Tr --- 0.1 --- The size of neighborhood for replacement
% nr --- 0.1 --- The maximum number of replacement
% RC --- 0 --- The reference point ratio coefficient
% drho_mean --- 0.1 --- $\Delta\rho$
% L0 --- 100 --- $L$
% 
%   Author: Ruihao Zheng


    methods
        function main(Algorithm,Problem)
            %% Parameter setting
            [Tm, Tr, nr, RC, drho_mean, L0] = Algorithm.ParameterSet(0.1, 0.1, 0.1, 0, 0.1, 100);

            %% initialization
            % Generate the weight vectors
            [W, Problem.N] = UniformPoint(Problem.N, Problem.M);
            Tm = ceil(Problem.N * Tm);
            Tr = ceil(Problem.N * Tr);
            nr = ceil(Problem.N * nr);
            % Detect the neighbours of each solution
            B = pdist2(W, W);
            [~,B] = sort(B, 2);
            Bm = B(:, 1:Tm);
            Br = B(:, 1:Tr);
            % Generate random population
            Population = Problem.Initialization();
            FontNo = NDSort(Population.objs, 1);
            Archive = Population(FontNo == 1);  % archive always maintain non-dominated solutions
            [~, ia] = unique(Archive.objs, 'row');
            Archive = Archive(ia);
            % Related to reference point calculation
            zmin = min(Population.objs, [], 1);
            zmax = max(Population.objs, [], 1);
            z = zmin - RC*(zmax-zmin);
            % Initialize rho and drho
            if drho_mean <= -1 && drho_mean >= -2
                rho = (2+drho_mean)*ones(Problem.N,1);  % constant rho in [0,1]
                drho_last = 0;
                drho_next = 0;
            elseif drho_mean > -1
                rho = ones(Problem.N,1);
                drho_last = drho_mean;
                drho_next = drho_mean;
            end
            % Related to subproblem performance
            L = L0;
            Eta = zeros(Problem.N,L);
            eta = zeros(Problem.N,1);
            pointer_Eta = 0;
            h = true(Problem.N,1);
            % Related to validation
            subp_test = randperm(Problem.N,1);
            pointer_Zeta = 0;
            Zeta = zeros(Problem.N, 3*length(subp_test));


            %% Optimization
            while Algorithm.NotTerminated(Archive)
                % Update Eta
                pointer_Eta = pointer_Eta + 1;
                Eta(h,pointer_Eta) = eta(h);
                eta(h) = 0;
                index = ~h;
                if pointer_Eta == 1
                    Eta(index,pointer_Eta) = Eta(index,L0);
                else
                    Eta(index,pointer_Eta) = Eta(index,pointer_Eta-1);
                end
                eta(index) = eta(index) + 1;
                index = Eta(:,pointer_Eta) < eta;
                Eta(index,pointer_Eta) = eta(index);
                h = false(Problem.N,1);
                if pointer_Eta >= L0
                    pointer_Eta = 0;
                end
                
                % Select subproblem for validation
                subp_test = randi(Problem.N);

                % Iteration for validation
                O_test = repmat(SOLUTION(),1,3*Tm*length(subp_test));
                rho_last = min(max(rho + drho_last, 0), 1);
                rho_next = min(max(rho - drho_next, 0), 1);
                Pop_tmp = [Population Archive];
                % Pop_tmp = Archive;
                objs = Pop_tmp.objs;
                Pop_test_last = repmat(SOLUTION(),1,Problem.N);
                Pop_test_cur = repmat(SOLUTION(),1,Problem.N);
                Pop_test_next = repmat(SOLUTION(),1,Problem.N);
                count = 0;
                for j = subp_test
                    % match
                    for jj = Bm(j,:)
                        g = CWST(objs, z, W(jj, :), rho_last(jj));
                        [~,I] = min(g);
                        Pop_test_last(jj) = Pop_tmp(I);
                        g = CWST(objs, z, W(jj, :), rho(jj));
                        [~,I] = min(g);
                        Pop_test_cur(jj) = Pop_tmp(I);
                        g = CWST(objs, z, W(jj, :), rho_next(jj));
                        [~,I] = min(g);
                        Pop_test_next(jj) = Pop_tmp(I);
                    end
                    % Generate offspring
                    for jj = 1 : Tm
                        P = [j, Bm(j, jj)];
                        Offspring_cur = Operator_GA4CO(Pop_test_cur(P(1:2)));
                        if all(Pop_test_cur(P(1:2)).objs == Pop_test_last(P(1:2)).objs, 'all')
                            Offspring_last = Offspring_cur;
                        else
                            Offspring_last = Operator_GA4CO(Pop_test_last(P(1:2)));
                        end
                        if all(Pop_test_cur(P(1:2)).objs == Pop_test_next(P(1:2)).objs, 'all')
                            Offspring_next = Offspring_cur;
                        else
                            Offspring_next = Operator_GA4CO(Pop_test_next(P(1:2)));
                        end
                        O_test((count*Tm)+jj+[0,length(O_test)/3,length(O_test)/3*2]) = [Offspring_last Offspring_cur Offspring_next];
                    end
                    count = count + 1;
                end
                % Update the reference point
                zmax = max(Population.objs, [], 1);
                zmin = min([zmin; O_test.objs]);
                z = zmin - RC*(zmax-zmin);
                % Statistics
                count = 0;
                for j = 1 : length(subp_test)
                    R = Br(subp_test(j), randperm(Tr));
                    for jj = 1 : Tm
                        % Count the total improvements
                        index_last = count*Tm+jj;
                        index_cur = count*Tm+length(O_test)/3+jj;
                        index_next = count*Tm+length(O_test)/3*2+jj;

                        g_old_last = CWST(Pop_test_last(R).objs, z, W(R, :), rho_last(R));
                        g_old_cur = CWST(Pop_test_cur(R).objs, z, W(R, :), rho(R));
                        g_old_next = CWST(Pop_test_next(R).objs, z, W(R, :), rho_next(R));
                        g_new_last = CWST(O_test(index_last).obj, z, W(R, :), rho_last(R));
                        g_new_cur = CWST(O_test(index_cur).obj, z, W(R, :), rho(R));
                        g_new_next = CWST(O_test(index_next).obj, z, W(R, :), rho_next(R));
                        index = g_old_last>g_new_last;
                        Zeta(R(index), 1) = Zeta(R(index), 1) + 1;
                        index = g_old_cur>g_new_cur;
                        Zeta(R(index), 2) = Zeta(R(index), 2) + 1;
                        index = g_old_next>g_new_next;
                        Zeta(R(index), 3) = Zeta(R(index), 3) + 1;

                        % Update Population
                        g_old = CWST(Population(R).objs, z, W(R, :), rho(R));
                        g_new = CWST(O_test(index_last).obj, z, W(R, :), rho(R));
                        I_R = R(find(g_old>=g_new, nr));
                        Population(I_R) = O_test(index_last);
                        I_imp = intersect(R(g_old>g_new),I_R);
                        h(I_imp) = true;
                        g_old = CWST(Population(R).objs, z, W(R, :), rho(R));
                        g_new = CWST(O_test(index_cur).obj, z, W(R, :), rho(R));
                        I_R = R(find(g_old>=g_new, nr));
                        Population(I_R) = O_test(index_cur);
                        I_imp = intersect(R(g_old>g_new),I_R);
                        h(I_imp) = true;
                        g_old = CWST(Population(R).objs, z, W(R, :), rho(R));
                        g_new = CWST(O_test(index_next).obj, z, W(R, :), rho(R));
                        I_R = R(find(g_old>=g_new, nr));
                        Population(I_R) = O_test(index_next);
                        I_imp = intersect(R(g_old>g_new),I_R);
                        h(I_imp) = true;
                    end
                    count = count + 1;
                end
                
                % Validation
                pointer_Zeta = pointer_Zeta + 1;
                if pointer_Zeta >= L
                    pointer_Zeta = 0;

                    Pop_tmp = [Population Archive];
                    objs = Pop_tmp.objs;
                    for j = 1 : Problem.N
                        tmp = zeros(1,3);
                        tmp(3) = sum( Zeta(B(j,1:ceil(Problem.N/2)), 1) );  % tie-breaking
                        tmp(2) = sum( Zeta(B(j,1:ceil(Problem.N/2)), 2) );
                        tmp(1) = sum( Zeta(B(j,1:ceil(Problem.N/2)), 3) );
                        [~,I] = max(tmp);
                        switch I
                            case 3
                                rho(j) = rho_last(j);
                            case 1
                                rho(j) = rho_next(j);
                        end
                        % match
                        if I ~= 2
                            g = CWST(objs, z, W(j, :), rho(j));
                            [~,I] = min(g);
                            Population(j) = Pop_tmp(I);
                        end
                    end

                    Zeta(:) = 0;
                end

                
                % Iteration for main
                O = repmat(SOLUTION(),1,Problem.N);
                % for j = 1 : Problem.N
                for j = randperm(Problem.N)
                    % Choose the parents
                    P = [j, Bm(j, randperm(Tm,1))];
                    R = Br(j, randperm(Tr));
                    
                    % Generate an offspring
                    Offspring = Operator_GA4CO(Population(P(1:2)));
                    O(j) = Offspring;
                    
                    % Update the reference point
                    zmin = min(zmin, Offspring.obj);
                    z = zmin - RC*(zmax-zmin);
                    
                    % Update the neighbours
                    g_old = CWST(Population(R).objs, z, W(R, :), rho(R));
                    g_new = CWST(Offspring.obj, z, W(R, :), rho(R));
                    I_R = R(find(g_old>=g_new, nr));
                    Population(I_R) = Offspring;
                    I_imp = intersect(R(g_old>g_new),I_R);
                    h(I_imp) = true;
                end
                
                % Update archive
                Archive = UpdateArchive(Archive,[O_test,O],Problem);
            end
        end
    end
end

%%
function g = CWST(objs, z, W, rho)
    g = rho .* sum((objs-z).*W, 2)  +  (1 - rho) .* max((objs-z).*W, [], 2);
end


function Archive = UpdateArchive(Archive,Z,Problem)
%Remove duplicate solutions and find non-dominated solutions. Truncation
%happens at the end.

    Archive = [Archive,Z];
    [~, ia] = unique(Archive.objs,'row');
    Archive = Archive(ia);
    FrontNo = NDSort(Archive.objs,1);
    Next = FrontNo==1;
    Archive = Archive(Next);
%     if Problem.FE >= Problem.maxFE
        N_archive  = length(Archive);
        if N_archive > Problem.N
            Next = true(1,N_archive);
            Del  = Truncation(Archive.objs,N_archive-Problem.N);
            Next(Del) = false;
            Archive = Archive(Next);
        end
%     end
end


function Del = Truncation(PopObj,K)
%Select part of the solutions by truncation
%ref: SPEA2

    Distance = pdist2(PopObj,PopObj);
    Distance(logical(eye(length(Distance)))) = inf;
    Del = false(1,size(PopObj,1));
    while sum(Del) < K
        Remain   = find(~Del);
        Temp     = sort(Distance(Remain,Remain),2);
        [~,Rank] = sortrows(Temp);
        Del(Remain(Rank(1))) = true;
    end
end


function Offspring = Operator_GA4CO(Parent,Parameter)
%Operator_GA4CO - Crossover and mutation operators of genetic algorithm for
%combinatorial optimisation problems
% 
%   If the offspring generating by crossover is identical to parents,
%   mutation must be used.

    %% Parameter setting
    if nargin > 1
        [prem_proC,perm_proM, bi_proC,bi_proM] = deal(Parameter{:});
    else
        [prem_proC,perm_proM, bi_proC,bi_proM] = deal(1,0.1,1,2);
    end
    if isa(Parent(1),'SOLUTION')  % 使算子可以嵌套
        calObj = true;
        Parent = Parent.decs;
    else
        calObj = false;
    end
    Parent1 = Parent(1:floor(end/2),:);
    Parent2 = Parent(floor(end/2)+1:floor(end/2)*2,:);
    [N,D]   = size(Parent1);
    Problem = PROBLEM.Current();
    
    switch Problem.encoding
        case 'permutation'
            %% Genetic operators for permutation based encoding
            % Order crossover
            Offspring = Parent1;
            if rand < prem_proC
                k = randi(D,1,N);
                iden_index = zeros(1, N);
                for i = 1 : N
                    Offspring(i,k(i)+1:end) = setdiff(Parent2(i,:),Parent1(i,1:k(i)),'stable');
                    if all(Offspring(i,:) == Parent1(i,:)) || all(Offspring(i,:) == Parent2(i,:))
                        % Record the offspring that is identical to parents
                        iden_index(i) = true;
                    end
                end
            end
            % Mutation
            k = randi(D,1,N);
            s = randi(D,1,N);
            for i = 1 : N
                if iden_index(i) || rand < perm_proM
                    P = k(i); Q = s(i);
                    while P == Q
                        P = randi(D);
                    end
                    if P > Q
                        % P should be less than Q
                        P = P + Q;
                        Q = P - Q;
                        P = P - Q;
                    end
                    switch class(Problem)
                        case 'MOTSP'
                            % inverse
                            Offspring(i,:) = Offspring(i, [1:P-1, Q:-1:P, Q+1:end]);  % Q+1>D时，Q+1:end返回空
                        case 'mQAP'
                            % swap
                            tmp = Offspring(i,P);
                            Offspring(i,P) = Offspring(i,Q);
                            Offspring(i,Q) = tmp;
                        otherwise
                            % insert
                            if s(i) < k(i)
                                Offspring(i,:) = Offspring(i,[1:s(i)-1,k(i),s(i):k(i)-1,k(i)+1:end]);
                            elseif s(i) > k(i)
                                Offspring(i,:) = Offspring(i,[1:k(i)-1,k(i)+1:s(i)-1,k(i),s(i):end]);
                            end
                    end
                else
                    % do nothing?
                    % other mutation?
                end
            end
        case 'binary'
            %% Genetic operators for binary encoding
            % Uniform crossover
            k = rand(N,D) < 0.5;
            k(repmat(rand(N,1)>bi_proC,1,D)) = false;
            Offspring    = Parent1;
            Offspring(k) = Parent2(k);
            % Bit-flip mutation
            iden_index = all(Offspring == Parent1, 2) | all(Offspring == Parent2, 2);
            Site = rand(N,D) < bi_proM/D;
            for i = 1 : N
                % enhance the mutation of offspring identical to parents
                if iden_index(i)
                    Site(i, randi([1 D])) = true;
                end
            end
            Offspring(Site) = ~Offspring(Site);
        otherwise
            % Offspring = OperatorGAhalf(Parent);
            error('Unsupported representation.')
    end
    if calObj
        Offspring = SOLUTION(Offspring);
    end
end
