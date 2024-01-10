function [IDx,Sigma]=GMM_cluster(X,Kmax)
warning off
%% input: X is the data set, each row is a sample 
%% input: Kmax is the maximum number of cluster 
%% output: IDx is the cluster ID of each solution
%% output: Sigma is the covariance matrix of each cluster 

         Options=statset('TolFun',10e-08,'MaxIter',200);
         for k=1:Kmax 
             gmfit{k} = fitgmdist(X,k,'RegularizationValue',0.001, 'CovarianceType','diagonal','Replicates',20,'Start','randSample','Options',Options);
             %gmfit{k} = fitgmdist(X,k,'RegularizationValue',10e-04, 'CovarianceType','full','Replicates',20,'Start','randSample','Options',Options);
            bic(k)=gmfit{k}.BIC;
            SIGMA{k}=gmfit{k}.Sigma;
         end       
        bic_k=[bic',[1:Kmax]'];
        min_bic_k=min(bic_k);
        max_bic_k=max(bic_k);               
        norm_bic_k=(bic_k-repmat(min_bic_k,Kmax,1))./repmat(max_bic_k-min_bic_k,Kmax,1);        
        d=sqrt(sum(norm_bic_k.^2,2));
        [~,k]=min(d);
        IDx=cluster(gmfit{k},X);
        Sigma=SIGMA{k};
end