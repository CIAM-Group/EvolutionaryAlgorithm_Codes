function [K,Fs,P]=GMMOR(Population,All_Fs, Lambda,Kmax)
    [IDx,~]=GMM_cluster(Population.objs,Kmax);   
    % The number of Clusters                 
    K=max(IDx) ;   
    Objectives=Population.objs;
    Objectives=Objectives(:,All_Fs);
    for k=1:K        
        new_Fs{k}=LHA(Objectives(IDx==k,:),Lambda);   
        Fs{k}=All_Fs(new_Fs{k});
        P{k}=Population(IDx==k);
    end       
end
