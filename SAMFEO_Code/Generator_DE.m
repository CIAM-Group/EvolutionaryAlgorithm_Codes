function U=Generator_DE(i,Pop,parent,parent_size,minVar,maxVar,n,F,CR,M)       

       U=[];
      %% DE/rand/bin  
       R=randi([1,parent_size],M,3);     
       F1=F(1:M); CR1=CR(1:M);
       V1=parent(R(:,1),:)+repmat(F1,1,n).*(parent(R(:,2),:)-parent(R(:,3),:));                                                                              
       t=rand(M,n)<=repmat(CR1,1,n);
       jrand=randi([1,n],1,M)';
       jrand_index=n*[0:M-1]'+jrand;
       t(jrand_index)=1;                      
       U1=t.*V1+(1-t).*repmat(Pop(i,:),M,1); 
       U1= Repair(U1, [minVar;maxVar]);     
       U=[U;U1]; 
       
       %% DE/current-to-rand/bin 
       R=randi([1,parent_size],M,3);     
       F2=F(M+1:2*M); CR2=CR(M+1:2*M);
       V2=repmat(Pop(i,:),M,1)+repmat(F2,1,n).*(parent(R(:,1),:)-repmat(Pop(i,:),M,1))+repmat(F2,1,n).*(parent(R(:,2),:)-parent(R(:,3),:));
       t=rand(M,n)<=repmat(CR2,1,n);
       jrand=randi([1,n],1,M)';
       jrand_index=n*[0:M-1]'+jrand;
       t(jrand_index)=1;                      
       U2=t.*V2+(1-t).*repmat(Pop(i,:),M,1); 
       U2= Repair(U2, [minVar;maxVar]);
       U=[U;U2];
                
      %% DE/current-to-pbest/bin  
       pbestid=randi([1,ceil(0.4*parent_size)],M,1);
       R=randi([1,parent_size],M,2);     
       F3=F(2*M+1:3*M); CR3=CR(2*M+1:3*M);      
       V3=repmat(Pop(i,:),M,1)+repmat(F3,1,n).*(parent(pbestid,:)-repmat(Pop(i,:),M,1))+repmat(F3,1,n).*(parent(R(:,1),:)-parent(R(:,2),:));    
       t=rand(M,n)<=repmat(CR3,1,n);
       jrand=randi([1,n],1,M)';
       jrand_index=n*[0:M-1]'+jrand;
       t(jrand_index)=1;                      
       U3=t.*V3+(1-t).*repmat(Pop(i,:),M,1);       
       U3= Repair(U3, [minVar;maxVar]);                
       U=[U;U3];                 
       
       %% DE/best/1
       R=randi([1,parent_size],M,2);       
       F4=F(3*M+1:4*M); CR4=CR(3*M+1:4*M);
       V4=repmat(parent(1,:),M,1)+repmat(F4,1,n).*(parent(R(:,1),:)-parent(R(:,2),:));     
       t=rand(M,n)<=repmat(CR4,1,n);
       jrand=randi([1,n],1,M)';
       jrand_index=n*[0:M-1]'+jrand;
       t(jrand_index)=1;                      
       U4=t.*V4+(1-t).*repmat(Pop(i,:),M,1); 
       U4= Repair(U4, [minVar;maxVar]);
       U=[U;U4];
             
       %% DE/rand/2
       R=randi([1,parent_size],M,5);   
       F5=F(4*M+1:5*M); CR5=CR(4*M+1:5*M);
       V5=parent(R(:,1),:)+repmat(F5,1,n).*(parent(R(:,2),:)-parent(R(:,3),:))+repmat(F5,1,n).*(parent(R(:,4),:)-parent(R(:,5),:));                                           
       t=rand(M,n)<=repmat(CR5,1,n);
       jrand=randi([1,n],1,M)';
       jrand_index=n*[0:M-1]'+jrand;
       t(jrand_index)=1;                      
       U5=t.*V5+(1-t).*repmat(Pop(i,:),M,1); 
       U5= Repair(U5, [minVar;maxVar]);
       U=[U;U5];
             
end