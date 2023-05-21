clear;
path0='';
file='FatigueData-CMA2022.mat';
load([path0,file]);

art=fatiguedata_cma2022.articles;
na=numel(art);
for i=1:na
    ds=art(i).scidata.datasets;
    nd=numel(ds);
    for j=1:nd
        fatiguedata_cma2022.articles(i).scidata.datasets(j).score=cal_rating_score(fatiguedata_cma2022.articles(i).scidata.datasets(j));
    end
end    


function score=cal_rating_score(ds,type)
    tot=0;
    fill=0;
    
    [t,f]=fill_rate_field(ds.fatigue);
    tot=tot+t;
    fill=fill+f;
    
    [t,f]=fill_rate_field(ds.materials);
    tot=tot+t;
    fill=fill+f;    
   

    [t,f]=fill_rate_field(ds.processing);
    tot=tot+t;
    fill=fill+f;     
    
    [t,f]=fill_rate_field(ds.testing);
    tot=tot+t;
    fill=fill+f;   
    
    [t,f]=fill_rate_field(ds.static_mech);
    tot=tot+t;
    fill=fill+f;  

    score=fill/tot;
end

function [tot,fill]=fill_rate_field(field)
    tot=0;
    fill=0;
    fn=fieldnames(field);
    for i=1:numel(fn)
        tot=tot+1;
        f=getfield(field,fn{i});
        if ~isempty(f)
            fill=fill+1;
        end
    end
end
