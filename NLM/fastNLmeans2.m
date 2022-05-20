function DenoisedImg=fastNLmeans2(I,ds,Ds,h)
I=double(I);
[m,n]=size(I);
PaddedImg = padarray(I,[Ds+ds+1,Ds+ds+1],'symmetric','both');
PaddedV = padarray(I,[Ds,Ds],'symmetric','both');
average=zeros(m,n);
wmax=average;
sweight=average;
h2=h*h;
d=(2*ds+1)^2;
for t1=-Ds:Ds
    for t2=-Ds:Ds
        if(t1==0&&t2==0)
            continue;
        end
        Sd=integralImgSqDiff(PaddedImg,Ds,t1,t2);
        SqDist2=Sd(2*ds+2:end-1,2*ds+2:end-1)+Sd(1:end-2*ds-2,1:end-2*ds-2)...
               -Sd(2*ds+2:end-1,1:end-2*ds-2)-Sd(1:end-2*ds-2,2*ds+2:end-1);
        SqDist2=SqDist2/d;
        w=exp(-SqDist2/h2);
        v = PaddedV(1+Ds+t1:end-Ds+t1,1+Ds+t2:end-Ds+t2);
        average=average+w.*v;
        wmax=max(wmax,w);
        sweight=sweight+w;
    end
end
average=average+wmax.*I;
average=average./(wmax+sweight);
DenoisedImg = average;

function Sd = integralImgSqDiff(PaddedImg,Ds,t1,t2)
Dist2=(PaddedImg(1+Ds:end-Ds,1+Ds:end-Ds)-PaddedImg(1+Ds+t1:end-Ds+t1,1+Ds+t2:end-Ds+t2)).^2;
Sd = cumsum(Dist2,1);
Sd = cumsum(Sd,2);