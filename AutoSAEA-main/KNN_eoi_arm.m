function  [hx, hf, reward ,NFEs, CE, gfs] = KNN_eoi_arm(ghx, ghf, offspring, hx, hf, FUN, NFEs, level, CE, gfs)
         
% {Knn, L1-exploitation}
     
      sidx = 1:length(ghf); %ghx and ghf have been sorted
      train_label1 = ceil(sidx*level/length(ghf)); % Obtain the label for classfier
      Parents_L1 = ghx(find(train_label1==1), :);
      
      mdl =ClassificationKNN.fit(ghx,train_label1,'Distance','minkowski');% knn classfier
      mdl.DistParameter = 2;
         
     %the prediction of knn
      label = predict(mdl,offspring); %rank 1
      select_pp = find(label == min(label));
      for ii3 = 1: length(select_pp)
         for j = 1 : size(Parents_L1, 1)
            dist(ii3,j) =  sqrt(sum((offspring(select_pp(ii3), :)-Parents_L1(j, :)).^2, 2));
         end
      end
      max_dist = max(dist,[],2); 
      [~, in] = min(max_dist);
      candidate_position = offspring(select_pp(in),:);
      [~,ih,~] = intersect(hx,candidate_position,'rows');  
      if isempty(ih)==1
         candidate_fit=FUN(candidate_position); 
         NFEs = NFEs + 1;

        % save candidate into dataset, and sort dataset
         hx=[hx; candidate_position];  hf=[hf, candidate_fit];       % update history database
        
        % update gfs for plotting 
         CE(NFEs,:)=[NFEs,candidate_fit];
         gfs(1,NFEs)=min(CE(1:NFEs,2));
        % update the low level arm reward 
         Arm = num2str('KNN_L1-exploitation ');
         [reward] = Low_level_r(ghf, hf, candidate_fit, NFEs, Arm);
        
     else
         reward = 0; % current database has not update 
     end
         
end