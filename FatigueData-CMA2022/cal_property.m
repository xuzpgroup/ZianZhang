path='/YOUR_PATH/';
file='FatigueData-CMA2022.mat';
prop='fs';     % fatigue strength
para={1e6,'linear','exclude all'};  % cycles to calculate fatigue strength | fitting type | run-out data processing
load([path,file])

ds=fatiguedata_cma2022.articles(30).scidata.datasets(1);
fs=cal_prop(ds,prop,para);

function p=cal_prop(ds,prop,para)
    p=nan;
    if strcmp(prop,'fs')
        if strcmp(ds.fatigue.fdata_type,'sn')
            cycle=para{1};
            fittype=para{2};
            rotype=para{3};
            p=cal_fs(ds.fatigue.fat_data,cycle,fittype,rotype);
        end
    end
end

function fs=cal_fs(data,cycle,fittype,rotype)
    fs=[];       
    if size(data,1)>=2
        x0=log10(data(:,2));
        y0=log10(data(:,1));
        ro=data(:,3);
        id_ro=find(ro==1);
        id_f=find(ro==0);
        [~,tmp]=max(x0(id_ro));
        id_max=id_ro(tmp);
        if strcmp(rotype,'exclude all')
            x=x0(id_f);
            y=y0(id_f);
        elseif strcmp(rotype,'include all')
            x=x0; 
            y=y0;
        elseif strcmp(rotype,'include max')
            x=x0(id_f);
            y=y0(id_f);   
            n=numel(x);
            x(n+1)=x0(id_max);
            y(n+1)=y0(id_max);
        end
        if strcmp(fittype,'linear')
            [A2,B2,sigma22]=linear_fit(y,x) ;  
            fs=10^(A2+B2*log10(cycle));
        end
    else
        disp(['Warning: fatigue data < 2, not calculated'])
    end
end

function [A,B,sigma2]=linear_fit(x,y)
    n=numel(x);
    xm=mean(x);
    ym=mean(y);
    term1=sum((x-xm).*(y-ym));
    term2=sum((x-xm).^2);
    B=term1/term2;
    A=ym-B*xm;
    yp=A+B*x;
    sigma2=sum((y-yp).^2)/(n-2);
end