% <mark_r> the height of the xaxis in pixels
% <mark_c> the width of the xaxis in pixels
function [px1,px2,py1,py2,x1,x2,y1,y2]=calibrate_axis(xaw,yaw,mark_r,mark_c,xxtick_num,yytick_num,xtlcl_box,ytlcl_box,bw)
    DEBUG=0;
    px1=nan;
    px2=nan;
    py1=nan;
    py2=nan;
    x1=nan;
    x2=nan;
    y1=nan;
    y2=nan;
    w=size(bw,2);
    h=size(bw,1);
    nx=numel(xxtick_num);
    ny=numel(yytick_num);
    % % find the first non-nan xtick label
    ct=1;
    while (isnan(xxtick_num(ct)))&&(ct<nx)
        ct=ct+1;
    end
    x1=xxtick_num(ct);
    box=xtlcl_box(ct,:);
    xmean=round((box(1)+box(2))/2);                           % center of the xtick label
    xlimit=[max([box(1),min(mark_c)-2,1]),box(2)];            % the x limit to find the ticks
    ylimit=[min(mark_r)-ceil((box(4)-box(3))/2),box(3)-1];    % use the height of tick label
    %px1=calibrate_xaxis(xaw,mark_r,xmean,xlimit,bw);
    px1=calibrate_xaxis2(xaw,mark_r,xlimit,ylimit,bw,1);
    % if found no tick for the tick label, use the mean position of the
    % tick label
    if isnan(px1)
        px1=xmean;
    end   
    
    % % find the last non-nan xtick label
    ct=nx;
    while (isnan(xxtick_num(ct)))&&(ct>1)
        ct=ct-1;
    end  
    x2=xxtick_num(ct);
    box=xtlcl_box(ct,:);    
    xmean=round((box(1)+box(2))/2);
    xlimit=[box(1),box(2)];
    ylimit=[min(mark_r)-ceil((box(4)-box(3))/2),box(3)-1];    % use the height of tick label
    %px2=calibrate_xaxis(xaw,mark_r,xmean,xlimit,bw);
    px2=calibrate_xaxis2(xaw,mark_r,xlimit,ylimit,bw,2);
    if isnan(px2)
        px2=xmean;
    end
    
    % % find the first non-nan ytick label
    ct=ny;
    while (isnan(yytick_num(ct)))&&(ct>1)
        ct=ct-1;
    end   
    y1=yytick_num(ct);
    box=ytlcl_box(ct,:);    
    ymean=round((box(3)+box(4))/2);
    xlimit=[box(2)+1,max(mark_c)+ceil((box(2)-box(1))/2)];
    ylimit=[box(3),box(4)];
    %py1=calibrate_yaxis(yaw,mark_c,ymean,xlimit,bw);   
    py1=calibrate_yaxis2(yaw,mark_c,xlimit,ylimit,bw);   
    if isnan(py1)
        py1=ymean;
    end
    
    % % find the last non-nan xtick label
    ct=1;
    while (isnan(yytick_num(ct)))&&(ct<ny)
        ct=ct+1;
    end  
    y2=yytick_num(ct);
    box=ytlcl_box(ct,:);  
    ymean=round((box(3)+box(4))/2);
    xlimit=[box(2)+1,max(mark_c)+ceil((box(2)-box(1))/2)];
    ylimit=[box(3),min([box(4),h,max(mark_r)+2])];
    %py2=calibrate_yaxis(yaw,mark_c,ymean,xlimit,bw);
    py2=calibrate_yaxis2(yaw,mark_c,xlimit,ylimit,bw);
    if isnan(py2)
        py2=ymean;
    end
    if DEBUG
        rbot=max(mark_r);
        cleft=min(mark_c);
        imshow(bw)
        hold on
        p(1)=plot(px1,rbot,'b.','MarkerSize',20)
        p(2)=plot(px2,rbot,'r.','MarkerSize',20)
        p(3)=plot(cleft,py1,'b.','MarkerSize',20)
        p(4)=plot(cleft,py2,'r.','MarkerSize',20)        
        delete(p)
    end
end

function x=calibrate_xaxis2(xaw,mark_r,xlimit,ylimit,bw,type)
    % % type: 1: the left anchor; 2: the right anchor
    DEBUG=0;
    if DEBUG
        figure(1)
        imshow(bw);
        hold on
    end
    bwr=bw*(0-1)+1;
    top=[];
    bot=[];
    xrng=[xlimit(1):xlimit(2)];
    x=mean(xrng);
    for i=1:numel(xrng)
        ct2=min(mark_r);
        while ct2>ylimit(1)
            if bwr(ct2,xrng(i))==1
                ct2=ct2-1;
            else
                break;
            end
        end
        top(i)=ct2;
        
        ct2=max(mark_r);
        while ct2<ylimit(2)
            if bwr(ct2,xrng(i))==1
                ct2=ct2+1;
            else
                break;
            end
        end
        bot(i)=ct2; 
        if DEBUG
            p=plot([xrng(i),xrng(i)],[top(i),bot(i)],'b.-','MarkerSize',10);
            delete(p);
        end
    end
    len=bot-top;
    maxl=max(len);
    id=find(len==maxl);
    sum1=0;
    width=1;
    if type==1                  % the left anchor, in case grid is on and influence the desicion
        sum1=sum1+xrng(id(1));
        for i=2:numel(id)
            if (id(i)-id(i-1))==1
                sum1=sum1+xrng(id(i));
                width=width+1;
            else
                break;
            end
        end
    elseif type==2              % the right anchor, in case grid is on and influence the desicion
        sum1=sum1+xrng(id(end));
        for i=numel(id)-1:-1:1
            if (id(i+1)-id(i))==1
                sum1=sum1+xrng(id(i));
                width=width+1;
            else
                break;
            end
        end
    end
    x=sum1/width;
end


function y=calibrate_yaxis2(yaw,mark_c,xlimit,ylimit,bw)
    % % type: 1: the bottom anchor; 2: the top anchor
    % % zza: the parameter 'type' can be added as func calibrate_xaxis2 
    DEBUG=0;
    if DEBUG
        figure(1)
        imshow(bw);
        hold on
    end
    bwr=bw*(0-1)+1;
    left=[];
    right=[];
    yrng=[ylimit(1):ylimit(2)];
    y=mean(yrng);
    for i=1:numel(yrng)
        ct2=min(mark_c);
        while ct2>xlimit(1)
            if bwr(yrng(i),ct2)==1
                ct2=ct2-1;
            else
                break;
            end
        end
        left(i)=ct2;
        
        ct2=max(mark_c);
        while ct2<xlimit(2)
            if bwr(yrng(i),ct2)==1
                ct2=ct2+1;
            else
                break;
            end
        end
        right(i)=ct2;  
        if DEBUG
            p=plot([left(i),right(i)],[yrng(i),yrng(i)],'b.-','MarkerSize',10);
            delete(p);
        end
    end
    len=right-left;
    maxl=max(len);
    id=find(len==maxl);
    sum1=0;
    for i=1:numel(id)
        sum1=sum1+yrng(id(i));
    end
    y=sum1/numel(id);
end

function x=calibrate_xaxis(xaw,mark_r,cmean0,limit,bw)
    DEBUG=0;
    if DEBUG
        figure(1)
        imshow(bw);
        hold on
    end
    w=size(bw,2);
    h=size(bw,1);
    x=nan;
    bwr=bw*(0-1)+1;
    % % extend to the bottom first
    ifget=0;
    rbot=max(mark_r);
    rbot0=rbot;
    rtop=min(mark_r);
    rtop0=rtop;  
    direction=0;
    % % detect the initial tick
    len=0;
    plus=min(xaw,3);     % zza: adjustable para.
    ifdetect=0;
    len=sum(bwr((rtop0-plus):(rbot0+plus),cmean0));
    if DEBUG
        p=plot(cmean0,rbot,'r.');
        delete(p)
    end
    if len>=xaw+plus
        ifdetect=1;
        cmean=cmean0;
    end
    shift=0;
    dlimit=(limit(2)-limit(1))/2;
    while (~ifdetect)&&(shift<dlimit)
        shift=shift+1;
        cmean1=cmean0-shift;
        len=sum(bwr((rtop0-plus):(rbot0+plus),cmean1));
        if len>=xaw+plus
            ifdetect=1;
            cmean=cmean1;
            direction=-1;
            break;
        end
        cmean2=cmean0+shift;
        len=sum(bwr((rtop0-plus):(rbot0+plus),cmean2));
        if len>=xaw+plus
            ifdetect=1;
            cmean=cmean2;
            direction=1;
            break;
        end 
        if DEBUG
            p(1)=plot(cmean1,rbot,'r.');
            p(2)=plot(cmean2,rbot,'r.');
            delete(p);
        end
    end   
    if ~ifdetect
        x=nan;
        return;
    end
    while (bwr(rbot+1,cmean)==1)&& ((rbot-rbot0)<xaw*4)  % zza: adjustable para.
        if DEBUG
            p=plot(cmean,rbot,'r.');
            delete(p);
        end
        rbot=rbot+1;
    end
    len=rbot-rbot0;
    if len>3     % zza: adjustable para.
        for i=cmean-1:-1:limit(1)
            len1=sum(bwr((rbot0+1):rbot,i));
            if len1<len*0.95        % zza: adjustable para.
                break;
            end
            if DEBUG
                p=plot([i,i],[rbot0+1,rbot]);
                delete(p);
            end
        end
        xleft=i+1;
        for i=(cmean+1):limit(2)
            len1=sum(bwr((rbot0+1):rbot,i));
            if len1<len*0.95        % zza: adjustable para.
                break;
            end
        end
        xright=i-1;
        ifget=1;
    end
    % % extend to the top
    if ~ifget
        len=0;
        while (bwr(rtop-1,cmean)==1) && ((rtop0-rtop)<xaw*4)     % zza: adjustable para.
            rtop=rtop-1;
        end
        len=rtop0-rtop;
        if len>3     % zza: adjustable para.
            for i=cmean-1:-1:limit(1)
                len1=sum(bwr(rtop:rtop0-1,i));
                if len1<len*0.95        % zza: adjustable para.
                    break;
                end
            end
            xleft=i+1;
            for i=cmean+1:1:limit(2)
                len1=sum(bwr(rtop:rtop0,i));
                if len1<len*0.95        % zza: adjustable para.
                    break;
                end
            end
            xright=i-1; 
        end
    end
    if len>3
        x=(xleft+xright)/2;
    end
    if DEBUG
        p=plot([x,x],[rtop,rbot],'-','LineWidth',2,'color','y');
        delete(p)
    end
    hold off
end

function y=calibrate_yaxis(yaw,mark_c,rmean0,limit,bw)
    DEBUG=0;
    if DEBUG
        clf;
        figure(1);
        imshow(bw);
        hold on
    end
    w=size(bw,2);
    h=size(bw,1);
    y=nan;
    bwr=bw*(0-1)+1;
    % % extend to the bottom first
    ifget=0;
    cright=max(mark_c);
    cright0=cright;
    cleft=min(mark_c);
    cleft0=cleft;  
    direction=0;
    % % detect the initial tick
    len=0;
    plus=min(yaw,3);     % zza: adjustable para.
    ifdetect=0;
    len=sum(bwr(rmean0,(cleft0-plus):(cright0+plus)));
    if DEBUG
        p=plot(cleft,rmean0,'r.');
        delete(p)
    end
    if len>=yaw+plus
        ifdetect=1;
        rmean=rmean0;
    end
    shift=0;
    dlimit=(limit(2)-limit(1))/2;
    while (~ifdetect)&&(shift<dlimit)
        shift=shift+1;
        rmean1=rmean0-shift;
        len=sum(bwr(rmean1,(cleft0-plus):(cright0+plus)));
        if len>=yaw+plus
            ifdetect=1;
            rmean=rmean1;
            direction=-1;
            break;
        end
        rmean2=rmean0+shift;
        len=sum(bwr(rmean2,(cleft0-plus):(cright0+plus)));
        if len>=yaw+plus
            ifdetect=1;
            rmean=rmean2;
            direction=1;
            break;
        end 
        if DEBUG
            p(1)=plot(cleft,rmean1,'b.');
            p(2)=plot(cleft,rmean2,'r.');
            delete(p);
        end
    end   
    if ~ifdetect
        return;
    end
    len=0;
    while (bwr(rmean,cleft-1)==1) && ((cleft0-cleft)<yaw*3)     % zza: adjustable para.
        if DEBUG
            p=plot(cleft,rmean,'r.');
            delete(p);
        end
        cleft=cleft-1;
    end
    len=cleft0-cleft;
    if len>3     % zza: adjustable para.
        for i=rmean-1:-1:limit(1)
            if DEBUG
                p=plot([cleft,cleft0-1],[i,i]);
                delete(p);
            end 

            len1=sum(bwr(i,cleft:cleft0-1));
            if len1<len*0.95        % zza: adjustable para.
                break;
            end

        end
        ytop=i+1;
        for i=rmean+1:limit(2)

            if DEBUG
                p=plot([cleft,cleft0-1],[i,i]);
                delete(p);
            end     

            len1=sum(bwr(i,cleft:cleft0-1));
            if len1<len*0.95        % zza: adjustable para.
                break;
            end

        end
        ybot=i-1; 
        ifget=1;
    end    
    
    % % extend to the right
    if ~ifget
        len=0;
        while (bwr(rmean,cright+1)==1) &&  (cright-cright0<yaw*4)   % zza: adjustable para.
            if DEBUG
                p=plot(cright,rmean,'r.');
                delete(p);
            end
            cright=cright+1;
        end        
        len=cright-cright0;
        if len>3     % zza: adjustable para.
            for i=rmean+1:h
                if DEBUG
                    p=plot([cright0+1,cright],[i,i]);
                    delete(p);
                end            
                len1=sum(bwr(i,(cright0+1):cright));
                if len1<len*0.95        % zza: adjustable para.
                    break;
                end

            end
            ybot=i+1;
            for i=(rmean-1):-1:1
                if DEBUG
                    p=plot([cright0+1,cright],[i,i]);
                    delete(p);
                end              
                len1=sum(bwr(i,(cright0+1):cright));
                if len1<len*0.95        % zza: adjustable para.
                    break;
                end
            end
            ytop=i-1;
        end
    end
    if len>0
        y=(ytop+ybot)/2;
    end
    if DEBUG
        p=plot([cleft,cright],[y,y],'-','LineWidth',2,'color','y');
        delete(p)
    end
    hold off
end
