function offspring = EDA(ghx, LB, UB, T)

      mu =mean(ghx, 1);
      sigma2 = cov(ghx);
      offspring = mvnrnd(mu, sigma2, T*(size(ghx, 1)));
      VRmin2=repmat(LB,size(offspring,1),1);
      VRmax2=repmat(UB,size(offspring,1),1);
      for i2 =1:size(offspring,1)
          indexB = find(offspring(i2, :) < VRmin2(1, 1) | offspring(i2, :) > VRmax2(1,1));
          offspring(i2, indexB)= VRmin2(i2,indexB)+rand*(VRmax2(i2,indexB)-VRmin2(i2,indexB));
      end

      
end