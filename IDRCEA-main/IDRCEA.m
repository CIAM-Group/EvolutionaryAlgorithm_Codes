function [hf,MaxFEs,gfs] = IDRCEA(FUN,D,LB,UB)

% -------------- parameter initialization----------------------
p = 0.4;
T = 20;
%control parameter for DE
F1=[0.5:0.1:1]; 
CR1 = [0.5,0.9,1];
F2=[0:0.1:1]; 
CR2=[0,0.5,0.9,1];

if D <= 30
    initial_sample_size=100; 
    level = 5;
elseif D < 100
    initial_sample_size=140; 
    level = 7;
elseif D >= 100
    initial_sample_size=200;     
    level = 10;
end

M = initial_sample_size/level;
NFEs=0;
MaxFEs=1000; 
gfs = zeros(1,MaxFEs);

% -------------- generate initial samples-----------------------
gs = initial_sample_size;
sam=repmat(LB,initial_sample_size,1)+(repmat(UB,initial_sample_size,1)-repmat(LB,initial_sample_size,1)).*lhsdesign(initial_sample_size,D);
fitness = FUN(sam);
for i=1:initial_sample_size    
    NFEs=NFEs+1;
    CE(NFEs,:)=[NFEs,fitness(i)];
    gfs(1,NFEs)=min(CE(1:NFEs,2));
end
hx=sam; hf=fitness;

while NFEs < MaxFEs 
      [~, sort_index] = sort(hf);
      ghf=hf(sort_index(1:gs));     ghx=hx(sort_index(1:gs),:);
      Parents_L1 = hx(sort_index(1:M),:); 
% -------------- IDS generate offspring -----------------------
      offspring = [];
      VRmin1=repmat(LB,length(ghf),1);
      VRmax1=repmat(UB,length(ghf),1);
      % DE
      if  NFEs < p*MaxFEs
          offspring1=DErand(ghx,F1,CR1,VRmax1,VRmin1,T);
          offspring = [offspring;offspring1];  %DE/rand/1
      else
          seed = ghx(1,:);
          offspring2 = DEbest(ghx,seed,F2,CR2,VRmax1,VRmin1,T);
          offspring = [offspring;offspring2];  %DE/best/1  
      end
      % EDA
      offspring3 = EDA(ghx, LB, UB, T); %EDA based mutivariable normal distribution
      offspring = [offspring;offspring3];
% -------------- RCP ----------------------- 
     % RBF-KNN
      srgtOPT=srgtsRBFSetOptions(ghx,ghf', @my_rbfbuild, [],'CUB', 0.0002,1);
      srgtSRGT = srgtsRBFFit(srgtOPT);
      for i=1:level
          train_label1(1+(i-1)*M:M*i) = i;
      end
      mdl = ClassificationKNN.fit(ghx,train_label1,'Distance','minkowski');
      mdl.DistParameter = 2;
     
      % PCPD
      Off_fitness = my_rbfpredict(srgtSRGT.RBF_Model, srgtSRGT.P, offspring);
      [~,sidx]=sort(Off_fitness);         % sort point based on fitness, get point indexs  
      Off_label_KNN = predict(mdl,offspring); 

      for i = 1: size(sidx,1)  
        Off_label_RBF(:,i) =  ceil(find(sidx==i)*level/(initial_sample_size*2*T));
      end
      rank_sum = Off_label_KNN + Off_label_RBF';  
      index_sum = find(rank_sum==min(rank_sum));
      candidate =[];
      [~, in_rbf] = min(Off_fitness(index_sum));
      candidate = [candidate; offspring(index_sum(in_rbf),:)]; %performance criterion
      distance_b = dist(offspring(index_sum, :), Parents_L1');
      max_dist = max(distance_b,[],2); 
      [~, in] = min(max_dist);
      [~,ih,~]=intersect(offspring(index_sum(in),:),candidate,'rows'); % 
      if isempty(ih)==1
         candidate = [candidate; offspring(index_sum(in),:)];%distribution criterion
      end
      % evaluate candidate
      flag = 0;
      rand_index = randperm(size(candidate, 1));
      for i =1: length(rand_index)
          if  flag ==1  
              break
          else
          candidate_position = candidate(rand_index(i), :);
          end
          [~,ih,~]=intersect(hx,candidate_position,'rows'); 
          if isempty(ih)~=1
             continue;
          end
          
          candidate_fit=FUN(candidate_position);
          NFEs = NFEs + 1;
          if NFEs > 1000
             break 
          end
          % save candidate into dataset
          hx=[hx; candidate_position];  hf=[hf, candidate_fit];      
          % update gfs for plotting
          CE(NFEs,:)=[NFEs,candidate_fit];
          gfs(1,NFEs)=min(CE(1:NFEs,2));
          if  candidate_fit == min(hf)
              flag = 1;
              disp(['Current optimal value = ' num2str(candidate_fit) ' NFE=' num2str(NFEs)]);
          end  
     end
end
end
         