path='/YOUR_PATH/';
file='FatigueData-CMA2022.mat';
prop='fs';                          % fatigue strength
para={1e6,'linear','exclude all'};  % cycles to calculate fatigue strength | fitting type | run-out data processing
load([path,file])

ds=fatiguedata_cma2022.articles(1).scidata.datasets(1);
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
        x0=data(:,2);
        y0=data(:,1);
        ro=data(:,3);
        id_ro=find(ro==1);
        id_f=find(ro==0);
        [~,tmp]=max(x0(id_ro));
        id_max=id_ro(tmp);
        if strcmp(fittype,'linear')
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
            [A2,B2,sigma22]=linear_fit(y,x) ;  
            fs=10^(A2+B2*log10(cycle));
        elseif strcmp(fittype,'stromeryer')
            x=x0(id_f);
            y=y0(id_f);
            n=numel(x);
            minx=min(x);
            x_ex=[];
            y_ex=[];
            n_ex=0;
            for i=1:numel(id_ro)
                if x0(id_ro(i))>minx
                    n=n+1;
                    x(n)=x0(id_ro(i));
                    y(n)=y0(id_ro(i));
                else
                    n_ex=n_ex+1;
                    x_ex(n_ex)=x0(id_ro(i));
                    y_ex(n_ex)=y0(id_ro(i));
                end
            end
            try
                [A,B,C]=stromeryer_fit(x,y);
                fs=10.^((log10(cycle)-A)/B)+C;
            catch
                disp('fail to fit by the Stromeryer equation, use linear fit instead')
                x=x0(id_f);
                y=y0(id_f);
                fs=cal_fs(data,cycle,'linear',rotype);
            end
        end
    else
        disp(['Warning: fatigue data < 2, not calculated'])
    end
end

function [A,B,sigma2]=linear_fit(x,y)
    x=log10(x);
    y=log10(y);
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

function [A,B,C]=stromeryer_fit(x,y)
    n=numel(x);
    minx=min(x);
    ftype=fittype('a+b*log10(x-c)','problem','c','dependent',{'y'},'independent',{'x'},'coefficients',{'a','b'});
    f=fit(x,log10(y),ftype,'problem',minx/2);
    
    fopt=fitoptions();
    ftype=fittype('a+b*log10(x-c)','dependent',{'y'},'independent',{'x'},'coefficients',{'a','b','c'});
    myfit=fit(x,log10(y),ftype,'StartPoint',[f.a,f.b,minx/2]);
    A=myfit.a;
    B=myfit.b;
    C=myfit.c;
end