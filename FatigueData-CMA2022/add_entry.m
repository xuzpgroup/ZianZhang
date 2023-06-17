path='\YOUR_PATH\';
file='FatigueData-CMA2022.mat';
load([path,file])

db=fatiguedata_cma2022;
entry='hardness';       % the name of the entry
epath='.static_mech';   % the path from fatigue datasets to the destination 
unit='HV';              % the unit of the entry
data={1,1,[300]; ...
      2,3,[200]};  % each line is a data triplet, column 1: the id of article; column 2: the id of dataset; column 3: value;

db=add_data_entry(db,entry,epath,data,unit);
  
function db=add_data_entry(db,entry,epath,data,unit)
    if isfield(db.unit,entry)
        disp(['Warning: the unit of entry ',entry,' exists, added as ',entry,'_user']);
        db.unit=setfield(db.unit,[entry,'_user'],unit);
    else
        db.unit=setfield(db.unit,entry,unit);
    end
    art=db.articles;
    na=numel(art);
    for i=1:na
        ds=art(i).scidata.datasets;
        ns=numel(ds);
        for j=1:ns
            try
                eval(sprintf('db.articles(%d).scidata.datasets(%d)%s.%s=[];',i,j,epath,entry));
            catch
                disp(['Fail to add entry ''',entry,'''']);
                return
            end
        end
    end
    for i=1:size(data,1)
        try
            eval(sprintf('db.articles(%d).scidata.datasets(%d)%s.%s=data{%d,3};',data{i,1},data{i,2},epath,entry,i));
        catch
            disp(['Fail to add value at article ',num2str(data{i,1}),' dataset ',num2str(data{i,2})]);
        end
    end
end
