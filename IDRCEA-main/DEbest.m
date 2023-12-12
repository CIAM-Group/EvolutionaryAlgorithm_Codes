
% DEoperating consist of mutation and crossover
function [UU] = DEbest(P,Xpbest,F,CR,UB,LB,T)
    [NP,Dim] = size(P);
    UU=[];
    for jj =1 :T
        
        for i=1:NP 
            F1=F(randi([1,length(F)],1,1));
            CR1=CR(randi([1,length(CR)],1,1))';
            % mutation
            k0=randi([1,NP]);
            while(k0==i)
                k0=randi([1,NP]);   
            end
            P1=P(k0,:);
            k1=randi([1,NP]);
            while(k1==i||k1==k0)
                k1=randi([1,NP]);
            end
            P2=P(k1,:);
    %       Xpbest = hisx(1,:);
            V(i,:)=Xpbest+F1.*(P1-P2); 
            % bound
            for j=1:Dim
              if (V(i,j)>UB(i,j)||V(i,j)<LB(i,j))
                 V(i,j)=LB(i,j)+rand*(UB(i,j)-LB(i,j));         
              end
            end

            % crossover
            jrand=randi([1,Dim]); 
            for j=1:Dim
                k3=rand;
                if(k3<=CR1||j==jrand)
                    U(i,j)=V(i,j);
                else
                    U(i,j)=P(i,j);      
                end
            end
        end
        UU = [UU;U];
    end
end