clear;
% %------------------------------------------------------------- % %
% % INPUT                                                        % %
% %------------------------------------------------------------- % %
figpath='.\example\';                % the path of the figure, '.\' is the current path.
figname='segment.jpg';       % the name of the figure.
outpath='.\';                % the output path for storing segmented figures, '.\' is the current path.
thre_bw=0.9;                 % the threshold to tranform grayscale figure to black and white figure.
thre_panel=0.04;             % the threshold of relative size to regard the figure object as a figure panel..
thre_axis=0.7;               % the threshold to detect the axis.
% %------------------------------------------------------------- % %

flag=0;
rgb=imread([figpath,figname]);     % read the rgb figure
tmp=findstr(figname,'.');
name=figname(1:tmp(end)-1);          % strip the file extension
try
    [core_box,extend_box]=process_figure(rgb,thre_bw,thre_panel,thre_axis);
    flag=1;
catch
    disp(['ERROR for ',figname])
end

imshow(rgb)
hold on
if flag
    for i=1:size(extend_box,1)
        plotbox(extend_box(i,:),'b',0.5);
        plotbox(core_box(i,:),'r',1);
        im_extend=rgb(extend_box(i,3):extend_box(i,4),extend_box(i,1):extend_box(i,2),:);
        im_core=rgb(core_box(i,3):core_box(i,4),core_box(i,1):core_box(i,2),:);
        imwrite(im_extend,[outpath,name,'_extend_',num2str(i),'.jpg']);
        imwrite(im_core,[outpath,name,'_core_',num2str(i),'.jpg']);
    end
end

% %------------------------------------------------------------- % %
% % Functions                                                    % %
% %------------------------------------------------------------- % %

function [core_box,extend_box]=process_figure(rgb,thre_bw,thre_panel,thre_axis)
% % <core_box>: the boxes warping large figure objects determined by thre_panel.
% %             1x4 array, the leftmost, rightmost, uppermost and lowermost pixels
% % <extend_box>: the boxes warping large figure objects and affiliated titles, axis labels and tickslabels.
% %             1x4 array, the leftmost, rightmost, uppermost and lowermost pixels
    if ndims(rgb)==3
        gray=rgb2gray(rgb);                             % turn the rgb to grayscale figure
        bw=imbinarize(gray,thre_bw);                    % turn the grayscale to black-white figure
    else
        bw=imbinarize(rgb,thre_bw);                     % turn the grayscale to black-white figure
    end
    im_width=size(bw,2);
    im_height=size(bw,1);
    im_pixel=im_width*im_height;                        % num. of pixel of the figure
    bg=sum(bw,'all')/im_pixel;                          % determine the background color   
    extend_box=[];
    core_box=[];
    % % seperate the figure objects
    [n_cls,row,col,center,box,ob_wh]=seperated_object(bw);
    % % DEBUG
    %figure(1)
    %rgb2=zeros(size(rgb))+255;
    %rgb2=dye_color(rgb2,row,col); 
    %imshow(uint8(rgb2))   

    % % merge overlapped objects
    [n_cls,row,col,center,box,ob_wh]=merge_overlap_object(n_cls,row,col,box);
    % % DEBUG
    %figure(2)
    %rgb2=zeros(size(rgb))+255;
    %rgb2=dye_color(rgb2,row,col); 
    %imshow(uint8(rgb2))     
    
    % % get id of major objects and minor objects 
    [major,minor]=major_box(n_cls,ob_wh,im_pixel,thre_panel); 
    % % DEBUG
    %imshow(bw)
    %hold on
    %for i=1:numel(major)
    %   plotbox(box(major(i),:),'b',1);
    %end    
    %hold off
   
    % % process major objects
    thre_axis0=thre_axis;
    for boxid=1:numel(major)
        % % get the extended target box    
        target_box=box(major(boxid),:);
        large_box=surrounding_box(box,major,boxid,im_width,im_height);
        % % DEBUG
        %imshow(bw)
        %hold on
        %plotbox(extend_box,'b',1);    
        %hold off
        
        % % DEBUG
        %imshow(bw)
        %hold on

        % % detect axis
        thre_axis=thre_axis0;
        [xpos,ypos]=detect_axis(1-bw,n_cls,large_box,thre_axis);
        % % if not axis found cutdown the <thre_axis>
        while ~isempty(xpos) || ~isempty(ypos)
            thre_axis=thre_axis*0.9;
            if thre_axis<0.1
                break;
            end
            [xpos,ypos]=detect_axis(1-bw,n_cls,large_box,thre_axis);
        end
        
        % % DEBUG
        %plot([xpos(2),xpos(3)],[xpos(1),xpos(1)],'r','LineWidth',3)
        %plot([ypos(1),ypos(1)],[ypos(2),ypos(3)],'r','LineWidth',3)

        % % detect x ticklabels   
        xtis=detect_xticks(bw,xpos,target_box,large_box,box,ob_wh,minor);
        % % DEBUG
        %for i=1:numel(xtis)
        %  p(i)=plotbox(box(xtis(i),:),'b',0.5);
        %end
        %delete(p);

        % % detect xlabel
        xlab=detect_xlabel(bw,xpos,target_box,large_box,box,ob_wh,minor,xtis);
        % DEBUG
        %for i=1:numel(xlab)
        %  p(i)=plotbox(box(xlab(i),:),'b',0.5);
        %end
        %delete(p)   

        % % detect ylabel   
        ylab=detect_ylabel(bw,ypos,target_box,large_box,box,ob_wh,minor);
        % % DEBUG
        %for i=1:numel(ylab)
        %  p(i)=plotbox(box(ylab(i),:),'b',0.5);
        %end
        %delete(p)    

        % % title
        if ~isempty(ylab)
            leftbound=min(box(ylab,1));
        else
            leftbound=max(0,target_box(1)-(target_box(2)-target_box(1))*0.1);
        end
        if ~isempty(xtis)
            rightbound=max(max(box(xtis,2)),target_box(2));
        else
            rightbound=target_box(2);
        end
        tit=detect_title(bw,target_box,large_box,box,ob_wh,minor,leftbound,rightbound);
        % % DEBUG
        %for i=1:numel(tit)
        %  p(i)=plotbox(box(tit(i),:),'b',0.5);
        %end
        %delete(p) 

        figs=union([major(boxid)],xtis);
        figs=union(figs,xlab);
        figs=union(figs,ylab);
        figs=union(figs,tit);
        currentbox(1)=min(box(figs,1));
        currentbox(2)=max(box(figs,2));
        currentbox(3)=min(box(figs,3));
        currentbox(4)=max(box(figs,4));
        extend_box(boxid,:)=currentbox;
        core_box(boxid,:)=box(major(boxid),:);
        % % DEBUG
        %plotbox(currentbox,'b',0.5);
        %hold off
        
    end
end

function [n_cls,row,col,center,box,ob_wh]=seperated_object(bw)
    [L,n0]=bwlabel(bw*(0-1)+1,4);
    maxid=0;
    n_cls=0;
    for i=1:n0
        [r,c]=find(L==i);
        if numel(r)>3
            n_cls=n_cls+1;
            center(n_cls,:)=[mean(c),mean(r)];
            rmax=max(r,[],1);
            rmin=min(r,[],1);
            cmax=max(c,[],1);
            cmin=min(c,[],1);
            row{n_cls}=r;
            col{n_cls}=c;
            box(n_cls,:)=[cmin,cmax,rmin,rmax];
            ob_wh(n_cls,:)=[cmax-cmin+1,rmax-rmin+1];
        end
    end
end

function [n_cls,row,col,center,box,ob_wh]=merge_overlap_object(n_cls0,row0,col0,box0);
    row={};
    col={};
    center=[];
    box=[];
    ob_wh=[];
    g=zeros(n_cls0);   % graph to record which components is connected
    for i=1:n_cls0
        for j=i+1:n_cls0
            if detect_overlap(box0(i,:),box0(j,:))
                g(i,j)=1;
                g(j,i)=1;
            end
        end
    end
    G=graph(g);
    [bins,binsize]=conncomp(G);
    n_cls=max(bins);
    for i=1:n_cls
        id=find(bins==i);
        [row{i},col{i},center(i,:),box(i,:),ob_wh(i,:)]=merge_object_data(row0,col0,id);
    end
end

function flag=detect_overlap(bx1,bx2)
    flag=0;
    rpos=0;   % 1: upper; 2: middle; 3: lower
    cpos=0;   % 1: left ; 2: middel; 3: right
    if bx1(2)<bx2(1) 
        cpos=1;
    elseif bx1(1)>bx2(2)
        cpos=3;
    else
        cpos=2;
    end
    if bx1(4)<bx2(3)
        rpos=1;
    elseif bx1(3)>bx2(4)
        rpos=3;
    else
        rpos=2;
    end
    if rpos==2 && cpos==2
        flag=1;
    end
end

function [row,col,center,box,ob_wh]=merge_object_data(row0,col0,id)
    row=[];
    col=[];
    center=[];
    box=[];
    ob_wh=[];
    pt=0;
    for i=1:numel(id)
        n=numel(row0{id(i)});
        row(pt+1:pt+n,1)=row0{id(i)};
        col(pt+1:pt+n,1)=col0{id(i)};
        pt=pt+n;
    end
    center=[mean(col),mean(row)];
    rmax=max(row,[],1);
    rmin=min(row,[],1);
    cmax=max(col,[],1);
    cmin=min(col,[],1);
    box=[cmin,cmax,rmin,rmax];
    ob_wh=[cmax-cmin+1,rmax-rmin+1];    
end

function [major,minor]=major_box(n_cls,ob_wh,tot_area,thre)
    major=[];
    minor=[];
    ct=0;
    ct2=0;
    area=ob_wh(:,1).*ob_wh(:,2);
    [area2,id]=sort(area,'descend');
    for i=1:n_cls
        if area2(i)/tot_area>thre || (ct>=1 && area2(i)/area2(1)>0.1)    % % if the object is large enough, it will be output.
            ct=ct+1;
            major(ct)=id(i);
        else
            ct2=ct2+1;
            minor(ct2)=id(i);
        end

    end
end

function exbox=surrounding_box(box,major,boxid,im_width,im_height)
    id=major(boxid);
    exbox=[1,im_width,1,im_height];
    for i=1:numel(major)
        if i~=boxid
            id2=major(i);
            loc=neighbox_location(box(id2,:),box(id,:));
            if loc==1
                if box(id2,4)>exbox(3)
                    exbox(3)=box(id2,4)+1;
                end
            elseif loc==2
                if box(id2,3)<exbox(4)
                    exbox(4)=box(id2,3)-1;
                end
            elseif loc==3
                if box(id2,2)>exbox(1)
                    exbox(1)=box(id2,2)+1;
                end
            elseif loc==4
                if box(id2,1)<exbox(2)
                    exbox(2)=box(id2,1)-1;
                end
            end
        end
    end
end

function loc=neighbox_location(bx1,bx2)
    % The relative position of bx1 to bx2
    rpos=0;   % 1: upper; 2: middle; 3: lower
    cpos=0;   % 1: left ; 2: middel; 3: right
    loc=0;
    if bx1(2)<bx2(1) 
        cpos=1;
    elseif bx1(1)>bx2(2)
        cpos=3;
    else
        cpos=2;
    end
    if bx1(4)<bx2(3)
        rpos=1;
    elseif bx1(3)>bx2(4)
        rpos=3;
    else
        rpos=2;
    end
    if rpos==1 && cpos==2
        loc=1;  % upper
    elseif rpos==3 && cpos==2
        loc=2;  % lower
    elseif rpos==2 && cpos==1
        loc=3;  % left
    elseif rpos==2 && cpos==3
        loc=4;  % right
    end
end

function [xpos,ypos]=detect_axis(bw,n_cls,box,thre)

    h=box(4)-box(3)+1;
    w=box(2)-box(1)+1;
    xpos=[0,box(2),0];
    ypos=[0,box(4),0];    
    mark_r=[];
    xaw=0;
    sumr=sum(bw(box(3):box(4),box(1):box(2)),2);
    sumc=sum(bw(box(3):box(4),box(1):box(2)),1);
    maxlen=0;
    for i=h:-1:1
        %disp(i)
        %p=plot([box(1),box(2)],[i,i],'r');
        ends=get_axis_ends(bw(box(3)+i-1,box(1):box(2)));
        len=ends(2)-ends(1);
        if (len>w*thre)
            if len>maxlen
                xpos(1)=box(3)+i-1;
                maxlen=len;
            end
            if (ends(1)+box(1)-1)<=xpos(2)
                xpos(2)=ends(1)+box(1)-1;
            end
            if (ends(2)+box(1)-1)>=xpos(3)
                xpos(3)=ends(2)+box(1)-1;
            end
        elseif maxlen>0 && len<0.5*maxlen
            break;
        end 
        %delete(p);
    end
    
    maxlen=0;
    for i=1:w
        %p=plot([i,i],[box(3),box(4)],'r');                                                     
        if (sumc(i)>h*thre)
            ends=get_axis_ends(bw(box(3):box(4),box(1)+i-1));
            len=ends(2)-ends(1);
            if (len>h*thre)  
                if len>maxlen
                    ypos(1)=box(1)+i-1;
                    maxlen=len;
                end
                if (ends(1)+box(3)-1)<=ypos(2)
                    ypos(2)=ends(1)+box(3)-1;
                end
                if (ends(2)+box(3)-1)>=ypos(3)
                    ypos(3)=ends(2)+box(3)-1;
                end
            elseif maxlen>0 && len<0.5*maxlen
                break;
            end    
        end
        %delete(p);
    end
end

function ends=get_axis_ends(bw)
    n=numel(bw);
    sec=[];
    ct=0;
    flag=0;
    ends=[0,0];
    for i=1:n
        if bw(i)==1
            if flag==0
                flag=1;
                ct=ct+1;
                sec(ct,1)=i;
            end
        elseif ct>0 && flag==1
            flag=0;
            sec(ct,2)=i-1;
        end
    end
    if flag==1
        sec(ct,2)=n;
        flag=0;
    end
    if ~isempty(sec)
        len=sec(:,2)-sec(:,1);
        [~,id]=max(len);
        ends=sec(id,:);
    end
end

function xtis=detect_xticks(bw,xpos,tarbox,extend_box,box,ob_wh,minor)
    xtis=[];
    cand=[];  % candidate box
    ct=0;
    xlen=xpos(3)-xpos(2);
    boxarea=(tarbox(2)-tarbox(1))*(tarbox(4)-tarbox(3));
    minbox=box(minor,:);
    min_wh=ob_wh(minor,:);
    delta=minbox(:,3)-xpos(1);
    [delta2,id]=sort(delta);
    id_clst=0;
    % % get the object closest to the axis
    for i=1:numel(delta2)
        if delta2(i)>0 && ( ( minbox(id(i),1)<xpos(3) && minbox(id(i),1)>xpos(2)) ...
                         || ( minbox(id(i),2)<xpos(3) && minbox(id(i),2)>xpos(2))) ...  % the reference object should be under the axis
           && (minbox(id(i),3)>=extend_box(3) && minbox(id(i),4)<=extend_box(4))
            w1=min_wh(id(i),1);
            h1=min_wh(id(i),2);
        	if w1>8 && h1>8 && (w1*h1>boxarea*1e-5)   % require the object to be sufficient large
                id_clst=id(i);  % the id of the closest box
                break;
            end
        end
    end
    if id_clst==0
        return
    end
    ct=ct+1;
    cand(ct)=id_clst;
    
    botline=minbox(id_clst,4)+min_wh(id_clst,2)*0.2;
    botline0=botline;
    for i=1:size(minbox,1)
        if i~=id_clst
            if delta(i)>0
                %p=plotbox(minbox(i,:),'r',2);
                dist=[minbox(i,2)-xpos(2),minbox(i,1)-xpos(3)];
                if minbox(i,4)<botline && (  (dist(1)>=0 && dist(2)<=0) || ( (dist(1)<0) && (abs(dist(1))<xlen*0.3) ) || ( (dist(2)>0) && (abs(dist(2))<xlen*0.3) )  )
                    ct=ct+1;
                    cand(ct)=i;
                end
                %delete(p) 
            end
        end
    end
    
    % % update a new potential bottom line
    for i=1:size(minbox,1)
        if ~ismember(i,cand)
            if delta(i)>0 
                %p=plotbox(minbox(i,:),'r',2);
                dist=[minbox(i,2)-xpos(2),minbox(i,1)-xpos(3)];
                if minbox(i,3)<botline0 && min_wh(i,2)>min_wh(id_clst,2)*1.4 ...
                    && (  (dist(1)>=0 && dist(2)<=0) || ( (dist(1)<0) && (abs(dist(1))<xlen*0.3) ) || ( (dist(2)>0) && (abs(dist(2))<xlen*0.3) ) )
                    for j=1:numel(cand)
                        %p1=plotbox(minbox(cand(j),:),'b',2);
                        % check the left end of the new
                        if min(abs(minbox(i,2)-minbox(cand(j),2)),abs(minbox(i,2)-minbox(cand(j),1))) < (minbox(cand(j),2)-minbox(cand(j),1))
                            if (minbox(i,4)+min_wh(i,2)*0.1)>botline
                                botline=minbox(i,4)+min_wh(i,2)*0.1;
                            end
                            %delete(p1);
                            break;
                        end
                        %delete(p1);
                    end
                end
                %delete(p);
            end
        end
    end
    % % select object within the new bottom line
    ct2=0;
    cand2=[];
    has_sup=[];
    for i=1:size(minbox,1)
        if ~ismember(i,cand)
            %p=plotbox(minbox(i,:),'r',2);
            if delta(i)>0 && minbox(i,3)<botline  
                flag=0;
                ct2=ct2+1;
                cand2(ct2)=i;
                for j=1:numel(cand)
                    % check the left end of the new
                    if min(abs(minbox(i,2)-minbox(cand(j),2)),abs(minbox(i,2)-minbox(cand(j),1))) < (minbox(cand(j),2)-minbox(cand(j),1))
                        has_sup(ct2)=1;
                        flag=1;
                        break;
                    end
                end
                if flag==0
                    has_sup(ct2)=0;
                end
            end
            %delete(p)
        end
    end    
    if sum(has_sup)>0
        cand(ct+1:ct+ct2)=cand2;
        ct=ct+ct2;
    end
    
    % % check objects not under the axis 
    candbox=minbox(cand,:);
    xcenter=(candbox(:,2)+candbox(:,1))/2;
    maxw=max(candbox(:,2)-candbox(:,1));
    [xcenter,id]=sort(xcenter);
    ct0=ct;
    cand3=[];
    ct3=0;
    for i=1:ct0
        if   (minbox(cand(id(i)),1)>=xpos(2) && minbox(cand(id(i)),1)<=xpos(3)) ...
           ||(minbox(cand(id(i)),2)>=xpos(2) && minbox(cand(id(i)),2)<=xpos(3)) 
            %p=plotbox(minbox(cand(id(i)),:),'r',2);
            ct3=ct3+1;
            cand3(ct3)=cand(id(i));
            %delete(p);
        end    
    end     
    % % get the box id <lid> on the left end
    lid=0;
    for i=1:ct0
        if minbox(cand(id(i)),2)>xpos(2)  % xpos(2) is the left end of the x axis
            lid=i;
            break;
        end
    end   
    if lid>0
        for i=lid:-1:2
            %p=plotbox(minbox(cand(id(i-1)),:),'r',2);
            if (xcenter(i)-xcenter(i-1))<maxw*1.5
                ct3=ct3+1;
                cand3(ct3)=cand(id(i-1));
            else
                %delete(p);
                break;
            end
            %delete(p);
        end
    end
    % get the box id <lid> on the right end
    rid=0;
    for i=1:ct0
        if minbox(cand(id(i)),1)>xpos(3)  % xpos(2) is the left end of the x axis
            rid=i;
            break;
        end
    end  
    if rid>0
        for i=rid:ct0
            %p=plotbox(minbox(cand(id(i)),:),'r',2);
            if (xcenter(i)-xcenter(i-1))<maxw*1.8
                ct3=ct3+1;
                cand3(ct3)=cand(id(i));
            else
                %delete(p);
                break;
            end
            %delete(p);
        end
    end
    xtis=minor(cand3);
end

function xlab=detect_xlabel(bw,xpos,tarbox,extend_box,box,ob_wh,minor,xtis)
    xlab=[];
    cand=[];  % candidate box
    ct=0;
    boxarea=(tarbox(2)-tarbox(1))*(tarbox(4)-tarbox(3));
    minbox=box(minor,:);
    min_wh=ob_wh(minor,:);
    if ~isempty(xtis)
        upbound=max(box(xtis,4));
    else
        upbound=xpos(1);
    end
    
    % % get the major characters of the label
    flag=zeros(numel(minor),5);
    botline=upbound;
    for i=1:numel(minor)
        %p=plotbox(minbox(i,:),'b',0.5);
        if ((minbox(i,3)-upbound)<min_wh(i,2)*2 ) 
            flag(i,1)=1;
        end
        if (minbox(i,4)>upbound)
            flag(i,2)=1;
        end
        if ~ismember(minor(i),xtis)
            flag(i,3)=1;
        end
        if (minbox(i,1)>=extend_box(1)) && (minbox(i,2)<=extend_box(2)) && (minbox(i,3)>=extend_box(3)) && (minbox(i,4)<=extend_box(4))
            flag(i,4)=1;
        end
        if sum(flag(i,1:4))==4
            botline=max(botline,minbox(i,4));
        end
        %delete(p);
    end
    
    for i=1:numel(minor)
        if minbox(i,3)<=botline
            flag(i,1)=1;
        end
        if sum(flag(i,1:4))==4
            ct=ct+1;
            cand(ct)=i;
        end
    end
    % % remove those objects in other boxes
    [~,id]=sort(minbox(cand,1));    % sort from left to right according to the left bound
    mark=1;
    for i=1:numel(id)
        if minbox(cand(id(i)),1)>xpos(2)
            mark=i;
            break;
        end
    end
    if mark>1
        mark1=mark-1;
    else
        mark1=1;
    end
    for i=mark-1:-1:1
        %p=plotbox(minbox(cand(id(i)),:),'b',0.5);
        if (minbox(cand(id(i+1)),1)-minbox(cand(id(i)),2))>max(min_wh(cand(id(i+1)),1),min_wh(cand(id(i)),1))
            mark1=i+1;
        end
        %delete(p)
    end
    mark=1;
    for i=1:numel(id)
        if minbox(cand(id(i)),1)<xpos(2)
            mark=i;
            break;
        end
    end
    flag=0;   % used to denote if a objects far away exist
    for i=mark:numel(id)
        if minbox(cand(id(i)),1)>xpos(3)
            %p=plotbox(minbox(cand(id(i)),:),'b',0.5);
            if i>1 && (minbox(cand(id(i)),1)-minbox(cand(id(i-1)),2))<max(min_wh(cand(id(i-1)),1),min_wh(cand(id(i)),1))
                continue
            else
                flag=1;
                %delete(p);                
                break;
            end
            %delete(p);
        end
    end
    if i>=1
        if flag
            xlab=minor(cand(id(mark1:i-1)));
        else
            xlab=minor(cand(id(mark1:i)));
        end
    end
end    

function ylab=detect_ylabel(bw,ypos,tarbox,extend_box,box,ob_wh,minor)
    ylab=[];
    cand=[];  % candidate box
    ct=0;
    ylen=ypos(3)-ypos(2);
    boxarea=(tarbox(2)-tarbox(1))*(tarbox(4)-tarbox(3));
    minbox=box(minor,:);
    min_wh=ob_wh(minor,:);
    delta=ypos(1)-minbox(:,2);
    [delta2,id]=sort(delta);
    % % find the boxes on the left
    for i=1:numel(delta2)
        %p=plotbox(minbox(id(i),:),'b',0.5);
        if (delta2(i)>0) && (minbox(id(i),1)>=extend_box(1)) && (minbox(id(i),2)<=extend_box(2)) && (minbox(id(i),3)>=extend_box(3)) && (minbox(id(i),4)<=extend_box(4))  
            ct=ct+1;
            cand(ct)=id(i);            
        end
        %delete(p);
    end
    % % get neighbors along the vertical direction
    nc=numel(cand);
    conn=zeros([nc,nc]);
    conn2=zeros([nc,nc]);
    for i=1:nc
        for j=i+1:nc
            ii=cand(i);   % get the true index
            jj=cand(j);
            %p1=plotbox(minbox(ii,:),'b',0.5);
            %p2=plotbox(minbox(jj,:),'b',0.5);
            %disp([num2str(i),' ',num2str(j)]);
            [flag,flag2]=check_vertical_neigh(minbox(ii,:),minbox(jj,:),min_wh(ii,:),min_wh(jj,:));
            if flag
                conn(i,j)=1;
                conn(j,i)=1;
            end
            if flag2
                conn2(i,j)=1;
                conn2(j,i)=1; 
            end
            %delete(p1);
            %delete(p2);
        end
    end
    % % use a small threshold to distinguish ylabel from yticks
    G=graph(conn);
    % % to get the connnected components
    [bins,bsize]=conncomp(G);
    % % get the ylen of the bins
    ylen=[];
    for i=1:numel(bsize)
        id=find(bins==i);
        ymin=min(minbox(cand(id),3));
        ymax=max(minbox(cand(id),4));
        ylen(i)=ymax-ymin;
    end
    [~,id_bin]=max(ylen);
    % if the max size of bins are equal, we use the most left one
    %id_bin=find(bsize==maxsize);        % id of bins
    minleft=extend_box(2);
    id3=[];
    for i=1:numel(id_bin)
        id2=find(bins==id_bin(i));      % id of candidata <cand>
        %for j=1:numel(id2)
        %    p(i)=plotbox(minbox(cand(id2(j)),:),'b',0.5);
        %    hold on
        %end
        %delete(p);
        mintmp=min(minbox(cand(id2),1));
        if mintmp<minleft
            minleft=mintmp;
            id3=id2;                % id of candidata <cand> of the leftmost and largest bin
        end 
    end
    % % use a large threshold to include complete ylabel
    G2=graph(conn2);
    [bins2,bsize2]=conncomp(G2); 
    if ~isempty(id3)
        id_bin=bins2(id3(1));
        id4=find(bins2==id_bin);
        ylab=minor(cand(id4));
    end
end

function [flag,flag2]=check_vertical_neigh(bx1,bx2,wh1,wh2)
    % % flag use threshold of 0.5, flag2 use threshold of 1.5
    flag=0;
    flag2=0;
    dist=box_distance(bx1,bx2);
    minw=min(wh1(1),wh2(1));
    maxh=max(wh1(2),wh2(2));
    %if dist(1)==0 || ( dist(1)<0 && ( abs(dist(1))/minw > 0.5) ) 
    if dist(1)==0 || ( dist(1)<4 ) 
        if dist(2)<maxh*0.5
            flag=1;
        end
        if dist(2)<maxh*1.5
            flag2=1;
        end
    end
    
end

function dist=box_distance(box1,box2)
    % % for <dist>, 0 means contain, positive means distance, negative means overlap distance
    % % the 1st element is the horizontal distance, the 2nd element is the vertical distance 
    dist=[0,0];
    if box1(1)>box2(1)
        tmp=box1;
        box1=box2;
        box2=tmp;       
    end
    delta(1)=box1(2)-box2(1);
    delta(2)=box1(2)-box2(2);
    if delta(1)<0
        dist(1)=0-delta(1);
    elseif delta(1)>0 && delta(2)<0
        dist(1)=0-delta(1);
    end

    if box1(3)>box2(4)
        tmp=box1;
        box1=box2;
        box2=tmp;       
    end
    delta(1)=box1(4)-box2(3);
    delta(2)=box1(4)-box2(4);
    if delta(1)<0
        dist(2)=0-delta(1);
    elseif delta(1)>0 && delta(2)<0
        dist(2)=0-delta(1);
    end 
end

function tit=detect_title(bw,tarbox,extend_box,box,ob_wh,minor,leftbound,rightbound)
    tit=[];
    cand=[];  % candidate box
    ct=0;
    htar=(tarbox(4)-tarbox(3));
    wtar=(tarbox(2)-tarbox(1));
    hext=extend_box(4)-extend_box(3);
    wext=extend_box(4)-extend_box(3);
    boxarea=htar*wtar;
    minbox=box(minor,:);
    min_wh=ob_wh(minor,:);
    bot=tarbox(3);  % the upper end of the box
    for i=1:numel(minor)
        %p=plotbox(minbox(i,:),'b',0.5);
        if ( (minbox(i,3)-bot)<0 ) && ( (bot-minbox(i,4))<min(htar*0.3,min_wh(i,2)) )  && ( minbox(i,1)>leftbound ) && ( minbox(i,2)<rightbound ) ...
             && (minbox(i,1)>=extend_box(1)) && (minbox(i,2)<=extend_box(2)) && (minbox(i,3)>=extend_box(3)) && (minbox(i,4)<=extend_box(4))
            ct=ct+1;
            cand(ct)=minor(i);
        end
        %delete(p);
    end
    tit=cand;
end

function p=plotbox(bx,color,linewidth)
    if numel(bx)==4
        p=plot([bx(1),bx(2),bx(2),bx(1),bx(1)],[bx(3),bx(3),bx(4),bx(4),bx(3)],'color',color,'LineWidth',linewidth);
    end
end

function rgb=dye_color(rgb,row,col)
    s=size(rgb);
    dim=ndims(rgb);
    color=colormap(lines);
    nrow=numel(row);
    for i=1:nrow
        n=numel(row{i});
        zr=zeros(n,1);
        cid=mod(i,64)+1;
        if dim==3
            id_red=sub2ind(s,row{i},col{i},zr+1);
            id_green=sub2ind(s,row{i},col{i},zr+2);
            id_blue=sub2ind(s,row{i},col{i},zr+3);
            rgb(id_red)=round(color(cid,1)*255);
            rgb(id_green)=round(color(cid,2)*255);
            rgb(id_blue)=round(color(cid,3)*255);
        elseif dim==2
            id=sub2ind(s,row{i},col{i});
            rgb(id)=round((i-1)*floor(255/nrow));
        end
    end    
end