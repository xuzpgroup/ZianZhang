% <alpa>: the scale factor for threshold distance
function [xxlabel,yylabel,xxlabels,yylabels,xlabcl_box,ylabcl_box,xxtick_num,yytick_num,xxtick_str,yytick_str,xtlcl_box,ytlcl_box]=recognize_axis_character(n_cls,center,box,ob_wh,pos_xa,pos_ya,row,col,wf,hf,origin,bw0,alpa)
    DEBUG_xaxis=0;
    DEBUG_yaxis=0;
    DEBUG_scan_xlabel=0;
    DEBUG_scan_ylabel=0;
    bw0=bw0*(0-1)+1;  % reverse bw0
    bw=zeros(size(bw0,1),size(bw0,2))+1;
    rgb=zeros(size(bw0,1),size(bw0,2),3)+255;
    rgb=uint8(rgb);
    
    if DEBUG_xaxis||DEBUG_yaxis||DEBUG_scan_xlabel||DEBUG_scan_ylabel
        figure(1)
        imshow(bw0*(0-1)+1)
        hold on
    end
    xxlabel='';
    yylabel='';
    xxtick_num=[];
    yytick_num=[];
    xxtick_str={};
    yytick_str={};
    xtlcl_box=[];
    ytlcl_box=[];
    
    xc=center(:,1);
    yc=center(:,2);
    w=size(bw0,2);
    h=size(bw0,1);
    min_edge=min(ob_wh,[],2);
    % % mark all cluster with gray color in rgb
    for i=1:n_cls
        r=row{i};
        c=col{i};
        for j=1:size(r,1)
            rgb(r(j),c(j),1:3)=[100,100,100];
        end
    end

    xchar=[];
    nxc=0;
    % objects for xaxis
    for i=1:n_cls
        if (box(i,3)>pos_xa)
            r=row{i};
            c=col{i};
            for j=1:size(r,1)
                bw(r(j),c(j))=0;
                rgb(r(j),c(j),1:3)=[200,200,0];
            end
            nxc=nxc+1;
            xchar(nxc)=i;
            if DEBUG_xaxis
                p(nxc)=plotbox(box(i,:));
            end
        end
    end    
    if exist('p')
        delete(p)
    end
    
    % objects for yaxis
    ychar=[];
    nyc=0;
    for i=1:n_cls
        if (box(i,2)<pos_ya)&&(box(i,3)<pos_xa)
            r=row{i};
            c=col{i};
            for j=1:size(r,1)
                bw(r(j),c(j))=0;
                rgb(r(j),c(j),1:3)=[0,200,0];
            end
            nyc=nyc+1;
            ychar(nyc)=i;
            if DEBUG_yaxis
                p(nyc)=plotbox(box(i,:));
            end            
        end
    end
    if exist('p')
        delete(p)
    end    
    
    % % seperate ylabel and yticklabel
    hscan=ceil(hf/3);
    hc=round(hf/2+origin(2));
    top=hc-hscan;
    bot=min(hc+hscan,h);
    touch=0;
    sum1=zeros(1,ceil(pos_ya));
    sum1=sum(bw0(top:bot,1:ceil(pos_ya)),1);
    ysep=0;  % the position to seperate ylabel and yticks
    for i=1:ceil(pos_ya)
        if (touch==1)&&(sum1(i)==0)
            ysep=i;
            break;
        end    
        if sum1(i)>(hscan*0.1)  % zza: tmp value, will be added as para. for the function
            touch=1;
        end
        %if DEBUG_scan_ylabel
        %    p=plot([i,i],[top,bot],'r');
        %    pause(0.1)
        %    delete(p)
        %end
    end
    
    ylab=[];    % ylabel
    n_ylab=0;
    ytl=[];     % yticklabel
    n_ytl=0;
    for i=1:nyc
        id=ychar(i);
        if center(id,1)<ysep
            n_ylab=n_ylab+1;
            ylab(n_ylab)=id;
        else
            n_ytl=n_ytl+1;
            ytl(n_ytl)=id;
        end
    end
    [ylabcl,ylabcl_box,n_ylabcl]=merge_object(ylab,n_ylab,xc,yc,min_edge,box,2);
    [ytlcl,ytlcl_box,n_ytlcl]=merge_object(ytl,n_ytl,xc,yc,min_edge,box,2);
    % % sort the tick acoording to the y coordinates
    ytlcl_yc=(ytlcl_box(:,3)+ytlcl_box(:,4))/2;
    [ytlcl_yc,sid]=sort(ytlcl_yc,'ascend');
    ytlcl0=ytlcl;
    ytlcl_box0=ytlcl_box;
    for i=1:n_ytlcl
        ytlcl{i}=ytlcl0{sid(i)};
        ytlcl_box(i,:)=ytlcl_box0(sid(i),:);
    end
    % % recognize the ylabel
    yylabels={};
    offset=20;
    ohalf=round(offset/2);
    for i=1:n_ylabcl
        yb=ylabcl_box(i,:);
        bw_local=zeros(yb(4)-yb(3)+offset,yb(2)-yb(1)+offset)+1;
        bw_local(ohalf:(ohalf+yb(4)-yb(3)),ohalf:(yb(2)-yb(1)+ohalf))=bw0(yb(3):yb(4),yb(1):yb(2))*(0-1)+1;
        yylabels{i}=ocr(imrotate(bw_local,-90),'TextLayout','Block');
        yylabel=[yylabel,yylabels{i}.Text,' '];
    end    
    % % recognize the yticks
    yytick={};
    yytick_num=[];
    for i=1:n_ytlcl
        %yb=ytlcl_box(i,:);
        %bw_local=zeros(yb(4)-yb(3)+offset,yb(2)-yb(1)+offset)+1;
        %bw_local(ohalf:(ohalf+yb(4)-yb(3)),ohalf:(yb(2)-yb(1)+ohalf))=bw0(yb(3):yb(4),yb(1):yb(2))*(0-1)+1;
        %yytick{i}=ocr(bw_local,'TextLayout','Block','CharacterSet','0123456789E+-.');
        [num,normnum,expon,norm_str,expon_str,norm.tree,expon_tree]=recognize_ticknum(ytlcl{i},ytlcl_box(i,:),box,xc,yc,ob_wh,bw0);
        %if ~isnan(expon)
        %    yytick{i}=[norm_tree.Word,'^',expon_tree.Word];
        %else
        %    yytick{i}=norm_tree.Word;
        %end        
        if numel(num)==1
            yytick_num(i)=num;
        else
            yytick_num(i)=nan;
        end
        if numel(expon_str)==0
            yytick_str{i}=norm_str;
        else
            yytick_str{i}=[norm_str,'^',expon_str];
        end
    end
    if DEBUG_yaxis
        imshow(rgb)
        hold on
        for i=1:n_ylabcl
            yb=ylabcl_box(i,:);
            p1(i)=patch([yb(1),yb(1),yb(2),yb(2)], ...
                       [yb(3),yb(4),yb(4),yb(3)], 'b','FaceColor','none');
            txt1(i)=text(yb(1)-10,yb(4),yylabels{i}.Text,'Rotation',90,'FontSize',14);
        end
        for i=1:n_ytlcl
            yb=ytlcl_box(i,:);
            p2(i)=patch([yb(1),yb(1),yb(2),yb(2)], ...
                       [yb(3),yb(4),yb(4),yb(3)], 'b','FaceColor','none');
            %txt2(i)=text(yb(1),yb(4)+30,yytick{i}.Text);
            txt2(i)=text(yb(1),yb(4)+10,num2str(yytick_num(i)),'FontSize',14);
        end        
    end
    
    

    % % seperate xlabel and xticklabel
    wscan=ceil(wf/3);
    wc=round(wf/2+origin(1));
    left=max(wc-wscan,1);
    right=wc+wscan;
    touch=0;
    yrang=h-ceil(pos_xa)+1;
    sum1=zeros(1,yrang);
    sum1=sum(bw0(ceil(pos_xa):h,left:right),2);
    sum1=flip(sum1);
    xsep=h;   % the position to seperate xlabel and xticks
    for i=1:yrang
        if (touch==1)&&(sum1(i)==0)
            xsep=h-i+1;
            break;
        end    
        if (sum1(i)>(wscan*0.05)) % zza: tmp value, will be added as para. for the function
            touch=1;
        end
        if DEBUG_scan_xlabel
            tmp=bw0(h-i+1,left:right);
            bw0(h-i+1,left:right)=1;
            imshow(bw0)
            bw0(h-i+1,left:right)=tmp;
        end
    end
    
    xlab=[];    % xlabel
    n_xlab=0;
    xtl=[];     % xticklabel
    n_xtl=0;
    for i=1:nxc
        id=xchar(i);
        if center(id,2)>xsep
            n_xlab=n_xlab+1;
            xlab(n_xlab)=id;
        else
            n_xtl=n_xtl+1;
            xtl(n_xtl)=id;
        end
    end
    [xlabcl,xlabcl_box,n_xlabcl]=merge_object(xlab,n_xlab,xc,yc,min_edge,box,alpa);  %2
    [xtlcl,xtlcl_box,n_xtlcl]=merge_object(xtl,n_xtl,xc,yc,min_edge,box,alpa);
    
    % % sort the tick acoording to the x coordinates
    xtlcl_xc=(xtlcl_box(:,1)+xtlcl_box(:,2))/2;
    [xtlcl_xc,sid]=sort(xtlcl_xc,'ascend');
    xtlcl0=xtlcl;
    xtlcl_box0=xtlcl_box;
    for i=1:n_xtlcl
        xtlcl{i}=xtlcl0{sid(i)};
        xtlcl_box(i,:)=xtlcl_box0(sid(i),:);
    end
    % % recognize the xlabel
    xxlabels={};
    offset=20;
    ohalf=round(offset/2);
    for i=1:n_xlabcl
        xb=xlabcl_box(i,:);
        bw_local=zeros(xb(4)-xb(3)+offset,xb(2)-xb(1)+offset)+1;
        bw_local(ohalf:(ohalf+xb(4)-xb(3)),ohalf:(xb(2)-xb(1)+ohalf))=bw0(xb(3):xb(4),xb(1):xb(2))*(0-1)+1;
        xxlabels{i}=ocr(bw_local,'TextLayout','Block');
        xxlabel=[xxlabel,strip_char_2(xxlabels{i}.Text),' '];
    end    
    % % recognize the xticks
    xxtick={};
    for i=1:n_xtlcl
        %xb=xtlcl_box(i,:);
        %bw_local=zeros(xb(4)-xb(3)+offset,xb(2)-xb(1)+offset)+1;
        %bw_local(ohalf:(ohalf+xb(4)-xb(3)),ohalf:(xb(2)-xb(1)+ohalf))=bw0(xb(3):xb(4),xb(1):xb(2))*(0-1)+1;
        %xxtick{i}=ocr(bw_local,'TextLayout','Block','CharacterSet','0123456789E+-.');
        [num,normnum,expon,norm_str,expon_str,norm.tree,expon_tree]=recognize_ticknum(xtlcl{i},xtlcl_box(i,:),box,xc,yc,ob_wh,bw0);
        if numel(num)==1
            xxtick_num(i)=num;
        else
            xxtick_num(i)=nan;
        end
        if numel(expon_str)==0
            xxtick_str{i}=norm_str;
        else
            xxtick_str{i}=[norm_str,'^',expon_str];
        end
    end
    
    if DEBUG_xaxis
        for i=1:n_xlabcl
            xb=xlabcl_box(i,:);
            p3(i)=patch([xb(1),xb(1),xb(2),xb(2)], ...
                       [xb(3),xb(4),xb(4),xb(3)], 'b','FaceColor','none');
            txt3(i)=text(xb(2),xb(4)+10,xxlabels{i}.Text,'FontSize',14);
        end
        for i=1:n_xtlcl
            xb=xtlcl_box(i,:);
            p4(i)=patch([xb(1),xb(1),xb(2),xb(2)], ...
                       [xb(3),xb(4),xb(4),xb(3)], 'b','FaceColor','none');
            %txt4(i)=text(xb(2)+10,xb(4)+10,xxtick{i}.Text);
            txt4(i)=text(xb(2)+10,xb(4),num2str(xxtick_num(i)),'FontSize',14);
        end        
    end
    
    if DEBUG_xaxis
        delete(p3);delete(txt3);
        delete(p4);delete(txt4);
    end
    if DEBUG_yaxis
        delete(p1);delete(txt1);
        delete(p2);delete(txt2);
    end        
end

function [num,normnum,expon,norm_str,expon_str,norm_tree,expon_tree]=recognize_ticknum(cluster,clusbox,box,xc,yc,ob_wh,bw)
    DEBUG=0;
    if DEBUG
        p=plot([clusbox(1),clusbox(2),clusbox(2),clusbox(1),clusbox(1)], ...
               [clusbox(3),clusbox(3),clusbox(4),clusbox(4),clusbox(3)]);
    end
    n=numel(cluster);
    aveh=0;
    cy=[];
    avecen=0;
    for i=1:n
        id=cluster(i);
        aveh=ob_wh(cluster(i),2)+aveh;
        cy(i)=mean(box(id,3:4));
    end
    aveh=aveh/n;
    %avecen=mean(cy);
    avecen=clusbox(4)-0.55*(clusbox(4)-clusbox(3));    % zza: para. could be adjust in the future.
    super=[];
    n_super=0;
    expon=nan;    
    normal=[];
    n_norm=0;
    normnum=nan;
    norm_str='';
    expon_str='';
    norm.tree=nan;
    expon_tree=nan;
    num=nan;
    for i=1:n
        id=cluster(i);
        % (ob_wh(id,2)<aveh*0.8) && (ob_wh(id,2)>aveh*0.05) && (box(id,4)<avecen)
        if (ob_wh(id,2)>aveh*0.05) && (cy(i)<(avecen-aveh*0.1))
            n_super=n_super+1;
            super(n_super)=id;
        else
            n_norm=n_norm+1;
            normal(n_norm)=id;
        end
        if DEBUG
            p1=plotbox(box(id,:));
            delete(p1);
        end        
    end
    offset=5;
    if n_super>0
        superbox=cluster_box(super,box);
        bw1=boxselect_boundary(bw,superbox,offset);
        expon_tree=ocr(bw1,'TextLayout','Block','CharacterSet','0123456789.-+');
        expon_str=strip_char(expon_tree.Text);
        tmp=str2num(expon_str);
        if numel(tmp)==1
            expon=tmp;
        end
        normbox=cluster_box(normal,box);
        bw1=boxselect_boundary(bw,normbox,offset);
        norm_tree=ocr(bw1,'TextLayout','Block','CharacterSet','0123456789.');
        norm_str=strip_char(norm_tree.Text);
        tmp=str2num(norm_str);
        if numel(tmp)==1
            normnum=tmp;
        end
        if ~isnan(normnum)
            if ~isnan(expon)
                num=normnum^(expon);
            else
                num=normnum;
            end
        end
    else
        normbox=cluster_box(normal,box);
        bw1=boxselect_boundary(bw,normbox,offset);
        norm_tree=ocr(bw1,'TextLayout','Block','CharacterSet','0123456789Ee.+-');
        norm_str=strip_char(norm_tree.Text);
        tmp=str2num(norm_str);
        if (numel(tmp)==1)
            num=tmp;
        end
    end
    if DEBUG
        delete(p);
    end
end


    
% <cluster> stores the global id of objects
function [cluster,clbox,ncl]=merge_object(id,n,xc,yc,min_edge,box,alpa)
    cluster={};
    clbox=[];
    ncl=0;
    gh=zeros(n,n);
    for i=1:n-1
        for j=i+1:n
            id1=id(i);
            id2=id(j);
            dist0=(xc(id1)-xc(id2))^2+(yc(id1)-yc(id2))^2;
            if dist0<(alpa*(min_edge(id1)+min_edge(id2))^2)
                gh(i,j)=1;
                gh(j,i)=1;
            end
        end
    end
    [bins,binsize]=conncomp(graph(gh));
    ncl=numel(binsize);
    cluster={};
    for i=1:ncl
        cluster{i}=[];
    end
    for i=1:n
        cluster{bins(i)}=[cluster{bins(i)},id(i)];
    end
    for i=1:ncl
        clbox(i,:)=cluster_box(cluster{i},box);
    end
end


function p=plotbox(bx)
    p=plot([bx(1),bx(2),bx(2),bx(1),bx(1)],[bx(3),bx(3),bx(4),bx(4),bx(3)],'r','LineWidth',0.5);
end

function string=strip_char(string0)
    string='';
    for i=1:numel(string0)
        if (~strcmp(string0(i),' '))&&(abs(string0(i))~=8629)  % 8629: the ascii of ?
            string=[string,string0(i)];
        end
    end
end    