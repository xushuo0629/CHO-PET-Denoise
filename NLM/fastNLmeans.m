function DenoisedImg=fastNLmeans(I,ds,Ds,h)  
%I:含噪声图像  
%ds:邻域窗口半径   =5
%Ds:搜索窗口半径   =5
%h:高斯函数平滑参数  =5
%DenoisedImg：去噪图像  
% 一般而言，考虑到算法复杂度，搜索区域大概取21x21，相似度比较的块的可以取7x7。
% 实际中，常常需要根据噪声来选取合适的参数。
% 当高斯噪声的标准差σ 越大时，为了提高算法鲁棒性，需要增大块区域，同样也需要增加搜索区域。
% 同时，滤波系数h 与 σ 满足正相关：h=kσ，当块变大时，k 需要适当减小。

I=double(I);  
[m,n]=size(I);  
PaddedImg = padarray(I,[Ds+ds+1,Ds+ds+1],'symmetric','both');  
PaddedV = padarray(I,[Ds,Ds],'symmetric','both');  
average=zeros(m,n);  
sweight=average;  
wmax=average;  
h2=h*h;  
d2=(2*ds+1)^2;  
for t1=-Ds:Ds  
    for t2=-Ds:Ds  
        if(t1==0&&t2==0)  
            continue;  
        end  
        St=integralImgSqDiff(PaddedImg,Ds,t1,t2);  
        v = PaddedV(1+Ds+t1:end-Ds+t1,1+Ds+t2:end-Ds+t2);  
        w=zeros(m,n);  
        for i=1:m  
            for j=1:n  
                i1=i+ds+1;  
                j1=j+ds+1;  
                Dist2=St(i1+ds,j1+ds)+St(i1-ds-1,j1-ds-1)-St(i1+ds,j1-ds-1)-St(i1-ds-1,j1+ds);  
                Dist2=Dist2/d2;  
                w(i,j)=exp(-Dist2/h2);  
                sweight(i,j)=sweight(i,j)+w(i,j);  
                average(i,j)=average(i,j)+w(i,j)*v(i,j);  
            end  
        end  
        wmax=max(wmax,w);  
    end  
end  
average=average+wmax.*I;  
sweight=sweight+wmax;  
DenoisedImg=average./sweight;  
