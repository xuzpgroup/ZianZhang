function show_figure(id)
    global db
    path='E:\Data\Literature Data\S-N\';
    figure(2)
    
    if exist([path,id,'.jpeg'])
        imshow([path,id,'.jpeg'])
    elseif exist([path,id,'.png'])
        imshow([path,id,'.png'])
    else
        disp('NOT FOUND')
    end
    set(gcf,'Units','centimeter','Position',[0,0,15,8])
    nsn=numel(db);
    for i=1:nsn
        if ischar(db(i).figname)
            if strcmp(db(i).figname,id)
                disp(db(i).figpath)
                break;
            end
        elseif isnumeric(db(i).figname)
            if db(i).figname==str2num(id)
                disp(db(i).figpath)
                disp(db(i).figid)
                break;
            end
        end
    end
end