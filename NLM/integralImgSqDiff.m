
function Sd = integralImgSqDiff(PaddedImg,Ds,t1,t2)  
%PaddedImg：边缘填充后的图像  
%Ds:搜索窗口半径  
%(t1,t2):偏移量  
%Sd:积分图像  
[m,n]=size(PaddedImg);  
m1=m-2*Ds;  
n1=n-2*Ds;  
Sd=zeros(m1,n1);  
Dist2=(PaddedImg(1+Ds:end-Ds,1+Ds:end-Ds)-PaddedImg(1+Ds+t1:end-Ds+t1,1+Ds+t2:end-Ds+t2)).^2;  
for i=1:m1  
    for j=1:n1  
         if i==1 && j==1  
             Sd(i,j)=Dist2(i,j);  
         elseif i==1 && j~=1  
             Sd(i,j)=Sd(i,j-1)+Dist2(i,j);   
         elseif i~=1 && j==1  
             Sd(i,j)=Sd(i-1,j)+Dist2(i,j);  
         else  
             Sd(i,j)=Dist2(i,j)+Sd(i-1,j)+Sd(i,j-1)-Sd(i-1,j-1);  
         end  
     end  
end  