function data=symbol_recognition(rgb,bw,symbol,symbol_bw,incbox,excbox)
    DEBUG=0;
    
    data={};
    thre_blank=256-40;
    thre_colordev=30;
    thre_colordev_tot=60;
    thre_shape=0.90;
    thre_color=0.3;
    h=size(rgb,1);
    w=size(rgb,2);
    [row0,col0]=find(bw==0);
    [row0,col0]=select_pix(row0,col0,incbox,excbox);
    for i=1:numel(symbol)
        if DEBUG
            figure(1)
            imshow(symbol{i})
        end
        hs=size(symbol{i},1);
        ws=size(symbol{i},2);
        xeff=[];
        yeff=[];
        ct=0;
        color_tp=[];
        mask=[];
        data{i}=[];

        nfill=sum(~symbol_bw{i},'all');
        [row,col]=search_space(row0,col0,hs,ws,h,w);
        np=numel(row);
        degree=[];
        ct=0;
        [row2,col2]=find(symbol_bw{i}==0);
        center=[mean(col2),mean(row2)];
        score_shape=zeros(h,w);
        score_color=zeros(h,w);
        pos=[];
        for j=1:np
            % shape
            delta=[];
            color_target=[];
            match=[];
            blank=[];
            
            symbol{i}=double(symbol{i});
            pad_bw=bw(row(j):row(j)+hs-1,col(j):col(j)+ws-1);
            delta=~xor(pad_bw,symbol_bw{i});
            mask=and(delta,~symbol_bw{i});

            nmatch=sum(mask,'all');
            sscore=nmatch/nfill;
            if sscore>=thre_shape
                pad=double(rgb(row(j):row(j)+hs-1,col(j):col(j)+ws-1,1:3));
                delta=double(abs(pad-symbol{i}));        
                delta(:,:,1)=delta(:,:,1)+(~mask)*255;
                delta(:,:,2)=delta(:,:,2)+(~mask)*255;
                delta(:,:,3)=delta(:,:,3)+(~mask)*255;
                %s2=sum(delta,3);                     
                delta(delta<=thre_colordev)=1;
                delta(delta>thre_colordev)=0;
                s1=sum(delta,3);
                s1(s1<3)=0;
                s1(s1==3)=1;
                %s2(s2<=thre_colordev_tot)=1;
                %s2(s2>thre_colordev_tot)=0;
                %s1=and(s1,s2);
                cscore=sum(s1,'all')/nfill;
                if cscore>thre_color
                    ct=ct+1;
                    pos(ct,1:2)=round([col(j)+center(1)-1,row(j)+center(2)-1]);
                    pos(ct,1)=min(pos(ct,1),w);
                    pos(ct,1)=max(pos(ct,1),1);
                    pos(ct,2)=min(pos(ct,2),h);
                    pos(ct,2)=max(pos(ct,2),1);                    
                    score_shape(pos(ct,2),pos(ct,1))=sscore;
                    score_color(pos(ct,2),pos(ct,1))=cscore;
                    if DEBUG
                        figure(1)
                        set(gcf,'unit','centimeters','position',[1.5,7,10,10]);
                        subplot(3,2,1)
                        imshow(symbol{i})
                        subplot(3,2,2)
                        imshow(pad);
                        subplot(3,2,3)
                        imshow(s1);
                        subplot(3,2,4)
                        imshow(mask)
                        %subplot(3,2,5)
                        %imshow(s2)                    
                    end                     
                end                               
            end             
        end         
        im0=zeros(h,w);
        ind=sub2ind([h,w],pos(:,2),pos(:,1));
        im0(ind)=1;
        bwcn=bwconncomp(im0);
        pid=bwcn.PixelIdxList;
        nobj=bwcn.NumObjects;
        for j=1:nobj
            [row3,col3]=ind2sub([h,w],pid{j});
            cs1=score_color(pid{j});
            ss1=score_shape(pid{j});
            y=sum(row3.*ss1,'all')/sum(ss1,'all');
            x=sum(col3.*ss1,'all')/sum(ss1,'all');
            data{i}(j,1:2)=[x,y];
        end
    end
end

function [row,col]=search_space(row,col,hs,ws,maxh,maxw)
    np=numel(row);
    h2=hs; %ceil(hs/2);
    w2=ws; %ceil(ws/2);
    for i=1:np
        row2=[row(i)-h2:row(i)+h2]';
        col2=[col(i)-h2:col(i)+h2]';
        row=[row;row2];
        col=[col;col2];
    end
    id=[row,col];
    id=unique(id,'rows');
    row=id(:,1);
    col=id(:,2);
    incl=find(row>=1);
    incl=intersect(find(row<=maxh-hs+1),incl);
    incl=intersect(find(col>=1),incl);
    incl=intersect(find(col<=maxw-ws+1),incl);
    row=row(incl);
    col=col(incl);
end


function [row,col]=select_pix(row0,col0,incbox,excbox)
    row=[];
    col=[];
    ct=0;
    for j=1:numel(row0)
        flag_in=0;
        for k=1:numel(incbox)
            if inbox1([col0(j),row0(j)],incbox{k})
                flag_in=1;
                break;
            end
        end
        flag_ex=0;
        for k=1:numel(excbox)
            if inbox1([col0(j),row0(j)],excbox{k})
                flag_ex=1;
                break;
            end
        end  
        if flag_in && ~flag_ex
            ct=ct+1;
            row(ct,1)=row0(j);
            col(ct,1)=col0(j);
        end    
    end
end