function data=extract_data_by_color(rgb,color,incbox,excbox)
    h=size(rgb,1);
    w=size(rgb,2);
    crit=30;
    for i=1:numel(color)
        ct=0;
        data_tmp=[];        
        for i2=1:size(color{i},1)
            c=reshape(color{i}(i2,:),[1,1,3]);
            if isempty(c)
                continue
            end

            if ~sum(isnan(c),'all')
                delta=abs(double(rgb)-double(c));
                delr=delta(:,:,1);
                delg=delta(:,:,2);
                delb=delta(:,:,3);
                indr=find(delr<=crit);
                indg=find(delg<=crit);
                indb=find(delb<=crit);
                tmp=intersect(indr,indg);
                candidate=intersect(tmp,indb);
                [I,J]=ind2sub([h,w],candidate);
                for j=1:numel(I)
                    flag_in=0;
                    for k=1:numel(incbox)
                        if inbox1([J(j),I(j)],incbox{k})
                            flag_in=1;
                            break;
                        end
                    end
                    flag_ex=0;
                    for k=1:numel(excbox)
                        if inbox1([J(j),I(j)],excbox{k})
                            flag_ex=1;
                            break;
                        end
                    end  
                    if flag_in && ~flag_ex
                        ct=ct+1;
                        data_tmp(ct,1:2)=[J(j),I(j)];
                    end    
                end
            end
        end
        data{i}=unique(data_tmp,'rows');
    end